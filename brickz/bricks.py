"""
Enhanced Bricks System with Custom Creation and Categories
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
import json
import uuid
from enum import Enum

class BrickCategory(Enum):
    """Six main brick categories with color coding"""
    STYLES = ("styles", "#4ECDC4", "How to approach the task")
    GOALS = ("goals", "#45B7D1", "What to accomplish")
    SCOPES = ("scopes", "#F7DC6F", "Level of focus")
    PERSONAS = ("personas", "#BB8FCE", "Expert perspective")
    FORMATS = ("formats", "#F1948A", "Output structure")
    CONTEXTS = ("contexts", "#82E0AA", "Situational factors")
    
    def __init__(self, key, color, description):
        self.key = key
        self.color = color
        self.description = description

@dataclass
class Brick:
    """Enhanced brick with custom creation support"""
    id: str
    name: str
    category: BrickCategory
    description: str
    modifier_text: str
    workpaths: List[str]
    is_custom: bool = False
    creator: str = "system"
    usage_count: int = 0
    rating: float = 0.0

class BrickLibrary:
    """Enhanced brick library with custom creation and personal collections"""
    
    def __init__(self, data_file: str = "data/bricks.json"):
        self.data_file = data_file
        self.bricks: Dict[str, Brick] = {}
        self.user_collections: Dict[str, List[str]] = {}
        self._load_system_bricks()
    
    def _load_system_bricks(self):
        """Load the core system bricks"""
        system_bricks = [
            # STYLES
            Brick("sty_pythonic", "pythonic", BrickCategory.STYLES, 
                  "Clean, idiomatic Python code", 
                  "following Pythonic best practices and conventions", 
                  ["coding"]),
            Brick("sty_defensive", "defensive", BrickCategory.STYLES,
                  "Robust error handling and validation",
                  "with defensive programming and comprehensive error handling",
                  ["coding"]),
            Brick("sty_elegant", "elegant", BrickCategory.STYLES,
                  "Sophisticated and refined approach",
                  "with elegant, sophisticated design and implementation",
                  ["all"]),
            
            # GOALS
            Brick("gol_optimize", "optimize", BrickCategory.GOALS,
                  "Speed and efficiency gains",
                  "to optimize performance, reduce complexity, and improve speed",
                  ["coding"]),
            Brick("gol_security", "secure", BrickCategory.GOALS,
                  "Harden against vulnerabilities", 
                  "to improve security and protect against vulnerabilities",
                  ["coding"]),
            
            # SCOPES
            Brick("sco_function", "function", BrickCategory.SCOPES,
                  "Single function optimization",
                  "focusing on individual function improvement",
                  ["coding"]),
            Brick("sco_system", "system", BrickCategory.SCOPES,
                  "System-wide optimization",
                  "focusing on system-wide performance and architecture",
                  ["coding"]),
            
            # PERSONAS
            Brick("per_senior", "senior_engineer", BrickCategory.PERSONAS,
                  "Senior developer perspective",
                  "from the perspective of a senior software engineer",
                  ["coding"]),
            Brick("per_security", "security_expert", BrickCategory.PERSONAS,
                  "Security specialist analysis",
                  "from the perspective of a security expert and penetration tester",
                  ["coding"]),
            
            # FORMATS
            Brick("fmt_structured", "structured", BrickCategory.FORMATS,
                  "Well-organized output",
                  "in a well-structured, organized format",
                  ["all"]),
            
            # CONTEXTS
            Brick("ctx_production", "production", BrickCategory.CONTEXTS,
                  "Production environment",
                  "considering production environment requirements",
                  ["coding"])
        ]
        
        for brick in system_bricks:
            self.bricks[brick.id] = brick
    
    def get_bricks_for_workpath(self, workpath: str) -> Dict[str, List[Brick]]:
        """Get all bricks organized by category for a specific workpath"""
        result = {}
        
        for category in BrickCategory:
            category_bricks = []
            for brick in self.bricks.values():
                if workpath in brick.workpaths or "all" in brick.workpaths:
                    if brick.category == category:
                        category_bricks.append(brick)
            
            if category_bricks:
                result[category.key] = category_bricks
        
        return result
    
    def get_brick(self, brick_id: str) -> Optional[Brick]:
        """Get a specific brick by ID"""
        return self.bricks.get(brick_id)
    
    def validate_custom_brick(self, name: str, category: BrickCategory, 
                            modifier_text: str) -> Tuple[bool, str]:
        """Validate a custom brick before creation"""
        if not name or len(name) < 2:
            return False, "Brick name must be at least 2 characters"
        if not modifier_text or len(modifier_text) < 10:
            return False, "Modifier text must be at least 10 characters"
        return True, "Valid"
    
    def create_custom_brick(self, name: str, category: BrickCategory, description: str, 
                          modifier_text: str, workpaths: List[str], creator: str = "user") -> Brick:
        """Create a new custom brick"""
        brick_id = f"cst_{category.key}_{str(uuid.uuid4())[:8]}"
        
        brick = Brick(
            id=brick_id,
            name=name,
            category=category,
            description=description,
            modifier_text=modifier_text,
            workpaths=workpaths,
            is_custom=True,
            creator=creator
        )
        
        self.bricks[brick_id] = brick
        return brick
    
    def increment_usage(self, brick_id: str):
        """Increment usage count for a brick"""
        if brick_id in self.bricks:
            self.bricks[brick_id].usage_count += 1
    
    def get_popular_bricks(self, limit: int = 10) -> List[Brick]:
        """Get most popular bricks by usage count"""
        sorted_bricks = sorted(self.bricks.values(), key=lambda b: b.usage_count, reverse=True)
        return sorted_bricks[:limit]
    
    def search_bricks(self, query: str, workpath: str = None) -> List[Brick]:
        """Search bricks by name, description, or modifier text"""
        query_lower = query.lower()
        results = []
        
        for brick in self.bricks.values():
            if workpath and workpath not in brick.workpaths and "all" not in brick.workpaths:
                continue
                
            if (query_lower in brick.name.lower() or 
                query_lower in brick.description.lower() or
                query_lower in brick.modifier_text.lower()):
                results.append(brick)
        
        return results
    
    def get_mad_libs_prompts(self, category: BrickCategory) -> Dict[str, str]:
        """Get Mad Libs style prompts for creating custom bricks"""
        prompts = {
            BrickCategory.STYLES: {
                "descriptor": "What kind of style approach?",
                "verb": "What action should it emphasize?",
                "context": "In what context?"
            },
            BrickCategory.GOALS: {
                "descriptor": "What kind of outcome?",
                "verb": "What should be achieved?",
                "target": "What specifically?"
            }
        }
        
        return prompts.get(category, {
            "descriptor": "Describe the brick type",
            "action": "What should it do?",
            "context": "In what context?"
        })
