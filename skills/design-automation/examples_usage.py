"""
Design Automation Examples
Exemplos práticos de uso da skill unificada de automação de design
"""

import json
from design_automation_client import DesignAutomationClient
from template_library import TemplateLibrary


# ===========================================================
# EXEMPLO 1: Criar e Versionar um Pôster
# ===========================================================

def example_1_create_and_version_poster():
    """Gera um pôster e cria versões"""
    print("\n" + "="*60)
    print("EXEMPLO 1: Criar e Versionar um Pôster")
    print("="*60)
    
    client = DesignAutomationClient()
    
    # Gerar pôster inicial
    poster_1 = client.generate_poster(
        prompt="Tech Conference 2024 poster with modern minimalist design, blue and purple colors, bold sans-serif typography",
        output_path="tech_conference_v1.png",
        steps=30,
        guidance=3.5
    )
    
    print(f"Status: {poster_1['status']}")
    print(f"Output: {poster_1['output']}")
    
    # Criar versão
    if poster_1['status'] == 'success':
        version_1 = client.create_version(
            design_id="tech_conference_2024",
            file_path=poster_1['output'],
            description="Primeira versão - layout minimalista"
        )
        
        print(f"Version Created: {version_1['version']}")
        print(f"Description: {version_1['description']}")
        
        # Ver histórico
        history = client.get_design_history("tech_conference_2024")
        print(f"\nDesign History: {len(history)} version(s)")
        for v in history:
            print(f"  - {v['version']}: {v['description']} ({v['timestamp']})")


# ===========================================================
# EXEMPLO 2: Gerar Múltiplos Pôsteres em Lote
# ===========================================================

def example_2_batch_poster_generation():
    """Gera múltiplos pôsteres simultaneamente"""
    print("\n" + "="*60)
    print("EXEMPLO 2: Gerar Múltiplos Pôsteres em Lote")
    print("="*60)
    
    client = DesignAutomationClient()
    
    prompts = [
        "Summer Festival 2024 poster with vibrant colors, tropical elements, bold typography",
        "Black Friday Sale poster with dramatic lighting, gold accents, urgency-focused design",
        "Charity Gala Evening poster with elegant design, formal aesthetic, sophisticated typography"
    ]
    
    results = client.generate_multiple_posters(
        prompts=prompts,
        output_dir="./batch_posters",
        steps=28,
        guidance=3.5
    )
    
    successful = sum(1 for r in results if r['status'] == 'success')
    print(f"Batch Processing Complete: {successful}/{len(results)} successful")
    
    for i, result in enumerate(results, 1):
        status = "✓" if result['status'] == 'success' else "✗"
        print(f"{status} Poster {i}: {result['status']}")


# ===========================================================
# EXEMPLO 3: Exportar em Múltiplos Formatos
# ===========================================================

def example_3_multi_format_export():
    """Exporta design em diversos formatos"""
    print("\n" + "="*60)
    print("EXEMPLO 3: Exportar em Múltiplos Formatos")
    print("="*60)
    
    client = DesignAutomationClient()
    
    # Assumindo que temos um design
    export_result = client.export_multi_format(
        input_path="tech_conference_v1.png",
        output_dir="./design_exports",
        formats=["png", "pdf", "svg", "webp"],
        quality="high"
    )
    
    print(f"Export Status: {export_result['status']}")
    print(f"Output Directory: {export_result['output_directory']}")
    print("\nExports:")
    
    for fmt, details in export_result['exports'].items():
        print(f"  - {fmt.upper()}: {details['status']}")


# ===========================================================
# EXEMPLO 4: Gerenciar Biblioteca de Templates
# ===========================================================

def example_4_template_library_management():
    """Trabalha com biblioteca de templates"""
    print("\n" + "="*60)
    print("EXEMPLO 4: Gerenciar Biblioteca de Templates")
    print("="*60)
    
    lib = TemplateLibrary()
    
    # Criar templates para redes sociais
    templates_data = [
        {
            "name": "Instagram Story",
            "category": "social_media",
            "dimensions": {"width": 1080, "height": 1920},
            "brand_colors": ["#FF6B6B", "#4ECDC4"],
            "description": "Story padrão para Instagram"
        },
        {
            "name": "LinkedIn Post",
            "category": "social_media",
            "dimensions": {"width": 1200, "height": 627},
            "brand_colors": ["#0077B5", "#FFFFFF"],
            "description": "Post padrão para LinkedIn"
        },
        {
            "name": "A4 Flyer",
            "category": "print",
            "dimensions": {"width": 2480, "height": 3508},
            "brand_colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
            "description": "Folheto A4 de alta resolução"
        }
    ]
    
    created = 0
    for template_data in templates_data:
        template = lib.create_template(**template_data)
        print(f"✓ Created: {template['name']} ({template['category']})")
        created += 1
    
    # Listar por categoria
    print("\n--- Social Media Templates ---")
    for t in lib.get_templates_by_category("social_media"):
        print(f"  • {t['name']} ({t['dimensions']['width']}x{t['dimensions']['height']})")
    
    # Estatísticas
    stats = lib.get_statistics()
    print(f"\n--- Library Statistics ---")
    print(f"Total Templates: {stats['total_templates']}")
    print(f"Categories: {', '.join(stats['categories_list'])}")


