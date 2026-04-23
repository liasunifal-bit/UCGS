# Plano de Reconstrução — Schema UCGS v2

> **Status:** 🟡 Aguardando aprovação
> **Projeto:** liasunifal@gmail.com's Project (`llqphjlpypnyvknpfdyn`)
> **Região:** us-west-2
> **PostgreSQL:** 17.6.1
> **Data:** 2026-04-20

---

## 1. Título da Demanda

Reconstrução completa do schema `public` do sistema UCGS (Unidade Clínica de Gestão em Saúde) no Supabase.

## 2. Objetivo da Implementação

Recriar do zero toda a estrutura de banco de dados do dashboard UCGS, corrigindo inconsistências do schema anterior (nomes de colunas conflitantes entre triggers e tabelas, funções órfãs, schema fragmentado em múltiplos SQLs desalinhados) e entregando um schema **unificado, coeso e seguro**.

## 3. Contexto do Problema

| Item | Estado |
|------|--------|
| Tabelas no `public` | **0** (todas removidas via DROP CASCADE) |
| Funções órfãs | **Limpas** (12 funções removidas) |
| Triggers | **0** |
| Dados perdidos | Tabela `profiles` tinha 2 registros, `vacinas` tinha 6. Demais estavam vazias |
| Problema raiz | Schema anterior tinha 3 arquivos SQL conflitantes (`profiles_table.sql`, `tabelas_clinicas.sql`, `fix_trigger_handle_new_user.sql`) com colunas incompatíveis entre si |

## 4. Arquitetura Impactada

```
┌────────────────────────────────────────────────────┐
│                SUPABASE PROJECT                     │
├─────────┬──────────┬───────────┬───────────────────┤
│  Auth   │ Database │  Storage  │  Edge Functions   │
│         │ (public) │           │                   │
│ users   │ 25+ tbl  │ buckets   │ (futuro)          │
│ JWT     │ RLS      │ policies  │                   │
│ triggers│ functions│           │                   │
└─────────┴──────────┴───────────┴───────────────────┘
```

### Domínios do Schema

| # | Domínio | Tabelas | Descrição |
|---|---------|---------|-----------|
| 1 | **Core** | `profiles`, `pacientes`, `audit_log`, `notificacoes` | Infraestrutura base |
| 2 | **Prontuário** | `entradas_prontuario`, `evolucoes` | Timeline clínica multidisciplinar |
| 3 | **Enfermagem** | `processos_sae`, `evolucoes_sae` | SAE (NANDA→NOC→NIC) |
| 4 | **Nutrição** | `avaliacoes_nutri`, `planos_alimentares`, `restricoes_alimentares` | Antropometria + dietas |
| 5 | **Fisioterapia** | `avaliacoes_fisio`, `sessoes_fisio` | Avaliação + sessões |
| 6 | **Odontologia** | `prontuarios_odonto`, `procedimentos_odonto`, `imagens_odonto` | Odontograma + CPO-D |
| 7 | **Psicologia** | `sessoes_psicologia` | Sessões + CID/DSM |
| 8 | **Vacinas** | `vacinas`, `doses_vacina` | Cartão vacinal |
| 9 | **Exames** | `exames_clinicos` | Lab + imagem |
| 10 | **Seg. Trabalho** | `mapas_risco`, `protocolos_manutencao`, `historico_manutencao` | PPRA/PGR |
| 11 | **Métricas** | `snapshots_metricas`, `historico_eventos` | Dashboard + analytics |

## 5. Pré-requisitos

- [x] Banco limpo (0 tabelas, 0 funções custom)
- [x] Extensão `uuid-ossp` disponível
- [x] Extensão `pg_trgm` instalada
- [x] Extensão `unaccent` instalada
- [ ] Definição final dos campos de `profiles` (alinhada com o trigger)
- [ ] Aprovação do usuário para executar

## 6. Etapas de Implementação

### Etapa 1 — Funções Utilitárias
Criar funções base reutilizáveis:
- `fn_set_updated_at()` — atualiza `updated_at` automaticamente
- `fn_is_admin()` — verifica se o usuário é admin
- `fn_get_my_role()` — retorna role do usuário autenticado

### Etapa 2 — Tabela `profiles` + Trigger de Auth
- Tabela espelho de `auth.users`
- Campos: `id`, `nome_completo`, `email`, `cpf`, `telefone`, `role`, `especialidade`, `registro_profissional`, `matricula`, `setor`, `foto_url`, `ativo`, `created_at`, `updated_at`
- Roles: `admin`, `medico`, `enfermeiro`, `tecnico_enfermagem`, `fisioterapeuta`, `nutricionista`, `dentista`, `psicologo`, `farmaceutico`
- Trigger `on_auth_user_created` com `SECURITY DEFINER`

