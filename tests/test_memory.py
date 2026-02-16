"""
Tests for Tanya's memory core system.
"""
import os
import sys
import tempfile
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_memory_core_basic():
    """Test basic memory remember and recall."""
    # Use temp dir for isolation
    temp_dir = tempfile.mkdtemp()
    try:
        os.environ['TANYA_MEMORY_PATH'] = temp_dir
        from brain_py.memory.memory_core import MemoryCore
        
        memory = MemoryCore()
        
        # Test remember
        memory.remember("test_key", "test_value")
        
        # Test recall
        result = memory.recall("test_key", "default")
        assert result == "test_value", f"Expected 'test_value', got '{result}'"
        
        print("✓ test_memory_core_basic passed")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_memory_core_default():
    """Test recall returns default for missing keys."""
    temp_dir = tempfile.mkdtemp()
    try:
        os.environ['TANYA_MEMORY_PATH'] = temp_dir
        from brain_py.memory.memory_core import MemoryCore
        
        memory = MemoryCore()
        
        result = memory.recall("nonexistent", "default_value")
        assert result == "default_value", f"Expected 'default_value', got '{result}'"
        
        print("✓ test_memory_core_default passed")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def test_memory_core_list():
    """Test storing and retrieving lists."""
    temp_dir = tempfile.mkdtemp()
    try:
        os.environ['TANYA_MEMORY_PATH'] = temp_dir
        from brain_py.memory.memory_core import MemoryCore
        
        memory = MemoryCore()
        
        # Store a list
        test_list = [{"a": 1}, {"b": 2}]
        memory.remember("items", test_list)
        
        # Retrieve it
        result = memory.recall("items", [])
        assert result == test_list, f"Expected {test_list}, got {result}"
        
        print("✓ test_memory_core_list passed")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    test_memory_core_basic()
    test_memory_core_default()
    test_memory_core_list()
    print("\n✅ All memory tests passed!")
