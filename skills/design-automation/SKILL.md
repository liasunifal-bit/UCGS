---
name: design-automation
description: "Framework unificado para automação e geração de designs. Use para: criar pôsteres de alta qualidade, designs com texto integrado, cartazes estéticos, integração com Canva, automação de fluxos de design, gerenciamento de templates de marca, upload de ativos, exportação em múltiplos formatos e controle de versões de designs. Dispara para qualquer solicitação de criação de designs visuais, pôsteres, materiais de marketing, automação no Canva, ou gerenciamento de ativos de design."
---

# Design Automation Studio

O **Design Automation Studio** é um framework unificado que combina:
- **PosterCraft**: Geração de pôsteres estéticos com renderização precisa de texto
- **Canva Connect API**: Automação programática de designs e gerenciamento de ativos
- **Recursos Adicionais**: Exportação multi-formato, versionamento, templates reutilizáveis, histórico de mudanças

Use esta skill quando precisar criar, editar, automatizar ou gerenciar designs de qualquer tipo.

## 1. Fluxo de Trabalho - Geração de Pôsteres (PosterCraft)

### Passo 1: Definir o Conceito
Identifique o tema, texto principal e estilo visual desejado para o pôster.

### Passo 2: Preparar o Prompt
Use prompts descritivos que combinem elementos artísticos e informações textuais.

**Exemplo:**
```
"Urban Canvas Street Art Expo poster with bold graffiti-style lettering and dynamic colorful splashes, high resolution, aesthetic layout."
```

### Passo 3: Executar a Geração
```bash
python3 /scripts/generate_poster.py \
  --prompt "Seu prompt aqui" \
  --output "resultado.png" \
  --steps 28 \
  --guidance 3.5
```

### Parâmetros Recomendados
- **Steps**: 28 a 50 para melhor qualidade
- **Guidance Scale**: 3.5 é o padrão equilibrado
- **Seed**: Use sementes fixas para reprodutibilidade

### Dicas de Design para Pôsteres
- **Contraste**: Texto com contraste suficiente com o fundo
- **Hierarquia**: Descreva o texto principal como "bold" ou "large"
- **Estilo**: Experimente "Minimalist", "Cyberpunk", "Vintage", "Art Deco"

---

## 2. Fluxo de Trabalho - Integração com Canva

### Configuração Inicial