### Etapa 3 — Tabela `pacientes`
- Cadastro central com dados demográficos + endereço
- Auto-geração de número de prontuário (`PRN-YYYYMMDDHHMMSS`)
- Trigger para auto-prontuário

### Etapa 4 — Tabelas Clínicas (Prontuário + Especialidades)
- `entradas_prontuario` — timeline consolidada
- `processos_sae` + `evolucoes_sae` — enfermagem
- `avaliacoes_nutri` + `planos_alimentares` + `restricoes_alimentares` — nutrição
- `avaliacoes_fisio` + `sessoes_fisio` — fisioterapia
- `prontuarios_odonto` + `procedimentos_odonto` + `imagens_odonto` — odontologia
- `sessoes_psicologia` — psicologia
- `vacinas` + `doses_vacina` — imunização
- `exames_clinicos` — exames

### Etapa 5 — Tabelas de Segurança do Trabalho
- `mapas_risco` — PPRA/PGR
- `protocolos_manutencao` — protocolos de equipamentos
- `historico_manutencao` — registros de manutenção

### Etapa 6 — Tabelas de Suporte (Audit + Métricas)
- `audit_log` — log genérico com trigger reutilizável
- `notificacoes` — sistema de notificações internas
- `historico_eventos` — log categorizado
- `snapshots_metricas` — cache de métricas para dashboard

### Etapa 7 — Ativação de RLS em TODAS as tabelas
- `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` em cada tabela
- Deny-by-default confirmado

### Etapa 8 — Criação de Policies RLS
Padrão por tabela:
- `SELECT`: autenticados podem ler (profissionais veem todos os pacientes/prontuários)
- `INSERT`: autenticados com `auth.uid() = autor_id` (autoria validada)
- `UPDATE`: apenas autor ou admin
- `DELETE`: apenas admin (quando permitido)

### Etapa 9 — Índices de Performance
- FKs: `paciente_id`, `autor_id`, `profissional_id`
- Filtros frequentes: `status`, `tipo`, `categoria`, `data_criacao`
- Busca textual: GIN trigram em `nome` de pacientes

## 7. Riscos e Pontos de Atenção

| Risco | Severidade | Mitigação |
|-------|-----------|-----------|
| Trigger `handle_new_user` com colunas erradas | 🔴 Crítico | Alinhar 100% com schema de `profiles` antes de criar |
| RLS ausente em alguma tabela | 🔴 Crítico | Checklist pós-migração com query de verificação |
| `service_role` exposta no front | 🔴 Crítico | Apenas `anon key` no cliente; validar `.env` |
| Perda de dados dos 2 `profiles` existentes | 🟡 Médio | Dados de teste; serão recriados no signup |
| N+1 em queries do dashboard | 🟡 Médio | Índices desde o início; `EXPLAIN ANALYZE` em produção |

## 8. Dependências Técnicas

| Dependência | Status |
|-------------|--------|
| Extensão `uuid-ossp` | ✅ Disponível |
| Extensão `pg_trgm` | ✅ Instalada |
| Extensão `unaccent` | ✅ Instalada |
| Supabase Auth configurado | ✅ Ativo |
| Front-end (login.HTML) | ✅ Existe |

## 9. Ordem Recomendada de Execução

```
Migration 1 → Funções utilitárias (fn_set_updated_at, fn_is_admin, fn_get_my_role)
Migration 2 → profiles + trigger on_auth_user_created
Migration 3 → pacientes + trigger auto-prontuário
Migration 4 → Tabelas clínicas (prontuário + todas especialidades)
Migration 5 → Tabelas de segurança do trabalho
Migration 6 → Tabelas de suporte (audit_log, notificacoes, metricas)
Migration 7 → RLS ENABLE em todas as tabelas
Migration 8 → Policies RLS por tabela e operação
Migration 9 → Índices de performance
```

## 10. Critérios de Validação

- [ ] Todas as tabelas criadas e listadas via `list_tables`
- [ ] RLS habilitado em 100% das tabelas (`rls_enabled: true`)
- [ ] Trigger `on_auth_user_created` funcional (testar com signup)
- [ ] Nenhuma tabela sem policy de acesso
- [ ] Queries de inspeção (`inspecao_schema_completo.sql`) retornam dados consistentes
- [ ] Funções utilitárias respondem corretamente

## 11. Próximos Passos Após Implementação

1. Testar signup e verificar criação automática de `profiles`
2. Popular tabela `vacinas` com dados de referência
3. Conectar front-end (login.HTML → dashboard)
4. Configurar Storage buckets para imagens odontológicas
5. Implementar Edge Functions para lógica de negócio avançada

---

> **⚠️ AGUARDANDO APROVAÇÃO** — Nenhuma execução será iniciada sem confirmação do usuário.
