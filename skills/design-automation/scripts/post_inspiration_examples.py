"""
Post Inspiration Examples
Exemplos práticos de posts com inspiração dos templates
"""

# ===========================================================================
# EXEMPLO 1: POSTS DE TECNOLOGIA/STARTUP
# ===========================================================================

POST_TECH_EXAMPLES = {
    "titulo": "Posts para Startups e Tech",
    "estilo": "Energético, moderno, dinâmico",
    "exemplos": [
        {
            "titulo": "Lançamento de Produto",
            "prompt": """
            Crie um post Instagram para lançamento de aplicativo.
            Estilo: Energético e moderno com gradientes azuis e roxos.
            Elementos: Formas geométricas, animação, efeitos dinâmicos.
            Tipografia: Títulos bold em Sans-serif, subtítulos medium.
            Cores: #4ECDC4 (primária), #FF6B6B (destaque), #45B7D1 (secundária)
            Mensagem: "Inovação que transforma"
            """,
            "dicas": [
                "Use formas que sugerem movimento",
                "Contraste alto para destaque",
                "Tipografia bold para impacto",
                "Ícones minimalistas em branco"
            ],
            "plataforma": "Instagram",
            "dimensões": "1080x1080px"
        },
        {
            "titulo": "Conquista de Milestone",
            "prompt": """
            Design para comemorar 100k usuários.
            Estilo: Dinâmico com confetes e efeitos de celebração.
            Números grandes em primeiro plano.
            Cores vibrantes: neon, gradientes.
            Tipografia: Números gigantes, texto suportivo.
            """,
            "dicas": [
                "Números grandes dominam o espaço",
                "Elementos de celebração (confetes)",
                "Cores que transmitem alegria",
                "Espaço para logo da empresa"
            ],
            "plataforma": "Instagram",
            "dimensões": "1080x1080px"
        },
        {
            "titulo": "Call-to-Action para Download",
            "prompt": """
            Post CTA para download de app.
            Visual: Botão destacado, ícones de app stores.
            Cores: Verde para ação, contraste com fundo escuro.
            Texto: Principal "BAIXE AGORA", secundário com benefícios.
            Elementos: Setas, pontos de destaque.
            """,
            "dicas": [
                "Botão visualmente proeminente",
                "Ícones App Store e Google Play claros",
                "Benefícios listados brevemente",
                "Urgência sutilmente sugerida"
            ],
            "plataforma": "Instagram/Facebook",
            "dimensões": "1080x1080px / 1200x628px"
        }
    ]
}

# ===========================================================================
# EXEMPLO 2: POSTS DE NEGÓCIO/CORPORATIVO
# ===========================================================================

POST_BUSINESS_EXAMPLES = {
    "titulo": "Posts para Empresas e B2B",
    "estilo": "Profissional, confiável, estruturado",
    "exemplos": [
        {
            "titulo": "Dica de Negócios",
            "prompt": """
            Design para compartilhar dica de negócio no LinkedIn.
            Layout: 3 colunas com números/ícones.
            Cores: Azul corporativo (#0077B5), branco, cinza.
            Tipografia: Títulos em Sans-serif bold, corpo regular.
            Formato: Número grande + título + descrição breve.
            """,
            "dicas": [
                "Números grandes e visíveis",
                "Máximo 3 dicas por post",
                "Ícones profissionais",
                "Logo da empresa no canto"
            ],
            "plataforma": "LinkedIn",
            "dimensões": "1200x628px"
        },
        {
            "titulo": "Case Study/Resultado",
            "prompt": """
            Post de case study mostrando resultado.
            Visual: Antes e depois, ou gráfico de crescimento.
            Cores: Verde para crescimento, branco, neutros.
            Percentual destacado (ex: +300%)
            Estrutura: Problema > Solução > Resultado
            """,
            "dicas": [
                "Resultado numérico em destaque",
                "Comparação visual antes/depois",
                "Logo do cliente (se possível)",
                "Texto explicativo conciso"
            ],
            "plataforma": "LinkedIn",
            "dimensões": "1200x628px"
        },
        {
            "titulo": "Citação de Liderança",
            "prompt": """
            Post com citação motivacional de líder.
            Design: Citação grande, imagem de fundo sutil.
            Tipografia: Fonte elegante, citação em 48px+
            Cores: Neutras com um destaque de cor.
            Foto do autor no canto inferior.
            """,
            "dicas": [
                "Citação clara e legível",
                "Fonte elegante e profissional",
                "Foto de alta qualidade do autor",
                "Fundo sutil, não competir com texto"
            ],
            "plataforma": "LinkedIn/Instagram",
            "dimensões": "1080x1080px"
        }
    ]
}

