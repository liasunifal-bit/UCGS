# Design System: Carrossel Instagram — IA na Saúde

## Especificações Gerais

- **Dimensões**: 1080×1080px (quadrado) — padrão Instagram
- **Slides**: 7-8 slides por carrossel
- **Implementação**: HTML single-file com navegação por botões
- **Fonte**: `Inter`, fallback `system-ui, sans-serif` (importar do Google Fonts)
- **Arquivo de saída**: `.html` interativo para captura de tela

---

## Paleta de Cores

### Paleta Padrão — "Clínico Moderno" (usar quando identidade visual não informada)

```css
:root {
  /* Backgrounds */
  --bg-primary: #0d1b2a;       /* Azul noite clínico (fundo principal) */
  --bg-card: #112240;          /* Card mais claro */
  --bg-accent: #1b3a5c;        /* Hover / destaque sutil */

  /* Texto */
  --text-primary: #e8f4f8;     /* Branco levemente azulado */
  --text-secondary: #8bbbd4;   /* Azul claro para subtítulos */
  --text-muted: #5a8fa8;       /* Texto terciário */

  /* Acentos */
  --accent-primary: #00b4d8;   /* Azul ciano — cor de ação */
  --accent-secondary: #0077b6; /* Azul médio */
  --accent-warm: #48cae4;      /* Ciano claro */

  /* Tags de área clínica */
  --tag-diagnostico: #0ea5e9;
  --tag-gestao: #8b5cf6;
  --tag-farmacia: #10b981;
  --tag-mental: #f59e0b;
  --tag-wearables: #06b6d4;
  --tag-ti-clinica: #6366f1;
  --tag-regulacao: #ef4444;

  /* UI */
  --border: rgba(0, 180, 216, 0.2);
  --shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}
```

### Variante Clara — "Saúde Humana" (quando usuário pedir estilo mais acolhedor)

```css
:root {
  --bg-primary: #f8fafc;
  --bg-card: #ffffff;
  --text-primary: #0f172a;
  --text-secondary: #334155;
  --accent-primary: #0077b6;
  --accent-secondary: #00b4d8;
}
```

---

## Tipografia

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Hierarquia */
.slide-title    { font-size: 32px; font-weight: 800; line-height: 1.2; }
.slide-body     { font-size: 18px; font-weight: 400; line-height: 1.6; }
.slide-tag      { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; }
.slide-source   { font-size: 13px; font-weight: 400; opacity: 0.65; }
.slide-number   { font-size: 13px; font-weight: 500; opacity: 0.5; }
```

---

## Estrutura HTML Base

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IA na Saúde — Carrossel</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    /* Reset */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
      font-family: 'Inter', system-ui, sans-serif;
      background: #0a1628;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 20px;
    }

    /* Container do slide */
    .carousel-wrapper {
      position: relative;
      width: 540px; /* 1080/2 para preview */
      aspect-ratio: 1;
    }

    .slide {
      display: none;
      width: 100%;
      height: 100%;
      border-radius: 12px;
      overflow: hidden;
      position: relative;
    }
    .slide.active { display: flex; }

    /* Navegação */
    .nav {
      display: flex;
      gap: 12px;
      margin-top: 20px;
      justify-content: center;
      align-items: center;
    }
    .nav-btn {
      background: rgba(0, 180, 216, 0.2);
      border: 1px solid rgba(0, 180, 216, 0.4);
      color: #00b4d8;
      padding: 10px 24px;
      border-radius: 8px;
      cursor: pointer;
      font-family: 'Inter', sans-serif;
      font-size: 14px;
      font-weight: 600;
      transition: background 0.2s;
    }
    .nav-btn:hover { background: rgba(0, 180, 216, 0.35); }
    .nav-dots {
      display: flex;
      gap: 6px;
    }
    .dot {
      width: 6px; height: 6px;
      border-radius: 50%;
      background: rgba(255,255,255,0.25);
      cursor: pointer;
      transition: background 0.2s;
    }
    .dot.active { background: #00b4d8; }

    /* Slide info */
    .slide-counter {
      margin-top: 12px;
      color: rgba(255,255,255,0.4);
      font-size: 13px;
      text-align: center;
    }
  </style>
</head>
<body>

<div class="carousel-wrapper">
  <!-- SLIDE 1: CAPA -->
  <div class="slide active" id="slide-1">
    <!-- Conteúdo da capa aqui -->
  </div>

  <!-- SLIDES 2-6: Notícias -->
  <!-- Repetir para cada notícia -->

  <!-- SLIDE FINAL: CTA -->
  <div class="slide" id="slide-final">
    <!-- CTA aqui -->
  </div>
</div>

<div class="nav">
  <button class="nav-btn" onclick="changeSlide(-1)">← Anterior</button>
  <div class="nav-dots" id="dots"></div>
  <button class="nav-btn" onclick="changeSlide(1)">Próximo →</button>
</div>
<div class="slide-counter" id="counter">Slide 1 de N</div>

<script>
  let current = 0;
  const slides = document.querySelectorAll('.slide');
  const dotsContainer = document.getElementById('dots');
  const counter = document.getElementById('counter');

  // Criar dots
  slides.forEach((_, i) => {
    const dot = document.createElement('div');
    dot.className = 'dot' + (i === 0 ? ' active' : '');
    dot.onclick = () => goTo(i);
    dotsContainer.appendChild(dot);
  });

  function goTo(n) {
    slides[current].classList.remove('active');
    dotsContainer.children[current].classList.remove('active');
    current = (n + slides.length) % slides.length;
    slides[current].classList.add('active');
    dotsContainer.children[current].classList.add('active');
    counter.textContent = `Slide ${current + 1} de ${slides.length}`;
  }

  function changeSlide(dir) { goTo(current + dir); }
  
  // Teclado
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') changeSlide(1);
    if (e.key === 'ArrowLeft') changeSlide(-1);
  });
</script>
</body>
</html>
```

