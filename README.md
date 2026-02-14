# 🤖 Tanya — Tactical Autonomous Neural Yielding Agent Framework

> 🧠 Modular Agent Architecture  
> ⚙️ Local-First Execution  
> 🛡️ Policy-Enforced Autonomy  
> 👨‍💻 Engineered by nayak-indie (Vinayak)

---

# 📌 Overview

**Tanya (Tactical Autonomous Neural Yielding Agent)** is a modular, local-first AI agent framework designed for:

- Structured reasoning
- Layered memory management
- Skill-based execution control
- Safe system interaction
- Semi-autonomous operational loops
- Optional backend performance acceleration

Tanya is **not just a chatbot**.

She is a structured computational agent framework built for controlled autonomy and modular expansion.

---

# 🧭 Philosophy & Design Principles

Tanya is built on the following core directives:

- ✔ Modular > Monolithic
- ✔ Controlled Autonomy > Chaos
- ✔ Structured Reasoning > Prompt Guessing
- ✔ Skill-Validated Execution > Direct System Calls
- ✔ Policy-Governed Behavior > Unbounded Authority
- ✔ Reversible Operations > Destructive Execution

Tanya does **not** claim sentience or consciousness.

When asked who she is, she responds:

> "I am Tanya, an AI agent framework created by nayak-indie."

She operates strictly within defined architectural constraints.

---

# 🏗️ Architecture Overview

## 📂 Project Structure

```bash
brain_py/
│
├── autonomy/
├── cognition/
├── core/
├── dialogue/
├── glue/
├── interface/
├── memory/
├── policies/
├── reasoning/
├── skills/
├── system/
└── vision/

core_rust/
tools/

🧠 Core Components
🔹 Autonomy Layer

Responsible for:

Exploration logic

Curiosity heuristics

Background execution loops

Controlled task polling

🔹 Reasoning Layer

Handles:

Task decomposition

Multi-step planning

Reflection cycles

Output stabilization

Structured problem solving

🔹 Memory System

Includes:

Short-term memory

Working memory

Long-term memory (SQLite-backed)

Persistent state tracking

Context summarization

🔹 Skills Registry

All external actions must pass through skill handlers.

result = skill_registry.execute("file_read", args)


🚫 No raw shell execution
🚫 No unmanaged subprocess calls
🚫 No direct filesystem manipulation

🔹 Policy Enforcement

Acts as a boundary layer between reasoning and execution.

Enforces:

Operational limits

Ethical constraints

Permission gating

Safe execution fallbacks

🔹 Rust Backend (core_rust/)

Optional performance-oriented backend layer.

Provides:

Sandboxed execution

Deterministic utilities

Future concurrency support

Low-level performance acceleration

🧠 Model Strategy

Tanya supports dual inference routing.

1️⃣ Local GGUF Inference (Preferred)

Example model:

Mistral-7B-Instruct-v0.3-Q4_K_M.gguf


Loaded using:

llama-cpp-python

Advantages

Fully offline

Low latency

Direct model control

No external dependency

2️⃣ Ollama Fallback

Used if local GGUF model is unavailable.

Default endpoint:

http://localhost:11434/api/generate


Supports:

HTTP streaming

Local model hosting

Flexible experimentation

🔁 Model Selection Logic
if gguf_exists and llama_cpp_available:
    use_local_model()
else:
    use_ollama()

⚡ Setup
✅ Requirements

Python 3.10+

requests

llama-cpp-python (recommended)

📦 Installation

Using requirements file:

pip install -r requirements.txt


Manual installation:

pip install requests
pip install llama-cpp-python

▶️ Running Tanya
PowerShell Example
$env:LLAMA_N_THREADS = "8"
$env:LLAMA_DEVICE = "cpu"
$env:TANYA_GRANT_FILE_ACCESS = "true"
$env:OLLAMA_URL = "http://localhost:11434/api/generate"

conda activate tanya
python tanya_terminal_chat.py

⚙️ Performance Optimization

Recommended environment variables:

LLAMA_N_THREADS=8
OMP_NUM_THREADS=8
LLAMA_DEVICE=cpu
TANYA_WARM_LLAMA=true


Benchmark model performance:

python tools/benchmark_llama.py


Disable warm-up blocking:

TANYA_WARM_LLAMA=false

🧪 Development Background

Tanya was developed using:

✨ Cursor as development interface

🧠 Manual architectural design

🔧 Custom reasoning pipeline engineering

🛠️ Iterative backend restructuring

🧩 Modular experimentation cycles

The orchestration flow, boundary enforcement, and system architecture were manually designed and refined.

This is not a one-shot auto-generated system.

It is an evolving agent framework under active refinement.

🛡️ Safety Model

Tanya:

❌ Does not overwrite files without explicit skill authorization

❌ Does not execute destructive system commands

❌ Does not escalate privileges

❌ Does not silently self-modify core architecture

✅ Logs structured execution events

✅ Operates within policy-defined limits

Filesystem access path:

brain_py.skills.file_manager


Internet access path:

brain_py.autonomy.explorer

📂 Repository Status

⚠️ Current state:

Partially shuffled directory structure

Contains experimental modules

Includes development artifacts

May contain unnecessary files

May include cache remnants (e.g., HuggingFace cache)

Requires structural cleanup

Requires continued development

This repository is not production-clean yet.

Refactoring and pruning are ongoing.

🔬 Experimental Areas

Semi-autonomous background loops

Structured self-improvement scaffolding

Rust performance bridges

Multi-model routing

Memory abstraction improvements

Backend learning workflows

Breaking changes may occur.

🎯 Vision

Tanya is evolving toward:

Structured agent orchestration

Goal-driven modular execution

Safe autonomous capability expansion

Developer-augmented productivity

Controlled adaptive workflows

Not limitless.
Not uncontrolled.

But engineered autonomy.

👨‍💻 Author

Created and engineered by:

nayak-indie (Vinayak)

⚠️ Disclaimer

This is a personal experimental AI agent framework.

Use caution when enabling:

Filesystem access

Internet access

Background autonomy loops

Elevated execution permissions

Always test in controlled environments.

⭐ Project Status

🟡 Active Development
🧠 Experimental Agent Architecture
⚙️ Modular System Design
🚧 Cleanup & refinement required
and

# Tanya Repo

This repo contains the code and configs for Tanya.

## Download the large model

The Mistral-7B-Instruct GGUF model (~4.1GB) is **too big for GitHub**.  
You can download it by running:

```bash
./download_gguf.sh

Tanya is not just a chatbot.
She is a framework in progress.