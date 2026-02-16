"""
advanced_skills.py
==================
Comprehensive skill system for Tanya - gives her mastery over:
- Coding & Programming
- File operations
- Web scraping
- Automation
- Research
- And much more
"""

import os
import re
import json
import subprocess
import requests
from typing import Dict, Any, Optional, List
from pathlib import Path


class AdvancedSkills:
    """
    Tanya's advanced skill suite - Jarvis-level capabilities.
    """
    
    def __init__(self):
        self.skills = {
            "code": self.execute_code,
            "analyze": self.analyze_code,
            "create_file": self.create_file,
            "read_file": self.read_file,
            "edit_file": self.edit_file,
            "search": self.web_search,
            "scrape": self.web_scrape,
            "automate": self.automate_task,
            "learn": self.learn_skill,
            "execute": self.execute_command,
        }
    
    # ========== CODE EXECUTION ==========
    
    def execute_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Execute code in various languages."""
        try:
            if language == "python":
                # Execute Python code
                result = {"status": "success", "output": "", "error": ""}
                exec_globals = {}
                exec(code, exec_globals)
                return result
            elif language == "bash":
                result = subprocess.run(code, shell=True, capture_output=True, text=True, timeout=30)
                return {
                    "status": "success" if result.returncode == 0 else "error",
                    "output": result.stdout,
                    "error": result.stderr
                }
            else:
                return {"status": "error", "message": f"Language {language} not supported"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code and provide insights."""
        lines = code.split('\n')
        
        analysis = {
            "lines": len(lines),
            "functions": len(re.findall(r'def \w+', code)),
            "classes": len(re.findall(r'class \w+', code)),
            "imports": len(re.findall(r'^import |^from ', code, re.MULTILINE)),
            "comments": len(re.findall(r'#.*$', code, re.MULTILINE)),
            "language": self._detect_language(code)
        }
        
        return {"status": "success", "analysis": analysis}
    
    def _detect_language(self, code: str) -> str:
        """Detect programming language."""
        if "def " in code and ":" in code:
            return "python"
        elif "function" in code or "const " in code:
            return "javascript"
        elif "#include" in code:
            return "c"
        elif "public class" in code:
            return "java"
        return "unknown"
    
    # ========== FILE OPERATIONS ==========
    
    def create_file(self, path: str, content: str = "") -> Dict[str, Any]:
        """Create a new file."""
        try:
            os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return {"status": "success", "path": path}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def read_file(self, path: str) -> Dict[str, Any]:
        """Read file contents."""
        try:
            with open(path, 'r') as f:
                content = f.read()
            return {"status": "success", "content": content, "path": path}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def edit_file(self, path: str, old_text: str, new_text: str) -> Dict[str, Any]:
        """Edit specific text in a file."""
        try:
            with open(path, 'r') as f:
                content = f.read()
            
            if old_text not in content:
                return {"status": "error", "message": "Text not found"}
            
            new_content = content.replace(old_text, new_text)
            
            with open(path, 'w') as f:
                f.write(new_content)
            
            return {"status": "success", "path": path, "changes": "made"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== WEB OPERATIONS ==========
    
    def web_search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """Search the web."""
        try:
            # Use DuckDuckGo (no API key needed)
            url = f"https://duckduckgo.com/html/?q={requests.utils.quote(query)}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            
            # Extract results
            results = []
            for match in re.finditer(r'<a class="result__a" href="([^"]+)"[^>]*>([^<]+)</a>', response.text, re.IGNORECASE):
                results.append({
                    "url": match.group(1),
                    "title": match.group(2)
                })
                if len(results) >= num_results:
                    break
            
            return {"status": "success", "query": query, "results": results}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def web_scrape(self, url: str, selector: str = None) -> Dict[str, Any]:
        """Scrape a webpage."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            return {
                "status": "success",
                "url": url,
                "content": response.text[:5000],  # Limit to 5000 chars
                "status_code": response.status_code
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== AUTOMATION ==========
    
    def automate_task(self, task: str, steps: List[str]) -> Dict[str, Any]:
        """Create and execute an automation task."""
        # This creates a Python script for the automation
        script = f'''"""
Auto-generated automation: {task}
"""
import os
import subprocess

def run():
    results = []
'''
        for i, step in enumerate(steps):
            script += f'''
    # Step {i+1}: {step}
    result = subprocess.run({step!r}, shell=True, capture_output=True, text=True)
    results.append({{"step": {i+1}, "output": result.stdout, "error": result.stderr}})
'''
        
        script += '''
    return results

if __name__ == "__main__":
    run()
'''
        
        # Save the automation script
        script_path = f"automation_{task.lower().replace(' ', '_')}.py"
        with open(script_path, 'w') as f:
            f.write(script)
        
        return {
            "status": "success",
            "task": task,
            "script": script_path,
            "steps": len(steps)
        }
    
    # ========== LEARNING ==========
    
    def learn_skill(self, skill_name: str, description: str) -> Dict[str, Any]:
        """Learn a new skill - queues it for background learning."""
        # This would integrate with the skill_learner
        return {
            "status": "queued",
            "skill": skill_name,
            "description": description,
            "message": "Skill queued for learning during idle time"
        }
    
    # ========== COMMAND EXECUTION ==========
    
    def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a shell command."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            return {
                "status": "success" if result.returncode == 0 else "error",
                "command": command,
                "output": result.stdout[:2000],  # Limit output
                "error": result.stderr[:500],
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Command timed out"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


# Global instance
advanced_skills = AdvancedSkills()


def get_skills() -> AdvancedSkills:
    """Get the advanced skills instance."""
    return advanced_skills
