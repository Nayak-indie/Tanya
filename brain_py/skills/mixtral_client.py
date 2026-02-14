import os
import sys
import json
import requests
import threading
import contextlib


# Context manager to suppress C-level stdout/stderr prints (redirect fds 1 and 2 to devnull)
@contextlib.contextmanager
def _suppress_native_output():
    try:
        devnull = open(os.devnull, 'w')
    except Exception:
        yield
        return
    try:
        # Save original file descriptors
        orig_stdout_fd = sys.stdout.fileno()
        orig_stderr_fd = sys.stderr.fileno()
        saved_stdout = os.dup(orig_stdout_fd)
        saved_stderr = os.dup(orig_stderr_fd)
        os.dup2(devnull.fileno(), orig_stdout_fd)
        os.dup2(devnull.fileno(), orig_stderr_fd)
        try:
            yield
        finally:
            # Restore
            os.dup2(saved_stdout, orig_stdout_fd)
            os.dup2(saved_stderr, orig_stderr_fd)
            os.close(saved_stdout)
            os.close(saved_stderr)
    finally:
        try:
            devnull.close()
        except Exception:
            pass

# Mixtral/Ollama client with optional local GGUF (llama_cpp) support

_last_streamed = False

# Persistent llama instance (initialized lazily)
_llama = None
_llama_lock = threading.Lock()


def _init_llama_if_possible():
    """Background initialization to warm the GGUF model if available."""
    global _llama
    with _llama_lock:
        if _llama is not None:
            return
        try:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            gguf_name = "Mistral-7B-Instruct-v0.3-Q4_K_M.gguf"
            gguf_path = os.path.join(repo_root, gguf_name)
            if not os.path.exists(gguf_path):
                return
            # Import and initialize while suppressing native prints from llama.cpp
            from llama_cpp import Llama
            # allow tuning via environment variables
            n_threads = os.getenv("LLAMA_N_THREADS")
            device = os.getenv("LLAMA_DEVICE")  # optional, e.g., 'cpu' or 'cuda'
            kwargs = {}
            if n_threads:
                try:
                    kwargs["n_threads"] = int(n_threads)
                except Exception:
                    pass
            if device:
                # llama_cpp may accept 'backend' / 'n_gpu_layers' or device hints; pass as-is when supported
                try:
                    kwargs["device"] = device
                except Exception:
                    pass
            with _suppress_native_output():
                _llama = Llama(model_path=gguf_path, **kwargs)
        except Exception:
            # leave _llama as None and let send_message fall back
            _llama = None


# Start background warm-up (best-effort, non-blocking)
try:
    threading.Thread(target=_init_llama_if_possible, daemon=True).start()
except Exception:
    pass


def warmup_now(timeout: float = None) -> bool:
    """Synchronously initialize the persistent Llama instance (blocking up to `timeout` seconds).
    Returns True if initialization succeeded and a Llama instance is available."""
    global _llama
    # Fast-path
    if _llama is not None:
        return True
    # Start a thread and join it (so initialization runs with same code path)
    t = threading.Thread(target=_init_llama_if_possible, daemon=True)
    t.start()
    t.join(timeout)
    return _llama is not None


def _messages_to_prompt(messages):
    # join user messages; keep simple for terminal usage
    return "\n".join([m.get("content", "") for m in messages if m.get("role") == "user"]) or ""