# ===========================================================================
# EXEMPLO 3: POSTS DE MODA E ESTILO DE VIDA
# ===========================================================================

POST_LIFESTYLE_EXAMPLES = {
    "titulo": "Posts para Moda e Estilo de Vida",
    "estilo": "Sofisticado, visual, inspirador",
    "exemplos": [
        {
            "titulo": "Lançamento de Coleção",
            "prompt": """
            Post para nova coleção de moda.
            Visual: Imagem do produto em destaque, fundo minimalista.
            Cores: Ouro, preto, branco (luxo), ou cores da coleção.
            Tipografia: Nome da coleção elegante, descrição minimalista.
            Elementos: Número da edição, exclusividade.
            """,
            "dicas": [
                "Imagem de produto centrada",
                "Fundo limpo e minimalista",
                "Tipografia elegante",
                "Limite de cores (2-3 cores)",
                "Espaço em branco generoso"
            ],
            "plataforma": "Instagram",
            "dimensões": "1080x1080px"
        },
        {
            "titulo": "Outfit do Dia",
            "prompt": """
            Post OOTD (Outfit of the Day).
            Visual: Foto de moda com elementos gráficos.
            Cores: Cor do outfit domina, acessórios em destaque.
            Tipografia: Descrição breve do look.
            Elementos: Links para produtos, tag de marcas.
            """,
            "dicas": [
                "Foto de alta qualidade",
                "Composição bem balanceada",
                "Tags de marcas integradas",
                "Link de compra discreto",
                "Descrição do look breve"
            ],
            "plataforma": "Instagram",
            "dimensões": "1080x1080px"
        },
        {
            "titulo": "Venda/Promoção",
            "prompt": """
            Post de venda ou desconto.
            Visual: Percentual grande (ex: 50% OFF), imagem de produto.
            Cores: Laranja ou vermelho para urgência, branco.
            Tipografia: Desconto gigante, data limite pequena.
            Estrutura: Destaque de desconto > Produto > CTA
            """,
            "dicas": [
                "Percentual ou valor em destaque",
                "Data limite visível",
                "Botão de compra claro",
                "Sensação de urgência (discretamente)",
                "Imagem de produto de qualidade"
            ],
            "plataforma": "Instagram/Shopify",
            "dimensões": "1080x1080px"
        }
    ]
}

# ===========================================================================
# EXEMPLO 4: POSTS DE EDUCAÇÃO E CONTEÚDO
# ===========================================================================

POST_EDUCATION_EXAMPLES = {
    "titulo": "Posts para Educação e Conteúdo",
    "estilo": "Informativo, claro, engajante",
    "exemplos": [
        {
            "titulo": "Tutorial em Passos",
            "prompt": """
            Post ensinando algo em passos numerados.
            Visual: Grid com números 1, 2, 3... em destaque.
            Cores: Cor primária para números, neutras para fundo.
            Tipografia: Número grande, texto descritivo.
            Ícones: Minimalistas para representar cada passo.
            """,
            "dicas": [
                "Números grandes (36-48px)",
                "Máximo 5-6 passos",
                "Ícones simples e claros",
                "Espaço entre passos",
                "Fonte legível no tamanho pequeno"
            ],
            "plataforma": "Instagram",
            "dimensões": "1080x1080px"
        },
        {
            "titulo": "Pergunta Interativa",
            "prompt": """
            Post com pergunta para gerar engagement.
            Visual: Fundo colorido, pergunta grande.
            Tipografia: Pergunta dominante (48px+), opcões claras.
            Cores: Vibrante, destaca a pergunta.
            Elementos: Emojis para as opções.
            """,
            "dicas": [
                "Pergunta clara e específica",
                "Opções visuais e interativas",
                "Emojis relevantes",
                "Fundo que contrasta",
                "Fonte grande e legível"
            ],
            "plataforma": "Instagram Stories/Feed",
            "dimensões": "1080x1080px"
        },
        {
            "titulo": "Infográfico Educativo",
            "prompt": """
            Post com informações em formato visual.
            Visual: Ícones, gráficos, dados organizados.
            Cores: Cor primária + neutras (2-3 cores).
            Estrutura: Título > Dados visuais > Conclusão.
            Tipografia: Hierarquia clara (título > subtítulo > corpo).
            """,
            "dicas": [
                "Dados claros e visíveis",
                "Ícones que representam conceitos",
                "Gráficos simples e diretos",
                "Cores consistentes",
                "Muito espaço em branco"
            ],
            "plataforma": "Instagram/LinkedIn",
            "dimensões": "1080x1080px / 1200x628px"
        }
    ]
}

