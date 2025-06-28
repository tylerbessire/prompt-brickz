"""
Workpath Manager for v2.0
"""

class WorkpathManager:
    """Manages the three workpaths: coding, conversational, exploratory"""
    
    WORKPATHS = {
        1: "coding",
        2: "conversational", 
        3: "exploratory"
    }
    
    def __init__(self):
        self.current_workpath = None
    
    def select_workpath(self, workpath_input):
        """Select workpath by number or name"""
        if isinstance(workpath_input, int):
            if workpath_input in self.WORKPATHS:
                self.current_workpath = self.WORKPATHS[workpath_input]
                return True
        elif isinstance(workpath_input, str):
            if workpath_input.lower() in self.WORKPATHS.values():
                self.current_workpath = workpath_input.lower()
                return True
        return False
    
    def get_current_workpath(self):
        """Get the currently selected workpath"""
        return self.current_workpath
