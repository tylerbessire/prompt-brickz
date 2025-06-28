"""
Interactive Brickz Builder - Mad-Libs interface for prompt construction
"""

from .core.bricks import BrickLibrary, Brick
from .core.workpaths import WorkpathManager
from .templates.template_engine import TemplateEngine
from .models.anti_claude import AntiClaude
from typing import Dict, Optional
import json

class BrickzBuilder:
    """
    Interactive builder for Mad-Libs style prompt construction
    with hidden two-pass PSE optimization
    """
    
    def __init__(self):
        self.brick_library = BrickLibrary()
        self.workpath_manager = WorkpathManager()
        self.template_engine = TemplateEngine()
        self.anti_claude = AntiClaude()
        
        self.current_workpath = None
        self.selected_bricks = {}
        self.content = None
        self.build_history = []
    
    def select_workpath(self, workpath):
        """Select workpath: coding, conversational, or exploratory"""
        if self.workpath_manager.select_workpath(workpath):
            self.current_workpath = workpath
            print(f"✅ Workpath selected: {workpath}")
            return True
        else:
            print(f"❌ Invalid workpath: {workpath}")
            return False
    
    def show_available_bricks(self):
        """Display available bricks for current workpath in Mad-Libs style"""
        if not self.current_workpath:
            print("❌ Please select a workpath first")
            return
        
        bricks_by_category = self.brick_library.get_bricks_for_workpath(self.current_workpath)
        
        print(f"\n🧱 Available Bricks for {self.current_workpath.title()}:")
        print("="*60)
        
        for category, bricks in bricks_by_category.items():
            print(f"\n{category.title()}: ", end="")
            brick_options = []
            for brick in bricks:
                brick_options.append(f"[{brick.name}]")
            print(" ".join(brick_options))
        
        print("\n" + "="*60)
    
    def add_bricks(self, **brick_selections):
        """Add bricks using keyword arguments (style=pythonic, goal=optimize)"""
        if not self.current_workpath:
            print("❌ Please select a workpath first")
            return False
        
        # Validate selections
        if not self.brick_library.validate_selection(brick_selections, self.current_workpath):
            print("❌ Invalid brick selection for current workpath")
            return False
        
        # Add valid bricks
        for category, brick_name in brick_selections.items():
            brick = self.brick_library.get_brick(brick_name)
            if brick:
                self.selected_bricks[category] = brick
                print(f"🧱 Added {category}: [{brick.name}] - {brick.description}")
        
        print(f"✅ {len(brick_selections)} bricks selected")
        return True
    
    def interactive_mode(self):
        """Launch interactive Mad-Libs interface"""
        print("🧱 Interactive Prompt Bricks Builder")
        print("="*50)
        
        # Step 1: Workpath selection
        print("\n🛤️  Choose your workpath:")
        print("1. Coding - Code improvement and optimization")
        print("2. Conversational - Enhanced dialogue and assistance")  
        print("3. Exploratory - Research and investigation")
        
        while True:
            try:
                choice = input("\nSelect workpath (1-3): ").strip()
                workpath_map = {"1": "coding", "2": "conversational", "3": "exploratory"}
                if choice in workpath_map and self.select_workpath(workpath_map[choice]):
                    break
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                return None
        
        # Step 2: Show available bricks
        self.show_available_bricks()
        
        # Step 3: Interactive brick selection
        print("\n🎮 Mad-Libs Style Brick Selection:")
        print("Enter your choices (or press Enter to skip):")
        
        bricks_by_category = self.brick_library.get_bricks_for_workpath(self.current_workpath)
        selected = {}
        
        for category, bricks in bricks_by_category.items():
            brick_names = [brick.name for brick in bricks]
            print(f"\n{category.title()}: {', '.join(brick_names)}")
            
            while True:
                choice = input(f"Choose {category} (or Enter to skip): ").strip().lower()
                if not choice:  # Skip this category
                    break
                elif choice in brick_names:
                    selected[category] = choice
                    print(f"✅ Selected: {choice}")
                    break
                else:
                    print(f"❌ Invalid choice. Options: {', '.join(brick_names)}")
        
        if selected:
            self.add_bricks(**selected)
        
        # Step 4: Content input
        print(f"\n📝 Enter your {self.current_workpath} content:")
        if self.current_workpath == "coding":
            print("Paste your code (type 'END' on new line when finished):")
        else:
            print("Enter your content (type 'END' on new line when finished):")
        
        content_lines = []
        while True:
            try:
                line = input()
                if line.strip() == "END":
                    break
                content_lines.append(line)
            except KeyboardInterrupt:
                break
        
        self.content = "\n".join(content_lines)
        
        # Step 5: Build prompt
        if self.content.strip():
            prompt = self.build_prompt()
            print("\n" + "="*60)
            print("🎯 YOUR OPTIMIZED PROMPT:")
            print("="*60)
            print(prompt)
            print("="*60)
            
            # Step 6: Options
            print("\n🚀 What would you like to do?")
            print("1. Copy to clipboard")
            print("2. Save to file") 
            print("3. Two-pass optimization (PSE mode)")
            print("4. Start over")
            
            return self._handle_post_build_options(prompt)
        
        return None
    
    def build_prompt(self):
        """Build the final prompt using selected bricks"""
        if not self.current_workpath or not self.content:
            return "❌ Missing workpath or content"
        
        # Get the appropriate template
        template = self.template_engine.get_template_for_workpath(self.current_workpath)
        
        # Build modifier text from selected bricks
        modifiers = []
        for category, brick in self.selected_bricks.items():
            modifiers.append(brick.modifier_text)
        
        modifier_text = self._combine_modifiers(modifiers)
        
        # Build the prompt
        prompt = template.format(
            content=self.content,
            modifiers=modifier_text,
            **{category: brick.name for category, brick in self.selected_bricks.items()}
        )
        
        # Record build
        self.build_history.append({
            "workpath": self.current_workpath,
            "bricks": {cat: brick.name for cat, brick in self.selected_bricks.items()},
            "content_length": len(self.content),
            "prompt_length": len(prompt)
        })
        
        return prompt
    
    def two_pass_optimize(self, content=None):
        """Hidden two-pass optimization using PSE"""
        target_content = content or self.content
        if not target_content:
            return "❌ No content provided"
        
        print("🔄 Running two-pass optimization...")
        
        # Pass 1: Basic improvement
        basic_prompt = f"Improve this {self.current_workpath} content:\n\n{target_content}"
        print("📈 Pass 1: Basic improvement...")
        # In real implementation, this would call an AI model
        improved_content = f"[Improved version of: {target_content[:100]}...]"
        
        # Pass 2: PSE enhancement (hidden from user)
        pse_prompt = self.anti_claude.format_for_pse(
            improved_content, 
            f"Anti-Claude provided this basic solution. As a {self.selected_bricks.get('review', 'senior expert')}, "
            f"please create a significantly better version."
        )
        print("🚀 Pass 2: PSE optimization...")
        
        print("✅ Two-pass optimization complete!")
        return pse_prompt
    
    def _combine_modifiers(self, modifiers):
        """Combine multiple brick modifiers into natural language"""
        if not modifiers:
            return ""
        elif len(modifiers) == 1:
            return modifiers[0]
        elif len(modifiers) == 2:
            return f"{modifiers[0]} and {modifiers[1]}"
        else:
            return f"{', '.join(modifiers[:-1])}, and {modifiers[-1]}"
    
    def _handle_post_build_options(self, prompt):
        """Handle user options after prompt generation"""
        while True:
            try:
                choice = input("\nEnter your choice (1-4): ").strip()
                if choice == "1":
                    print("📋 Prompt copied to clipboard! (simulation)")
                    return prompt
                elif choice == "2": 
                    filename = input("Enter filename (default: prompt.txt): ").strip() or "prompt.txt"
                    print(f"💾 Prompt saved to {filename}! (simulation)")
                    return prompt
                elif choice == "3":
                    optimized = self.two_pass_optimize()
                    print("\n" + "="*60)
                    print("🚀 PSE-OPTIMIZED PROMPT:")
                    print("="*60)
                    print(optimized)
                    print("="*60)
                    return optimized
                elif choice == "4":
                    return self.interactive_mode()
                else:
                    print("❌ Invalid choice. Please enter 1-4.")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                return prompt
    
    def reset(self):
        """Reset builder state"""
        self.current_workpath = None
        self.selected_bricks = {}
        self.content = None
        print("🔄 Builder reset")
