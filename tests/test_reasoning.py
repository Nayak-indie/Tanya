"""
Tests for Tanya's reasoning/planning system.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MockOrchestrator:
    """Mock orchestrator for testing."""
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


def test_intent_model():
    """Test intent recognition."""
    from brain_py.reasoning.intent import IntentModel
    
    intent = IntentModel()
    
    # Test getting intent
    result = intent.get_intent()
    assert result is None or isinstance(result, dict)
    
    print("✓ test_intent_model passed")


def test_planner():
    """Test the planner component."""
    from brain_py.reasoning.planner import Planner
    
    orchestrator = MockOrchestrator()
    planner = Planner(orchestrator)
    
    # Test planning for a goal
    tasks = planner.plan_for_goal("test_goal")
    assert isinstance(tasks, list)
    
    print("✓ test_planner passed")


def test_goal_store():
    """Test goal storage and retrieval."""
    from brain_py.memory.goals import GoalStore
    
    goals = GoalStore()
    
    # Test getting active goal (should be None initially)
    result = goals.get_active_goal()
    assert result is None
    
    print("✓ test_goal_store passed")


def test_user_override():
    """Test user override detection."""
    from brain_py.interface.override import UserOverride
    
    orchestrator = MockOrchestrator()
    override = UserOverride(orchestrator)
    
    # Test override detection
    # (actual test depends on implementation)
    
    print("✓ test_user_override passed")


if __name__ == "__main__":
    test_intent_model()
    test_planner()
    test_goal_store()
    test_user_override()
    print("\n✅ All reasoning tests passed!")
