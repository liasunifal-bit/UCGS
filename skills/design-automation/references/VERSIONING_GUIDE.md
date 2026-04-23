# Guia Completo: Gerenciamento de Versões na Design Automation

## 📋 Visão Geral

O **Version Manager** é um subsistema avançado que fornece controle completo sobre o histórico de designs, permitindo rastreamento detalhado, comparação, rollback e gerenciamento de checkpoints.

## 🎯 Funcionalidades Principais

### 1. **Criação de Versões**
Cada vez que você modifica um design, pode criar uma nova versão com descrição de mudanças.

```python
from version_manager import VersionManager

manager = VersionManager()

version = manager.create_version(
    design_id="poster_summer_2024",
    file_path="poster_v1.png",
    description="Layout inicial com cores vibrantes",
    author="designer_01",
    tags=["initial", "draft"],
    metadata={
        "prompt": "Summer festival poster...",
        "steps": 30,
        "guidance": 3.5
    }
)

# Resultado:
# {
#   "version_number": 1,
#   "semantic_version": "1.1",
#   "created_at": "2024-03-19T...",
#   "author": "designer_01",
#   "description": "Layout inicial com cores vibrantes",
#   "file_size": 2457600,
#   "file_hash": "abc123...",
#   "tags": ["initial", "draft"],
#   "status": "active"
# }
```

### 2. **Histórico de Versões**
Visualize todas as versões de um design de forma organizada.

```python
# Obter histórico completo
history = manager.get_version_history("poster_summer_2024")

for version in history:
    print(f"v{version['semantic_version']}: {version['description']}")
    print(f"  Autor: {version['author']}")
    print(f"  Data: {version['created_at']}")
    print(f"  Tamanho: {version['file_size']} bytes")
    print()

# Output:
# v1.1: Layout inicial com cores vibrantes
#   Autor: designer_01
#   Data: 2024-03-19T10:30:00
#   Tamanho: 2457600 bytes
#
# v1.2: Ajuste de tipografia e contraste
#   Autor: designer_02
#   Data: 2024-03-19T14:45:00
#   Tamanho: 2501234 bytes
```

### 3. **Comparação de Versões**
Compare duas versões para ver o que mudou.

```python
comparison = manager.compare_versions(
    design_id="poster_summer_2024",
    version1=1,
    version2=2
)

print(f"Arquivo mudou? {comparison['differences']['file_changed']}")
print(f"Mudança de tamanho: {comparison['differences']['size_difference']} bytes")
print(f"Diferença de tempo: {comparison['differences']['time_difference_seconds']} segundos")
print(f"Tags mudaram? {comparison['differences']['tags_changed']}")

# Output:
# Arquivo mudou? True
# Mudança de tamanho: 43634 bytes
# Diferença de tempo: 14700 segundos
# Tags mudaram? False
```

### 4. **Rollback (Reverter para Versão Anterior)**
Restaure seu design para qualquer versão anterior instantaneamente.

```python
# Voltar para versão 1
rollback = manager.rollback_version(
    design_id="poster_summer_2024",
    version_number=1
)

if rollback['status'] == 'success':
    print(f"✓ Revertido para versão 1")
    print(f"Arquivo: {rollback['file_path']}")
```

### 5. **Tags para Organização**
Use tags para organizar e categorizar versões.

```python
# Adicionar tags a uma versão
manager.tag_version(
    design_id="poster_summer_2024",
    version_number=2,
    tags=["approved", "client_reviewed"]
)

# Encontrar versões com tag específica
approved = manager.get_versions_by_tag("poster_summer_2024", "approved")
for v in approved:
    print(f"Versão {v['semantic_version']}: {v['description']}")

# Tags pré-definidas recomendadas:
# - "initial" - Primeira versão
# - "draft" - Rascunho
# - "review" - Em revisão
# - "approved" - Aprovado
# - "final" - Versão final
# - "archived" - Arquivado
# - "checkpoint" - Ponto importante
```

### 6. **Checkpoints (Marcos Importantes)**
Crie pontos de referência importantes no histórico do design.

