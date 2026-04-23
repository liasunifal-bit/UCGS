"""
Design Version Manager
Sistema avançado de gerenciamento de versões de designs
"""

import json
import os
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import difflib


@dataclass
class VersionMetadata:
    """Metadata de uma versão"""
    version_number: str
    created_at: str
    modified_at: str
    author: str
    description: str
    file_path: str
    file_size: int
    file_hash: str
    tags: List[str]
    changes: Dict
    is_stable: bool = False
    is_published: bool = False


class DesignVersionManager:
    """Gerenciador avançado de versões de designs"""
    
    def __init__(self, designs_base_path: str = "./designs_versions"):
        """
        Inicializa gerenciador de versões
        
        Args:
            designs_base_path: Caminho base para armazenar designs versionados
        """
        self.base_path = Path(designs_base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self.versions_db = {}  # {design_id: [versions]}
        self.changes_log = {}  # {design_id: [changes]}
        self.collaborators = {}  # {design_id: [authors]}
        
        self._load_database()
    
    def _load_database(self) -> None:
        """Carrega banco de dados de versões"""
        db_file = self.base_path / "versions_database.json"
        
        if db_file.exists():
            try:
                with open(db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.versions_db = data.get('versions', {})
                    self.changes_log = data.get('changes', {})
                    self.collaborators = data.get('collaborators', {})
            except Exception as e:
                print(f"Error loading database: {e}")
    
    def _save_database(self) -> None:
        """Salva banco de dados de versões"""
        db_file = self.base_path / "versions_database.json"
        
        data = {
            'versions': self.versions_db,
            'changes': self.changes_log,
            'collaborators': self.collaborators
        }
        
        try:
            with open(db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving database: {e}")
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calcula hash SHA256 de um arquivo"""
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()
    
    def create_version(
        self,
        design_id: str,
        file_path: str,
        author: str = "system",
        description: str = "",
        tags: List[str] = None,
        changes: Dict = None,
        is_stable: bool = False
    ) -> Dict:
        """
        Cria uma nova versão de um design
        
        Args:
            design_id: ID único do design
            file_path: Caminho do arquivo
            author: Autor da versão
            description: Descrição das mudanças
            tags: Tags para categorizar (ex: ['approved', 'production'])
            changes: Dict com detalhes das mudanças
            is_stable: Se é uma versão estável
            
        Returns:
            Dict com informações da versão criada
        """
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}"}
        
        # Inicializar se é primeiro design
        if design_id not in self.versions_db:
            self.versions_db[design_id] = []
            self.changes_log[design_id] = []
            self.collaborators[design_id] = []
        
        # Calcular número da versão
        version_number = len(self.versions_db[design_id]) + 1
        version_str = f"1.{version_number}"
        
        # Criar diretório para design
        design_path = self.base_path / design_id
        design_path.mkdir(parents=True, exist_ok=True)
        
        # Copiar arquivo para storage
        file_extension = Path(file_path).suffix
        versioned_file = design_path / f"v{version_number}{file_extension}"
        shutil.copy2(file_path, str(versioned_file))
        
        # Calcular hash
        file_hash = self._calculate_file_hash(str(versioned_file))
        
        # Criar metadata
        metadata = {
            "version_number": version_str,
            "created_at": datetime.now().isoformat(),
            "modified_at": datetime.now().isoformat(),
            "author": author,
            "description": description,
            "file_path": str(versioned_file),
            "file_size": os.path.getsize(versioned_file),
            "file_hash": file_hash,
            "tags": tags or [],
            "changes": changes or {},
            "is_stable": is_stable,
            "is_published": False
        }
        
        # Registrar versão
        self.versions_db[design_id].append(metadata)
        
        # Registrar no changelog
        if design_id not in self.changes_log:
            self.changes_log[design_id] = []
        
        change_entry = {
            "timestamp": datetime.now().isoformat(),
            "version": version_str,
            "author": author,
            "action": "created",
            "description": description,
            "changes": changes
        }
        self.changes_log[design_id].append(change_entry)
        
        # Registrar colaborador
        if author not in self.collaborators.get(design_id, []):
            if design_id not in self.collaborators:
                self.collaborators[design_id] = []
            self.collaborators[design_id].append(author)
        
        self._save_database()
        
        return {
            "status": "success",
            "version": version_str,
            "metadata": metadata,
            "message": f"Version {version_str} created successfully"
        }
    
    def get_version(self, design_id: str, version: str) -> Optional[Dict]:
        """
        Recupera informações de uma versão específica
        
        Args:
            design_id: ID do design
            version: Número da versão (ex: "1.2")
            
        Returns:
            Dict com metadata da versão ou None
        """
        versions = self.versions_db.get(design_id, [])
        
        for v in versions:
            if v["version_number"] == version:
                return v
        
        return None
    
    def get_version_history(self, design_id: str, limit: int = None) -> List[Dict]:
        """
        Retorna histórico de versões de um design
        
        Args:
            design_id: ID do design
            limit: Limite de versões a retornar (None = todas)
            
        Returns:
            Lista de versões ordenadas cronologicamente
        """
        versions = self.versions_db.get(design_id, [])
        
        if limit:
            versions = versions[-limit:]
        
        return versions
    
    def get_changelog(
        self,
        design_id: str,
        limit: int = None
    ) -> List[Dict]:
        """
        Retorna changelog (log de mudanças) de um design
        
        Args:
            design_id: ID do design
            limit: Limite de entradas
            
        Returns:
            Lista de mudanças cronológicas
        """
        changelog = self.changes_log.get(design_id, [])
        
        if limit:
            changelog = changelog[-limit:]
        
        return changelog
    
    def compare_versions(
        self,
        design_id: str,
        version1: str,
        version2: str
    ) -> Dict:
        """
        Compara duas versões de um design
        
        Args:
            design_id: ID do design
            version1: Primeira versão
            version2: Segunda versão
            
        Returns:
            Dict com diferenças entre versões
        """
        v1 = self.get_version(design_id, version1)
        v2 = self.get_version(design_id, version2)
        
        if not v1 or not v2:
            return {"status": "error", "message": "One or both versions not found"}
        
        comparison = {
            "design_id": design_id,
            "version1": version1,
            "version2": version2,
            "differences": {}
        }
        
        # Comparar tamanho
        comparison["differences"]["file_size"] = {
            "version1": v1["file_size"],
            "version2": v2["file_size"],
            "change_bytes": v2["file_size"] - v1["file_size"]
        }
        
        # Comparar hashes
        comparison["differences"]["content_changed"] = v1["file_hash"] != v2["file_hash"]
        
        # Comparar tags
        comparison["differences"]["tags"] = {
            "version1": v1["tags"],
            "version2": v2["tags"],
            "added": list(set(v2["tags"]) - set(v1["tags"])),
            "removed": list(set(v1["tags"]) - set(v2["tags"]))
        }
        
        # Comparar metadata de mudanças
        if v1["changes"] and v2["changes"]:
            comparison["differences"]["metadata_changes"] = {
                "version1": v1["changes"],
                "version2": v2["changes"]
            }
        
        comparison["differences"]["created_at"] = {
            "version1": v1["created_at"],
            "version2": v2["created_at"]
        }
        
        comparison["differences"]["authors"] = {
            "version1": v1["author"],
            "version2": v2["author"]
        }
        
        return comparison
    
    def rollback_version(
        self,
        design_id: str,
        version: str,
        author: str = "system",
        create_backup: bool = True
    ) -> Dict:
        """
        Reverte um design para uma versão anterior
        
        Args:
            design_id: ID do design
            version: Versão para restaurar
            author: Autor da reversion
            create_backup: Se deve criar backup da versão atual
            
        Returns:
            Dict com status da reversion
        """
        current_versions = self.versions_db.get(design_id, [])
        target_version = self.get_version(design_id, version)
        
        if not target_version:
            return {"status": "error", "message": f"Version {version} not found"}
        
        # Criar backup da versão atual se solicitado
        if create_backup and current_versions:
            current = current_versions[-1]
            self.create_version(
                design_id=design_id,
                file_path=current["file_path"],
                author=author,
                description=f"Backup before rollback to {version}",
                tags=["backup"],
                changes={"rollback_from": current["version_number"]}
            )
        
        # Copiar arquivo da versão alvo para versão atual
        design_path = self.base_path / design_id
        current_file = design_path / f"current{Path(target_version['file_path']).suffix}"
        
        shutil.copy2(target_version["file_path"], str(current_file))
        
        # Registrar reversion no changelog
        self.changes_log[design_id].append({
            "timestamp": datetime.now().isoformat(),
            "version": f"rollback_to_{version}",
            "author": author,
            "action": "rollback",
            "description": f"Reverted to version {version}",
            "changes": {"rolled_back_to": version}
        })
        
        self._save_database()
        
        return {
            "status": "success",
            "message": f"Successfully rolled back to version {version}",
            "rolled_back_to": version,
            "current_file": str(current_file)
        }
    
    def tag_version(
        self,
        design_id: str,
        version: str,
        tags: List[str],
        replace: bool = False
    ) -> Dict:
        """
        Adiciona ou substitui tags de uma versão
        
        Args:
            design_id: ID do design
            version: Número da versão
            tags: Tags a adicionar
            replace: Se True, substitui tags existentes
            
        Returns:
            Dict com resultado
        """
        v = self.get_version(design_id, version)
        
        if not v:
            return {"status": "error", "message": f"Version {version} not found"}
        
        if replace:
            v["tags"] = tags
        else:
            v["tags"] = list(set(v["tags"] + tags))
        
        self._save_database()
        
        return {
            "status": "success",
            "version": version,
            "tags": v["tags"]
        }
    
    def mark_stable(
        self,
        design_id: str,
        version: str
    ) -> Dict:
        """
        Marca uma versão como estável (production-ready)
        
        Args:
            design_id: ID do design
            version: Versão a marcar
            
        Returns:
            Dict com resultado
        """
        # Desmarcar versão anterior se houver
        versions = self.versions_db.get(design_id, [])
        for v in versions:
            if v["is_stable"]:
                v["is_stable"] = False
        
        # Marcar nova versão como estável
        v = self.get_version(design_id, version)
        if v:
            v["is_stable"] = True
            v["tags"] = list(set(v.get("tags", []) + ["stable", "production"]))
            self._save_database()
            
            return {
                "status": "success",
                "message": f"Version {version} marked as stable",
                "version": version
            }
        
        return {"status": "error", "message": f"Version {version} not found"}
    
    def publish_version(
        self,
        design_id: str,
        version: str
    ) -> Dict:
        """
        Marca uma versão como publicada
        
        Args:
            design_id: ID do design
            version: Versão a publicar
            
        Returns:
            Dict com resultado
        """
        v = self.get_version(design_id, version)
        
        if not v:
            return {"status": "error", "message": f"Version {version} not found"}
        
        v["is_published"] = True
        v["tags"] = list(set(v.get("tags", []) + ["published"]))
        self._save_database()
        
        return {
            "status": "success",
            "message": f"Version {version} published",
            "version": version
        }
    
    def get_stable_version(self, design_id: str) -> Optional[Dict]:
        """
        Recupera versão estável (production) de um design
        
        Args:
            design_id: ID do design
            
        Returns:
            Dict com versão estável ou None
        """
        versions = self.versions_db.get(design_id, [])
        
        for v in versions:
            if v.get("is_stable"):
                return v
        
        return None
    
    def get_published_versions(self, design_id: str) -> List[Dict]:
        """
        Recupera todas as versões publicadas
        
        Args:
            design_id: ID do design
            
        Returns:
            Lista de versões publicadas
        """
        versions = self.versions_db.get(design_id, [])
        return [v for v in versions if v.get("is_published")]
    
    def get_versions_by_tag(
        self,
        design_id: str,
        tag: str
    ) -> List[Dict]:
        """
        Recupera versões com uma tag específica
        
        Args:
            design_id: ID do design
            tag: Tag a filtrar
            
        Returns:
            Lista de versões com a tag
        """
        versions = self.versions_db.get(design_id, [])
        return [v for v in versions if tag in v.get("tags", [])]
    
    def get_design_statistics(self, design_id: str) -> Dict:
        """
        Retorna estatísticas de um design
        
        Args:
            design_id: ID do design
            
        Returns:
            Dict com estatísticas
        """
        versions = self.versions_db.get(design_id, [])
        changelog = self.changes_log.get(design_id, [])
        collaborators_list = self.collaborators.get(design_id, [])
        
        if not versions:
            return {"status": "error", "message": f"Design {design_id} not found"}
        
        file_sizes = [v["file_size"] for v in versions]
        
        return {
            "design_id": design_id,
            "total_versions": len(versions),
            "total_changes": len(changelog),
            "collaborators": collaborators_list,
            "collaborators_count": len(collaborators_list),
            "file_size_current": file_sizes[-1] if file_sizes else 0,
            "file_size_min": min(file_sizes) if file_sizes else 0,
            "file_size_max": max(file_sizes) if file_sizes else 0,
            "file_size_avg": sum(file_sizes) / len(file_sizes) if file_sizes else 0,
            "has_stable_version": any(v.get("is_stable") for v in versions),
            "published_versions_count": sum(1 for v in versions if v.get("is_published")),
            "creation_date": versions[0]["created_at"] if versions else None,
            "last_modified": versions[-1]["modified_at"] if versions else None
        }
    
    def export_version_history(
        self,
        design_id: str,
        output_path: str
    ) -> Dict:
        """
        Exporta histórico completo de versões
        
        Args:
            design_id: ID do design
            output_path: Caminho do arquivo JSON de saída
            
        Returns:
            Dict com resultado
        """
        versions = self.versions_db.get(design_id, [])
        changelog = self.changes_log.get(design_id, [])
        
        if not versions:
            return {"status": "error", "message": f"Design {design_id} not found"}
        
        export_data = {
            "design_id": design_id,
            "export_date": datetime.now().isoformat(),
            "versions": versions,
            "changelog": changelog,
            "statistics": self.get_design_statistics(design_id)
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return {
                "status": "success",
                "message": f"Version history exported to {output_path}",
                "output_path": output_path
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def clean_old_versions(
        self,
        design_id: str,
        keep_count: int = 10,
        keep_stable: bool = True
    ) -> Dict:
        """
        Remove versões antigas mantendo as mais recentes
        
        Args:
            design_id: ID do design
            keep_count: Número de versões a manter
            keep_stable: Se deve manter versão estável
            
        Returns:
            Dict com resultado
        """
        versions = self.versions_db.get(design_id, [])
        
        if len(versions) <= keep_count:
            return {
                "status": "info",
                "message": f"Design has only {len(versions)} versions, nothing to clean"
            }
        
        stable_version = None
        if keep_stable:
            stable_version = self.get_stable_version(design_id)
        
        versions_to_keep = set()
        versions_to_keep.update(v["version_number"] for v in versions[-keep_count:])
        
        if stable_version:
            versions_to_keep.add(stable_version["version_number"])
        
        versions_to_delete = [
            v for v in versions
            if v["version_number"] not in versions_to_keep
        ]
        
        deleted_count = 0
        for v in versions_to_delete:
            try:
                os.remove(v["file_path"])
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {v['file_path']}: {e}")
        
        self.versions_db[design_id] = [
            v for v in versions
            if v["version_number"] in versions_to_keep
        ]
        
        self._save_database()
        
        return {
            "status": "success",
            "message": f"Cleaned {deleted_count} old versions",
            "versions_kept": len(self.versions_db[design_id]),
            "versions_deleted": deleted_count
        }
    
    def list_all_designs(self) -> List[str]:
        """
        Lista todos os designs com versões
        
        Returns:
            Lista de design IDs
        """
        return list(self.versions_db.keys())
    
    def get_all_statistics(self) -> Dict:
        """
        Retorna estatísticas globais de todos os designs
        
        Returns:
            Dict com estatísticas agregadas
        """
        all_designs = self.list_all_designs()
        
        total_versions = sum(
            len(self.versions_db.get(d, []))
            for d in all_designs
        )
        
        total_size = sum(
            sum(v["file_size"] for v in self.versions_db.get(d, []))
            for d in all_designs
        )
        
        return {
            "total_designs": len(all_designs),
            "total_versions": total_versions,
            "total_storage_used": total_size,
            "designs": [self.get_design_statistics(d) for d in all_designs]
        }


# ===== EXEMPLO DE USO =====

if __name__ == "__main__":
    manager = DesignVersionManager()
    
    # Criar versão
    result = manager.create_version(
        design_id="campaign_2024",
        file_path="design.png",
        author="alice",
        description="Initial design with colors and typography",
        tags=["draft"],
        changes={"colors": ["#FF6B6B", "#4ECDC4"]}
    )
    print(f"Created: {result['status']}")
    
    # Ver histórico
    history = manager.get_version_history("campaign_2024")
    print(f"History: {len(history)} versions")
    
    # Marcar como estável
    stable = manager.mark_stable("campaign_2024", "1.1")
    print(f"Stable: {stable['status']}")
    
    # Estatísticas
    stats = manager.get_design_statistics("campaign_2024")
    print(f"Statistics: {json.dumps(stats, indent=2)}")
