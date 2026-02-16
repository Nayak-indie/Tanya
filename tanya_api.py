"""
tanya_api.py
============
Tanya API Server - serves as backend for Streamlit app and other interfaces.
Provides REST API for:
- Chat
- Memory
- Tasks
- System control
- File operations
"""

from flask import Flask, request, jsonify
import os
import sys
import json
import threading
import time
from datetime import datetime

# Add Tanya to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brain_py.memory.memory_core import MemoryCore
from brain_py.interface.orchestrator import Orchestrator
from brain_py.autonomy.background_runner import BackgroundRunner
from brain_py.policies.directive import CoreDirective
from brain_py.skills.system_access import SystemAccess


app = Flask(__name__)

# Initialize Tanya components
memory = MemoryCore()
orchestrator = Orchestrator(memory)
directive = CoreDirective()
system_access = SystemAccess()

# Background runner (for 24/7 learning)
background_runner = None


def init_background():
    """Initialize background learning."""
    global background_runner
    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
    background_runner = BackgroundRunner(
        memory=memory,
        curiosity_interval_minutes=10,
        consolidate_interval_minutes=60,
        ollama_url=ollama_url
    )
    background_runner.start()


# ============== API ROUTES ==============

@app.route('/')
def index():
    return jsonify({
        "name": "Tanya AI",
        "version": "2.0",
        "status": "online",
        "directive": directive.get_identity()
    })


@app.route('/status')
def status():
    """Get Tanya's current status."""
    return jsonify({
        "status": "online",
        "uptime": int(time.time() - directive.activation_time),
        "tasks_completed": directive.tasks_completed,
        "current_task": directive.current_task,
        "directive": directive.get_identity(),
        "background": background_runner.get_status() if background_runner else {},
        "system": system_access.get_system_info() if request.args.get('system') else {}
    })


@app.route('/chat', methods=['POST'])
def chat():
    """Chat with Tanya."""
    data = request.json
    message = data.get('message', '')
    model = data.get('model', 'llama3.1:8b')
    
    # Set current task
    directive.set_task(message)
    
    # Process through orchestrator
    event = type('Event', (), {
        'type': 1,  # USER_INPUT
        'payload': {'text': message}
    })()
    
    result = orchestrator.handle_event(event.type, event.payload)
    response = result.get("result", str(result)) if isinstance(result, dict) else str(result)
    
    # Mark task complete
    directive.complete_task()
    
    return jsonify({
        "response": response,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/memory', methods=['GET', 'POST'])
def memory_ops():
    """Get or set memory."""
    if request.method == 'GET':
        # Get memory contents
        return jsonify({
            "events": memory.recall("events", []),
            "conversations": memory.recall("conversations", []),
            "learnings": memory.recall("curiosity_learnings", []),
            "skills": memory.recall("skill_learnings", [])
        })
    else:
        # Set memory
        data = request.json
        key = data.get('key')
        value = data.get('value')
        if key and value:
            memory.remember(key, value)
            return jsonify({"status": "saved", "key": key})
        return jsonify({"status": "error", "message": "Missing key or value"})


@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    """Manage tasks."""
    if request.method == 'GET':
        return jsonify({
            "current": directive.current_task,
            "completed": directive.tasks_completed,
            "background_tasks": background_runner.get_status() if background_runner else {}
        })
    else:
        data = request.json
        task = data.get('task')
        if task:
            directive.set_task(task)
            return jsonify({"status": "task_set", "task": task})
        return jsonify({"status": "error"})


@app.route('/system', methods=['GET', 'POST'])
def system():
    """System operations."""
    if request.method == 'GET':
        return jsonify(system_access.get_system_info())
    else:
        data = request.json
        action = data.get('action')
        
        if action == 'run_command':
            return jsonify(system_access.run_command(data.get('command', '')))
        elif action == 'list_dir':
            return jsonify(system_access.list_directory(data.get('path', '.')))
        elif action == 'read_file':
            return jsonify(system_access.read_file(data.get('path', '')))
        elif action == 'write_file':
            return jsonify(system_access.write_file(data.get('path', ''), data.get('content', '')))
        elif action == 'search':
            return jsonify(system_access.search_files(data.get('directory', '.'), data.get('pattern', '')))
        else:
            return jsonify({"status": "error", "message": "Unknown action"})


@app.route('/directive')
def get_directive():
    """Get Tanya's core directive."""
    return jsonify(directive.get_status())


@app.route('/learn', methods=['POST'])
def learn():
    """Queue a skill to learn."""
    data = request.json
    description = data.get('description', '')
    
    if background_runner:
        result = background_runner.request_skill_learning(description)
        return jsonify(result)
    
    return jsonify({"status": "error", "message": "Background runner not initialized"})


@app.route('/trigger/curiosity')
def trigger_curiosity():
    """Manually trigger curiosity cycle."""
    if background_runner:
        return jsonify(background_runner.trigger_curiosity())
    return jsonify({"status": "error"})


@app.route('/trigger/consolidate')
def trigger_consolidate():
    """Manually trigger memory consolidation."""
    if background_runner:
        return jsonify(background_runner.trigger_consolidation())
    return jsonify({"status": "error"})


# ============== MAIN ==============

if __name__ == '__main__':
    print("🤖 Starting Tanya API Server...")
    
    # Initialize background learning
    init_background()
    
    port = int(os.getenv('PORT', 8000))
    print(f"📡 Tanya API running on http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
