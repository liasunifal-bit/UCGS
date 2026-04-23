---
name: postercraft
description: "Framework avançado para geração de pôsteres estéticos com renderização precisa de texto. Use para: criar pôsteres de alta qualidade, designs com texto integrado, cartazes de eventos e materiais visuais profissionais."
---

# PosterCraft

O **PosterCraft** é um framework unificado para a geração de pôsteres estéticos de alta qualidade que se destaca na renderização precisa de texto e na integração perfeita de arte abstrata.

## Fluxo de Trabalho

### 1. Definir o Conceito
Identifique o tema, o texto principal e o estilo visual desejado para o pôster. O PosterCraft funciona melhor com prompts descritivos que combinam elementos artísticos e informações textuais.

### 2. Preparar o Prompt
O prompt deve ser detalhado. Exemplo:
> "Urban Canvas Street Art Expo poster with bold graffiti-style lettering and dynamic colorful splashes, high resolution, aesthetic layout."

### 3. Executar a Geração
Use o script de inferência para gerar o pôster. O script padrão utiliza o modelo FLUX.1-dev como base e o transformador customizado do PosterCraft para garantir a qualidade do texto.

```bash
python3 /home/ubuntu/skills/postercraft/scripts/generate_poster.py \
  --prompt "Seu prompt aqui" \
  --output "resultado.png" \
  --steps 28 \
  --guidance 3.5
```

### 4. Parâmetros Recomendados
- **Steps**: 28 a 50 para melhor qualidade.
- **Guidance Scale**: 3.5 é o padrão equilibrado.
- **Seed**: Use sementes fixas para reprodutibilidade ou aleatórias para exploração.

## Recursos Adicionais
- **Repositório Original**: [MeiGen-AI/PosterCraft](https://github.com/MeiGen-AI/PosterCraft)
- **Modelos Suportados**: FLUX.1-dev, Qwen3-8B.

## Dicas de Design
- **Contraste**: Certifique-se de que o texto solicitado tenha contraste suficiente com o fundo descrito.
- **Hierarquia**: Descreva o texto principal como "bold" ou "large" para garantir que ele seja o foco central.
- **Estilo**: Experimente estilos como "Minimalist", "Cyberpunk", "Vintage" ou "Art Deco" para variar a estética.
