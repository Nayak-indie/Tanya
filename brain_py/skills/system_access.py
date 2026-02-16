"""
system_access.py
================
Full system access for Tanya - like Jarvis
Provides file system, process, network, and automation capabilities
"""

import os
import sys
import subprocess
import shutil
import psutil
import json
import time
from pathlib import Path
from typing import Optional, List, Dict, Any


class SystemAccess:
    """
    Full system access capabilities for Tanya.
    This gives Tanya complete control over the system - like Jarvis.
    
    Capabilities:
    - File system operations
    - Process management
    - Network operations
    - System information
    - Automation
    - Application control
    """
    
    def __init__(self, allow_destructive: bool = False):
        self.allow_destructive = allow_destructive
        self.home = str(Path.home())
        self.allowed_dirs = [
            self.home,
            "/tmp",
            os.getcwd()
        ]
    
    # ========== FILE OPERATIONS ==========
    
    def read_file(self, path: str) -> Dict[str, Any]:
        """Read a file's contents."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return {"status": "success", "content": f.read()}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Write content to a file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"status": "success", "path": path}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def list_directory(self, path: str = ".") -> Dict[str, Any]:
        """List directory contents."""
        try:
            items = []
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                stat = os.stat(full_path)
                items.append({
                    "name": item,
                    "type": "dir" if os.path.isdir(full_path) else "file",
                    "size": stat.st_size,
                    "modified": stat.st_mtime
                })
            return {"status": "success", "path": path, "items": items}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def create_directory(self, path: str) -> Dict[str, Any]:
        """Create a directory."""
        try:
            os.makedirs(path, exist_ok=True)
            return {"status": "success", "path": path}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def delete_file(self, path: str) -> Dict[str, Any]:
        """Delete a file (if allowed)."""
        if not self.allow_destructive:
            return {"status": "denied", "message": "Destructive operations disabled"}
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return {"status": "success", "path": path}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def copy_file(self, src: str, dst: str) -> Dict[str, Any]:
        """Copy a file or directory."""
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            return {"status": "success", "from": src, "to": dst}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def move_file(self, src: str, dst: str) -> Dict[str, Any]:
        """Move a file or directory."""
        try:
            shutil.move(src, dst)
            return {"status": "success", "from": src, "to": dst}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def search_files(self, directory: str, pattern: str) -> Dict[str, Any]:
        """Search for files matching a pattern."""
        try:
            matches = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if pattern.lower() in file.lower():
                        matches.append(os.path.join(root, file))
            return {"status": "success", "matches": matches[:50]}  # Limit to 50
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== PROCESS OPERATIONS ==========
    
    def list_processes(self) -> Dict[str, Any]:
        """List running processes."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return {"status": "success", "processes": processes[:100]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def kill_process(self, pid: int) -> Dict[str, Any]:
        """Kill a process by PID."""
        if not self.allow_destructive:
            return {"status": "denied", "message": "Destructive operations disabled"}
        try:
            os.kill(pid, 9)
            return {"status": "success", "pid": pid}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def run_command(self, command: str, shell: bool = True) -> Dict[str, Any]:
        """Run a shell command."""
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=60
            )
            return {
                "status": "success",
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Command timed out"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== SYSTEM INFO ==========
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information."""
        try:
            return {
                "status": "success",
                "platform": sys.platform,
                "python_version": sys.version,
                "cpu_count": os.cpu_count(),
                "memory": {
                    "total": psutil.virtual_memory().total,
                    "available": psutil.virtual_memory().available,
                    "percent": psutil.virtual_memory().percent
                },
                "disk": {
                    "total": psutil.disk_usage('/').total,
                    "used": psutil.disk_usage('/').used,
                    "free": psutil.disk_usage('/').free,
                    "percent": psutil.disk_usage('/').percent
                },
                "uptime": time.time() - psutil.boot_time()
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== NETWORK OPERATIONS ==========
    
    def check_url(self, url: str) -> Dict[str, Any]:
        """Check if a URL is accessible."""
        import requests
        try:
            response = requests.get(url, timeout=10)
            return {
                "status": "success",
                "url": url,
                "status_code": response.status_code,
                "accessible": response.status_code < 400
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def download_file(self, url: str, dest: str) -> Dict[str, Any]:
        """Download a file from URL."""
        import requests
        try:
            response = requests.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            with open(dest, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return {"status": "success", "url": url, "saved_to": dest}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== APPLICATION CONTROL ==========
    
    def open_application(self, app_name: str) -> Dict[str, Any]:
        """Open an application."""
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", "-a", app_name])
            elif sys.platform == "win32":  # Windows
                subprocess.run(["start", app_name], shell=True)
            else:  # Linux
                subprocess.run([app_name])
            return {"status": "success", "app": app_name}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def open_url(self, url: str) -> Dict[str, Any]:
        """Open a URL in default browser."""
        try:
            import webbrowser
            webbrowser.open(url)
            return {"status": "success", "url": url}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    # ========== AUTOMATION ==========
    
    def schedule_task(self, task: str, delay_seconds: int = 0) -> Dict[str, Any]:
        """Schedule a task to run."""
        import threading
        import scheduling
        
        def run_task():
            time.sleep(delay_seconds)
            self.run_command(task)
        
        thread = threading.Thread(target=run_task, daemon=True)
        thread.start()
        
        return {
            "status": "scheduled",
            "task": task,
            "delay": delay_seconds
        }
    
    # ========== CLIPBOARD ==========
    
    def get_clipboard(self) -> Dict[str, Any]:
        """Get clipboard contents."""
        try:
            import pyperclip
            return {"status": "success", "content": pyperclip.paste()}
        except:
            return {"status": "error", "message": "Clipboard access not available"}
    
    def set_clipboard(self, text: str) -> Dict[str, Any]:
        """Set clipboard contents."""
        try:
            import pyperclip
            pyperclip.copy(text)
            return {"status": "success"}
        except:
            return {"status": "error", "message": "Clipboard access not available"}


# Global instance
_system_access = SystemAccess()


def get_system_access() -> SystemAccess:
    """Get the global system access instance."""
    return _system_access
