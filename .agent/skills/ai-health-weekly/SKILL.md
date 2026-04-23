---
name: ai-health-weekly
description: >
  Gera automaticamente um relatório semanal sobre o uso de Inteligência Artificial na Saúde e posts de carrossel para Instagram a partir de 3 fontes especializadas em saúde digital. Use esta skill SEMPRE que o usuário pedir: relatório de IA na saúde, atualização semanal de IA em saúde, post de Instagram sobre IA na saúde, notícias de saúde digital, "gerar update de IA na saúde", "criar post de saúde com IA", relatório clínico de IA, ou qualquer variação envolvendo inteligência artificial aplicada à saúde, medicina, hospitais ou sistemas clínicos. Também use quando o usuário mencionar MedPulse AI, MobiHealthNews, Healthcare IT News ou IA hospitalar.
---

# Skill: AI Health Weekly

Gera dois entregáveis semanais sobre IA aplicada à saúde:
1. **Relatório em PDF** — Curadoria das principais notícias da semana com análise clínica e de mercado, design profissional enterprise-grade
2. **Carrossel para Instagram** — HTML interativo com visual clínico moderno, pronto para captura; + legenda completa para publicação

---

## Fontes de Dados

Sempre buscar conteúdo nestas 3 URLs especializadas:

| Fonte | URL | Foco |
|---|---|---|
| MedPulse AI | https://medpulseai.com/ | IA clínica, diagnóstico assistido, ferramentas médicas |
| MobiHealthNews | https://www.mobihealthnews.com/ | Saúde digital, wearables, healthtech |
| Healthcare IT News | https://www.healthcareitnews.com/white-papers | Papers técnicos, sistemas hospitalares, TI clínica |

---

## Fluxo de Trabalho

### Passo 1 — Coleta de Conteúdo

Use `web_fetch` em cada uma das 3 fontes. Para cada uma, extraia:
- Títulos das matérias/papers mais recentes (últimos 7 dias prioritário)
- Resumos ou trechos disponíveis
- Datas de publicação
- Categoria/especialidade clínica quando disponível

```
web_fetch: https://medpulseai.com/
web_fetch: https://www.mobihealthnews.com/
web_fetch: https://www.healthcareitnews.com/white-papers
```

Se uma fonte falhar, continuar com as demais e registrar no relatório.

### Passo 2 — Curadoria e Análise Clínica

Selecione as **Top 5 a 8 notícias** da semana usando estes critérios (em ordem de prioridade):
1. **Impacto clínico direto** — afeta diagnóstico, tratamento ou fluxo hospitalar
2. **Inovação técnica** — IA generativa, modelos preditivos, sistemas de suporte à decisão
3. **Relevância regulatória ou ética** — aprovações FDA/ANVISA, vieses algorítmicos, privacidade
4. **Tendência de mercado healthtech**

Para cada notícia selecionada, prepare:
- **Título** em português BR (traduzir se necessário)
- **Resumo clínico** — 2-3 frases diretas e técnicas
- **Impacto prático** — 1 frase: "O que isso muda na prática clínica?"
- **Fonte** de origem
- **Tag de área**: `Diagnóstico` | `Gestão` | `Farmácia` | `Mental Health` | `Wearables` | `TI Clínica` | `Regulação`
- **Ícone representativo** (emoji ou código de ícone)

### Passo 3 — Gerar Relatório em PDF

Leia o skill `pdf` em `/mnt/skills/public/pdf/SKILL.md` para montar o PDF corretamente.

Gere o relatório seguindo o template em `references/relatorio-template.md`.

Estrutura do relatório PDF:
- **Capa** com data, logo-placeholder, título da edição
- **Panorama da Semana** — 3-4 frases de contexto macro
- **Destaques** — Top 5-8 notícias com análise
- **Tendência da Semana** — 1 tema emergente com análise crítica
- **Fontes e Referências**
- **Rodapé** com branding e data de geração

**Tom**: Técnico-clínico, objetivo, sem sensacionalismo. Em português BR.

Salvar como: `/mnt/user-data/outputs/ai-saude-[AAAA-MM-DD].pdf`

### Passo 4 — Gerar Carrossel para Instagram

Consulte `references/carousel-design.md` para especificações visuais.

**Estrutura do carrossel (slides)**:
1. **Capa** — "🏥 IA na Saúde | Semana de [Data]" + subtítulo de impacto
2. **Slides 2-6** — Uma notícia por slide (top 5)
3. **Slide 7** — "Tendência da Semana"
4. **Slide final** — CTA + handle do perfil

**Regras do carrossel**:
- Máx. 25 palavras por slide (leitura rápida mobile)
- Visual limpo: tipografia clara, hierarquia visual forte
- Tags coloridas por área clínica
- Sem blur excessivo, sem animações pesadas
- Paleta profissional de saúde (ver `references/carousel-design.md`)

Salvar como: `/mnt/user-data/outputs/carrossel-ia-saude-[AAAA-MM-DD].html`

### Passo 5 — Gerar Legenda para Instagram

Gere uma legenda completa para publicação no Instagram:

```
Formato:
- Linha de abertura impactante (hook)
- 3-5 bullets com os destaques da semana (emojis)
- Linha de CTA ("Salva esse post para não perder nada 📌")
- Hashtags: 15-20 relevantes em português e inglês
  (ex: #ianasamude #healthtech #inteligenciaartificial #saúdedigital #medicinadeamanha)
```

### Passo 6 — Identidade Visual

Se o usuário ainda não informou cores/nome do perfil:
> "Para personalizar o carrossel, me diga: nome do seu perfil no Instagram e paleta de cores (ou estilo: 'clínico e sóbrio' / 'moderno e tecnológico' / 'acolhedor e humano')."

Se não informado, usar a **paleta padrão clínica** definida em `references/carousel-design.md`.

### Passo 7 — Entrega Final

Apresentar ao usuário:
1. **PDF do relatório** via `present_files`
2. **HTML do carrossel** via `present_files`
3. **Legenda do Instagram** inline no chat (para copiar e colar)
4. Instrução de uso: "Abra o HTML no navegador, navegue pelos slides e capture cada tela para publicar como carrossel no Instagram."

---

## Notas Importantes

- **Idioma**: Todo conteúdo final em Português BR, mesmo que a fonte seja em inglês
- **Citações**: Sempre parafrasear; nunca reproduzir trechos longos das fontes
- **Atualidade**: Priorizar conteúdo dos últimos 7 dias
- **Design clínico**: Interface limpa, sem poluição visual, foco em leitura rápida
- **Erros de fetch**: Se uma fonte não carregar, mencionar no relatório e continuar com as demais

---

## Referências

- `references/relatorio-template.md` — Template completo do relatório semanal (estrutura e conteúdo)
- `references/carousel-design.md` — Especificações de design do carrossel HTML (paleta, tipografia, código base)