---

## Templates de Slide

### Slide de Capa

```html
<div class="slide active" style="background: linear-gradient(135deg, #0d1b2a 0%, #0077b6 100%); flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 50px 40px;">
  <div style="font-size: 48px; margin-bottom: 16px;">🏥</div>
  <div style="font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #00b4d8; margin-bottom: 12px;">Atualização Semanal</div>
  <h1 style="font-size: 36px; font-weight: 800; color: #e8f4f8; line-height: 1.2; margin-bottom: 16px;">IA na Saúde</h1>
  <p style="font-size: 18px; color: #8bbbd4; line-height: 1.5; max-width: 380px;">[SUBTÍTULO IMPACTANTE DA SEMANA]</p>
  <div style="margin-top: 32px; font-size: 13px; color: #5a8fa8;">Semana de [DD/MM] a [DD/MM/AAAA]</div>
  <!-- Decoração: linha horizontal sutil -->
  <div style="position: absolute; bottom: 40px; left: 40px; right: 40px; height: 1px; background: rgba(0,180,216,0.3);"></div>
  <div style="position: absolute; bottom: 20px; left: 40px; right: 40px; font-size: 12px; color: #5a8fa8; text-align: center;">@[handle do perfil]</div>
</div>
```

### Slide de Notícia

```html
<div class="slide" style="background: #112240; flex-direction: column; padding: 40px; position: relative;">
  <!-- Header: número + tag -->
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
    <span style="font-size: 13px; color: #5a8fa8; font-weight: 500;">0[N] — destaque</span>
    <span style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; background: rgba([TAG-COLOR-RGB], 0.15); color: [TAG-COLOR]; border: 1px solid rgba([TAG-COLOR-RGB], 0.3); padding: 4px 12px; border-radius: 20px;">[ÁREA CLÍNICA]</span>
  </div>
  
  <!-- Título -->
  <h2 style="font-size: 22px; font-weight: 800; color: #e8f4f8; line-height: 1.3; margin-bottom: 16px;">[TÍTULO]</h2>
  
  <!-- Corpo -->
  <p style="font-size: 15px; color: #8bbbd4; line-height: 1.6; flex: 1;">[RESUMO — máx. 25 palavras]</p>
  
  <!-- Impacto -->
  <div style="background: rgba(0,180,216,0.08); border-left: 3px solid #00b4d8; border-radius: 0 8px 8px 0; padding: 12px 16px; margin-top: 20px;">
    <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #00b4d8; margin-bottom: 4px;">⚡ Impacto clínico</div>
    <p style="font-size: 13px; color: #8bbbd4; line-height: 1.5;">[1 FRASE DE IMPACTO PRÁTICO]</p>
  </div>
  
  <!-- Fonte -->
  <div style="margin-top: 16px; font-size: 12px; color: #5a8fa8;">Fonte: [NOME DA FONTE]</div>
  
  <!-- Barra de progresso decorativa -->
  <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #00b4d8, #0077b6);"></div>
</div>
```