# ===========================================================
# EXEMPLO 5: Autenticação e Integração Canva
# ===========================================================

def example_5_canva_integration():
    """Demonstra integração com Canva"""
    print("\n" + "="*60)
    print("EXEMPLO 5: Autenticação e Integração Canva")
    print("="*60)
    
    # Nota: Requer credenciais reais do Canva
    client = DesignAutomationClient(
        canva_client_id="seu_client_id",
        canva_client_secret="seu_client_secret"
    )
    
    print("Canva Integration Demo")
    print("-" * 40)
    
    # Fluxo de autenticação (requer interação do usuário)
    print("""
    Passo 1: Redirecionar usuário para autorização:
    https://www.canva.com/api/oauth/authorize?
      client_id=SEU_CLIENT_ID&
      redirect_uri=SEU_REDIRECT_URI&
      response_type=code&
      scope=design:content:read,design:content:write,asset:read,asset:write
    
    Passo 2: Usar código de autorização para autenticar
    (Necessário ter o código do usuário)
    """)
    
    # Exemplo de como seria usado após autenticação
    print("Após autenticação bem-sucedida:")
    print("  • client.canva_list_designs() - Lista todos os designs")
    print("  • client.canva_create_from_template() - Criar design de template")


# ===========================================================
# EXEMPLO 6: Fluxo Completo de Design
# ===========================================================

def example_6_complete_design_workflow():
    """Workflow completo: criar, versionar, exportar"""
    print("\n" + "="*60)
    print("EXEMPLO 6: Fluxo Completo de Design")
    print("="*60)
    
    client = DesignAutomationClient()
    lib = TemplateLibrary()
    
    # Passo 1: Criar template na biblioteca
    print("\n[1] Criando template na biblioteca...")
    template = lib.create_template(
        name="Marketing Campaign Poster",
        category="marketing",
        dimensions={"width": 1920, "height": 1080},
        brand_colors=["#FF6B6B", "#4ECDC4", "#45B7D1"],
        description="Template para campanhas de marketing Q1 2024"
    )
    print(f"✓ Template criado: {template['name']}")
    
    # Passo 2: Gerar pôster usando a descrição do template
    print("\n[2] Gerando pôster baseado no template...")
    poster = client.generate_poster(
        prompt="Marketing campaign poster with brand colors red and teal, modern design, high impact typography, 1920x1080",
        output_path="marketing_campaign_poster.png",
        steps=32,
        guidance=3.8
    )
    print(f"✓ Pôster gerado: {poster['output']}")
    
    # Passo 3: Criar versão
    print("\n[3] Registrando versão no histórico...")
    version = client.create_version(
        design_id="marketing_campaign_2024",
        file_path=poster['output'],
        description="Versão 1.0 - Design inicial aprovado"
    )
    print(f"✓ Versão criada: {version['version']}")
    
    # Passo 4: Exportar para múltiplos formatos
    print("\n[4] Exportando para múltiplos formatos...")
    exports = client.export_multi_format(
        input_path=poster['output'],
        output_dir="./campaign_exports",
        formats=["png", "pdf", "webp"],
        quality="high"
    )
    print(f"✓ Exportações configuradas para {len(exports['exports'])} formatos")
    
    # Passo 5: Registrar uso no template
    print("\n[5] Atualizando estatísticas do template...")
    lib.get_template(template['id'])  # Incrementa usage_count
    stats = lib.get_statistics()
    print(f"✓ Total de templates: {stats['total_templates']}")
    
    print("\n" + "="*60)
    print("✓ Workflow completo finalizado com sucesso!")
    print("="*60)


# ===========================================================
# EXECUTAR EXEMPLOS
# ===========================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " DESIGN AUTOMATION - EXEMPLOS DE USO ".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    # Descomentar para executar cada exemplo
    
    # example_1_create_and_version_poster()
    # example_2_batch_poster_generation()
    # example_3_multi_format_export()
    example_4_template_library_management()
    # example_5_canva_integration()
    example_6_complete_design_workflow()
    
    print("\n✓ Exemplos executados com sucesso!")
    print("\nPara mais informações, consulte a documentação em SKILL.md")
