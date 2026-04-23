"""
Exemplos de Uso - Gerenciamento Avançado de Versões
Design Automation Studio
"""

import json
from design_automation_client import DesignAutomationClient


# ===========================================================
# EXEMPLO 1: Workflow Completo com Versionamento
# ===========================================================

def example_1_complete_version_workflow():
    """Workflow completo: criar, revisar, approvar, publicar"""
    print("\n" + "="*70)
    print("EXEMPLO 1: Workflow Completo com Versionamento")
    print("="*70)
    
    client = DesignAutomationClient()
    design_id = "campaign_q1_2024"
    
    # PASSO 1: Designer cria versão inicial
    print("\n[PASSO 1] Designer cria design inicial...")
    v1 = client.create_version(
        design_id=design_id,
        file_path="design_initial.png",
        author="designer@company.com",
        description="Design inicial com paleta corporativa",
        tags=["draft"],
        changes={
            "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
            "layout": "centered",
            "fonts": ["Montserrat Bold", "Open Sans"]
        }
    )
    print(f"  ✓ Versão {v1['version']} criada por {v1['metadata']['author']}")
    
    # PASSO 2: Ver história até agora
    history = client.get_design_history(design_id)
    print(f"\n[PASSO 2] Histórico atual: {len(history)} versão(s)")
    
    # PASSO 3: Designer faz revisão e cria v2
    print("\n[PASSO 3] Designer revisa e cria versão 2...")
    v2 = client.create_version(
        design_id=design_id,
        file_path="design_revised.png",
        author="designer@company.com",
        description="Revisão: ajuste de tipografia e espaçamento",
        tags=["draft"],
        changes={
            "typography": "increased font size",
            "spacing": "adjusted padding",
            "alignment": "improved visual hierarchy"
        }
    )
    print(f"  ✓ Versão {v2['version']} criada")
    
    # PASSO 4: Comparar versões
    print("\n[PASSO 4] Comparando v1 com v2...")
    comparison = client.compare_versions(design_id, "1.1", "1.2")
    print(f"  • Conteúdo mudou: {comparison['differences']['content_changed']}")
    print(f"  • Tamanho anterior: {comparison['differences']['file_size']['version1']} bytes")
    print(f"  • Tamanho novo: {comparison['differences']['file_size']['version2']} bytes")
    
    # PASSO 5: Manager revisa e aprova
    print("\n[PASSO 5] Manager marca como revisado...")
    client.tag_version(
        design_id=design_id,
        version="1.2",
        tags=["manager-approved"]
    )
    print(f"  ✓ Tags adicionadas: manager-approved")
    
    # PASSO 6: Marketing faz última revisão
    print("\n[PASSO 6] Marketing faz revisão final...")
    v3 = client.create_version(
        design_id=design_id,
        file_path="design_final.png",
        author="marketing@company.com",
        description="Versão final - pronta para produção",
        tags=["final"],
        changes={
            "status": "production-ready",
            "quality_check": "passed"
        }
    )
    print(f"  ✓ Versão {v3['version']} criada por {v3['metadata']['author']}")
    
    # PASSO 7: Marcar como estável (production)
    print("\n[PASSO 7] Marcando como versão estável...")
    stable = client.mark_stable(design_id, "1.3")
    print(f"  ✓ {stable['status']}: {stable['message']}")
    
    # PASSO 8: Publicar
    print("\n[PASSO 8] Publicando versão...")
    published = client.publish_version(design_id, "1.3")
    print(f"  ✓ Publicado!")
    
    # PASSO 9: Ver changelog completo
    print("\n[PASSO 9] Changelog completo:")
    changelog = client.get_changelog(design_id)
    for entry in changelog:
        print(f"  • {entry['timestamp']}")
        print(f"    Autor: {entry['author']}")
        print(f"    Versão: {entry['version']}")
        print(f"    Descrição: {entry['description']}")
    
    # PASSO 10: Estatísticas finais
    print("\n[PASSO 10] Estatísticas do design:")
    stats = client.get_design_statistics(design_id)
    print(f"  • Total de versões: {stats['total_versions']}")
    print(f"  • Colaboradores: {', '.join(stats['collaborators'])}")
    print(f"  • Tem versão estável: {stats['has_stable_version']}")
    print(f"  • Versões publicadas: {stats['published_versions_count']}")
    print(f"  • Criado em: {stats['creation_date']}")


# ===========================================================
# EXEMPLO 2: Rollback de Emergência
# ===========================================================

