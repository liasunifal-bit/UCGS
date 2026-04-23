---
name: canva-connect-api
description: "Integração oficial com a Canva Connect API para automação de designs e gerenciamento de ativos. Use para: criar designs programaticamente, listar templates de marca, fazer upload de imagens e automatizar fluxos de trabalho no Canva."
---

# Canva Connect API

A Skill **Canva Connect API** permite que você interaja programaticamente com a plataforma Canva, automatizando a criação de designs e o gerenciamento de ativos de marca.

## Fluxo de Trabalho

### 1. Configuração Inicial
Para usar esta Skill, você deve primeiro criar uma integração no [Canva Developer Portal](https://www.canva.dev/).
- Obtenha seu **Client ID** e **Client Secret**.
- Configure os **Scopes** necessários (ex: `design:content:read`, `design:content:write`, `asset:read`, `asset:write`).
- Defina a **Redirect URL** para o seu ambiente de autenticação.

### 2. Autenticação (OAuth 2.0)
A API do Canva utiliza o fluxo OAuth 2.0. Você precisará trocar um código de autorização por um token de acesso.

```python
from canva_api_client import CanvaAPIClient
import os

client = CanvaAPIClient(
    client_id=os.getenv("CANVA_CLIENT_ID"),
    client_secret=os.getenv("CANVA_CLIENT_SECRET")
)
# Após obter o código do usuário:
# token = client.authenticate(code="USER_AUTH_CODE", redirect_uri="YOUR_REDIRECT_URI")
```

### 3. Operações Comuns

#### Listar Designs
Recupere uma lista dos designs do usuário para edição ou visualização.

#### Criar Design a partir de Template
Automatize a criação de novos designs usando templates de marca pré-definidos.

```python
# Exemplo de criação de design
# response = client.create_design_from_template(
#     template_id="BRAND_TEMPLATE_ID",
#     title="Novo Post de Instagram"
# )
```

#### Upload de Ativos
Envie imagens ou outros ativos diretamente para a biblioteca do Canva para serem usados em designs.

## Recursos da Skill
- **Scripts**: `scripts/canva_api_client.py` - Um cliente Python básico para interagir com os endpoints da API.
- **Documentação**: Consulte a [Documentação Oficial do Canva](https://www.canva.dev/docs/connect/) para detalhes sobre todos os endpoints disponíveis.

## Dicas de Automação
- **Webhooks**: Configure webhooks no portal do desenvolvedor para receber notificações quando designs forem atualizados.
- **Brand Templates**: Use templates de marca para garantir que todos os designs gerados programaticamente sigam a identidade visual da sua empresa.
- **Segurança**: Nunca exponha seu `Client Secret` em código público. Use variáveis de ambiente.