### Slide de Tendência

```html
<div class="slide" style="background: linear-gradient(180deg, #112240 0%, #0d1b2a 100%); flex-direction: column; padding: 40px;">
  <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #00b4d8; margin-bottom: 16px;">📈 Tendência da Semana</div>
  <h2 style="font-size: 24px; font-weight: 800; color: #e8f4f8; line-height: 1.3; margin-bottom: 20px;">[TEMA EMERGENTE]</h2>
  
  <div style="display: flex; flex-direction: column; gap: 12px; flex: 1;">
    <div style="display: flex; gap: 12px; align-items: flex-start;">
      <span style="font-size: 18px;">🔭</span>
      <p style="font-size: 14px; color: #8bbbd4; line-height: 1.5;">[OPORTUNIDADE OU APLICAÇÃO]</p>
    </div>
    <div style="display: flex; gap: 12px; align-items: flex-start;">
      <span style="font-size: 18px;">⚠️</span>
      <p style="font-size: 14px; color: #8bbbd4; line-height: 1.5;">[RISCO OU LIMITAÇÃO]</p>
    </div>
    <div style="display: flex; gap: 12px; align-items: flex-start;">
      <span style="font-size: 18px;">🎯</span>
      <p style="font-size: 14px; color: #8bbbd4; line-height: 1.5;">[PRÓXIMO PASSO ESPERADO]</p>
    </div>
  </div>
</div>
```

### Slide Final — CTA

```html
<div class="slide" style="background: linear-gradient(135deg, #0077b6 0%, #0d1b2a 100%); flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 50px 40px;">
  <div style="font-size: 44px; margin-bottom: 20px;">🔔</div>
  <h2 style="font-size: 26px; font-weight: 800; color: #e8f4f8; line-height: 1.3; margin-bottom: 16px;">Ative as notificações para não perder nada!</h2>
  <p style="font-size: 15px; color: #8bbbd4; line-height: 1.6; max-width: 360px; margin-bottom: 28px;">Todo [dia da semana] você recebe as principais atualizações de IA na saúde aqui no perfil.</p>
  <div style="background: rgba(0,180,216,0.15); border: 1px solid rgba(0,180,216,0.4); border-radius: 12px; padding: 16px 28px;">
    <p style="font-size: 20px; font-weight: 700; color: #00b4d8;">@[handle do perfil]</p>
  </div>
  <p style="margin-top: 24px; font-size: 13px; color: #5a8fa8;">💾 Salva esse carrossel para consultar depois</p>
</div>
```

---

## Tags por Área Clínica — Cores

| Área | CSS Color | RGB para background |
|---|---|---|
| Diagnóstico | `#0ea5e9` | `14, 165, 233` |
| Gestão | `#8b5cf6` | `139, 92, 246` |
| Farmácia | `#10b981` | `16, 185, 129` |
| Mental Health | `#f59e0b` | `245, 158, 11` |
| Wearables | `#06b6d4` | `6, 182, 212` |
| TI Clínica | `#6366f1` | `99, 102, 241` |
| Regulação | `#ef4444` | `239, 68, 68` |

---

## Regras de Design (Não Violar)

1. **Nunca** usar blur, glow exagerado ou box-shadow acima de `0 4px 20px rgba(0,0,0,0.4)`
2. **Nunca** usar mais de 3 tamanhos de fonte por slide
3. **Nunca** usar mais de 2 cores de texto por slide (primário + secundário)
4. **Sempre** garantir contraste mínimo 4.5:1 (WCAG AA)
5. **Sempre** manter padding interno de no mínimo 40px em todos os lados
6. **Máximo** 25 palavras no corpo de cada slide (fora título e tag)
7. **Sem** animações de entrada/saída — transições apenas na navegação
