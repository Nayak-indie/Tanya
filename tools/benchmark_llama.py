import os
import sys
import time

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
model_file = os.path.join(repo_root, 'Mistral-7B-Instruct-v0.3-Q4_K_M.gguf')
if not os.path.exists(model_file):
    print('ERROR: GGUF model not found at', model_file)
    sys.exit(2)

print('Model file:', model_file)
print('LLAMA_N_THREADS=', os.getenv('LLAMA_N_THREADS', '4'))
print('LLAMA_DEVICE=', os.getenv('LLAMA_DEVICE', 'cpu'))

try:
    from llama_cpp import Llama
except Exception as e:
    print('ERROR: failed to import llama_cpp:', e)
    sys.exit(3)

n_threads = int(os.getenv('LLAMA_N_THREADS', '4'))

prompt = (
    "[INST]\\nYou are a helpful assistant. Summarize the following in one short paragraph:\n" 
    "Text: The quick brown fox jumps over the lazy dog. Repeat in a friendly tone.\\n[/INST]"
)

print('Initializing Llama...')
start = time.time()
llm = Llama(model_path=model_file, n_threads=n_threads)
load_time = time.time() - start
print(f'Initialization time: {load_time:.2f}s')

print('Running generation (max_tokens=128, temperature=0.2)')
start = time.time()
resp = llm.create_completion(prompt=prompt, max_tokens=128, temperature=0.2)
gen_time = time.time() - start
# Try to extract text
text = ''
try:
    text = resp.get('choices', [{}])[0].get('text', '')
except Exception:
    text = str(resp)

num_tokens_out = len(text.split())
print(f'Generation time: {gen_time:.2f}s')
print(f'Output tokens (approx): {num_tokens_out}')
if gen_time > 0:
    print(f'Tokens/sec (approx): {num_tokens_out / gen_time:.2f}')
print('\n--- Model output ---')
print(text)
print('--- end output ---')
