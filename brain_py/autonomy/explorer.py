# brain_py/autonomy/explorer.py

import random
import os


class CuriosityExplorer:
    def __init__(self, memory):
        self.memory = memory

    def explore(self):
        choices = [
            self._scan_files,
            self._review_recent_activity,
            self._suggest_learning
        ]
        return random.choice(choices)()

    def _scan_files(self):
        files = os.listdir(".")
        return f"I noticed {len(files)} items in your workspace."

    def _review_recent_activity(self):
        return "You've been working intensely. No breaks logged."

    def _suggest_learning(self):
        return "Based on your patterns, learning systems design could help you."
