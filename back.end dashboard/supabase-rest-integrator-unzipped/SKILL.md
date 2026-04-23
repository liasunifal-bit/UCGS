---
name: supabase-rest-integrator
description: "Especialista em integração com APIs RESTful do Supabase. Use para: projetar conexões seguras entre front-end e Supabase, configurar headers de autenticação, implementar filtros PostgREST, paginação e operações CRUD seguras via fetch, cURL ou SDK."
---

# Supabase REST Integrator

Esta skill orienta a implementação de conexões seguras e performáticas entre aplicações front-end e o banco de dados do Supabase através da API RESTful gerada pelo PostgREST.

## Fluxo de Trabalho de Integração

1. **Definição do Objetivo**: Identifique a operação (GET, POST, PATCH, DELETE) e a tabela alvo.
2. **Configuração Base**: Utilize o endpoint `https://<project-ref>.supabase.co/rest/v1/<tabela>`.
3. **Autenticação**: Configure os headers obrigatórios (`apikey` com `anon_key` e `Authorization` com `Bearer <JWT>`).
4. **Construção da Requisição**:
   - **GET**: Defina colunas (`?select=...`), filtros (`?id=eq.1`), ordenação e paginação (Header `Range`).
   - **POST/PATCH**: Configure `Content-Type: application/json` e o body.
   - **PATCH/DELETE**: **Obrigatório** incluir filtro na URL para evitar mutações em massa.
5. **Implementação**: Forneça o código em `fetch`, `cURL` ou SDK oficial conforme a preferência.
6. **Validação e Diagnóstico**: Verifique status codes e o impacto das políticas de RLS.

## Regras de Segurança Absolutas

- **Proibido**: Nunca recomende ou utilize `service_role_key` no front-end/cliente.
- **Obrigatório**: Toda requisição `PATCH` ou `DELETE` deve conter um filtro seguro na URL.
- **RLS**: Sempre alerte que a visibilidade e manipulação dos dados dependem das políticas de Row Level Security configuradas no banco.
- **Otimização**: Priorize a seleção mínima de colunas (`?select=col1,col2`) para reduzir a carga de rede.

## Formato de Resposta Padrão

Para cada solicitação de integração, forneça:

1. **Contexto da Integração**: Objetivo e tabela.
2. **Detalhes Técnicos**: Endpoint, Método HTTP e Headers necessários.
3. **Payload/Query**: Query string ou Body JSON formatado.
4. **Exemplo de Código**: Implementação prática (fetch, cURL ou SDK).
5. **Dependência de RLS**: O que deve estar configurado no banco para a chamada funcionar.
6. **Validação e Riscos**: Como testar e quais erros comuns evitar.

## Recursos Disponíveis

- **Referências**: `/home/ubuntu/skills/supabase-rest-integrator/references/postgrest_operators.md` (Lista de operadores de filtro).

## Exemplos Rápidos

- **Filtro**: `?nome=ilike.%joao%`
- **Paginação**: Header `Range: 0-9`
- **Retorno de Dados**: Header `Prefer: return=representation`
