"""
Template Library Manager
Gerenciamento de templates reutilizáveis para designs
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class TemplateLibrary:
    """Gerencia biblioteca de templates reutilizáveis"""
    
    def __init__(self, library_path: str = "./template_library"):
        """
        Inicializa biblioteca de templates
        
        Args:
            library_path: Caminho para armazenar templates
        """
        self.library_path = Path(library_path)
        self.library_path.mkdir(parents=True, exist_ok=True)
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Carrega templates do disco"""
        templates_file = self.library_path / "templates.json"
        
        if templates_file.exists():
            with open(templates_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_templates(self) -> None:
        """Salva templates no disco"""
        templates_file = self.library_path / "templates.json"
        
        with open(templates_file, 'w', encoding='utf-8') as f:
            json.dump(self.templates, f, indent=2, ensure_ascii=False)
    
    def create_template(
        self,
        name: str,
        category: str,
        dimensions: Dict[str, int],
        brand_colors: List[str] = None,
        elements: Dict = None,
        description: str = ""
    ) -> Dict:
        """
        Cria novo template
        
        Args:
            name: Nome do template
            category: Categoria (social_media, print, web, etc)
            dimensions: Dict com width e height em px
            brand_colors: Cores corporativas em hex
            elements: Elementos gráficos padrão
            description: Descrição do template
            
        Returns:
            Dict com informações do template criado
        """
        template_id = f"{category}_{len(self.templates)}"
        
        template = {
            "id": template_id,
            "name": name,
            "category": category,
            "dimensions": dimensions,
            "brand_colors": brand_colors or [],
            "elements": elements or {},
            "description": description,
            "created_at": datetime.now().isoformat(),
            "usage_count": 0,
            "last_used": None
        }
        
        self.templates[template_id] = template
        self._save_templates()
        
        return template
    
    def get_template(self, template_id: str) -> Optional[Dict]:
        """
        Recupera um template específico
        
        Args:
            template_id: ID do template
            
        Returns:
            Dict com template ou None
        """
        template = self.templates.get(template_id)
        
        if template:
            # Incrementar uso
            template["usage_count"] = template.get("usage_count", 0) + 1
            template["last_used"] = datetime.now().isoformat()
            self._save_templates()
        
        return template
    
    def get_templates_by_category(self, category: str) -> List[Dict]:
        """
        Lista templates de uma categoria
        
        Args:
            category: Nome da categoria
            
        Returns:
            Lista de templates
        """
        return [t for t in self.templates.values() 
                if t.get("category") == category]
    
    def search_templates(self, query: str) -> List[Dict]:
        """
        Busca templates por nome ou descrição
        
        Args:
            query: Termo de busca
            
        Returns:
            Lista de templates encontrados
        """
        query_lower = query.lower()
        results = []
        
        for template in self.templates.values():
            if (query_lower in template.get("name", "").lower() or
                query_lower in template.get("description", "").lower()):
                results.append(template)
        
        return results
    
    def list_all_templates(self) -> List[Dict]:
        """Lista todos os templates"""
        return list(self.templates.values())
    
    def list_categories(self) -> List[str]:
        """Lista todas as categorias"""
        categories = set()
        for template in self.templates.values():
            categories.add(template.get("category"))
        return sorted(list(categories))
    
    def delete_template(self, template_id: str) -> bool:
        """
        Deleta um template
        
        Args:
            template_id: ID do template
            
        Returns:
            True se deletado com sucesso
        """
        if template_id in self.templates:
            del self.templates[template_id]
            self._save_templates()
            return True
        return False
    
    def update_template(
        self,
        template_id: str,
        **kwargs
    ) -> Optional[Dict]:
        """
        Atualiza propriedades de um template
        
        Args:
            template_id: ID do template
            **kwargs: Propriedades a atualizar
            
        Returns:
            Template atualizado ou None
        """
        if template_id not in self.templates:
            return None
        
        template = self.templates[template_id]
        
        for key, value in kwargs.items():
            if key not in ["id", "created_at"]:  # Campos protegidos
                template[key] = value
        
        template["updated_at"] = datetime.now().isoformat()
        self._save_templates()
        
        return template
    
    def get_most_used_templates(self, limit: int = 10) -> List[Dict]:
        """
        Retorna templates mais utilizados
        
        Args:
            limit: Número máximo de templates
            
        Returns:
            Lista ordenada por uso
        """
        sorted_templates = sorted(
            self.templates.values(),
            key=lambda x: x.get("usage_count", 0),
            reverse=True
        )
        return sorted_templates[:limit]
    
    def duplicate_template(
        self,
        template_id: str,
        new_name: str
    ) -> Optional[Dict]:
        """
        Duplica um template
        
        Args:
            template_id: ID do template original
            new_name: Nome para novo template
            
        Returns:
            Novo template ou None
        """
        original = self.templates.get(template_id)
        
        if not original:
            return None
        
        new_template = {
            **original,
            "id": f"{original['category']}_copy_{len(self.templates)}",
            "name": new_name,
            "created_at": datetime.now().isoformat(),
            "usage_count": 0,
            "last_used": None
        }
        
        self.templates[new_template["id"]] = new_template
        self._save_templates()
        
        return new_template
    
    def export_templates(self, output_path: str, category: str = None) -> bool:
        """
        Exporta templates para arquivo
        
        Args:
            output_path: Caminho do arquivo de saída
            category: Exportar apenas categoria específica (opcional)
            
        Returns:
            True se exportado com sucesso
        """
        try:
            if category:
                templates = self.get_templates_by_category(category)
            else:
                templates = list(self.templates.values())
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(templates, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error exporting templates: {e}")
            return False
    
    def import_templates(self, input_path: str, merge: bool = True) -> Dict:
        """
        Importa templates de arquivo
        
        Args:
            input_path: Caminho do arquivo
            merge: Se True, mescla com templates existentes
            
        Returns:
            Dict com resultado da importação
        """
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                imported = json.load(f)
            
            if not merge:
                self.templates = {}
            
            imported_count = 0
            for template in imported:
                if isinstance(template, dict) and "id" in template:
                    self.templates[template["id"]] = template
                    imported_count += 1
            
            self._save_templates()
            
            return {
                "status": "success",
                "imported_count": imported_count,
                "total_templates": len(self.templates)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas da biblioteca"""
        all_templates = list(self.templates.values())
        total_usage = sum(t.get("usage_count", 0) for t in all_templates)
        
        return {
            "total_templates": len(self.templates),
            "categories": len(self.list_categories()),
            "total_usage": total_usage,
            "average_usage": total_usage / len(all_templates) if all_templates else 0,
            "categories_list": self.list_categories()
        }


# ===== EXEMPLO DE USO =====

if __name__ == "__main__":
    # Inicializar biblioteca
    lib = TemplateLibrary()
    
    # Criar templates padrão
    instagram_post = lib.create_template(
        name="Instagram Post",
        category="social_media",
        dimensions={"width": 1080, "height": 1080},
        brand_colors=["#FF6B6B", "#4ECDC4", "#45B7D1"],
        description="Post padrão para Instagram"
    )
    print("Created:", json.dumps(instagram_post, indent=2))
    
    # Buscar por categoria
    social_templates = lib.get_templates_by_category("social_media")
    print(f"\nSocial Media Templates: {len(social_templates)}")
    
    # Estatísticas
    stats = lib.get_statistics()
    print(f"\nLibrary Statistics: {json.dumps(stats, indent=2)}")