```python
# Criar checkpoint
checkpoint = manager.create_checkpoint(
    design_id="poster_summer_2024",
    description="Design aprovado por cliente e pronto para impressão"
)

print(f"Checkpoint criado: {checkpoint['checkpoint_tag']}")
# Output: checkpoint_20240319_144500

# Ver todos os checkpoints
checkpoints = manager.get_all_checkpoints("poster_summer_2024")
for cp in checkpoints:
    print(f"{cp['version_number']}: {cp['description']}")
```

### 7. **Changelog Formatado**
Gere um changelog profissional de todas as mudanças.

```python
changelog = manager.get_changelog("poster_summer_2024", limit=10)

# Formato Markdown
markdown = "# Changelog - Poster Summer 2024\n\n"
for entry in changelog:
    markdown += f"## {entry['version']} ({entry['date']})\n"
    markdown += f"**Autor:** {entry['author']}\n"
    markdown += f"**Descrição:** {entry['description']}\n"
    markdown += f"**Tags:** {', '.join(entry['tags'])}\n\n"

print(markdown)

# Output:
# # Changelog - Poster Summer 2024
#
# ## 1.1 (2024-03-19T10:30:00)
# **Autor:** designer_01
# **Descrição:** Layout inicial com cores vibrantes
# **Tags:** initial, draft
#
# ## 1.2 (2024-03-19T14:45:00)
# **Autor:** designer_02
# **Descrição:** Ajuste de tipografia
# **Tags:** review, approved
```

### 8. **Deletar e Restaurar Versões**
Soft delete permite recuperar versões deletadas.

```python
# Marcar versão como deletada (soft delete)
delete_result = manager.delete_version(
    design_id="poster_summer_2024",
    version_number=1
)

# Restaurar versão deletada
restore_result = manager.restore_version(
    design_id="poster_summer_2024",
    version_number=1
)

if restore_result['status'] == 'success':
    print("✓ Versão restaurada")
```

### 9. **Estatísticas Detalhadas**
Análise completa do histórico de versões.

```python
stats = manager.get_statistics("poster_summer_2024")

print(f"Total de versões: {stats['total_versions']}")
print(f"Versões ativas: {stats['active_versions']}")
print(f"Checkpoints: {stats['checkpoints']}")
print(f"\nEstatísticas de Tamanho:")
print(f"  Tamanho atual: {stats['file_size_stats']['current']} bytes")
print(f"  Mínimo: {stats['file_size_stats']['min']} bytes")
print(f"  Máximo: {stats['file_size_stats']['max']} bytes")
print(f"  Média: {stats['file_size_stats']['average']:.0f} bytes")
print(f"\nAutores: {', '.join(stats['authors'])}")
print(f"Tags usadas: {', '.join(stats['tags'])}")

# Output:
# Total de versões: 5
# Versões ativas: 4
# Checkpoints: 1
#
# Estatísticas de Tamanho:
#   Tamanho atual: 2543890 bytes
#   Mínimo: 2400000 bytes
#   Máximo: 2600000 bytes
#   Média: 2500000 bytes
#
# Autores: designer_01, designer_02, client_reviewer
# Tags usadas: initial, draft, review, approved, final
```

### 10. **Exportar Histórico**
Exporte o histórico completo para arquivo JSON.

```python
# Exportar como JSON
success = manager.export_version_history(
    design_id="poster_summer_2024",
    output_path="poster_history.json"
)

if success:
    print("✓ Histórico exportado para poster_history.json")
    
    # Conteúdo do arquivo:
    # {
    #   "design_id": "poster_summer_2024",
    #   "exported_at": "2024-03-19T...",
    #   "total_versions": 5,
    #   "versions": [...]
    # }
```

## 🔄 Fluxo de Trabalho Recomendado

