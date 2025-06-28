"""
🧱 Prompt Bricks v2.0 - Interactive Mad-Libs Prompt Engineering

Revolutionary framework that combines user-friendly Mad-Libs interface
with hidden PSE optimization for 150% better AI output.
"""

from .core.workpaths import WorkpathManager
from .core.bricks import BrickLibrary, Brick
from .templates.template_engine import TemplateEngine
from .models.anti_claude import AntiClaude
from .brickz_builder import BrickzBuilder

__version__ = "2.0.0"
__author__ = "Tyler Bessire"
__email__ = "tylerbessire@gmail.com"

# Main exports
__all__ = [
    'BrickzBuilder',
    'WorkpathManager',
    'TemplateEngine', 
    'BrickLibrary',
    'Brick',
    'AntiClaude',
    'interactive_brickz',
    'quick_optimize'
]

def interactive_brickz():
    """Launch interactive Prompt Bricks interface"""
    print("🧱 Welcome to Interactive Prompt Bricks!")
    print("Build professional prompts with Mad-Libs simplicity")
    builder = BrickzBuilder()
    return builder.interactive_mode()

def quick_optimize(code, style="pythonic", goal="optimize", scope="function"):
    """One-liner for immediate code optimization"""
    builder = BrickzBuilder()
    builder.select_workpath("coding")
    builder.add_bricks(style=style, goal=goal, scope=scope)
    return builder.two_pass_optimize(code)

# Welcome message
def welcome():
    """Display welcome message"""
    print("🧱 Prompt Bricks v2.0")
    print("Interactive Mad-Libs prompt engineering")
    print("Hidden PSE optimization for 150% better results")
    print("\nTry: interactive_brickz() or quick_optimize('your code')")
