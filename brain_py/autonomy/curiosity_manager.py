from brain_py.memory.memory_core import MemoryCore

class CuriosityManager:
    def __init__(self, memory: MemoryCore):
        self.memory = memory

    def explore(self):
        explored = self.memory.recall("explored_topics", [])
        suggestion = "Review recent files and summarize insights"
        if suggestion not in explored:
            explored.append(suggestion)
            self.memory.remember("explored_topics", explored)
            return suggestion
        return None
