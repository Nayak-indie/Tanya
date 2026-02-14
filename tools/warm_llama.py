import time
import os
import sys

model_file = os.path.join(os.getcwd(), "Mistral-7B-Instruct-v0.3-Q4_K_M.gguf")
print("Model path:", model_file)
if not os.path.exists(model_file):
    print("ERROR: model file not found at", model_file)
    sys.exit(2)

try:
    from llama_cpp import Llama
except Exception as e:
    print("ERROR: import llama_cpp failed:", e)
    sys.exit(3)

n_threads = int(os.getenv("LLAMA_N_THREADS", "4"))
device = os.getenv("LLAMA_DEVICE", "cpu")
print(f"Initializing Llama (device={device}, n_threads={n_threads})...")
start = time.time()
try:
    llm = Llama(model_path=model_file, n_threads=n_threads)
except Exception as e:
    print("ERROR: Llama initialization failed:", e)
    sys.exit(4)
init_time = time.time() - start
print(f"Initialization OK (took {init_time:.2f}s)")

prompt = "Say 'warmup complete' and nothing else."
print("Sending prompt to model...")
start = time.time()
try:
    resp = llm.create_completion(prompt=prompt, max_tokens=64, temperature=0.2)
    text = resp.get("choices", [{}])[0].get("text") if isinstance(resp, dict) else str(resp)
except Exception as e:
    print("ERROR: create_completion failed:", e)
    sys.exit(5)
elapsed = time.time() - start
print("Model response (elapsed {:.2f}s):".format(elapsed))
print(text)
print("Warm-up script finished.")