# ===========================================================================
# EXEMPLO 5: POSTS DE ALIMENTOS/RESTAURANTE
# ===========================================================================

POST_FOOD_EXAMPLES = {
    "titulo": "Posts para Restaurante/Alimentação",
    "estilo": "Apetitoso, atraente, aconchegante",
    "exemplos": [
        {
            "titulo": "Destaque de Prato",
            "prompt": """
            Post de prato principal em destaque.
            Visual: Foto do prato profissional, fundo simples.
            Cores: Cores naturais do prato, fundo neutro.
            Tipografia: Nome do prato elegante, descrição breve.
            Elementos: Preço, ingredientes principais.
            """,
            "dicas": [
                "Fotografia profissional do prato",
                "Iluminação natural quando possível",
                "Fundo não competir com comida",
                "Nome do prato destaca-se",
                "Descrição breve mas atrativa"
            ],
            "plataforma": "Instagram",
            "dimensões": "1080x1080px"
        },
        {
            "titulo": "Receita Passo a Passo",
            "prompt": """
            Post compartilhando receita.
            Visual: 4-5 fotos dos passos da receita.
            Cores: Cores naturais dos ingredientes.
            Tipografia: Ingredientes listados, modo de preparo.
            Estrutura: Ingredientes > Modo > Dica + Nota
            """,
            "dicas": [
                "Fotos dos passos claras",
                "Lista de ingredientes visível",
                "Tempo de preparo destacado",
                "Consistência fotográfica",
                "Fonte fácil de ler"
            ],
            "plataforma": "Instagram",
            "dimensões": "1080x1080px"
        },
        {
            "titulo": "Promoção/Menu Especial",
            "prompt": """
            Post anunciando prato especial ou promoção.
            Visual: Imagem grande do prato, badge de especial.
            Cores: Destaque em cor quente (laranja, vermelho).
            Tipografia: "ESPECIAL DO DIA" grande, prato e preço.
            Elementos: Data válida, local.
            """,
            "dicas": [
                "Badge 'ESPECIAL' destacado",
                "Data de validade clara",
                "Preço em destaque",
                "Foto apetitosa do prato",
                "Local/Horário da disponibilidade"
            ],
            "plataforma": "Instagram/Facebook",
            "dimensões": "1080x1080px"
        }
    ]
}

# ===========================================================================
# EXEMPLO 6: POSTS DE SAÚDE E BEM-ESTAR
# ===========================================================================

POST_WELLNESS_EXAMPLES = {
    "titulo": "Posts para Saúde e Bem-estar",
    "estilo": "Calmo, inspirador, motivante",
    "exemplos": [
        {
            "titulo": "Dica de Saúde",
            "prompt": """
            Post compartilhando dica de bem-estar.
            Visual: Imagem serena (natureza, yoga), texto minimalista.
            Cores: Verdes, azuis, neutras (calmo).
            Tipografia: Dica grande e clara, descrição suportiva.
            Elementos: Ícone de saúde, quote inspirador.
            """,
            "dicas": [
                "Imagem que transmite calma",
                "Tipografia clara e legível",
                "Paleta de cores tranquila",
                "Dica prática e aplicável",
                "Espaço em branco generoso"
            ],
            "plataforma": "Instagram",
            "dimensões": "1080x1080px"
        },
        {
            "titulo": "Motivação e Transformação",
            "prompt": """
            Post antes e depois de transformação.
            Visual: Antes/Depois lado a lado ou em transição.
            Cores: Consistentes entre as duas imagens.
            Tipografia: Histórico breve e inspirador.
            Elementos: Resultados mensuráveis, datas.
            """,
            "dicas": [
                "Comparação clara antes/depois",
                "Resultados quantificáveis",
                "Texto motivador",
                "Datas das transformações",
                "Informações de programa/dieta"
            ],
            "plataforma": "Instagram",
            "dimensões": "1080x1080px"
        }
    ]
}

