"""
Inspiration Gallery Manager
Gerenciador de galeria de inspiração para criação de posts
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class InspirationGallery:
    """Gerencia galeria de inspiração para design de posts"""
    
    def __init__(self, gallery_path: str = "./inspiration_gallery"):
        """
        Inicializa galeria de inspiração
        
        Args:
            gallery_path: Caminho para armazenar galeria
        """
        self.gallery_path = Path(gallery_path)
        self.gallery_path.mkdir(parents=True, exist_ok=True)
        self.inspirations = self._load_inspirations()
    
    def _load_inspirations(self) -> Dict:
        """Carrega inspirações do disco"""
        inspirations_file = self.gallery_path / "inspirations.json"
        
        if inspirations_file.exists():
            with open(inspirations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_inspirations(self) -> None:
        """Salva inspirações no disco"""
        inspirations_file = self.gallery_path / "inspirations.json"
        
        with open(inspirations_file, 'w', encoding='utf-8') as f:
            json.dump(self.inspirations, f, indent=2, ensure_ascii=False)
    
    def add_inspiration(
        self,
        category: str,
        name: str,
        description: str,
        visual_elements: List[str],
        color_palette: List[str],
        typography: Dict,
        use_cases: List[str],
        mood: str,
        target_audience: str,
        image_path: str = None,
        reference_url: str = None,
        tags: List[str] = None
    ) -> Dict:
        """
        Adiciona uma inspiração à galeria
        
        Args:
            category: Categoria (instagram, tiktok, linkedin, etc)
            name: Nome da inspiração
            description: Descrição detalhada
            visual_elements: Elementos visuais (formas, textures, etc)
            color_palette: Cores em hex
            typography: Dict com info de tipografia
            use_cases: Casos de uso
            mood: Mood/atmosfera (energético, calmo, profissional, etc)
            target_audience: Público-alvo
            image_path: Caminho da imagem de referência
            reference_url: URL de referência
            tags: Tags para busca
            
        Returns:
            Dict com inspiração adicionada
        """
        inspiration_id = f"{category}_{name.lower().replace(' ', '_')}_{len(self.inspirations)}"
        
        inspiration = {
            "id": inspiration_id,
            "name": name,
            "category": category,
            "description": description,
            "visual_elements": visual_elements,
            "color_palette": color_palette,
            "typography": typography,
            "use_cases": use_cases,
            "mood": mood,
            "target_audience": target_audience,
            "image_path": image_path,
            "reference_url": reference_url,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "usage_count": 0
        }
        
        self.inspirations[inspiration_id] = inspiration
        self._save_inspirations()
        
        return inspiration
    
    def get_inspiration_by_category(self, category: str) -> List[Dict]:
        """
        Retorna inspirações de uma categoria
        
        Args:
            category: Nome da categoria
            
        Returns:
            Lista de inspirações
        """
        return [i for i in self.inspirations.values() 
                if i.get("category") == category]
    
    def get_inspiration_by_mood(self, mood: str) -> List[Dict]:
        """
        Retorna inspirações por mood
        
        Args:
            mood: Mood desejado
            
        Returns:
            Lista de inspirações
        """
        return [i for i in self.inspirations.values() 
                if i.get("mood").lower() == mood.lower()]
    
    def search_inspirations(self, query: str) -> List[Dict]:
        """
        Busca inspirações por nome, descrição ou tags
        
        Args:
            query: Termo de busca
            
        Returns:
            Lista de inspirações encontradas
        """
        query_lower = query.lower()
        results = []
        
        for inspiration in self.inspirations.values():
            if (query_lower in inspiration.get("name", "").lower() or
                query_lower in inspiration.get("description", "").lower() or
                any(query_lower in tag.lower() for tag in inspiration.get("tags", []))):
                results.append(inspiration)
        
        return results
    
    def get_random_inspiration(self, category: str = None) -> Optional[Dict]:
        """
        Retorna inspiração aleatória
        
        Args:
            category: Filtrar por categoria (opcional)
            
        Returns:
            Inspiração aleatória
        """
        import random
        
        if category:
            options = self.get_inspiration_by_category(category)
        else:
            options = list(self.inspirations.values())
        
        if options:
            return random.choice(options)
        return None
    
    def get_inspiration_prompt(self, inspiration_id: str) -> str:
        """
        Gera prompt para PosterCraft baseado em inspiração
        
        Args:
            inspiration_id: ID da inspiração
            
        Returns:
            Prompt para geração de pôster
        """
        inspiration = self.inspirations.get(inspiration_id)
        
        if not inspiration:
            return ""
        
        # Atualizar contagem de uso
        inspiration["usage_count"] = inspiration.get("usage_count", 0) + 1
        self._save_inspirations()
        
        # Construir prompt detalhado
        visual = ", ".join(inspiration.get("visual_elements", []))
        colors = ", ".join(inspiration.get("color_palette", []))
        mood = inspiration.get("mood", "")
        
        prompt = f"""
        Design Style: {inspiration['name']}
        Mood: {mood}
        Visual Elements: {visual}
        Color Palette: {colors}
        Typography Style: {inspiration['typography'].get('style', 'modern')}
        Target Audience: {inspiration['target_audience']}
        Description: {inspiration['description']}
        
        Create a professional {inspiration['category']} post with these characteristics.
        High quality, modern design, professional finish.
        """
        
        return prompt.strip()
    
    def get_color_suggestions(self, inspiration_id: str) -> Dict:
        """
        Retorna sugestões de cores de uma inspiração
        
        Args:
            inspiration_id: ID da inspiração
            
        Returns:
            Dict com cores e harmonias
        """
        inspiration = self.inspirations.get(inspiration_id)
        
        if not inspiration:
            return {}
        
        return {
            "primary_colors": inspiration["color_palette"][:3],
            "accent_colors": inspiration["color_palette"][3:],
            "full_palette": inspiration["color_palette"],
            "color_harmony": "complementary",  # ou "analogous", "triadic"
            "usage": {
                "background": inspiration["color_palette"][0],
                "text": inspiration["color_palette"][1],
                "accent": inspiration["color_palette"][2]
            }
        }
    
    def get_typography_guide(self, inspiration_id: str) -> Dict:
        """
        Retorna guia tipográfico de uma inspiração
        
        Args:
            inspiration_id: ID da inspiração
            
        Returns:
            Dict com recomendações tipográficas
        """
        inspiration = self.inspirations.get(inspiration_id)
        
        if not inspiration:
            return {}
        
        typography = inspiration.get("typography", {})
        
        return {
            "title": {
                "font": typography.get("title_font", "Sans-serif Bold"),
                "size": typography.get("title_size", "48px"),
                "weight": typography.get("title_weight", "bold"),
                "style": typography.get("title_style", "uppercase")
            },
            "subtitle": {
                "font": typography.get("subtitle_font", "Sans-serif"),
                "size": typography.get("subtitle_size", "24px"),
                "weight": typography.get("subtitle_weight", "regular")
            },
            "body": {
                "font": typography.get("body_font", "Sans-serif"),
                "size": typography.get("body_size", "14px"),
                "weight": typography.get("body_weight", "regular")
            }
        }
    
    def get_layout_suggestions(self, inspiration_id: str) -> List[str]:
        """
        Retorna sugestões de layout baseado em inspiração
        
        Args:
            inspiration_id: ID da inspiração
            
        Returns:
            Lista de sugestões de layout
        """
        inspiration = self.inspirations.get(inspiration_id)
        
        if not inspiration:
            return []
        
        layouts = {
            "energético": [
                "Texto no canto superior esquerdo com diagonal dinâmica",
                "Imagem grande no fundo com texto sobreposto",
                "Grade assimétrica com elementos flutuantes"
            ],
            "calmo": [
                "Texto centralizado com espaço em branco",
                "Layout grid simétrico",
                "Imagem grande com texto minimalista"
            ],
            "profissional": [
                "Header com logo, body com texto, footer com CTA",
                "Duas colunas: texto à esquerda, visual à direita",
                "Barra superior colorida com conteúdo abaixo"
            ],
            "criativo": [
                "Elementos sobrepostos com ângulos",
                "Composição circular",
                "Tipografia grande sobreposta a imagem"
            ]
        }
        
        mood = inspiration.get("mood", "").lower()
        return layouts.get(mood, layouts["criativo"])
    
    def get_most_used(self, limit: int = 10) -> List[Dict]:
        """
        Retorna inspirações mais utilizadas
        
        Args:
            limit: Número máximo
            
        Returns:
            Lista ordenada por uso
        """
        sorted_inspirations = sorted(
            self.inspirations.values(),
            key=lambda x: x.get("usage_count", 0),
            reverse=True
        )
        return sorted_inspirations[:limit]
    
    def list_categories(self) -> List[str]:
        """Lista todas as categorias disponíveis"""
        categories = set()
        for inspiration in self.inspirations.values():
            categories.add(inspiration.get("category"))
        return sorted(list(categories))
    
    def list_moods(self) -> List[str]:
        """Lista todos os moods disponíveis"""
        moods = set()
        for inspiration in self.inspirations.values():
            moods.add(inspiration.get("mood"))
        return sorted(list(moods))
    
    def generate_design_brief(self, inspiration_id: str) -> str:
        """
        Gera um brief detalhado para designers
        
        Args:
            inspiration_id: ID da inspiração
            
        Returns:
            String com brief formatado
        """
        inspiration = self.inspirations.get(inspiration_id)
        
        if not inspiration:
            return ""
        
        brief = f"""
