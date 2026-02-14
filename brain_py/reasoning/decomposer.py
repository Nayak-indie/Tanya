"""
decomposer.py
--------------
Breaks complex tasks into smaller steps.
"""

class Decomposer:
    """
    Break down a proposal into actionable steps.
    Currently a pass-through since proposals from Planner are already single actionable steps.
    """

    def break_down(self, proposal: dict) -> dict:
        """
        Receives a proposal dict and returns it as a single actionable step.
        For now, proposals are already well-formed for dispatch.
        Future: decompose complex multi-step proposals into substeps.
        """
        return proposal
