# Tanya Core Philosophy Update - Implementation Plan

## Completed Tasks
- [x] Analyze codebase and create plan
- [x] Get user approval for plan
- [x] Create brain_py/memory/memory_core.py with MemoryCore class (JSON file-based, remember/recall/forget)
- [x] Create brain_py/vision/vision_core.py with VisionCore class (webcam sampling, stores in memory)
- [x] Update brain_py/dialogue/conversation.py to use MemoryCore for conversation history and topic inference
- [x] Create brain_py/interface/speech.py for TTS with mood/context reflection
- [x] Update brain_py/interface/voice.py for voice recognition with voiceprint (user-specific)
- [x] Create brain_py/autonomy/curiosity_manager.py for exploration based on memory history
- [x] Create brain_py/automation/designer.py for storing and executing automation templates
- [x] Update brain_py/interface/orchestrator.py to use MemoryCore instead of list
- [x] Update main.py to initialize MemoryCore and pass to components
- [x] Update brain_py/cognition/thoughts.py for inner voice stored in memory
- [x] Create/Update personality module to store traits/rules in memory
- [x] **NEW: Create curiosity_loop.py** - Proactive research when idle
- [x] **NEW: Create skill_learner.py** - Auto-learns new skills
- [x] **NEW: Create consolidator.py** - Memory organization when idle
- [x] **NEW: Create background_runner.py** - 24/7 autonomous operation
- [x] **NEW: Update main.py** - Integrates background learning
- [x] **NEW: Create systemd service** - Run 24/7 as system service

## Pending Tasks
- [ ] Update eyes overlay (if exists) to reflect activity states
- [ ] Integrate vision (requires webcam)
- [ ] Test memory persistence across sessions
- [ ] Test conversation memory continuity
- [ ] Test speech output with modulation
- [ ] Test curiosity-driven autonomy
- [ ] Test automation learning

## 24/7 Active Learning System
### How it works:
1. **Curiosity Loop** - Every 10min idle, researches topics from memory
2. **Consolidation** - Every 60min idle, summarizes & organizes memories
3. **Skill Learning** - Queues & learns new capabilities autonomously
4. **Background Runner** - Manages all loops in background threads

### To run 24/7:
```bash
# Install Ollama models (on your machine)
ollama pull llama3.1:8b

# Run directly
python main.py

# Or as systemd service
sudo cp setup/systemd/tanya.service /etc/systemd/system/
sudo systemctl enable tanya
sudo systemctl start tanya
```

## Followup Steps
- [ ] Test memory persistence across sessions
- [ ] Integrate vision (requires webcam)
- [ ] Test conversation memory continuity
- [ ] Test speech output with modulation
- [ ] Test curiosity-driven autonomy
- [ ] Test automation learning
- [ ] Add more skill templates for auto-learning