```
1. Criar Design Inicial
   └─ create_version(description="Design inicial")
      └─ tag_version(tags=["initial", "draft"])

2. Primeira Revisão
   └─ create_version(description="Ajustes de feedback")
      └─ tag_version(tags=["review"])

3. Aprovação de Cliente
   └─ tag_version(tags=["approved"])

4. Checkpoint - Pronto para Produção
   └─ create_checkpoint(description="Aprovado para impressão")

5. Exportações Finais
   └─ create_version(description="Versão final para impressão")
      └─ tag_version(tags=["final"])

6. Arquivo
   └─ tag_version(tags=["archived"])
```

## 💾 Estrutura de Armazenamento

```
./design_history/
├── version_registry.json          # Registro central
└── design_1/
    ├── v1/
    │   └── poster_v1.png
    ├── v2/
    │   └── poster_v2.png
    └── checkpoints.json
```

## 🔐 Boas Práticas

### ✅ O que fazer:
- Usar descrições claras e descritivas
- Criar versões depois de cada mudança significativa
- Usar tags consistentemente
- Criar checkpoints em marcos importantes
- Exportar histórico regularmente

### ❌ O que evitar:
- Criar versão para cada pequeno ajuste (criar versão a cada 15-30 minutos)
- Usar descrições vagas como "fixes" ou "ajustes"
- Misturar tags sem padrão
- Deletar versões sem backup
- Deixar histórico sem limpeza regular

## 📊 Casos de Uso

### Cenário 1: Revisão de Cliente
```python
# Cliente solicita mudanças
manager.create_version(
    design_id="poster_summer_2024",
    file_path="poster_v3.png",
    description="Mudanças solicitadas pelo cliente: azul mais escuro, fonte maior",
    author="designer_01"
)

# Se cliente aprovar
manager.tag_version(
    design_id="poster_summer_2024",
    version_number=3,
    tags=["client_approved"]
)
```

### Cenário 2: Múltiplas Variações
```python
# Criar variações para A/B testing
for variant in ["red", "blue", "green"]:
    manager.create_version(
        design_id="poster_summer_2024",
        file_path=f"poster_variant_{variant}.png",
        description=f"Variante com cores em {variant}",
        tags=["variant", f"color_{variant}", "ab_test"]
    )
```

### Cenário 3: Backup e Recovery
```python
# Fazer backup regularmente
manager.export_version_history(
    design_id="poster_summer_2024",
    output_path="backups/poster_summer_2024.json"
)

# Se algo der errado, reverter para último checkpoint
checkpoints = manager.get_all_checkpoints("poster_summer_2024")
last_cp = checkpoints[-1]
manager.rollback_version(
    design_id="poster_summer_2024",
    version_number=last_cp["version_number"]
)
```

## 🛠️ API Completa

```python
# Criação e Gestão
manager.create_version()           # Criar nova versão
manager.get_version()              # Obter versão específica
manager.get_version_history()      # Obter histórico completo

# Operações
manager.compare_versions()         # Comparar versões
manager.rollback_version()         # Reverter para versão
manager.create_checkpoint()        # Criar checkpoint

# Tags e Organização
manager.tag_version()              # Adicionar tags
manager.get_versions_by_tag()      # Buscar por tag
manager.get_approved_versions()    # Versões aprovadas
manager.get_final_version()        # Versão final

# Manutenção
manager.delete_version()           # Soft delete
manager.restore_version()          # Restaurar deletado

# Análise
manager.get_statistics()           # Estatísticas
manager.get_changelog()            # Changelog formatado
manager.export_version_history()   # Exportar para JSON
manager.get_all_checkpoints()      # Listar checkpoints
```

## 🔗 Integração com DesignAutomationClient

```python
from design_automation_client import DesignAutomationClient

client = DesignAutomationClient()

# Gerar pôster
result = client.generate_poster(
    prompt="...",
    output_path="poster.png"
)

# Criar versão automaticamente
version = client.create_version(
    design_id="my_poster",
    file_path=result['output'],
    description="Versão gerada por PosterCraft"
)

# Ver histórico
history = client.get_design_history("my_poster")
```

---

**Próximas etapas:** Integre versionamento em seus workflows diários para controle máximo sobre seus designs!
