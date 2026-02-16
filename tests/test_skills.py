"""
Tests for Tanya's skill system.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MockOrchestrator:
    """Mock orchestrator for testing skills."""
    def __init__(self):
        self.memory = MockMemory()


class MockMemory:
    """Mock memory for testing."""
    def __init__(self):
        self.data = {}
    
    def remember(self, key, value):
        self.data[key] = value
    
    def recall(self, key, default=None):
        return self.data.get(key, default)


def test_skill_store_greet():
    """Test the greet skill."""
    from brain_py.skills.skills import SkillStore
    
    store = SkillStore()
    orchestrator = MockOrchestrator()
    
    result = store.execute(orchestrator, "greet", {"name": "TestUser"})
    
    assert result["status"] == "done"
    assert "TestUser" in result["result"]
    
    print("✓ test_skill_store_greet passed")


def test_skill_store_echo():
    """Test the echo skill."""
    from brain_py.skills.skills import SkillStore
    
    store = SkillStore()
    orchestrator = MockOrchestrator()
    
    result = store.execute(orchestrator, "echo", {"text": "Hello World"})
    
    assert result["status"] == "done"
    assert "Hello World" in result["result"]
    
    print("✓ test_skill_store_echo passed")


def test_skill_store_unknown():
    """Test unknown skill returns error."""
    from brain_py.skills.skills import SkillStore
    
    store = SkillStore()
    orchestrator = MockOrchestrator()
    
    result = store.execute(orchestrator, "nonexistent_skill", {})
    
    assert result["status"] == "fail"
    assert "No skill found" in result["result"]
    
    print("✓ test_skill_store_unknown passed")


def test_skill_store_file_operations():
    """Test file operation skills."""
    from brain_py.skills.skills import SkillStore
    
    store = SkillStore()
    orchestrator = MockOrchestrator()
    
    # Test file.list
    result = store.execute(orchestrator, "file.list", {"directory": "."})
    assert result["status"] == "done"
    
    print("✓ test_skill_store_file_operations passed")


if __name__ == "__main__":
    test_skill_store_greet()
    test_skill_store_echo()
    test_skill_store_unknown()
    test_skill_store_file_operations()
    print("\n✅ All skill tests passed!")
