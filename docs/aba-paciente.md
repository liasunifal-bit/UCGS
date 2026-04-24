# Contexto Técnico: Aba Paciente & Prontuário Eletrônico

## 1. Visão Geral
A **Aba Paciente** gerencia o fluxo completo de dados clínicos e cadastrais no ecossistema UCGS. O módulo está implementado em Javascript Vanilla (ES6+) e é composto por dois subsistemas principais, ambos injetados no dashboard central:
1. **Gestão de Pacientes** (Prefixo `pac-`): Cadastro, edição, listagem e controle de status.
2. **Prontuário Eletrônico do Paciente - PEP** (Prefixo `prt-`): Timeline clínica, evoluções, prescrições e gestão de exames.

## 2. Arquitetura de Dados (Integração Supabase)
A aba paciente foi modernizada para sincronizar com o banco de dados Supabase via `window.PacientesService`.
- **`pacFetchSupabase()`**: Método assíncrono que busca a lista de pacientes diretamente do Supabase e atualiza o estado local (`window.pacStateArray`).
- **`pacSave()` / `pacToggleStatus()`**: Realizam chamadas de inserção (`insertPaciente`) e atualização (`updatePaciente`) no backend antes de re-renderizar a tabela (optimistic-like UI ou recarga após sucesso).
- **Fallback de Armazenamento**: O sistema foi estruturado com compatibilidade para demonstração offline (usando arrays estáticos ou `localStorage` quando o serviço não está instanciado).

## 3. Estrutura do Módulo de Pacientes (`pac-`)
- **Máscaras e Validação**: Funções globais (`pacMaskCPF`, `pacMaskPhone`, `pacMaskCEP`) e validação estrita de CPF (`pacValidateCPF`).
- **Tabela e Paginação**: Renderização dinâmica (`pacRenderTable`) com 10 pacientes por página e busca reativa por Nome, CPF ou Prontuário.
- **Painel de Estatísticas**: Contagem de pacientes totais, ativos, inativos e cadastros do mês.
- **Modal de Cadastro/Edição**: 
  - Geração automática de identificadores lógicos (`PAC-XXX`) e número de prontuário (`PRN-XXXXXX`).
  - Coleta de dados socio-demográficos e endereço completo.

## 4. Prontuário Eletrônico do Paciente (`prt-`)
O módulo de prontuário é focado no acompanhamento detalhado e histórico clínico.
- **Estrutura de Abas**:
  - `Timeline`: Histórico cronológico de eventos.
  - `Resumo Clínico`: Alergias, comorbidades, tipagem sanguínea, biometria (Peso/Altura/IMC) e medicações ativas.
  - `Prescrições`: Histórico de medicamentos prescritos.
  - `Exames`: Resultados laboratoriais e de imagem.
- **Tipologia de Evoluções**: Categorização visual por cor (`prtDotColor`) e tipo: 
  - *Evolução* (Azul)
  - *Prescrição* (Verde)
  - *Exame* (Laranja)
  - *Procedimento* (Roxo)
  - *Enfermagem / Intercorrência* (Vermelho)
- **Seleção de Pacientes**: Uma barra lateral (`prtRenderPatientList`) que filtra rapidamente os pacientes ativos/internados para visualização do prontuário específico, usando uma arquitetura baseada em ID (`selectedPatientId`).

## 5. Convenções de Nomenclatura (CSS/JS)
Para garantir isolamento de escopo no contexto do Painel de Controle:
- Variáveis de estado prefixadas com `pac` (ex: `pacStateArray`, `pacCurrentPage`) e `prt` (ex: `prtState`).
- Classes CSS prefixadas com `.pac-` (Tabelas, Cards, Modais) e `.prt-` (Layout do Prontuário, Timeline, Badges).
- Manipulação visual através do padrão Glassmorphism v25 definido globalmente.

---
*Documentação gerada após integração completa do módulo de pacientes e prontuários.*
