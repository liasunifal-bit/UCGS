"""
Design Automation Client
Integração unificada de PosterCraft, Canva API e Gerenciamento de Versões
"""

import requests
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from design_version_manager import DesignVersionManager


class DesignAutomationClient:
    """Cliente unificado para automação de designs"""
    
    def __init__(self, canva_client_id: str = None, canva_client_secret: str = None, versions_path: str = "./designs_versions"):
        """
        Inicializa o cliente de automação de design
        
        Args:
            canva_client_id: ID da aplicação Canva
            canva_client_secret: Secret da aplicação Canva
            versions_path: Caminho para armazenar versões de designs
        """
        self.canva_client_id = canva_client_id or os.getenv("CANVA_CLIENT_ID")
        self.canva_client_secret = canva_client_secret or os.getenv("CANVA_CLIENT_SECRET")
        self.canva_base_url = "https://api.canva.com/v1"
        self.canva_access_token = None
        self.designs_registry = {}
        self.versions_history = {}
        
        # Inicializar gerenciador de versões
        self.version_manager = DesignVersionManager(designs_base_path=versions_path)
        
    # ===== POSTERCRAFT METHODS =====
    
    def generate_poster(
        self,
        prompt: str,
        output_path: str,
        steps: int = 28,
        guidance: float = 3.5,
        seed: Optional[int] = None
    ) -> Dict:
        """
        Gera um pôster usando PosterCraft
        
        Args:
            prompt: Descrição do pôster desejado
            output_path: Caminho do arquivo de saída
            steps: Número de passos de inferência
            guidance: Guidance scale para controle de prompt
            seed: Semaphore para reprodutibilidade (opcional)
            
        Returns:
            Dict com status, arquivo de saída e metadata
        """
        try:
            cmd = [
                "python3",
                "/scripts/generate_poster.py",
                "--prompt", prompt,
                "--output", output_path,
                "--steps", str(steps),
                "--guidance", str(guidance)
            ]
            
            if seed is not None:
                cmd.extend(["--seed", str(seed)])
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "output": output_path,
                    "prompt": prompt,
                    "parameters": {
                        "steps": steps,
                        "guidance": guidance,
                        "seed": seed
                    },
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr,
                    "stdout": result.stdout
                }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def generate_multiple_posters(
        self,
        prompts: List[str],
        output_dir: str,
        steps: int = 28,
        guidance: float = 3.5
    ) -> List[Dict]:
        """
        Gera múltiplos pôsteres em lote
        
        Args:
            prompts: Lista de prompts
            output_dir: Diretório de saída
            steps: Passos de inferência
            guidance: Guidance scale
            
        Returns:
            Lista de resultados
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        results = []
        
        for idx, prompt in enumerate(prompts):
            output_path = os.path.join(output_dir, f"poster_{idx+1}.png")
            result = self.generate_poster(
                prompt=prompt,
                output_path=output_path,
                steps=steps,
                guidance=guidance,
                seed=None
            )
            results.append(result)
        
        return results
    
    # ===== CANVA INTEGRATION METHODS =====
    
    def canva_authenticate(self, code: str, redirect_uri: str) -> Optional[str]:
        """
        Autentica no Canva usando OAuth 2.0
        
        Args:
            code: Código de autorização do usuário
            redirect_uri: URI de redirecionamento configurado
            
        Returns:
            Token de acesso ou None em caso de erro
        """
        try:
            url = f"{self.canva_base_url}/oauth/token"
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": redirect_uri,
                "client_id": self.canva_client_id,
                "client_secret": self.canva_client_secret
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                self.canva_access_token = response.json().get("access_token")
                return self.canva_access_token
            else:
                raise Exception(f"Authentication failed: {response.text}")
        except Exception as e:
            raise Exception(f"Canva authentication error: {str(e)}")
    
    def canva_list_designs(self) -> Dict:
        """
        Lista todos os designs do usuário no Canva
        
        Returns:
            Dict com lista de designs
        """
        if not self.canva_access_token:
            return {"error": "Not authenticated with Canva"}
        
        try:
            url = f"{self.canva_base_url}/designs"
            headers = {"Authorization": f"Bearer {self.canva_access_token}"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Error listing designs: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    def canva_create_from_template(
        self,
        template_id: str,
        title: str
    ) -> Dict:
        """
        Cria um novo design baseado em template no Canva
        
        Args:
            template_id: ID do template de marca
            title: Título do novo design
            
        Returns:
            Dict com detalhes do design criado
        """
        if not self.canva_access_token:
            return {"error": "Not authenticated with Canva"}
        
        try:
            url = f"{self.canva_base_url}/designs"
            headers = {
                "Authorization": f"Bearer {self.canva_access_token}",
                "Content-Type": "application/json"
            }
            data = {
                "brand_template_id": template_id,
                "title": title
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            
            if response.status_code in [200, 201]:
                result = response.json()
                self.designs_registry[result.get("id")] = result
                return result
            else:
                return {"error": f"Error creating design: {response.text}"}
        except Exception as e:
            return {"error": str(e)}
    
    # ===== VERSION MANAGEMENT METHODS =====
    
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
        Cria uma versão de um design com histórico completo
        
        Args:
            design_id: ID único do design
            file_path: Caminho do arquivo do design
            author: Autor da versão
            description: Descrição da versão/mudanças
            tags: Tags para categorizar (ex: ['approved', 'production'])
            changes: Dict com detalhes técnicos das mudanças
            is_stable: Se é uma versão estável/production
            
        Returns:
            Dict com informações da versão criada
        """
        return self.version_manager.create_version(
            design_id=design_id,
            file_path=file_path,
            author=author,
            description=description,
            tags=tags,
            changes=changes,
            is_stable=is_stable
        )
    
    def get_design_history(self, design_id: str, limit: int = None) -> List[Dict]:
        """
        Retorna histórico completo de versões de um design
        
        Args:
            design_id: ID do design
            limit: Limite de versões a retornar
            
        Returns:
            Lista de versões ordenadas cronologicamente
        """
        return self.version_manager.get_version_history(design_id, limit=limit)
    
    def get_changelog(self, design_id: str, limit: int = None) -> List[Dict]:
        """
        Retorna changelog (log de mudanças) detalhado de um design
        
        Args:
            design_id: ID do design
            limit: Limite de entradas
            
        Returns:
            Lista de mudanças com metadata completa
        """
        return self.version_manager.get_changelog(design_id, limit=limit)
    
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
            version1: Primeira versão (ex: "1.2")
            version2: Segunda versão (ex: "1.3")
            
        Returns:
            Dict com diferenças detalhadas
        """
        return self.version_manager.compare_versions(design_id, version1, version2)
    
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
            version: Versão para restaurar (ex: "1.1")
            author: Autor da reversion
            create_backup: Se deve criar backup da versão atual
            
        Returns:
            Dict com status da reversion
        """
        return self.version_manager.rollback_version(
            design_id=design_id,
            version=version,
            author=author,
            create_backup=create_backup
        )
    
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
            tags: Tags a adicionar/substituir
            replace: Se True, substitui tags existentes
            
        Returns:
            Dict com resultado
        """
        return self.version_manager.tag_version(design_id, version, tags, replace)
    
    def mark_stable(self, design_id: str, version: str) -> Dict:
        """
        Marca uma versão como estável (production-ready)
        
        Args:
            design_id: ID do design
            version: Versão a marcar como estável
            
        Returns:
            Dict com resultado
        """
        return self.version_manager.mark_stable(design_id, version)
    
    def publish_version(self, design_id: str, version: str) -> Dict:
        """
        Marca uma versão como publicada
        
        Args:
            design_id: ID do design
            version: Versão a publicar
            
        Returns:
            Dict com resultado
        """
        return self.version_manager.publish_version(design_id, version)
    
    def get_stable_version(self, design_id: str) -> Optional[Dict]:
        """
        Recupera versão estável (production) de um design
        
        Args:
            design_id: ID do design
            
        Returns:
            Dict com versão estável ou None
        """
        return self.version_manager.get_stable_version(design_id)
    
    def get_published_versions(self, design_id: str) -> List[Dict]:
        """
        Recupera todas as versões publicadas de um design
        
        Args:
            design_id: ID do design
            
        Returns:
            Lista de versões publicadas
        """
        return self.version_manager.get_published_versions(design_id)
    
    def get_versions_by_tag(self, design_id: str, tag: str) -> List[Dict]:
        """
        Recupera versões com uma tag específica
        
        Args:
            design_id: ID do design
            tag: Tag a filtrar
            
        Returns:
            Lista de versões com a tag
        """
        return self.version_manager.get_versions_by_tag(design_id, tag)
    
    def get_design_statistics(self, design_id: str) -> Dict:
        """
        Retorna estatísticas completas de um design
        
        Args:
            design_id: ID do design
            
        Returns:
            Dict com estatísticas de versões, colaboradores, tamanho, etc
        """
        return self.version_manager.get_design_statistics(design_id)
    
    def export_version_history(
        self,
        design_id: str,
        output_path: str
    ) -> Dict:
        """
        Exporta histórico completo de versões para arquivo JSON
        
        Args:
            design_id: ID do design
            output_path: Caminho do arquivo JSON de saída
            
        Returns:
            Dict com resultado
        """
        return self.version_manager.export_version_history(design_id, output_path)
    
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
        return self.version_manager.clean_old_versions(design_id, keep_count, keep_stable)
    
    # ===== EXPORT METHODS =====
    
    def export_design(
        self,
        input_path: str,
        output_path: str,
        format: str = "png",
        quality: str = "high",
        dpi: int = 300
    ) -> Dict:
        """
        Exporta um design em diferentes formatos
        
        Args:
            input_path: Caminho do arquivo de entrada
            output_path: Caminho de saída
            format: Formato (png, pdf, svg, webp)
            quality: Qualidade (low, medium, high)
            dpi: DPI para exportação
            
        Returns:
            Dict com status da exportação
        """
        try:
            # Esta função seria implementada com ferramentas como
            # PIL, reportlab (PDF), svgwrite, etc.
            
            if not os.path.exists(input_path):
                return {"status": "error", "message": f"File not found: {input_path}"}
            
            return {
                "status": "pending",
                "message": f"Export to {format} configured",
                "input": input_path,
                "output": output_path,
                "format": format,
                "quality": quality,
                "dpi": dpi
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def export_multi_format(
        self,
        input_path: str,
        output_dir: str,
        formats: List[str] = None,
        quality: str = "high"
    ) -> Dict:
        """
        Exporta um design em múltiplos formatos simultaneamente
        
        Args:
            input_path: Arquivo de entrada
            output_dir: Diretório de saída
            formats: Lista de formatos desejados
            quality: Qualidade de exportação
            
        Returns:
            Dict com status de todas as exportações
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        formats = formats or ["png", "pdf", "svg"]
        results = {}
        
        base_name = Path(input_path).stem
        
        for fmt in formats:
            output_path = os.path.join(output_dir, f"{base_name}.{fmt}")
            result = self.export_design(
                input_path=input_path,
                output_path=output_path,
                format=fmt,
                quality=quality
            )
            results[fmt] = result
        
        return {
            "status": "success",
            "message": "Multi-format export configured",
            "exports": results,
            "output_directory": output_dir
        }
    
    # ===== TEMPLATE LIBRARY METHODS =====
    
    def create_template(
        self,
        name: str,
        dimensions: Tuple[int, int],
        brand_colors: List[str] = None,
        description: str = ""
    ) -> Dict:
        """
        Cria um template na biblioteca
        
        Args:
            name: Nome do template
            dimensions: Tupla (width, height)
            brand_colors: Lista de cores hex corporativas
            description: Descrição do template
            
        Returns:
            Dict com informações do template
        """
        template = {
            "id": f"template_{len(self.designs_registry)}",
            "name": name,
            "dimensions": {"width": dimensions[0], "height": dimensions[1]},
            "brand_colors": brand_colors or [],
            "description": description,
            "created_at": datetime.now().isoformat()
        }
        
        self.designs_registry[template["id"]] = template
        return template
    
    def get_templates(self) -> List[Dict]:
        """
        Retorna lista de templates disponíveis
        
        Returns:
            Lista de templates
        """
        return [v for v in self.designs_registry.values() 
                if "name" in v and "dimensions" in v]


# ===== EXEMPLO DE USO =====

if __name__ == "__main__":
    # Inicializar cliente
    client = DesignAutomationClient()
    
    # Gerar pôster
    result = client.generate_poster(
        prompt="Vibrant summer festival poster with bold typography and tropical colors",
        output_path="festival_poster.png",
        steps=30,
        guidance=3.5
    )
    print("PosterCraft Result:", json.dumps(result, indent=2))
    
    # Criar versão
    if result["status"] == "success":
        version = client.create_version(
            design_id="festival_poster_1",
            file_path=result["output"],
            description="Initial design version"
        )
        print("Version Created:", json.dumps(version, indent=2))
        
        # Exportar em múltiplos formatos
        export_result = client.export_multi_format(
            input_path=result["output"],
            output_dir="./exports",
            formats=["png", "pdf", "svg"],
            quality="high"
        )
        print("Export Result:", json.dumps(export_result, indent=2))