def _try_local_gguf_stream(prompt: str):
    """Attempt local GGUF inference using llama_cpp. Returns (output, streamed_bool).
    Raises an exception if not available or if generation fails.
    """
    global _llama
    # prefer the warmed instance if available
    if _llama is None:
        # attempt to initialize on-demand
        with _llama_lock:
            if _llama is None:
                repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
                gguf_name = "Mistral-7B-Instruct-v0.3-Q4_K_M.gguf"
                gguf_path = os.path.join(repo_root, gguf_name)
                if not os.path.exists(gguf_path):
                    raise FileNotFoundError(f"GGUF model not found at {gguf_path}")
                try:
                    from llama_cpp import Llama
                    with _suppress_native_output():
                        _llama = Llama(model_path=gguf_path)
                except Exception as e:
                    print("[notice] 'llama_cpp' not available or failed to init; falling back to Ollama HTTP streaming.", file=sys.stderr)
                    _llama = None
                    raise
    llama = _llama
    if llama is None:
        raise RuntimeError("Local Llama instance unavailable")

    output = ""
    # Prefer streaming API if available (collect full output, do not print progressively)
    try:
        # use smaller max_tokens to speed up responses
        # suppress native prints during generation
        for chunk in _streaming_create_completion_suppressed(llama, prompt, max_tokens=128):
            try:
                if isinstance(chunk, dict):
                    choices = chunk.get("choices") or []
                    if choices:
                        c = choices[0]
                        text_part = ""
                        if isinstance(c, dict):
                            text_part = c.get("text") or c.get("delta", {}).get("content") or ""
                        if text_part:
                            output += text_part
            except Exception:
                continue
        return output, True
    except TypeError:
        # streaming not supported; fallback to single response
        with _suppress_native_output():
            resp = llama.create_completion(prompt=prompt, max_tokens=128)
        text = ""
        try:
            text = resp["choices"][0].get("text", "")
        except Exception:
            try:
                text = resp["choices"][0]["text"]
            except Exception:
                text = str(resp)
        return text, False


    def _streaming_create_completion_suppressed(llama, prompt: str, max_tokens: int = 128):
        """Helper: wrap llama.create_completion(..., stream=True) while suppressing native output."""
        try:
            with _suppress_native_output():
                for chunk in llama.create_completion(prompt=prompt, max_tokens=max_tokens, stream=True):
                    yield chunk
        except Exception:
            # fallback to direct streaming call without suppression if something goes wrong
            for chunk in llama.create_completion(prompt=prompt, max_tokens=max_tokens, stream=True):
                yield chunk


def send_message(messages):
    """Send chat messages. Tries Ollama HTTP streaming first, then local GGUF via llama_cpp.
    Returns the full output string (may already have been printed progressively).
    """
    global _last_streamed
    user_content = _messages_to_prompt(messages)
    # Build a system-like prompt wrapper to preserve previous behavior
    # Try to load dynamic prompt if available
    try:
        from brain_py.skills.system_prompt_manager import load_system_prompt
        dynamic_prompt = load_system_prompt()
    except Exception:
        dynamic_prompt = ""

    if dynamic_prompt:
        system_prompt = dynamic_prompt
    else:
        # More directive identity-focused system prompt (fewer constraints)
        system_prompt = (
            "You are Tanya — an assistant created by Vinayak (nayak-indie).\n"
            "State your identity clearly when asked: 'I am Tanya, your assistant created by Vinayak.'\n"
            "Be confident, helpful, and concise. Prioritize answering the user's question directly, then offer one concise follow-up or suggestion.\n"
            "When appropriate, reference your ability to inspect files, run local tools, and reason about code or tasks.\n"
            "Do not invent facts; if unsure, state uncertainty and propose a next step to find the answer."
        )

    prompt = system_prompt + "\n" + user_content + "\n" + system_prompt

    # Try Ollama HTTP streaming first (preferred)
    try:
        url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        # shorter timeout to fail fast when server unreachable
        with requests.post(url, json={"model": "tanya", "prompt": prompt, "stream": True, "max_tokens": 128}, stream=True, timeout=10) as resp:
            resp.raise_for_status()
            output = ""
            _last_streamed = False
            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    part = data.get("response") or data.get("token") or ""
                    if part:
                        output += part
                        _last_streamed = True
                except Exception:
                    continue
            return output
    except Exception:
        # fall back to local GGUF via llama_cpp
        try:
            out, streamed = _try_local_gguf_stream(prompt)
            _last_streamed = bool(streamed)
            return out
        except Exception as e:
            return f"[Error: Ollama HTTP failed and local GGUF fallback failed: {e}]"


if __name__ == "__main__":
    import sys
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Hello, Mixtral!"
    messages = [{"role": "user", "content": prompt}]
    print(send_message(messages))