╔════════════════════════════════════════════════════════════════════╗
║                         DESIGN BRIEF                              ║
╚════════════════════════════════════════════════════════════════════╝

PROJETO: {inspiration['name']}
CATEGORIA: {inspiration['category'].upper()}
DATA: {datetime.now().strftime('%d/%m/%Y')}

OBJETIVO:
{inspiration['description']}

PÚBLICO-ALVO:
{inspiration['target_audience']}

CASOS DE USO:
{''.join([f'  • {use}\n' for use in inspiration['use_cases']])}

MOOD/ATMOSFERA:
{inspiration['mood']}

PALETA DE CORES:
{''.join([f'  • {color}\n' for color in inspiration['color_palette']])}

ELEMENTOS VISUAIS:
{''.join([f'  • {element}\n' for element in inspiration['visual_elements']])}

TIPOGRAFIA:
  • Título: {inspiration['typography'].get('title_font', 'N/A')}
  • Subtítulo: {inspiration['typography'].get('subtitle_font', 'N/A')}
  • Corpo: {inspiration['typography'].get('body_font', 'N/A')}

RECOMENDAÇÕES:
  • Mantenha a proporção de branco
  • Use contrastes fortes para legibilidade
  • Priorize mobile-first design
  • Teste em diferentes tamanhos

