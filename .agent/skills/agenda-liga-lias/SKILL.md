---
name: agenda-liga-lias
description: >
  Cria a agenda visual semanal da Liga LIAS (Liga de Inteligência Artificial na Saúde – UNIFAL-MG)
  como arquivo PNG pronto para compartilhar no WhatsApp, Instagram ou importar no Canva.
  Use este skill SEMPRE que o usuário pedir para criar, gerar, montar ou atualizar a agenda
  da liga, agenda semanal da LIAS, agenda da semana, ou qualquer variação dessas frases.
  Também acione quando o usuário fornecer datas, eventos ou lembretes e pedir para montar
  um card ou visual para enviar nos grupos. O skill gera automaticamente o PNG final com
  as cores e identidade visual da Liga LIAS, sem precisar de ferramentas externas.
---

# Agenda Liga LIAS — Gerador Visual

Este skill gera um PNG da agenda semanal da Liga LIAS a partir das informações fornecidas pelo usuário. O visual segue a identidade da liga: fundo azul petróleo escuro, verde teal (#1D9E75) e azul (#2a8ab8), tipografia Montserrat/Inter, e a logo da liga no cabeçalho.

---

## Fluxo de execução

### 1. Coletar informações

Se o usuário não fornecer todas as informações abaixo, pergunte antes de gerar:

- **Período da semana** (ex: "23 a 27 de março de 2025")
- **Datas importantes** — para cada evento:
  - Dia e mês
  - Nome do evento
  - Horário
  - Modalidade (online / presencial)
  - Tags extras (grupos, nomes, etc.)
- **Modelo de divulgação no Instagram** (dia da semana + nome do pôster) — se houver
- **Informações para os ligantes** — recado geral (ex: tarefas no site)
- **Logo da liga** — verificar se o usuário anexou o arquivo de imagem. Se não houver, usar o SVG fallback embutido no template.

### 2. Montar o calendário corretamente

Antes de gerar o HTML, calcule em qual **dia da semana** cada data importante cai:

- Seg=0, Ter=1, Qua=2, Qui=3, Sex=4, Sáb=5, Dom=6
- A linha do calendário exibe **7 dias consecutivos** iniciando na segunda-feira da semana do evento principal
- Coloque destaque (círculo verde) **somente nos dias com evento**
- Dias de fim de semana recebem a classe `fds` (cor mais apagada)

Use Python para calcular:
```python
from datetime import date
d = date(AAAA, MM, DD)
print(d.strftime("%A"), d.weekday())  # 0=seg, 4=sex
```

### 3. Gerar o PNG

Execute o script `scripts/gerar_png.py` passando as variáveis coletadas. Leia o script antes de executar para entender os parâmetros.

```bash
python3 /tmp/agenda-liga-lias/scripts/gerar_png.py \
  --semana "23 a 27 de março de 2025" \
  --logo "/caminho/para/logo.jpeg"
```

> O script aceita os dados via variáveis Python diretamente (edite a seção `# === DADOS ===` no topo do script antes de executar). Isso é mais confiável do que argumentos de linha de comando para conteúdo com caracteres especiais.

### 4. Apresentar o arquivo

Copie o PNG gerado para `/mnt/user-data/outputs/agenda_liga_lias.png` e use `present_files` para entregá-lo ao usuário.

---

## Identidade visual (referência rápida)

| Elemento | Valor |
|---|---|
| Fundo principal | `#0d2535` |
| Fundo cards | `#112a3a` |
| Verde primário | `#1D9E75` |
| Verde escuro | `#0F6E56` |
| Azul primário | `#2a8ab8` |
| Azul escuro | `#185FA5` |
| Texto principal | `#d8f0ea` |
| Texto secundário | `#5a9aaa` |
| Borda cards | `#1e4a5e` |
| Fonte títulos | Montserrat 700/800 |
| Fonte corpo | Inter 400/500 |

---

## Estrutura do card (seções)

1. **Header** — logo à esquerda + título "Agenda Liga LIAS" + subtítulo + pill da semana
2. **Datas importantes** — um card por evento com data destacada, título, horário, tags
3. **Divulgação no Instagram** — grid 2 colunas (segundas / sextas)
4. **Informações para os ligantes** — card com ícone "i"
5. **Visão da semana** — calendário de 7 dias, destaque apenas nos dias com evento
6. **Footer** — nome da liga + UNIFAL-MG + ano

Seções sem conteúdo devem ser **omitidas** do card gerado.

---

## Notas importantes

- **Largura do card**: 800px, fundo body `#0a1520`
- **Screenshot**: use Playwright (`playwright install chromium`) para capturar apenas o elemento `.card`
- **Logo**: se fornecida pelo usuário, converter para base64 e embutir no HTML. Se não fornecida, o SVG fallback é exibido automaticamente.
- **Fontes**: carregadas via Google Fonts (requer conexão). Se offline, Montserrat/Inter fazem fallback para `sans-serif`.
- Para ver o template HTML completo, leia `scripts/gerar_png.py`.
