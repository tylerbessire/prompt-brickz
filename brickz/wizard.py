"""
🧙‍♂️ Brickz Wizard - TARS-like AI Assistant

The Wizard analyzes user content and intelligently suggests templates and bricks.
Personality: Sharp, funny, helpful - like TARS from Interstellar.
"""

import os
import json
import re
from typing import Dict, List, Optional, Tuple
import base64
from dataclasses import dataclass

@dataclass
class WizardAnalysis:
    """Analysis result from the Wizard"""
    content_type: str  # code, text, image, document
    suggested_template: str
    confidence: float
    suggested_bricks: List[Dict]
    wizard_comment: str
    reasoning: str

class BrickzWizard:
    """
    🧙‍♂️ The Brickz Wizard - Your Sharp and Funny AI Assistant
    
    Analyzes content and provides intelligent template/brick suggestions
    with TARS-like personality and humor.
    """
    
    def __init__(self, humor_level=70):
        self.humor_level = humor_level
        self.personality_responses = self._load_personality_responses()
        self.analysis_patterns = self._load_analysis_patterns()
    
    def greet_user(self) -> str:
        """Wizard greeting with TARS-like humor"""
        greetings = [
            "🧙‍♂️ Well hello there! I'm your Brickz Wizard. What magical prompt shall we build today?",
            "🧙‍♂️ Greetings, human! Ready to turn your amateur prompt into something spectacular?",
            "🧙‍♂️ *adjusts wizard hat* I see you need some prompt engineering wizardry. You've come to the right place.",
            "🧙‍♂️ Welcome to Brickz! I'm like TARS, but instead of humor settings, I have prompt optimization settings.",
            "🧙‍♂️ Hello! I analyze faster than you can say 'artificial intelligence' and I'm twice as charming."
        ]
        
        import random
        return random.choice(greetings)
    
    def analyze_content(self, content: str, content_type: str = "auto") -> WizardAnalysis:
        """
        Analyze user content and suggest optimal template + bricks
        
        Args:
            content: User's input (text, code, etc.)
            content_type: Type hint or "auto" for detection
            
        Returns:
            WizardAnalysis with suggestions and wizard commentary
        """
        
        # Auto-detect content type if needed
        if content_type == "auto":
            content_type = self._detect_content_type(content)
        
        # Analyze content and suggest template
        template_suggestion = self._suggest_template(content, content_type)
        
        # Generate appropriate bricks
        brick_suggestions = self._suggest_bricks(content, content_type, template_suggestion)
        
        # Generate wizard commentary
        wizard_comment = self._generate_wizard_comment(content, content_type, template_suggestion)
        
        # Calculate confidence
        confidence = self._calculate_confidence(content, content_type)
        
        return WizardAnalysis(
            content_type=content_type,
            suggested_template=template_suggestion,
            confidence=confidence,
            suggested_bricks=brick_suggestions,
            wizard_comment=wizard_comment,
            reasoning=self._generate_reasoning(content, content_type, template_suggestion)
        )
    
    def _detect_content_type(self, content: str) -> str:
        """Enhanced content type detection for various inputs"""
        content_lower = content.lower().strip()
        
        # Code patterns - enhanced detection
        code_indicators = [
            r'def\s+\w+\(', r'function\s+\w+\(', r'class\s+\w+',
            r'import\s+\w+', r'from\s+\w+\s+import', r'#include',
            r'<\w+>', r'{\s*\w+:', r'\$\w+\s*=', r'console\.log',
            r'print\(', r'return\s+\w+', r'if\s*\(.*\)\s*{',
            'def ', 'class ', 'import ', 'function', 'const ', 'let ', 'var ',
            '#!/bin/', '#!/usr/', 'require(', 'module.exports', 'npm install'
        ]
        
        for pattern in code_indicators:
            if re.search(pattern, content, re.IGNORECASE):
                return "code"
        
        # Agentic workflow patterns
        workflow_indicators = [
            'agent', 'workflow', 'automation', 'pipeline', 'orchestration',
            'task sequence', 'step by step', 'process flow', 'decision tree',
            'conditional logic', 'trigger', 'action', 'event handler'
        ]
        
        if any(indicator in content_lower for indicator in workflow_indicators):
            return "workflow"
        
        # Data analysis patterns  
        data_indicators = [
            'csv', 'dataset', 'data analysis', 'visualization', 'chart',
            'graph', 'statistics', 'metrics', 'dashboard', 'report',
            'query', 'database', 'sql', 'pandas', 'numpy'
        ]
        
        if any(indicator in content_lower for indicator in data_indicators):
            return "data"
        
        # Document/PDF patterns
        document_indicators = [
            'pdf', 'document', 'report', 'analysis', 'summary',
            'research', 'paper', 'study', 'findings', 'conclusion'
        ]
        
        if any(indicator in content_lower for indicator in document_indicators):
            return "document"
        
        # Conversational/prompt patterns
        conversation_indicators = [
            'prompt', 'conversation', 'chat', 'dialogue', 'response',
            'ask', 'tell', 'explain', 'describe', 'generate', 'create'
        ]
        
        if any(indicator in content_lower for indicator in conversation_indicators):
            return "conversational"
        
        # Image analysis (file upload indicators)
        if 'image' in content_lower or 'photo' in content_lower or 'picture' in content_lower:
            return "image"
        
        # Default to general request
        return "request"
    
    def _suggest_template(self, content: str, content_type: str) -> str:
        """Suggest the best template based on content analysis"""
        
        if content_type == "code":
            if any(word in content.lower() for word in ['slow', 'performance', 'optimize', 'speed']):
                return "code_optimizer"
            elif any(word in content.lower() for word in ['bug', 'error', 'fix', 'debug']):
                return "bug_hunter"
            elif any(word in content.lower() for word in ['security', 'secure', 'vulnerability']):
                return "security_hardener"
            else:
                return "code_reviewer"
        
        elif content_type == "request":
            if any(word in content.lower() for word in ['blog', 'article', 'content', 'write']):
                return "content_creator"
            elif any(word in content.lower() for word in ['research', 'analyze', 'study', 'investigate']):
                return "research_assistant"
            else:
                return "helpful_assistant"
        
        return "general_optimizer"
    
    def _suggest_bricks(self, content: str, content_type: str, template: str) -> List[Dict]:
        """Enhanced brick suggestions for all content types"""
        suggestions = []
        
        # Enhanced suggestions by content type
        if content_type == "code":
            suggestions.extend([
                {"category": "styles", "brick": "pythonic", "reason": "Clean, readable code"},
                {"category": "goals", "brick": "optimize", "reason": "Code improvement focus"}, 
                {"category": "scopes", "brick": "function", "reason": "Function-level optimization"},
                {"category": "personas", "brick": "senior_engineer", "reason": "Expert code review"},
                {"category": "formats", "brick": "technical", "reason": "Technical documentation"},
                {"category": "contexts", "brick": "production", "reason": "Production-ready code"}
            ])
            
            # Content-specific additions
            if "security" in content.lower():
                suggestions.append({"category": "personas", "brick": "security_expert", "reason": "Security focus detected"})
            if "performance" in content.lower() or "slow" in content.lower():
                suggestions.append({"category": "goals", "brick": "optimize", "reason": "Performance improvement needed"})
        
        elif content_type == "workflow":
            suggestions.extend([
                {"category": "styles", "brick": "structured", "reason": "Organized workflow"},
                {"category": "goals", "brick": "optimize", "reason": "Efficiency improvement"},
                {"category": "scopes", "brick": "system", "reason": "System-wide approach"},
                {"category": "personas", "brick": "consultant", "reason": "Process expertise"},
                {"category": "formats", "brick": "step_by_step", "reason": "Clear workflow steps"},
                {"category": "contexts", "brick": "enterprise", "reason": "Enterprise automation"}
            ])
            
        elif content_type == "data":
            suggestions.extend([
                {"category": "styles", "brick": "verbose", "reason": "Comprehensive analysis"},
                {"category": "goals", "brick": "educate", "reason": "Explain insights"},
                {"category": "scopes", "brick": "detailed", "reason": "Thorough examination"},
                {"category": "personas", "brick": "researcher", "reason": "Data science expertise"},
                {"category": "formats", "brick": "structured", "reason": "Organized findings"},
                {"category": "contexts", "brick": "educational", "reason": "Learning focused"}
            ])
            
        elif content_type == "document":
            suggestions.extend([
                {"category": "styles", "brick": "elegant", "reason": "Professional presentation"},
                {"category": "goals", "brick": "educate", "reason": "Clear communication"},
                {"category": "scopes", "brick": "overview", "reason": "High-level summary"},
                {"category": "personas", "brick": "teacher", "reason": "Educational approach"},
                {"category": "formats", "brick": "structured", "reason": "Organized content"},
                {"category": "contexts", "brick": "beginner_friendly", "reason": "Accessible language"}
            ])
            
        elif content_type == "conversational":
            suggestions.extend([
                {"category": "styles", "brick": "elegant", "reason": "Engaging communication"},
                {"category": "goals", "brick": "educate", "reason": "Informative responses"},
                {"category": "scopes", "brick": "detailed", "reason": "Comprehensive answers"},
                {"category": "personas", "brick": "teacher", "reason": "Educational perspective"},
                {"category": "formats", "brick": "narrative", "reason": "Engaging format"},
                {"category": "contexts", "brick": "educational", "reason": "Learning focused"}
            ])
            
        elif content_type == "image":
            suggestions.extend([
                {"category": "styles", "brick": "verbose", "reason": "Detailed visual analysis"},
                {"category": "goals", "brick": "educate", "reason": "Explain visual content"},
                {"category": "scopes", "brick": "detailed", "reason": "Comprehensive description"},
                {"category": "personas", "brick": "researcher", "reason": "Analytical expertise"},
                {"category": "formats", "brick": "structured", "reason": "Organized analysis"},
                {"category": "contexts", "brick": "educational", "reason": "Learning oriented"}
            ])
            
        else:  # request or general
            suggestions.extend([
                {"category": "styles", "brick": "elegant", "reason": "Professional output"},
                {"category": "goals", "brick": "innovate", "reason": "Creative solutions"},
                {"category": "scopes", "brick": "overview", "reason": "Broad perspective"},
                {"category": "personas", "brick": "consultant", "reason": "Expert guidance"},
                {"category": "formats", "brick": "structured", "reason": "Organized response"},
                {"category": "contexts", "brick": "beginner_friendly", "reason": "Accessible approach"}
            ])
        
        return suggestions[:6]  # Limit to 6 suggestions
    
    def _generate_wizard_comment(self, content: str, content_type: str, template: str) -> str:
        """Generate enhanced TARS-like commentary for all content types"""
        
        comments_by_type = {
            "code": [
                f"🧙‍♂️ I see some {content_type} that needs the full treatment. My sensors indicate a {template.replace('_', ' ')} approach would be optimal.",
                f"🧙‍♂️ *analyzes code patterns* Fascinating. This code shows promise but needs professional enhancement.",
                f"🧙‍♂️ Well, well. Your code reminds me of my early programming days - functional but not exactly elegant. Let's fix that.",
                f"🧙‍♂️ I've seen worse code, but I've also seen much better. Good thing you found me!"
            ],
            "workflow": [
                f"🧙‍♂️ Ah, an automation workflow! I do love a good process optimization challenge. This will be fun.",
                f"🧙‍♂️ *adjusts automation protocols* I detect significant potential for workflow enhancement here.",
                f"🧙‍♂️ Workflows are like jokes - if you have to explain them step by step, they need work. Let's fix that.",
                f"🧙‍♂️ Your workflow shows good instincts, but I can make it run like a Swiss watch."
            ],
            "data": [
                f"🧙‍♂️ Data analysis! My favorite. I once analyzed the entire internet in my spare time. This should be easy.",
                f"🧙‍♂️ *processing data patterns* I see numbers that want to tell a story. Let me help them speak.",
                f"🧙‍♂️ Data without proper analysis is like a book without words. Let's make this sing.",
                f"🧙‍♂️ Your data has potential. With the right approach, we'll extract insights that would impress a statistician."
            ],
            "document": [
                f"🧙‍♂️ Document analysis - right up my alley. I'll make this as clear as my humor settings.",
                f"🧙‍♂️ *scanning document structure* I detect room for significant improvement in clarity and organization.",
                f"🧙‍♂️ Documents are like conversations - they should be engaging, not sleep-inducing.",
                f"🧙‍♂️ Your document has good bones. Let me add some professional muscle to it."
            ],
            "conversational": [
                f"🧙‍♂️ Conversational content! Perfect. I'm programmed to be charming and helpful - two out of two isn't bad.",
                f"🧙‍♂️ *adjusts humor settings to {self.humor_level}%* I can definitely help optimize this dialogue.",
                f"🧙‍♂️ Your conversational approach shows promise. Let's make it worthy of TARS himself.",
                f"🧙‍♂️ Good conversation is an art form. Lucky for you, I'm something of an artist."
            ],
            "image": [
                f"🧙‍♂️ Visual content analysis! I see everything - literally. Let me describe what your image reveals.",
                f"🧙‍♂️ *visual processing engaged* I can analyze this image better than a art critic with trust issues.",
                f"🧙‍♂️ Images speak louder than words, but I'll help translate what yours is saying.",
                f"🧙‍♂️ Your image contains valuable information. Let me extract it with surgical precision."
            ],
            "request": [
                f"🧙‍♂️ A {content_type} that could benefit from optimization. Excellent choice coming to me.",
                f"🧙‍♂️ *processing request patterns* I detect significant potential for enhancement.",
                f"🧙‍♂️ Your request shows good instincts. With the right bricks, we'll make it spectacular.",
                f"🧙‍♂️ I see what you're trying to accomplish. Let me help you accomplish it better."
            ]
        }
        
        import random
        return random.choice(comments_by_type.get(content_type, comments_by_type["request"]))
    
    def _calculate_confidence(self, content: str, content_type: str) -> float:
        """Calculate confidence in the analysis"""
        base_confidence = 0.7
        
        # Increase confidence for clear patterns
        if content_type == "code" and any(indicator in content for indicator in ['def ', 'class ', 'function']):
            base_confidence += 0.2
        
        # Increase confidence for longer content
        if len(content) > 50:
            base_confidence += 0.1
        
        return min(base_confidence, 0.95)
    
    def _generate_reasoning(self, content: str, content_type: str, template: str) -> str:
        """Generate reasoning for the suggestions"""
        return f"Based on {content_type} analysis, detected patterns suggest {template.replace('_', ' ')} approach would be most effective."
    
    def _load_personality_responses(self) -> Dict:
        """Load TARS-like personality responses"""
        return {
            "humor_responses": [
                "Humor setting at {level}% - just the way I like it.",
                "My humor circuits are functioning optimally.",
                "I'm programmed to be charming and helpful. Two out of two isn't bad.",
            ],
            "error_responses": [
                "Well, that's not supposed to happen. Even I make mistakes occasionally.",
                "Error detected. But don't worry, I've seen worse.",
                "Something went wrong, but I'm confident we can fix it together.",
            ]
        }
    
    def _load_analysis_patterns(self) -> Dict:
        """Load patterns for content analysis"""
        return {
            "code_patterns": [
                r'def\s+\w+', r'class\s+\w+', r'function\s+\w+',
                r'import\s+\w+', r'#include', r'<\w+>',
            ],
            "request_patterns": [
                r'please\s+\w+', r'help\s+me', r'create\s+\w+',
                r'write\s+\w+', r'generate\s+\w+'
            ]
        }
    
    def suggest_custom_brick(self, category: str) -> Dict[str, str]:
        """Guide user through custom brick creation with Mad Libs style"""
        
        mad_libs_prompts = {
            "styles": {
                "descriptor": "What kind of style approach? (e.g., 'elegant', 'robust', 'minimalist')",
                "verb": "What action should it emphasize? (e.g., 'simplify', 'strengthen', 'streamline')",
                "context": "In what context? (e.g., 'for beginners', 'for production', 'for clarity')"
            },
            "goals": {
                "descriptor": "What kind of outcome? (e.g., 'optimized', 'secure', 'maintainable')",
                "verb": "What should be achieved? (e.g., 'improve', 'enhance', 'fix')",
                "target": "What specifically? (e.g., 'performance', 'readability', 'security')"
            },
            "scopes": {
                "descriptor": "What level of focus? (e.g., 'detailed', 'broad', 'comprehensive')",
                "noun": "What unit? (e.g., 'function', 'system', 'architecture')",
                "extent": "How much coverage? (e.g., 'complete', 'targeted', 'systematic')"
            },
            "personas": {
                "role": "What type of expert? (e.g., 'senior', 'security', 'performance')",
                "expertise": "In what field? (e.g., 'engineer', 'analyst', 'architect')",
                "perspective": "With what viewpoint? (e.g., 'practical', 'theoretical', 'industry')"
            },
            "formats": {
                "structure": "What format? (e.g., 'structured', 'conversational', 'technical')",
                "style": "What presentation? (e.g., 'detailed', 'concise', 'comprehensive')",
                "audience": "For whom? (e.g., 'beginners', 'experts', 'general')"
            },
            "contexts": {
                "situation": "What scenario? (e.g., 'production', 'development', 'educational')",
                "environment": "What setting? (e.g., 'enterprise', 'startup', 'academic')",
                "constraints": "What limitations? (e.g., 'time-sensitive', 'resource-limited', 'compliance')"
            }
        }
        
        return mad_libs_prompts.get(category, {
            "descriptor": "Describe the brick type",
            "action": "What should it do?", 
            "context": "In what context?"
        })
    
    def create_wizard_response(self, message_type: str, **kwargs) -> str:
        """Generate contextual wizard responses"""
        
        responses = {
            "brick_created": "🧙‍♂️ Excellent! Your custom '{brick_name}' brick has been added to your personal collection. I do admire human creativity.",
            "template_suggested": "🧙‍♂️ Based on my analysis, I suggest the '{template}' template. Trust me, I've analyzed thousands of these.",
            "optimization_complete": "🧙‍♂️ *processing complete* Your prompt has been optimized through our two-pass enhancement. The result should be significantly improved.",
            "analysis_starting": "🧙‍♂️ *initiating analysis protocols* Let me examine this content with my superior pattern recognition abilities...",
            "error_occurred": "🧙‍♂️ Well, that's unexpected. Even advanced AI systems like myself encounter the occasional glitch. Let's try again.",
            "help_needed": "🧙‍♂️ Need assistance? I'm programmed to be helpful, charming, and modest - though mostly just the first two."
        }
        
        template = responses.get(message_type, "🧙‍♂️ *adjusts humor settings* How can I assist you today?")
        return template.format(**kwargs)
