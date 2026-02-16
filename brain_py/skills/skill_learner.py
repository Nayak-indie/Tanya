"""
skill_learner.py
================
Tanya's automatic skill acquisition system.
Learns new capabilities by reading code, docs, and self-writing modules.
"""

import os
import importlib
import inspect
from typing import Optional, Callable, Any
from brain_py.memory.memory_core import MemoryCore


class SkillLearner:
    """
    Autonomous skill acquisition and mastery.
    
    Capabilities:
    - Detect knowledge gaps
    - Fetch code from GitHub/web
    - Write new skill modules
    - Auto-register skills
    - Learn by doing (execute + refine)
    """

    def __init__(self, memory: MemoryCore):
        self.memory = memory
        self.learned_skills = []  # Track what we've learned
        self.failed_attempts = []  # Track failures for debugging

    def detect_gap(self, user_request: str) -> Optional[str]:
        """
        Detect if we lack a skill for this request.
        Returns skill name if gap detected, None otherwise.
        """
        # Simple keyword matching - enhance with embeddings later
        gap_indicators = [
            "can you", "would you", "i wish you could",
            "learn to", "teach yourself", "figure out how"
        ]
        
        request_lower = user_request.lower()
        
        # Check for explicit gap indicators
        for indicator in gap_indicators:
            if indicator in request_lower:
                return self._infer_skill_needed(user_request)
        
        return None

    def _infer_skill_needed(self, request: str) -> str:
        """Infer what skill would fulfill this request."""
        # Map common requests to skill categories
        request_lower = request.lower()
        
        if "file" in request_lower or "folder" in request_lower:
            return "file_manager"
        elif "search" in request_lower or "find" in request_lower:
            return "search"
        elif "web" in request_lower or "fetch" in request_lower or "url" in request_lower:
            return "web_fetch"
        elif "code" in request_lower or "program" in request_lower:
            return "code_runner"
        elif "remember" in request_lower or "remember" in request_lower:
            return "memory"
        
        return "unknown"

    def learn_from_github(self, repo_url: str, file_path: str = None) -> dict:
        """
        Fetch and learn from a GitHub repo.
        
        Args:
            repo_url: e.g., "https://github.com/user/repo"
            file_path: specific file to learn from (optional)
        
        Returns:
            Learning result with code insights
        """
        # This would use web_fetch to get raw code
        # For now, return a placeholder
        
        learnings = self.memory.recall("github_learnings", [])
        learnings.append({
            "repo": repo_url,
            "file": file_path,
            "timestamp": __import__("time").time()
        })
        self.memory.remember("github_learnings", learnings)
        
        return {
            "status": "queued",
            "repo": repo_url,
            "message": f"Queued learning from {repo_url}"
        }

    def write_new_skill(self, skill_name: str, skill_code: str) -> dict:
        """
        Write a new skill module to brain_py/skills/
        
        Args:
            skill_name: name of the skill (e.g., "image_generator")
            skill_code: Python code for the skill
        
        Returns:
            Result of skill creation
        """
        skills_dir = os.path.join(
            os.path.dirname(__file__), 
            "..", "skills", f"{skill_name}.py"
        )
        
        try:
            with open(skills_dir, "w") as f:
                f.write(skill_code)
            
            # Try to import and register
            try:
                module = importlib.import_module(f"brain_py.skills.{skill_name}")
                
                # Track successful learning
                self.learned_skills.append({
                    "name": skill_name,
                    "path": skills_dir,
                    "timestamp": __import__("time").time()
                })
                
                # Log to memory
                learnings = self.memory.recall("skill_learnings", [])
                learnings.append({
                    "skill": skill_name,
                    "status": "learned",
                    "timestamp": __import__("time").time()
                })
                self.memory.remember("skill_learnings", learnings)
                
                return {
                    "status": "success",
                    "skill": skill_name,
                    "path": skills_dir
                }
                
            except Exception as e:
                return {
                    "status": "written_but_failed_import",
                    "skill": skill_name,
                    "error": str(e)
                }
                
        except Exception as e:
            self.failed_attempts.append({
                "skill": skill_name,
                "error": str(e),
                "timestamp": __import__("time").time()
            })
            return {
                "status": "failed",
                "error": str(e)
            }

    def generate_skill_code(self, description: str, ollama_url: str = "http://localhost:11434") -> Optional[str]:
        """
        Use LLM to generate skill code from description.
        
        This is the "mastery" level - Tanya writes her own skills.
        """
        import requests
        
        prompt = f"""Write a Tanya skill module in Python.

Requirements:
- Inherit from base Skill class if available, or be a standalone function
- Include docstring
- Handle errors gracefully
- Return dict with 'status' and 'result' keys

Skill description: {description}

Write only the Python code, no explanations:"""

        try:
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": "llama3.1:8b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            if response.status_code == 200:
                return response.json().get("response", "").strip()
        except Exception as e:
            print(f"[SkillLearner] Code generation failed: {e}")
        
        return None

    def learn_and_register(self, description: str, ollama_url: str = "http://localhost:11434") -> dict:
        """
        Full cycle: detect gap → generate skill → write → register
        """
        # Generate skill code
        code = self.generate_skill_code(description, ollama_url)
        
        if not code:
            return {"status": "failed", "reason": "code_generation_failed"}
        
        # Extract skill name from description
        skill_name = description.lower().replace(" ", "_")[:30]
        
        # Write the skill
        result = self.write_new_skill(skill_name, code)
        
        return result

    def get_learned_skills(self) -> list:
        """Return list of skills Tanya has learned."""
        return self.learned_skills

    def get_knowledge_gaps(self) -> list:
        """Return requests Tanya couldn't fulfill."""
        gaps = self.memory.recall("knowledge_gaps", [])
        return gaps
