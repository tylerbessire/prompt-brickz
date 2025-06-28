"""
Enhanced Brick Library with Mad-Libs style components
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import json

@dataclass
class Brick:
    """Individual brick component for Mad-Libs style selection"""
    name: str
    category: str  # style, goal, scope, review, etc.
    description: str
    color: str  # For UI visualization
    modifier_text: str
    workpaths: List[str]  # Which workpaths this brick applies to

class BrickLibrary:
    """Enhanced library with categorized bricks for Mad-Libs interface"""
    
    def __init__(self):
        self.bricks = self._initialize_brick_collection()
    
    def _initialize_brick_collection(self):
        """Initialize the comprehensive brick collection"""
        return {
            # CODING WORKPATH BRICKS
            "coding_styles": [
                Brick("pythonic", "style", "Clean, idiomatic Python code", "#3776ab", 
                      "following Pythonic best practices and conventions", ["coding"]),
                Brick("defensive", "style", "Robust error handling and validation", "#dc3545", 
                      "with defensive programming and comprehensive error handling", ["coding"]),
                Brick("verbose_logging", "style", "Detailed logging and debugging", "#28a745", 
                      "with extensive logging and debugging capabilities", ["coding"]),
                Brick("minimalist", "style", "Clean, simple, essential code only", "#6c757d", 
                      "using minimalist design with essential functionality only", ["coding"]),
                Brick("performance_first", "style", "Speed and efficiency optimized", "#fd7e14", 
                      "prioritizing performance and computational efficiency", ["coding"]),
                Brick("functional", "style", "Functional programming paradigm", "#6f42c1", 
                      "using functional programming patterns and immutability", ["coding"]),
                Brick("object_oriented", "style", "Clean OOP design patterns", "#20c997", 
                      "following object-oriented design principles and patterns", ["coding"])
            ],
            
            "coding_goals": [
                Brick("fix_bugs", "goal", "Debug and resolve issues", "#dc3545", 
                      "to identify and fix bugs, errors, and logical issues", ["coding"]),
                Brick("optimize_performance", "goal", "Speed and efficiency gains", "#fd7e14", 
                      "to optimize performance, reduce complexity, and improve speed", ["coding"]),
                Brick("improve_security", "goal", "Harden against vulnerabilities", "#e83e8c", 
                      "to improve security and protect against vulnerabilities", ["coding"]),
                Brick("add_features", "goal", "Extend functionality", "#0dcaf0", 
                      "to add new features and extend existing functionality", ["coding"]),
                Brick("refactor_structure", "goal", "Improve code organization", "#6f42c1", 
                      "to refactor and improve code structure and maintainability", ["coding"]),
                Brick("enhance_readability", "goal", "Make code clearer", "#198754", 
                      "to enhance readability and code documentation", ["coding"]),
                Brick("modernize_code", "goal", "Update to latest standards", "#0d6efd", 
                      "to modernize code using latest language features and best practices", ["coding"])
            ],
            
            "coding_scopes": [
                Brick("function", "scope", "Single function optimization", "#17a2b8", 
                      "focusing on individual function improvement", ["coding"]),
                Brick("class", "scope", "Class-level improvements", "#28a745", 
                      "focusing on class design and method optimization", ["coding"]),
                Brick("module", "scope", "Module-wide refactoring", "#ffc107", 
                      "focusing on module-level organization and structure", ["coding"]),
                Brick("package", "scope", "Package architecture", "#6f42c1", 
                      "focusing on package structure and inter-module relationships", ["coding"]),
                Brick("system", "scope", "System-wide optimization", "#fd7e14", 
                      "focusing on system-wide performance and architecture", ["coding"]),
                Brick("api", "scope", "API design and endpoints", "#20c997", 
                      "focusing on API design, endpoints, and interface contracts", ["coding"])
            ],
            
            "coding_reviews": [
                Brick("senior_engineer", "review", "Senior developer perspective", "#0d6efd", 
                      "from the perspective of a senior software engineer", ["coding"]),
                Brick("tech_lead", "review", "Technical leadership view", "#6f42c1", 
                      "from the perspective of a technical lead and architect", ["coding"]),
                Brick("security_expert", "review", "Security specialist analysis", "#e83e8c", 
                      "from the perspective of a security expert and penetration tester", ["coding"]),
                Brick("performance_engineer", "review", "Optimization specialist", "#fd7e14", 
                      "from the perspective of a performance optimization engineer", ["coding"]),
                Brick("code_reviewer", "review", "Peer review standards", "#198754", 
                      "from the perspective of a thorough code reviewer", ["coding"])
            ],
            
            # CONVERSATIONAL WORKPATH BRICKS  
            "conversational_styles": [
                Brick("friendly", "style", "Warm and approachable tone", "#28a745", 
                      "in a friendly, warm, and approachable manner", ["conversational"]),
                Brick("professional", "style", "Business and formal tone", "#0d6efd", 
                      "in a professional, business-appropriate manner", ["conversational"]),
                Brick("casual", "style", "Relaxed and informal tone", "#ffc107", 
                      "in a casual, relaxed, and conversational manner", ["conversational"]),
                Brick("educational", "style", "Teaching and explanatory", "#17a2b8", 
                      "in an educational, explanatory, and informative manner", ["conversational"]),
                Brick("empathetic", "style", "Understanding and supportive", "#e83e8c", 
                      "with empathy, understanding, and emotional support", ["conversational"])
            ],
            
            # EXPLORATORY WORKPATH BRICKS
            "exploratory_approaches": [
                Brick("comprehensive", "approach", "Thorough and complete analysis", "#6f42c1", 
                      "through comprehensive and exhaustive analysis", ["exploratory"]),
                Brick("multi_perspective", "approach", "Multiple viewpoints", "#fd7e14", 
                      "from multiple perspectives and viewpoints", ["exploratory"]),
                Brick("evidence_based", "approach", "Data-driven investigation", "#198754", 
                      "using evidence-based and data-driven investigation", ["exploratory"]),
                Brick("creative", "approach", "Innovative and original thinking", "#e83e8c", 
                      "through creative and innovative exploration", ["exploratory"])
            ]
        }
    
    def get_bricks_for_workpath(self, workpath: str) -> Dict[str, List[Brick]]:
        """Get all bricks organized by category for a specific workpath"""
        result = {}
        for category, bricks in self.bricks.items():
            if workpath in category:  # e.g., "coding_styles" contains "coding"
                category_name = category.split('_')[1]  # Extract "styles" from "coding_styles"
                result[category_name] = [brick for brick in bricks if workpath in brick.workpaths]
        return result
    
    def get_brick(self, name: str) -> Optional[Brick]:
        """Get a specific brick by name"""
        for category in self.bricks.values():
            for brick in category:
                if brick.name == name:
                    return brick
        return None
    
    def get_random_selection(self, workpath: str) -> Dict[str, Brick]:
        """Get a random brick selection for quick start"""
        import random
        bricks_by_category = self.get_bricks_for_workpath(workpath)
        selection = {}
        for category, bricks in bricks_by_category.items():
            if bricks:
                selection[category] = random.choice(bricks)
        return selection
    
    def validate_selection(self, selection: Dict[str, str], workpath: str) -> bool:
        """Validate that selected bricks are compatible with workpath"""
        bricks_by_category = self.get_bricks_for_workpath(workpath)
        for category, brick_name in selection.items():
            if category not in bricks_by_category:
                return False
            valid_names = [brick.name for brick in bricks_by_category[category]]
            if brick_name not in valid_names:
                return False
        return True