def example_2_emergency_rollback():
    """Demonstra rollback rápido em caso de problema"""
    print("\n" + "="*70)
    print("EXEMPLO 2: Rollback de Emergência")
    print("="*70)
    
    client = DesignAutomationClient()
    design_id = "social_media_post"
    
    print("\n[Cenário] Design foi publicado mas precisa ser revertido")
    
    # Simular múltiplas versões
    print("\n[1] Histórico antes do problema:")
    history = client.get_design_history(design_id)
    for v in history[-3:]:  # Últimas 3 versões
        tags_str = ", ".join(v.get("tags", []))
        print(f"  • {v['version_number']}: {v['description']} [{tags_str}]")
    
    # Fazer rollback com backup
    print("\n[2] Detectado problema na v1.5, revertendo para v1.3...")
    rollback = client.rollback_version(
        design_id=design_id,
        version="1.3",
        author="emergency_handler",
        create_backup=True
    )
    
    print(f"  ✓ {rollback['message']}")
    print(f"  • Arquivo atual: {rollback['current_file']}")
    
    # Verificar que backup foi criado
    print("\n[3] Verificando que backup foi criado...")
    history_after = client.get_design_history(design_id)
    backup_versions = client.get_versions_by_tag(design_id, "backup")
    print(f"  ✓ Total de versões agora: {len(history_after)}")
    print(f"  • Backups criados: {len(backup_versions)}")


# ===========================================================
# EXEMPLO 3: Rastreamento de Colaboração
# ===========================================================

def example_3_collaboration_tracking():
    """Rastreia quem fez o quê e quando"""
    print("\n" + "="*70)
    print("EXEMPLO 3: Rastreamento de Colaboração")
    print("="*70)
    
    client = DesignAutomationClient()
    design_id = "collaborative_project"
    
    # Simular trabalho de múltiplos colaboradores
    authors = ["alice@company.com", "bob@company.com", "carol@company.com"]
    
    print("\n[Timeline] Colaboradores trabalhando no design:")
    
    for i, author in enumerate(authors, 1):
        description = f"Revisão e ajustes por {author.split('@')[0]}"
        client.create_version(
            design_id=design_id,
            file_path=f"design_v{i}.png",
            author=author,
            description=description,
            changes={"reviewer": author}
        )
        print(f"  ✓ {author} criou versão 1.{i}")
    
    # Ver quem trabalhou no projeto
    stats = client.get_design_statistics(design_id)
    print(f"\n[Colaboradores] {len(stats['collaborators'])} pessoas envolvidas:")
    for collaborator in stats['collaborators']:
        print(f"  • {collaborator}")
    
    # Ver mudanças de cada pessoa
    print(f"\n[Análise por autor]:")
    changelog = client.get_changelog(design_id)
    
    authors_changes = {}
    for entry in changelog:
        author = entry['author']
        if author not in authors_changes:
            authors_changes[author] = 0
        authors_changes[author] += 1
    
    for author, count in authors_changes.items():
        print(f"  • {author}: {count} mudança(s)")


# ===========================================================
# EXEMPLO 4: Sistema de Tags para Workflow
# ===========================================================

def example_4_tag_based_workflow():
    """Usa tags para gerenciar workflow"""
    print("\n" + "="*70)
    print("EXEMPLO 4: Sistema de Tags para Workflow")
    print("="*70)
    
    client = DesignAutomationClient()
    design_id = "marketing_campaign"
    
    # Criar versão inicial
    print("\n[Status 1] Draft inicial")
    client.create_version(
        design_id=design_id,
        file_path="design_draft.png",
        author="designer@company.com",
        description="Design inicial",
        tags=["draft", "design-team"]
    )
    print("  ✓ Tags: draft, design-team")
    
    # Designer aprova seu próprio trabalho
    print("\n[Status 2] Designer aprova")
    client.tag_version(
        design_id=design_id,
        version="1.1",
        tags=["designer-approved"],
        replace=False
    )
    print("  ✓ Tag adicionada: designer-approved")
    
    # Manager revisa
    print("\n[Status 3] Manager revisa")
    client.create_version(
        design_id=design_id,
        file_path="design_reviewed.png",
        author="manager@company.com",
        description="Revisão do manager com ajustes",
        tags=["manager-review"]
    )
    print("  ✓ Nova versão criada com tag: manager-review")
    
    # Client approval
    print("\n[Status 4] Cliente aprova")
    client.tag_version(
        design_id=design_id,
        version="1.2",
        tags=["client-approved"],
        replace=False
    )
    print("  ✓ Tag adicionada: client-approved")
    
    # Ready for production
    print("\n[Status 5] Pronto para produção")
    client.mark_stable(design_id, "1.2")
    print("  ✓ Marcado como versão estável")
    
    # Pesquisar por status
    print("\n[Query] Buscando versões aprovadas pelo cliente:")
    approved = client.get_versions_by_tag(design_id, "client-approved")
    print(f"  Encontradas: {len(approved)} versão(s)")
    for v in approved:
        print(f"    • {v['version_number']}: {v['description']}")


