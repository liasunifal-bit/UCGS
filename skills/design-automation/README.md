# Design Automation Studio

Skill unificada para automação completa de designs, combinando **PosterCraft** (geração de pôsteres com IA) e **Canva Connect API** (integração programática com Canva), com funcionalidades adicionais de versionamento, exportação multi-formato e gerenciamento de templates.

## 🎯 Funcionalidades Principais

### 1. **PosterCraft Integration**
- Geração de pôsteres estéticos com renderização precisa de texto
- Modelos FLUX.1-dev e Qwen3-8B
- Controle fino via parâmetros: steps, guidance scale, seed
- Suporte para geração em lote

### 2. **Canva API Integration**
- Autenticação OAuth 2.0
- Listagem e criação de designs programaticamente
- Automação baseada em templates de marca
- Upload de ativos e gerenciamento de biblioteca

### 3. **Gerenciamento de Versões**
- Histórico completo de mudanças
- Rollback para versões anteriores
- Rastreamento de alterações com timestamps
- Changelog automático

### 4. **Exportação Multi-Formato**
- PNG, PDF, SVG, WEBP
- Controle de qualidade e DPI
- Exportação em lote
- Otimização para diferentes plataformas

### 5. **Biblioteca de Templates**
- Organização por categoria
- Rastreamento de uso
- Templates de marca corporativa
- Busca e filtros
- Importação/exportação

### 6. **Recursos Futuros**
- Anotações e comentários
- Agendamento de publicações
- Integração com banco de dados de imagens
- Análise de desempenho

## 📦 Estrutura da Skill

```
design-automation/
├── SKILL.md                          # Documentação principal
├── scripts/
│   ├── design_automation_client.py    # Cliente unificado
│   ├── template_library.py            # Gerenciador de templates
│   ├── generate_poster.py             # Script PosterCraft (original)
│   └── canva_api_client.py           # Cliente Canva (original)
├── examples/
│   └── examples_usage.py             # Exemplos práticos
└── README.md                         # Este arquivo
```

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- pip ou conda
- Dependências do PosterCraft (FLUX.1-dev)

### Passos de Instalação

1. **Clone ou copie a skill**
```bash
# Se em um repositório
git clone <repo-url>
cd design-automation

# Ou copie os arquivos diretamente
cp -r design-automation /caminho/para/skills/
```

2. **Instale as dependências**
```bash
pip install requests Pillow reportlab svgwrite
```

3. **Configure credenciais (opcional, para Canva)**
```bash
export CANVA_CLIENT_ID="seu_client_id"
export CANVA_CLIENT_SECRET="seu_client_secret"
```

## 💡 Uso Rápido

### Exemplo 1: Gerar um Pôster
```python
from design_automation_client import DesignAutomationClient

client = DesignAutomationClient()

result = client.generate_poster(
    prompt="Summer festival poster with vibrant colors",
    output_path="festival.png",
    steps=30,
    guidance=3.5
)

print(result)  # {'status': 'success', 'output': 'festival.png', ...}
```

### Exemplo 2: Versionar um Design
```python
# Criar versão
version = client.create_version(
    design_id="festival_2024",
    file_path="festival.png",
    description="Versão inicial aprovada"
)

# Ver histórico
history = client.get_design_history("festival_2024")
for v in history:
    print(f"{v['version']}: {v['description']}")
```

### Exemplo 3: Exportar em Múltiplos Formatos
```python
# Exportar para vários formatos
result = client.export_multi_format(
    input_path="festival.png",
    output_dir="./exports",
    formats=["png", "pdf", "svg"],
    quality="high"
)
```

### Exemplo 4: Gerenciar Templates
```python
from template_library import TemplateLibrary

lib = TemplateLibrary()

# Criar template
template = lib.create_template(
    name="Instagram Post",
    category="social_media",
    dimensions={"width": 1080, "height": 1080},
    brand_colors=["#FF6B6B", "#4ECDC4"],
    description="Post padrão para Instagram"
)

# Listar por categoria
instagram_templates = lib.get_templates_by_category("social_media")

# Usar template (incrementa contador)
lib.get_template(template['id'])
```

