# Operadores PostgREST (Supabase REST API)

Ao realizar consultas `GET` na API REST do Supabase, utilize os seguintes operadores na query string:

| Operador | Descrição | Exemplo |
| :--- | :--- | :--- |
| `eq` | Igual a | `?id=eq.1` |
| `neq` | Diferente de | `?status=neq.active` |
| `gt` | Maior que | `?price=gt.100` |
| `gte` | Maior ou igual a | `?age=gte.18` |
| `lt` | Menor que | `?stock=lt.5` |
| `lte` | Menor ou igual a | `?score=lte.50` |
| `like` | Correspondência de padrão (case-sensitive) | `?name=like.*John*` |
| `ilike` | Correspondência de padrão (case-insensitive) | `?email=ilike.*@gmail.com` |
| `in` | Contido em uma lista | `?id=in.(1,2,3)` |
| `is` | Verificação de nulo/booleano | `?deleted_at=is.null` |
| `fts` | Full-Text Search | `?content=fts.supabase` |

## Seleção e Ordenação

- **Seleção de Colunas**: `?select=id,name,email`
- **Ordenação**: `?order=created_at.desc` ou `?order=name.asc`
- **Contagem**: Header `Prefer: count=exact`
