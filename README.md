Tanya — Local AI Agent
======================

Summary
-------
Tanya is a local, extensible AI agent framework customized for an individual developer (Vinayak). It runs local models (GGUF/llama_cpp) when available and falls back to an HTTP-based local server (Ollama) for generation. The project is under active development.

Quick run
---------
1. Ensure Python 3.10+ and a suitable environment is active (e.g., conda `tanya`).
2. If you have the GGUF model file `Mistral-7B-Instruct-v0.3-Q4_K_M.gguf` in the repo root, the code can use `llama-cpp-python` for local inference. Otherwise, run a local Ollama server and set `OLLAMA_URL` if different from the default.

Example:

PowerShell:

$env:OLLAMA_URL = "http://localhost:11434/api/generate"
& C:/Users/Vinayak/miniconda3/envs/tanya/python.exe c:/Users/Vinayak/Documents/Projects/Tanya/tanya_terminal_chat.py

Requirements (suggested)
------------------------
- python>=3.10
- requests
- llama-cpp-python (optional — required for GGUF/llama_cpp local inference)

You can install via:

pip install -r requirements.txt

or individually:

pip install requests
pip install "llama-cpp-python"  # optional for GGUF local model

Quick tips for low-latency local inference:

- Place `Mistral-7B-Instruct-v0.3-Q4_K_M.gguf` in the repository root.
- Install `llama-cpp-python` (pip install "llama-cpp-python").
- Configure environment variables before running Tanya:
  - `LLAMA_N_THREADS`: integer number of host threads for inference (e.g., 8).
  - `LLAMA_DEVICE`: optional device hint (e.g., `cpu` or `cuda`).
  - `TANYA_GRANT_FILE_ACCESS=true`: allows Tanya to list/read files when asked.

  Performance tips and quick commands

  - Warm the model at startup to avoid long first-response latency (Tanya supports a blocking warm-up via `mixtral_client.warmup_now`).
  - Environment recommendations:
    - `LLAMA_N_THREADS=8` for an 8-core CPU. Also set `OMP_NUM_THREADS` to the same value.
    - `LLAMA_DEVICE=cpu` (or `cuda` if you have GPU + proper build/runtime).

  Quick benchmark (from repo root):

  ```bash
  # activate your conda env (tanya)
  conda activate tanya
  python tools/benchmark_llama.py
  ```

  If you want Tanya to warm the model automatically on CLI startup, set (default true):

  ```bash
  export TANYA_WARM_LLAMA=true
  python tanya_terminal_chat.py
  ```

  To skip blocking warm-up and initialize lazily, set:

  ```bash
  export TANYA_WARM_LLAMA=false
  ```

Example (PowerShell):

```powershell
$env:LLAMA_N_THREADS = "8"
$env:LLAMA_DEVICE = "cpu"
$env:TANYA_GRANT_FILE_ACCESS = "true"
$env:OLLAMA_URL = "http://localhost:11434/api/generate"
pip install -r requirements.txt
& C:/Users/Vinayak/miniconda3/envs/tanya/python.exe c:/Users/Vinayak/Documents/Projects/Tanya/tanya_terminal_chat.py
```

Project layout (high level)
---------------------------
- brain_py/: Core agent code (reasoning, skills, memory, interface)
  - autonomy/: autonomy loop and managers
  - cognition/: thought utilities
  - core/: registries
  - dialogue/: conversation/orchestration
  - interface/: CLI/orchestrator/voice/override
  - memory/: stores and SQLite helpers
  - policies/: ethics/limits/personality
  - reasoning/: planner, decomposition, reflection
  - skills/: agent skills (local model clients, file manager, retrain helper)
  - system/: boot and events/logging
- hf_model/: (optional) Hugging Face model cache / artifacts
- Modelfile: Docker-like reference pointing at local GGUF
- Mistral-7B-Instruct-v0.3-Q4_K_M.gguf: (expected) GGUF model file (not included)
- tanya_terminal_chat.py: simple terminal chat UI (non-blocking, streams responses)
- tanya_chat_history.json, tanya_memory.json, tanya_user_model.json: persisted state files

How the client chooses the model
-------------------------------
1. If `Mistral-7B-Instruct-v0.3-Q4_K_M.gguf` exists in the repository root and `llama_cpp` is installed, the client will load it via `llama_cpp.Llama` and stream output to the terminal.
2. If local GGUF is unavailable or `llama_cpp` import fails, the client falls back to streaming HTTP calls to a local Ollama endpoint (`OLLAMA_URL`, default: `http://localhost:11434/api/generate`).

Notes & Development Status
--------------------------
- The project is actively under development. Many components are experimental (self-improvement, retraining, file-system skills).
- Expect frequent changes; follow the repo history when upgrading or changing model files.
- If you want, I can add a `requirements.txt` and a short run script to simplify getting started.

License / Safety
-----------------
- This is personal / experimental code. Be cautious about giving it access to the internet or critical file paths.

Last note
---------
The project is still under development and may contain incomplete features and rough edges. Contributions and iterative improvements are expected.
