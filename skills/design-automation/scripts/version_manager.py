"""
Advanced Version Manager
Gerenciamento avançado de versões com histórico, comparação e rollback
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib


class VersionManager:
    """Gerencia versões de designs com histórico detalhado"""
    
    def __init__(self, history_path: str = "./design_history"):
        """
        Inicializa gerenciador de versões
        
        Args:
            history_path: Caminho para armazenar histórico de versões
        """
        self.history_path = Path(history_path)
        self.history_path.mkdir(parents=True, exist_ok=True)
        self.version_registry = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Carrega registro de versões do disco"""
        registry_file = self.history_path / "version_registry.json"
        
        if registry_file.exists():
            with open(registry_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_registry(self) -> None:
        """Salva registro de versões no disco"""
        registry_file = self.history_path / "version_registry.json"
        
        with open(registry_file, 'w', encoding='utf-8') as f:
            json.dump(self.version_registry, f, indent=2, ensure_ascii=False)
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calcula hash SHA256 de um arquivo para detectar mudanças"""
        sha256_hash = hashlib.sha256()
        
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return f"error_{str(e)}"
    
    def create_version(
        self,
        design_id: str,
        file_path: str,
        description: str = "",
        author: str = "system",
        tags: List[str] = None,
        metadata: Dict = None
    ) -> Dict:
        """
        Cria uma nova versão de um design
        
        Args:
            design_id: ID único do design
            file_path: Caminho do arquivo do design
            description: Descrição das mudanças
            author: Autor da versão
            tags: Tags para categorizar (ex: ['approved', 'final'])
            metadata: Metadados adicionais
            
        Returns:
            Dict com informações da versão
        """
        if design_id not in self.version_registry:
            self.version_registry[design_id] = {
                "design_id": design_id,
                "created_at": datetime.now().isoformat(),
                "versions": [],
                "current_version": None,
                "total_versions": 0
            }
        
        design_record = self.version_registry[design_id]
        version_number = design_record["total_versions"] + 1
        
        # Informações do arquivo
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            file_hash = self._calculate_file_hash(file_path)
            file_modified = os.path.getmtime(file_path)
        else:
            file_size = 0
            file_hash = "file_not_found"
            file_modified = None
        
        version_info = {
            "version_number": version_number,
            "semantic_version": f"1.{version_number}",
            "created_at": datetime.now().isoformat(),
            "author": author,
            "description": description,
            "file_path": file_path,
            "file_size": file_size,
            "file_hash": file_hash,
            "file_modified": file_modified,
            "tags": tags or [],
            "metadata": metadata or {},
            "status": "active"
        }
        
        design_record["versions"].append(version_info)
        design_record["current_version"] = version_number
        design_record["total_versions"] = version_number
        
        self._save_registry()
        
        return version_info
    
    def get_version(self, design_id: str, version_number: int) -> Optional[Dict]:
        """
        Retorna informações de uma versão específica
        
        Args:
            design_id: ID do design
            version_number: Número da versão
            
        Returns:
            Dict com informações da versão ou None
        """
        design_record = self.version_registry.get(design_id)
        
        if not design_record:
            return None
        
        for version in design_record["versions"]:
            if version["version_number"] == version_number:
                return version
        
        return None
    
    def get_version_history(self, design_id: str) -> List[Dict]:
        """
        Retorna histórico completo de versões de um design
        
        Args:
            design_id: ID do design
            
        Returns:
            Lista de versões
        """
        design_record = self.version_registry.get(design_id)
        
        if not design_record:
            return []
        
        return design_record["versions"]
    
    def compare_versions(
        self,
        design_id: str,
        version1: int,
        version2: int
    ) -> Dict:
        """
        Compara duas versões de um design
        
        Args:
            design_id: ID do design
            version1: Primeira versão
            version2: Segunda versão
            
        Returns:
            Dict com diferenças encontradas
        """
        v1 = self.get_version(design_id, version1)
        v2 = self.get_version(design_id, version2)
        
        if not v1 or not v2:
            return {"error": "Uma ou ambas as versões não encontradas"}
        
        # Comparar hashes para detectar mudanças no arquivo
        file_changed = v1["file_hash"] != v2["file_hash"]
        
        comparison = {
            "design_id": design_id,
            "version1": {
                "version": v1["version_number"],
                "created_at": v1["created_at"],
                "author": v1["author"],
                "description": v1["description"],
                "file_size": v1["file_size"]
            },
            "version2": {
                "version": v2["version_number"],
                "created_at": v2["created_at"],
                "author": v2["author"],
                "description": v2["description"],
                "file_size": v2["file_size"]
            },
            "differences": {
                "file_changed": file_changed,
                "size_difference": v2["file_size"] - v1["file_size"],
                "tags_changed": v1["tags"] != v2["tags"],
                "time_difference_seconds": (
                    datetime.fromisoformat(v2["created_at"]) -
                    datetime.fromisoformat(v1["created_at"])
                ).total_seconds()
            }
        }
        
        return comparison
    
    def rollback_version(self, design_id: str, version_number: int) -> Dict:
        """
        Reverte um design para uma versão anterior
        
        Args:
            design_id: ID do design
            version_number: Versão para retornar
            
        Returns:
            Dict com status da reversion
        """
        design_record = self.version_registry.get(design_id)
        
        if not design_record:
            return {"status": "error", "message": "Design não encontrado"}
        
        version = self.get_version(design_id, version_number)
        
        if not version:
            return {"status": "error", "message": f"Versão {version_number} não encontrada"}
        
        if not os.path.exists(version["file_path"]):
            return {"status": "error", "message": "Arquivo da versão não existe"}
        
        design_record["current_version"] = version_number
        
        self._save_registry()
        
        return {
            "status": "success",
            "message": f"Revertido para versão {version_number}",
            "version_info": version,
            "file_path": version["file_path"]
        }
    
    def tag_version(
        self,
        design_id: str,
        version_number: int,
        tags: List[str]
    ) -> Optional[Dict]:
        """
        Adiciona tags a uma versão (ex: 'approved', 'final', 'archived')
        
        Args:
            design_id: ID do design
            version_number: Número da versão
            tags: Lista de tags
            
        Returns:
            Versão atualizada ou None
        """
        version = self.get_version(design_id, version_number)
        
        if not version:
            return None
        
        # Adicionar novas tags sem duplicar
        existing_tags = set(version["tags"])
        new_tags = set(tags)
        version["tags"] = list(existing_tags.union(new_tags))
        
        self._save_registry()
        
        return version
    
    def get_versions_by_tag(self, design_id: str, tag: str) -> List[Dict]:
        """
        Retorna todas as versões com uma tag específica
        
        Args:
            design_id: ID do design
            tag: Tag para buscar
            
        Returns:
            Lista de versões com a tag
        """
        history = self.get_version_history(design_id)
        return [v for v in history if tag in v["tags"]]
    
    def get_approved_versions(self, design_id: str) -> List[Dict]:
        """Retorna versões aprovadas (tagged com 'approved')"""
        return self.get_versions_by_tag(design_id, "approved")
    
    def get_final_version(self, design_id: str) -> Optional[Dict]:
        """Retorna versão final (tagged com 'final')"""
        finals = self.get_versions_by_tag(design_id, "final")
        return finals[0] if finals else None
    
    def delete_version(self, design_id: str, version_number: int) -> Dict:
        """
        Marca uma versão como deletada (soft delete)
        
        Args:
            design_id: ID do design
            version_number: Versão a deletar
            
        Returns:
            Dict com status
        """
        version = self.get_version(design_id, version_number)
        
        if not version:
            return {"status": "error", "message": "Versão não encontrada"}
        
        design_record = self.version_registry.get(design_id)
        
        if design_record["current_version"] == version_number:
            return {
                "status": "error",
                "message": "Não pode deletar versão atual. Faça rollback primeiro."
            }
        
        version["status"] = "deleted"
        version["deleted_at"] = datetime.now().isoformat()
        
        self._save_registry()
        
        return {"status": "success", "message": "Versão marcada como deletada"}
    
    def restore_version(self, design_id: str, version_number: int) -> Dict:
        """
        Restaura uma versão deletada
        
        Args:
            design_id: ID do design
            version_number: Versão a restaurar
            
        Returns:
            Dict com status
        """
        version = self.get_version(design_id, version_number)
        
        if not version:
            return {"status": "error", "message": "Versão não encontrada"}
        
        if version["status"] != "deleted":
            return {"status": "error", "message": "Versão não está deletada"}
        
        version["status"] = "active"
        version.pop("deleted_at", None)
        
        self._save_registry()
        
        return {"status": "success", "message": "Versão restaurada"}
    
    def create_checkpoint(
        self,
        design_id: str,
        description: str = ""
    ) -> Dict:
        """
        Cria um checkpoint (versão importante/milestone)
        
        Args:
            design_id: ID do design
            description: Descrição do checkpoint
            
        Returns:
            Dict com informações do checkpoint
        """
        design_record = self.version_registry.get(design_id)
        
        if not design_record:
            return {"status": "error", "message": "Design não encontrado"}
        
        current_version_num = design_record["current_version"]
        version = self.get_version(design_id, current_version_num)
        
        if not version:
            return {"status": "error", "message": "Versão atual não encontrada"}
        
        # Adicionar tag de checkpoint
        checkpoint_tag = f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.tag_version(design_id, current_version_num, [checkpoint_tag, "checkpoint"])
        
        checkpoint_info = {
            "checkpoint_tag": checkpoint_tag,
            "version_number": current_version_num,
            "created_at": datetime.now().isoformat(),
            "description": description,
            "version_info": version
        }
        
        return checkpoint_info
    
    def get_all_checkpoints(self, design_id: str) -> List[Dict]:
        """Retorna todos os checkpoints de um design"""
        history = self.get_version_history(design_id)
        checkpoints = []
        
        for version in history:
            if "checkpoint" in version["tags"]:
                checkpoints.append(version)
        
        return checkpoints
    
    def get_changelog(self, design_id: str, limit: int = None) -> List[Dict]:
        """
        Retorna changelog (histórico de mudanças) formatado
        
        Args:
            design_id: ID do design
            limit: Limitar número de entradas
            
        Returns:
            Lista de mudanças formatadas
        """
        history = self.get_version_history(design_id)
        changelog = []
        
        for i, version in enumerate(history):
            if version["status"] == "deleted":
                continue
            
            change_entry = {
                "version": version["semantic_version"],
                "date": version["created_at"],
                "author": version["author"],
                "description": version["description"],
                "tags": version["tags"],
                "type": "checkpoint" if "checkpoint" in version["tags"] else "update"
            }
            changelog.append(change_entry)
        
        if limit:
            changelog = changelog[-limit:]
        
        return changelog
    
    def export_version_history(self, design_id: str, output_path: str) -> bool:
        """
        Exporta histórico de versões para JSON
        
        Args:
            design_id: ID do design
            output_path: Caminho do arquivo de saída
            
        Returns:
            True se exportado com sucesso
        """
        try:
            history = self.get_version_history(design_id)
            
            export_data = {
                "design_id": design_id,
                "exported_at": datetime.now().isoformat(),
                "total_versions": len(history),
                "versions": history
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Erro exportando histórico: {e}")
            return False
    
    def get_statistics(self, design_id: str) -> Dict:
        """
        Retorna estatísticas de um design
        
        Args:
            design_id: ID do design
            
        Returns:
            Dict com estatísticas
        """
        design_record = self.version_registry.get(design_id)
        
        if not design_record:
            return {"error": "Design não encontrado"}
        
        history = design_record["versions"]
        active_versions = [v for v in history if v["status"] == "active"]
        deleted_versions = [v for v in history if v["status"] == "deleted"]
        
        # Calcular estatísticas de tamanho
        sizes = [v["file_size"] for v in active_versions if v["file_size"] > 0]
        
        stats = {
            "design_id": design_id,
            "total_versions": len(history),
            "active_versions": len(active_versions),
            "deleted_versions": len(deleted_versions),
            "checkpoints": len([v for v in active_versions if "checkpoint" in v["tags"]]),
            "file_size_stats": {
                "current": active_versions[-1]["file_size"] if active_versions else 0,
                "min": min(sizes) if sizes else 0,
                "max": max(sizes) if sizes else 0,
                "average": sum(sizes) / len(sizes) if sizes else 0,
                "total": sum(sizes)
            },
            "authors": list(set(v["author"] for v in active_versions)),
            "tags": list(set(tag for v in active_versions for tag in v["tags"])),
            "created_at": design_record["created_at"],
            "latest_version": {
                "number": design_record["current_version"],
                "created_at": active_versions[-1]["created_at"] if active_versions else None
            }
        }
        
        return stats


# ===== EXEMPLO DE USO =====

if __name__ == "__main__":
    manager = VersionManager()
    
    # Criar design com múltiplas versões
    print("=== Version Manager Demo ===\n")
    
    # Simular versões (usando arquivos de teste)
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Design v1")
        file1 = f.name
    
    # Criar primeira versão
    v1 = manager.create_version(
        design_id="poster_summer_2024",
        file_path=file1,
        description="Design inicial",
        author="designer_01",
        tags=["initial"]
    )
    print(f"✓ Versão criada: {v1['semantic_version']}")
    
    # Criar checkpoint
    checkpoint = manager.create_checkpoint(
        design_id="poster_summer_2024",
        description="Design aprovado para revisão"
    )
    print(f"✓ Checkpoint criado: {checkpoint['checkpoint_tag']}")
    
    # Ver estatísticas
    stats = manager.get_statistics("poster_summer_2024")
    print(f"\nEstatísticas:")
    print(f"  Total de versões: {stats['total_versions']}")
    print(f"  Checkpoints: {stats['checkpoints']}")
    print(f"  Autores: {', '.join(stats['authors'])}")
    
    # Ver changelog
    changelog = manager.get_changelog("poster_summer_2024")
    print(f"\nChangelog:")
    for entry in changelog:
        print(f"  {entry['version']} - {entry['description']} ({entry['author']})")
    
    # Limpar
    os.unlink(file1)
