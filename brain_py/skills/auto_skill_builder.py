"""
auto_skill_builder.py
---------------------
Allows Tanya to create new Python modules (skills) dynamically based on user requests.
"""
import os

def create_skill_module(skill_name, code, base_dir="brain_py/skills"):
    """
    Create a new skill module with the given name and code.
    """
    # Sanitize skill name
    safe_name = skill_name.lower().replace(" ", "_").replace("-", "_")
    file_path = os.path.join(base_dir, f"{safe_name}.py")
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    return file_path

# Example usage:
# create_skill_module("web_search", "def search(query):\n    return 'Not implemented yet'\n")
