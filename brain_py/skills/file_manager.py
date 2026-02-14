"""
file_manager.py
---------------
Skill for file operations: create, read, write files.
"""

import os


class FileManager:
    """
    Skills to manage files: create, read, write.
    """


    def create_file(self, path: str, content: str = ""):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File created: {path}"

    def edit_file(self, path: str, content: str):
        if not os.path.exists(path):
            return f"File not found: {path}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File edited: {path}"

    def delete_file(self, path: str):
        if not os.path.exists(path):
            return f"File not found: {path}"
        os.remove(path)
        return f"File deleted: {path}"

    def list_files(self, directory: str):
        if not os.path.exists(directory):
            return f"Directory not found: {directory}"
        return os.listdir(directory)

    def read_file(self, path: str):
        if not os.path.exists(path):
            return f"File not found: {path}"
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def append_file(self, path: str, content: str):
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return f"Content appended to: {path}"