═══════════════════════════════════════════════════════════════════
"""
        
        return brief
    
    def export_inspiration(self, inspiration_id: str, output_path: str) -> bool:
        """
        Exporta inspiração para JSON
        
        Args:
            inspiration_id: ID da inspiração
            output_path: Caminho de saída
            
        Returns:
            True se exportado com sucesso
        """
        inspiration = self.inspirations.get(inspiration_id)
        
        if not inspiration:
            return False
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(inspiration, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro exportando inspiração: {e}")
            return False
    
    def create_collection(self, name: str, inspiration_ids: List[str]) -> Dict:
        """
        Cria uma coleção de inspirações
        
        Args:
            name: Nome da coleção
            inspiration_ids: IDs das inspirações
            
        Returns:
            Dict com coleção
        """
        collection = {
            "name": name,
            "created_at": datetime.now().isoformat(),
            "inspirations": inspiration_ids,
            "count": len(inspiration_ids)
        }
        
        return collection


# ===== INSPIRAÇÕES PRÉ-DEFINIDAS =====

PRESET_INSPIRATIONS = [
    {
        "category": "instagram",
        "name": "Energético Moderno",
        "description": "Design dinâmico e vibrante para produtos tech e startups",
        "visual_elements": ["formas geométricas", "gradientes", "efeitos de movimento"],
        "color_palette": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#FFD93D"],
        "typography": {
            "title_font": "Poppins Bold",
            "subtitle_font": "Poppins SemiBold",
            "body_font": "Poppins Regular",
            "title_size": "48px",
            "title_style": "uppercase"
        },
        "use_cases": ["Lançamento de produtos", "Promoções", "Campanhas virais"],
        "mood": "energético",
        "target_audience": "Millennials e Gen Z",
        "tags": ["tech", "startup", "moderno"]
    },
    {
        "category": "instagram",
        "name": "Minimalista Elegante",
        "description": "Design limpo e sofisticado para marcas de luxo",
        "visual_elements": ["espaço em branco", "tipografia fina", "elementos sutil"],
        "color_palette": ["#FFFFFF", "#333333", "#CCCCCC", "#F5F5F5", "#D4AF37"],
        "typography": {
            "title_font": "Garamond Regular",
            "subtitle_font": "Garamond Light",
            "body_font": "Helvetica Regular",
            "title_size": "36px",
            "title_style": "sentence"
        },
        "use_cases": ["Produtos premium", "Serviços luxo", "Beleza e moda"],
        "mood": "calmo",
        "target_audience": "Público adulto premium",
        "tags": ["luxo", "minimalista", "elegante"]
    },
    {
        "category": "linkedin",
        "name": "Profissional Corporativo",
        "description": "Design formal para conteúdo corporativo e B2B",
        "visual_elements": ["linhas limpas", "ícones profissionais", "gráficos"],
        "color_palette": ["#0077B5", "#1A1A1A", "#FFFFFF", "#F2F2F2", "#00A4EF"],
        "typography": {
            "title_font": "Helvetica Bold",
            "subtitle_font": "Helvetica Regular",
            "body_font": "Helvetica Regular",
            "title_size": "32px",
            "title_style": "sentence"
        },
        "use_cases": ["Posts empresariais", "Estatísticas", "Pensamento de líder"],
        "mood": "profissional",
        "target_audience": "Profissionais e executivos",
        "tags": ["corporativo", "negócio", "b2b"]
    },
    {
        "category": "tiktok",
        "name": "Viral Divertido",
        "description": "Design descontraído e engraçado para conteúdo viral",
        "visual_elements": ["emojis", "texto grande", "cores neon", "stickers"],
        "color_palette": ["#FF1493", "#00D4FF", "#00FF00", "#FFFF00", "#FF6600"],
        "typography": {
            "title_font": "Arial Black",
            "subtitle_font": "Arial Bold",
            "body_font": "Arial Regular",
            "title_size": "56px",
            "title_style": "uppercase"
        },
        "use_cases": ["Humor", "Trends", "Educação descontraída"],
        "mood": "divertido",
        "target_audience": "Gen Z",
        "tags": ["viral", "divertido", "trends"]
    },
    {
        "category": "youtube",
        "name": "Thumbnail Impactante",
        "description": "Design que atrai cliques em thumbnails de vídeos",
        "visual_elements": ["face grandes", "setas", "texto contrastante", "emoji"],
        "color_palette": ["#FF0000", "#FFFF00", "#FFFFFF", "#000000", "#00D4FF"],
        "typography": {
            "title_font": "Arial Black",
            "subtitle_font": "Arial Bold",
            "body_font": "Arial Regular",
            "title_size": "64px",
            "title_style": "uppercase"
        },
        "use_cases": ["Thumbnails de vídeos", "Covers", "Introduções"],
        "mood": "impactante",
        "target_audience": "Espectadores de vídeos",
        "tags": ["youtube", "thumbnail", "video"]
    }
]


if __name__ == "__main__":
    gallery = InspirationGallery()
    
    # Adicionar inspirações pré-definidas
    for preset in PRESET_INSPIRATIONS:
        gallery.add_inspiration(**preset)
    
    print("✓ Inspirações adicionadas à galeria!")
    print(f"Total: {len(gallery.inspirations)}")
