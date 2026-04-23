---
name: supabase-architect (rls-patterns)
description: Advanced RLS pattern reference for the supabase-architect skill.
---

# RLS Patterns — Advanced Reference

## Princípio Fundamental

RLS = última linha de defesa no banco.
**Nunca dependa apenas de verificações no front-end.**

---

## 1. Deny-by-Default Verificação

Após habilitar RLS em qualquer tabela, confirme:

```sql
-- Esta query deve retornar 0 rows para role 'anon' sem policy:
SELECT * FROM public.sua_tabela; -- via anon key = sem acesso

-- Verificar policies ativas:
SELECT tablename, policyname, cmd, qual
FROM pg_policies
WHERE schemaname = 'public';
```

---

## 2. Padrão: Acesso por Ownership

```sql
-- Usuário acessa apenas seus próprios registros
CREATE POLICY "own records only"
  ON public.tabela FOR ALL
  USING (owner_id = auth.uid())
  WITH CHECK (owner_id = auth.uid());
```

---

## 3. Padrão: Multi-tenant por Org

```sql
-- Membros da org acessam dados da org
CREATE POLICY "org tenant isolation"
  ON public.tabela FOR SELECT
  USING (
    org_id IN (
      SELECT org_id FROM public.profiles WHERE id = auth.uid()
    )
  );
```

---

## 4. Padrão: Role-based (Admin vs Member)

```sql
-- Admin vê tudo na org; member vê apenas o próprio
CREATE POLICY "role based access"
  ON public.tabela FOR SELECT
  USING (
    org_id = public.current_user_org() AND (
      public.is_org_admin() OR owner_id = auth.uid()
    )
  );
```

---

## 5. Padrão: Dados Públicos com Leitura Anônima

```sql
-- Leitura pública (anon), escrita apenas autenticada
CREATE POLICY "public read"
  ON public.articles FOR SELECT
  USING (status = 'published');

CREATE POLICY "authenticated write"
  ON public.articles FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);
```

---

## 6. Padrão: Service Role Bypass

```sql
-- Service role bypassa RLS automaticamente.
-- Use apenas em Edge Functions com variável de ambiente SUPABASE_SERVICE_ROLE_KEY.
-- NUNCA expor no cliente front-end.
```

---

## 7. Armadilhas Comuns

| Armadilha | Solução |
|-----------|---------|
| Policy só com `FOR SELECT` — INSERT exposto | Criar policy `FOR INSERT WITH CHECK` separada |
| `USING (true)` sem condição | Sempre adicionar condição de identidade ou org |
| Esquecer `WITH CHECK` em INSERT/UPDATE | `USING` controla leitura; `WITH CHECK` controla escrita |
| Usar `auth.uid()` em função sem `SECURITY DEFINER` | Funções helper devem ser `SECURITY DEFINER` quando acessam `auth.uid()` indiretamente |
| RLS habilitado mas sem nenhuma policy | Resultado = nenhuma row visível (silencioso) |

---

## 8. Debug de RLS

```sql
-- Testar como um usuário específico:
SET LOCAL role = authenticated;
SET LOCAL request.jwt.claims = '{"sub": "uuid-do-usuario"}';
SELECT * FROM public.sua_tabela;
RESET ROLE;
```

---

## 9. Performance de RLS

- Encapsule subqueries de RLS em funções `STABLE` para cache de resultado por query
- Indexe colunas usadas em `USING` (`org_id`, `owner_id`, `user_id`)
- Use `EXPLAIN ANALYZE` para verificar se o filtro RLS está usando índices