### Exemplo 5: Integração com Canva
```python
# Autenticar
client.canva_authenticate(code="auth_code", redirect_uri="https://seu-app.com/callback")

# Listar designs
designs = client.canva_list_designs()

# Criar design de template
new_design = client.canva_create_from_template(
    template_id="TEMPLATE_ID",
    title="Nova Campanha"
)
```

## 🔧 Configuração Avançada

### Personalizar Geração de Pôsteres

```python
# Para pôsteres mais realistas
result = client.generate_poster(
    prompt="Professional business poster...",
    steps=50,      # Mais passos = melhor qualidade
    guidance=4.0   # Mais alto = segue prompt mais fielmente
)

# Com seed para reprodutibilidade
result = client.generate_poster(
    prompt="...",
    seed=42  # Mesmo seed = mesmo resultado
)
```

### Configurar Biblioteca de Templates

```python
# Caminho customizado
lib = TemplateLibrary(library_path="/mnt/templates")

# Importar templates existentes
result = lib.import_templates("templates_backup.json", merge=True)

# Exportar para backup
lib.export_templates("templates_backup.json")

# Ver estatísticas
stats = lib.get_statistics()
print(f"Total: {stats['total_templates']}")
print(f"Uso médio: {stats['average_usage']:.1f}")
```

### Fluxo Completo de Trabalho

Veja `examples/examples_usage.py` para exemplos completos de:
- Criar e versionar pôsteres
- Gerar em lote
- Exportar multi-formato
- Gerenciar templates
- Integração Canva

## 📚 Documentação

- **SKILL.md** - Documentação completa
- **examples_usage.py** - Exemplos práticos
- **design_automation_client.py** - Docstrings do cliente
- **template_library.py** - Docstrings do gerenciador

## 🔐 Segurança

### Credenciais
```bash
# Sempre use variáveis de ambiente
export CANVA_CLIENT_ID="..."
export CANVA_CLIENT_SECRET="..."

# Nunca faça commit de credenciais
# Adicione a .gitignore:
.env
*.secret
credentials.json
```

### Boas Práticas
- Regenere tokens regularmente
- Use HTTPS para callbacks
- Valide entrada de prompts
- Monitore uso da API
- Faça backup de designs críticos

## 🐛 Troubleshooting

### Problema: Texto não renderiza bem no PosterCraft
**Solução:** Aumente `steps` para 35-40 e `guidance` para 4.0-4.5

### Problema: Canva auth falha
**Solução:** Verifique credenciais, redirect URI, e scopes configurados

### Problema: Exportação muito lenta
**Solução:** Reduza DPI para web, processe em paralelo, use cache

### Problema: Conflitos de versão
**Solução:** Use timestamps em nomes, mantenha changelog detalhado

## 🤝 Contribuindo

Contribuições são bem-vindas! Para melhorias:

1. Abra uma issue descrevendo a funcionalidade/bug
2. Faça fork e crie branch (`git checkout -b feature/melhoria`)
3. Commit as mudanças (`git commit -am 'Add feature'`)
4. Push para branch (`git push origin feature/melhoria`)
5. Abra um Pull Request

## 📝 Changelog

### v1.0.0 (2024)
- ✨ Integração PosterCraft
- ✨ Integração Canva API
- ✨ Gerenciamento de versões
- ✨ Exportação multi-formato
- ✨ Biblioteca de templates
- 📚 Documentação completa

## 📄 Licença

Esta skill é fornecida como é, para uso em projetos de design e automação.

## 📧 Suporte

Para problemas ou dúvidas:
- Consulte a documentação em SKILL.md
- Verifique examples_usage.py
- Abra uma issue no repositório

## 🙏 Agradecimentos

- **MeiGen-AI** pelo PosterCraft
- **Canva** pela excelente API
- Comunidade de contribuidores

---

**Feito com ❤️ para designers e desenvolvedores automatizar e criar designs incríveis.**
