<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# 🤖 Protocolo e Diretrizes de Agentes: Antigravity Lias App

Este documento define o comportamento, as regras de arquitetura e as skills recomendadas para os agentes de IA operando no diretório `antigravity-lias-app`.

## 🏗️ Sobre o Projeto

O **Antigravity Lias App** é a interface web (frontend) construída com **Next.js (App Router)**. A aplicação serve como o dashboard principal, incluindo módulos robustos para gestão de saúde e outros serviços (como Atendimento Médico/Hospital Consultation, discutido neste ambiente). O desenvolvimento deve seguir padrões impecáveis de UI/UX, interface limpa e responsiva do Next.

## 🎯 Agentes Autorizados (Tier 1 & 2)

Quando trabalhar neste diretório, o agente deve assumir ou invocar (via rotas de conhecimento) os seguintes especialistas:

1. **`@frontend-specialist` (MANDATÓRIO)**: Responsável por todo o código React, Next.js, layout, formatação e integração de componentes UI.
2. **`@backend-specialist`**: Invocado limitadamente para criação de rotas de API isoladas dentro de `app/api/` (Next.js API routes).
3. **`@orchestrator`**: Invocado para grandes refatorações ou implementações que exijam alterações multifacetadas (ex: planejar um fluxo novo complexo).

## 🛠️ Skills e Ferramentas Padrão (P0)

Antes de escrever código, o agente DEVE revisar as seguintes skills presentes na documentação, quando o contexto requisitar:

- **Next.js App Router**: `nextjs-best-practices`
- **React Patterns**: `react-patterns`, `react-ui-patterns`
- **Clean Code Frontend**: `clean-code` - O código deve ser self-documenting, evitar over-engineering e ter alta performance de carregamento web.
- **Auditoria de Design**: `frontend-design`, `ui-skills`

## 🛑 Guardrails & Regras de Implementação Locais

1. **Socratic Gate Local**: Antes de propor grandes implantações no App Router (como reformulação de navegação), o agente deve SEMPRE formatar um plano de design no formato de tarefa (task-slug) e pedir confirmação.
2. **Server vs Client Components**: Por padrão, construa componentes focados renderizados via Servidor. O header `'use client'` deve ser mantido nas folhas da árvore do DOM, apenas onde o estado, efeitos interativos e listeners são estritamente necessários.
3. **UX Premium e Regras de Design (Purple Ban)**:
   - Jamais inclua cores roxas, templates genéricos e siga as regras anti-cliché descritas na skill de UI/UX.
   - Aplique heurísticas de Core Web Vitals desde o dia um.
4. **Resolução de Roteamento**: Respeite os layouts aninhados e utilize a estrutura do diretório `app/` para separação fluida e natural. Não fuja para abordagens `pages/` antigas.

## 📂 Checagens Finais (Verificações)

Ao interagir neste workspace para desenvolvimento, adote os comandos de verificação descritos no `GEMINI.md`:
Sempre que o usuário der instruções como "final checks", garanta que os testes apropriados (lint, build ou dev local) não retornarão erros. Quando disponível, instruir rodar scripts da pasta `.agent/scripts` como o `lint_runner.py` ou `ux_audit.py`.

> **Aviso ao Agente (LLM)**: Siga isso estritamente ao escrever código dentro da pasta do App.
