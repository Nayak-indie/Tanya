def describe_skills(orchestrator):
    skills = orchestrator.skill_registry.list_skills()

    lines = ["I can:"]
    for skill in skills:
        lines.append(f"- {skill.name}: {skill.description}")

    return "\n".join(lines)