Você deve criar uma integração no [Canva Developer Portal](https://www.canva.dev/):

1. Obtenha seu **Client ID** e **Client Secret**
2. Configure os **Scopes**: `design:content:read`, `design:content:write`, `asset:read`, `asset:write`
3. Defina a **Redirect URL** para seu ambiente

### Autenticação (OAuth 2.0)

```python
from canva_api_client import CanvaAPIClient
import os

client = CanvaAPIClient(
    client_id=os.getenv("CANVA_CLIENT_ID"),
    client_secret=os.getenv("CANVA_CLIENT_SECRET")
)

# Após obter código de autorização:
token = client.authenticate(code="USER_AUTH_CODE", redirect_uri="YOUR_REDIRECT_URI")
```

### Operações Comuns no Canva

#### Listar Designs
Recupere lista de designs do usuário para edição ou visualização.

#### Criar Design a partir de Template
```python
response = client.create_design_from_template(
    template_id="BRAND_TEMPLATE_ID",
    title="Novo Post de Instagram"
)
```

#### Upload de Ativos
Envie imagens ou ativos para a biblioteca do Canva.

### Dicas de Automação Canva
- **Webhooks**: Configure para receber notificações de atualizações
- **Brand Templates**: Use para garantir identidade visual consistente
- **Segurança**: Nunca exponha `Client Secret` em código público

---

## 3. Funcionalidades Adicionais

### 3.1 Exportação Multi-Formato

Exporte seus designs em diferentes formatos:
- **PNG**: Para web e redes sociais
- **PDF**: Para impressão profissional
- **SVG**: Para escalabilidade vetorial
- **WEBP**: Para otimização web

```python
# Exemplo
design.export(format="pdf", quality="high", dpi=300)
```

## 3. Gerenciamento Avançado de Versões

O **Design Automation Studio** inclui um sistema completo de versionamento com rastreamento de mudanças, histórico detalhado e rollback seguro.

### 3.1 Criar Versão com Metadata Completa

```python
client.create_version(
    design_id="campaign_2024",
    file_path="design_v1.png",
    author="alice@company.com",
    description="Versão inicial com cores corporativas",
    tags=["draft", "design-review"],
    changes={
        "colors": ["#FF6B6B", "#4ECDC4"],
        "fonts": ["Montserrat", "Open Sans"],
        "dimensions": "1920x1080"
    },
    is_stable=False
)
```

### 3.2 Histórico Completo de Versões

```python
# Ver todas as versões
history = client.get_design_history("campaign_2024")

# Cada versão inclui:
# - version_number: "1.1", "1.2", etc
# - created_at: timestamp ISO
# - author: quem criou
# - description: mudanças realizadas
# - tags: categorização
# - file_hash: integridade do arquivo
# - is_stable: se é versão de produção
# - is_published: se foi publicada
```

### 3.3 Changelog Detalhado

```python
# Retorna log de mudanças em ordem cronológica
changelog = client.get_changelog("campaign_2024")

# Cada entrada inclui:
# - timestamp
# - version
# - author
# - action: "created", "modified", "published", "rollback"
# - description
# - mudanças específicas
```

### 3.4 Comparar Versões

```python
# Comparar duas versões específicas
comparison = client.compare_versions(
    design_id="campaign_2024",
    version1="1.1",
    version2="1.2"
)

# Retorna:
# - Diferenças de tamanho do arquivo
# - Hash das versões (detecta mudanças)
# - Tags adicionadas/removidas
# - Mudanças de metadata
# - Autores de cada versão
```

### 3.5 Rollback Seguro

```python
# Reverter para versão anterior (com backup automático)
result = client.rollback_version(
    design_id="campaign_2024",
    version="1.1",
    author="alice@company.com",
    create_backup=True  # Cria backup da versão atual
)

# Seguro: versão anterior é copiada, novo backup é criado
```

### 3.6 Marcar Versão como Estável

```python
# Marcar versão como pronta para produção
client.mark_stable(
    design_id="campaign_2024",
    version="1.3"
)

# Benefícios:
# - Apenas uma versão estável por design
# - Automaticamente tagueada com "stable" e "production"
# - Protegida na limpeza automática de versões
```

### 3.7 Publicar Versão

```python
# Marcar versão como publicada
client.publish_version(
    design_id="campaign_2024",
    version="1.3"
)

# Uso: rastrear qual versão foi para produção/redes sociais
```

### 3.8 Taggear Versões

```python
# Adicionar tags para categorizar
client.tag_version(
    design_id="campaign_2024",
    version="1.2",
    tags=["client-approved", "final-review"],
    replace=False  # Adiciona às tags existentes
)

# Depois, recuperar por tag
approved_versions = client.get_versions_by_tag(
    design_id="campaign_2024",
    tag="client-approved"
)
```

### 3.9 Versão Estável e Publicadas

```python
# Obter versão estável (production-ready)
stable = client.get_stable_version("campaign_2024")

# Obter todas as versões publicadas
published = client.get_published_versions("campaign_2024")
```

### 3.10 Estatísticas de Design

```python
# Estatísticas completas do design
stats = client.get_design_statistics("campaign_2024")

# Retorna:
# - Total de versões: 5
# - Total de mudanças no log: 12
# - Colaboradores: ["alice", "bob", "carol"]
# - Tamanho de arquivo: min, max, média
# - Datas de criação e última modificação
# - Contagem de versões publicadas
# - Se possui versão estável
```

### 3.11 Exportar Histórico Completo

```python
# Exportar todo o histórico para arquivo JSON
client.export_version_history(
    design_id="campaign_2024",
    output_path="campaign_2024_history.json"
)

# Arquivo contém:
# - Todas as versões com metadata
# - Changelog completo
# - Estatísticas
# - Data de exportação
```

### 3.12 Limpeza Automática de Versões Antigas

```python
# Manter apenas 10 versões mais recentes
client.clean_old_versions(
    design_id="campaign_2024",
    keep_count=10,
    keep_stable=True  # Sempre manter versão estável
)

# Benefícios:
# - Libera espaço em disco
# - Mantém histórico recente limpo
# - Protege versão estável
```

### 3.3 Biblioteca de Templates

Crie e gerencie templates reutilizáveis:
- Templates de marca para consistência visual
- Dimensões padrão pré-configuradas
- Elementos gráficos compartilhados
- Paletas de cores corporativas

```python
template = TemplateLibrary.create(
    name="Instagram Post 2024",
    dimensions="1080x1080",
    brand_colors=["#FF6B6B", "#4ECDC4"]
)
```

### 3.4 Histórico de Mudanças e Rollback

Rastreamento completo de todas as alterações:
- Quem fez a mudança
- Quando foi feita
- O que foi modificado
- Reverter facilmente para qualquer estado anterior

### 3.5 Integração com Banco de Dados de Imagens (Futuro)

Suporte para:
- Unsplash, Pexels, Pixabay
- Bibliotecas corporativas
- Assets customizados

### 3.6 Sistema de Anotações e Comentários

Colaboração integrada:
- Adicione comentários em designs
- Solicite revisões
- Rastreie feedback em tempo real

### 3.7 Agendamento de Publicações

Publique automaticamente em horários otimizados:
- Agende publicações futuras
- Integração com redes sociais
- Análise de melhor horário

---

## 4. Fluxo de Trabalho Recomendado

```
1. Conceitualize o Design
   ↓
2. Escolha o Método
   ├─ Gerar com PosterCraft (IA)
   └─ Usar Templates Canva
   ↓
3. Personalize e Refine
   ├─ Ajuste cores, fontes, elementos
   └─ Adicione anotações se necessário
   ↓
4. Controle de Versão
   └─ Crie versão estável
   ↓
5. Exporte
   ├─ PNG para redes sociais
   ├─ PDF para impressão
   └─ SVG para arquivos
   ↓
6. Publique (Opcional)
   ├─ Imediato
   └─ Agendado
```

---

## 5. Segurança e Melhores Práticas

### Credenciais
- Sempre use variáveis de ambiente para API keys
- Nunca commit `Client Secret` no código
- Regenere tokens regularmente

### Performance
- Cache de templates para maior rapidez
- Compressão de imagens otimizada
- Limpeza automática de versões antigas

### Backup
- Sempre mantenha backups de designs críticos
- Use versionamento para histórico
- Exporte versões finais em múltiplos formatos

---

## 6. Scripts Disponíveis

### PosterCraft
- `scripts/generate_poster.py` - Gerar pôsteres com FLUX.1-dev

### Canva Integration
- `scripts/canva_api_client.py` - Cliente Python para Canva API

### Design Management
- `scripts/version_manager.py` - Gerenciar versões de designs
- `scripts/export_handler.py` - Exportar em múltiplos formatos
- `scripts/template_library.py` - Gerenciar biblioteca de templates

---

## 7. Recursos Externos

- [MeiGen-AI/PosterCraft](https://github.com/MeiGen-AI/PosterCraft)
- [Canva Developer Portal](https://www.canva.dev/)
- [Canva Connect API Docs](https://www.canva.dev/docs/connect/)
- [FLUX.1 Model Docs](https://huggingface.co/black-forest-labs/FLUX.1-dev)

---

## 8. Troubleshooting

### Problema: Texto não renderiza corretamente no PosterCraft
**Solução**: Aumente `--steps` para 35-40, ajuste `--guidance` para 4.0-4.5

### Problema: Autenticação Canva falha
**Solução**: Verifique `Client ID/Secret`, confirme redirect URI, revise scopes necessários

### Problema: Exportação lenta
**Solução**: Reduza DPI para web, use cache de versões, paralelizar processamento

### Problema: Conflitos de versão
**Solução**: Use timestamps em nomes de versão, mantenha changelog detalhado

---

## 9. Exemplos de Uso

### Criar e Exportar Pôster de Evento
```bash
python3 /scripts/generate_poster.py \
  --prompt "Tech Summit 2024 poster with modern design, bold typography, tech elements" \
  --output "tech_summit.png" \
  --steps 40
  
python3 /scripts/export_handler.py \
  --input tech_summit.png \
  --formats png,pdf,svg \
  --dpi 300
```

### Automatizar Design no Canva com Template de Marca
```python
client = CanvaAPIClient(client_id, client_secret)
client.authenticate(code, redirect_uri)

designs = client.list_designs()

# Criar novo design baseado em template
new_design = client.create_design_from_template(
    template_id="BRAND_TEMPLATE_123",
    title="Campanha Marketing Q1 2024"
)
```

---

## 10. Galeria de Inspiração

### 🎨 Inspirações Pré-definidas

A skill inclui uma **Galeria de Inspiração** completa com exemplos para diferentes tipos de posts:

#### Categorias Disponíveis

**1. Instagram Posts**
- Energético Moderno: Para startups e tech
- Minimalista Elegante: Para moda e luxo

**2. LinkedIn Posts**
- Profissional Corporativo: Para B2B e empresas

**3. TikTok/Reels**
- Viral Divertido: Para humor e trends

**4. YouTube**
- Thumbnail Impactante: Para canais de vídeo

**5. Moda e Estilo**
- Lançamento de coleção
- Outfit do dia
- Promoções

**6. Educação**
- Tutorial em passos
- Pergunta interativa
- Infográfico

#### Como Usar a Galeria

```python
from inspiration_gallery import InspirationGallery

gallery = InspirationGallery()

# Buscar por categoria
instagram_posts = gallery.get_inspiration_by_category("instagram")

# Buscar por mood
energetic = gallery.get_inspiration_by_mood("energético")

# Buscar por termo
tech_posts = gallery.search_inspirations("tech")

# Gerar prompt automático
prompt = gallery.get_inspiration_prompt(inspiration_id)

# Obter paleta de cores
colors = gallery.get_color_suggestions(inspiration_id)

# Obter guia tipográfico
typography = gallery.get_typography_guide(inspiration_id)

# Gerar brief profissional
brief = gallery.generate_design_brief(inspiration_id)
```

#### Exemplos de Posts por Objetivo

**Para Vendas/Conversão:**
- CTA claro ("COMPRE", "SAIBA MAIS")
- Desconto destacado
- Foto do produto em alta qualidade
- Preço visível
- Link de compra fácil

**Para Educação:**
- Título claro
- Passos numerados (máx 5-6)
- Ícones ilustrando
- Dados e estatísticas
- Conclusão clara

**Para Engajamento:**
- Pergunta clara
- Opções visuais
- Espaço para comentários
- Tema relevante
- CTA para comentar

#### Paletas de Cores Pré-definidas

- **Vibrante**: Energético, moderno
- **Profissional**: Corporativo, confiança
- **Natural**: Saúde, bem-estar
- **Criativa**: Inovação, design
- **Luxo**: Premium, elegância

---

## 11. Suporte e Feedback

Para questões, bugs ou sugestões de melhorias, consulte a documentação oficial das tools integradas ou relatar problemas nos repositórios correspondentes.