# ===========================================================
# EXEMPLO 5: Exportar para Auditoria
# ===========================================================

def example_5_export_for_audit():
    """Exporta histórico completo para arquivo de auditoria"""
    print("\n" + "="*70)
    print("EXEMPLO 5: Exportar Histórico para Auditoria")
    print("="*70)
    
    client = DesignAutomationClient()
    design_id = "audit_design"
    
    # Criar algumas versões
    print("\n[Criando histórico]")
    for i in range(3):
        client.create_version(
            design_id=design_id,
            file_path=f"design_v{i+1}.png",
            author=f"user{i+1}@company.com",
            description=f"Versão {i+1} com mudanças"
        )
    print(f"  ✓ Criadas 3 versões")
    
    # Exportar para auditoria
    print("\n[Exportando]")
    export_result = client.export_version_history(
        design_id=design_id,
        output_path="design_audit_history.json"
    )
    
    print(f"  ✓ {export_result['message']}")
    print(f"  • Arquivo: {export_result['output_path']}")
    
    # Mostrar conteúdo do arquivo
    print("\n[Arquivo de auditoria contém]")
    with open("design_audit_history.json", 'r') as f:
        audit_data = json.load(f)
    
    print(f"  • Design ID: {audit_data['design_id']}")
    print(f"  • Total de versões: {len(audit_data['versions'])}")
    print(f"  • Total de mudanças: {len(audit_data['changelog'])}")
    print(f"  • Estatísticas:")
    stats = audit_data['statistics']
    print(f"    - Colaboradores: {stats['collaborators_count']}")
    print(f"    - Período: {stats['creation_date'][:10]} até {stats['last_modified'][:10]}")


# ===========================================================
# EXEMPLO 6: Limpeza Automática
# ===========================================================

def example_6_automatic_cleanup():
    """Demonstra limpeza automática de versões antigas"""
    print("\n" + "="*70)
    print("EXEMPLO 6: Limpeza Automática de Versões Antigas")
    print("="*70)
    
    client = DesignAutomationClient()
    design_id = "long_project"
    
    # Simular muitas versões
    print("\n[Simulando] Criando 20 versões ao longo do tempo...")
    for i in range(20):
        client.create_version(
            design_id=design_id,
            file_path=f"design_v{i+1}.png",
            author="designer@company.com",
            description=f"Iteração {i+1}",
            tags=["iteration"] if i < 19 else ["final"]
        )
    
    history_before = client.get_design_history(design_id)
    print(f"  ✓ Total de versões: {len(history_before)}")
    
    # Marcar versão estável
    print("\n[Proteção] Marcando versão 10 como estável...")
    client.mark_stable(design_id, "1.10")
    print("  ✓ Versão estável protegida")
    
    # Limpeza
    print("\n[Limpeza] Mantendo apenas 5 versões mais recentes...")
    cleanup = client.clean_old_versions(
        design_id=design_id,
        keep_count=5,
        keep_stable=True
    )
    
    print(f"  ✓ {cleanup['message']}")
    print(f"  • Versões mantidas: {cleanup['versions_kept']}")
    print(f"  • Versões deletadas: {cleanup['versions_deleted']}")
    print(f"  • Versão estável protegida: Sim")


# ===========================================================
# EXECUTAR EXEMPLOS
# ===========================================================

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " DESIGN AUTOMATION - GERENCIAMENTO DE VERSÕES ".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    # Descomentar para executar
    example_1_complete_version_workflow()
    # example_2_emergency_rollback()
    # example_3_collaboration_tracking()
    # example_4_tag_based_workflow()
    # example_5_export_for_audit()
    # example_6_automatic_cleanup()
    
    print("\n✓ Exemplos de versionamento executados com sucesso!")
    print("\nConsulte a documentação completa em SKILL.md para mais detalhes.")
