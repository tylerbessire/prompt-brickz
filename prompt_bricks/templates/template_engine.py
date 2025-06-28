"""
Template Engine for Mad-Libs style prompt generation
"""

class TemplateEngine:
    """Generates templates for different workpaths with Mad-Libs placeholders"""
    
    def __init__(self):
        self.templates = {
            "coding": """Analyze and improve this code {modifiers}.

Current code:
{content}

Please provide an enhanced version that demonstrates:
- Superior {style} implementation
- Achievement of the {goal} objective
- Proper {scope}-level optimization
- Professional {review}-quality standards

Focus on creating production-ready code that significantly improves upon the original.""",

            "conversational": """Please help with this request {modifiers}.

Request:
{content}

Provide a response that is:
- Written {style}
- Achieves the goal of {goal}
- Appropriate for {scope} context
- Meets {review} quality standards""",

            "exploratory": """Conduct a thorough investigation {modifiers}.

Research topic:
{content}

Please provide:
- {approach} analysis
- Multiple {perspective} viewpoints  
- {depth} level of investigation
- {evidence} supporting information"""
        }
    
    def get_template_for_workpath(self, workpath):
        """Get the template for a specific workpath"""
        return self.templates.get(workpath, self.templates["coding"])
    
    def preview_template(self, workpath, sample_bricks=None):
        """Preview a template with sample brick values"""
        template = self.get_template_for_workpath(workpath)
        
        if sample_bricks:
            try:
                return template.format(**sample_bricks, content="[Your content here]", modifiers="[Your selected modifiers]")
            except KeyError as e:
                return f"Template preview error: Missing {e}"
        
        return template