# ===========================================================================
# RESUMO DE MELHORES PRÁTICAS
# ===========================================================================

BEST_PRACTICES = {
    "cores": {
        "principal_dica": "Máximo 3 cores primárias, 2 segundárias",
        "contraste": "Sempre teste contraste de texto vs fundo",
        "psicologia": {
            "vermelho": "urgência, ação, emoção",
            "azul": "confiança, profissionalismo",
            "verde": "crescimento, saúde, natureza",
            "amarelo": "alegria, energia, atenção",
            "rosa": "feminilidade, romance, criatividade"
        }
    },
    "tipografia": {
        "principal_dica": "Máximo 2 fontes diferentes",
        "tamanhos": {
            "titulo": "36-56px",
            "subtitulo": "24-32px",
            "corpo": "14-18px"
        },
        "dicas": [
            "Escolha fontes legíveis",
            "Evite muitos estilos diferentes",
            "Use hierarchy visual clara",
            "Tenha contraste texto/fundo"
        ]
    },
    "layout": {
        "principal_dica": "Siga a regra de terços",
        "grid": "Grid invisível de 3x3 ou 4x4",
        "espaçamento": "Use espaço em branco estrategicamente",
        "alinhamento": "Seja consistente com alinhamentos"
    },
    "imagens": {
        "qualidade": "Mínimo 1080x1080px para Instagram",
        "formato": "JPG para fotos, PNG para gráficos",
        "foco": "Objeto principal claro e centrado",
        "edição": "Aumente contraste e saturação levemente"
    },
    "textos": {
        "comprimento": "Máximo 150 caracteres para post principal",
        "chamada": "Use CTA claro (ex: 'Clique', 'Saiba Mais')",
        "emojis": "Use com moderação (máximo 3)",
        "hashtags": "5-10 hashtags relevantes"
    }
}

# ===========================================================================
# FUNÇÃO PARA GERAR POST PERSONALIZADO
# ===========================================================================

def gerar_prompt_customizado(
    tipo_negocio: str,
    objetivo: str,
    mood: str,
    cores_preferidas: list,
    plataforma: str
) -> str:
    """
    Gera um prompt customizado para criação de post
    
    Args:
        tipo_negocio: (tech, moda, restaurante, etc)
        objetivo: (vendas, educação, engajamento, etc)
        mood: (energético, calmo, profissional, etc)
        cores_preferidas: lista de cores hex
        plataforma: (instagram, tiktok, linkedin, etc)
    
    Returns:
        Prompt customizado
    """
    prompt = f"""
    Crie um post para {plataforma}.
    
    Negócio: {tipo_negocio}
    Objetivo: {objetivo}
    Mood/Atmosfera: {mood}
    Cores: {', '.join(cores_preferidas)}
    
    Requisitos:
    1. Design moderno e profissional
    2. Fácil de ler em dispositivos móveis
    3. Chama atenção nos primeiros 2 segundos
    4. Mensagem clara e direta
    5. Cores harmonizadas
    
    Inclua:
    - Tipografia hierárquica (título > subtítulo > corpo)
    - Elementos visuais relevantes
    - CTA claro (se aplicável)
    - Espaço em branco estratégico
    """
    
    return prompt.strip()


if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════╗")
    print("║       EXEMPLOS DE INSPIRAÇÃO PARA POSTS               ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # Mostrar exemplos
    categories = [
        POST_TECH_EXAMPLES,
        POST_BUSINESS_EXAMPLES,
        POST_LIFESTYLE_EXAMPLES,
        POST_EDUCATION_EXAMPLES,
        POST_FOOD_EXAMPLES,
        POST_WELLNESS_EXAMPLES
    ]
    
    for category in categories:
        print(f"\n{'='*60}")
        print(f"📌 {category['titulo']}")
        print(f"{'='*60}")
        print(f"Estilo: {category['estilo']}\n")
        
        for i, exemplo in enumerate(category['exemplos'], 1):
            print(f"{i}. {exemplo['titulo']}")
            print(f"   Plataforma: {exemplo['plataforma']}")
            print(f"   Dimensões: {exemplo['dimensões']}")
            print()
