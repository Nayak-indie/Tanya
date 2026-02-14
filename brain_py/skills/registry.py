# Global registry instance
# _registry = SkillRegistry()
# Register API-based skills here (if any, remove them)
"""API-based skills removed. Only local skills remain."""
class Skill:
    def __init__(self, name, description, authority, handler):
        self.name = name
        self.description = description
        self.authority = authority
        self.handler = handler


class SkillRegistry:
    def __init__(self):
        self.skills = {}

    def register(self, skill: Skill):
        self.skills[skill.name] = skill

    def list_skills(self):
        return list(self.skills.values())

    def get(self, name):
        return self.skills.get(name)


# Global registry instance
_registry = SkillRegistry()


def get_registry():
    return _registry
