import os
import subprocess
import time
import sys

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
script = os.path.join(repo_root, 'tanya_terminal_chat.py')
if not os.path.exists(script):
    print('ERROR: tanya_terminal_chat.py not found at', script)
    sys.exit(2)

env = os.environ.copy()
env.setdefault('LLAMA_N_THREADS', '8')
env.setdefault('LLAMA_DEVICE', 'cpu')
env.setdefault('TANYA_GRANT_FILE_ACCESS', 'true')
env.setdefault('OLLAMA_URL', 'http://localhost:11434/api/generate')

cmd = [sys.executable, script]
print('Running:', ' '.join(cmd))
print('Env LLAMA_N_THREADS=', env['LLAMA_N_THREADS'], 'LLAMA_DEVICE=', env['LLAMA_DEVICE'])
input_text = 'Hello Tanya\nexit\n'
start = time.time()
try:
    proc = subprocess.run(cmd, input=input_text.encode('utf-8'), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, timeout=180)
except subprocess.TimeoutExpired:
    print('ERROR: process timed out')
    sys.exit(3)
elapsed = time.time() - start
print('\n--- Process stdout ---')
print(proc.stdout.decode('utf-8', errors='replace'))
print('--- Process stderr ---')
print(proc.stderr.decode('utf-8', errors='replace'))
print(f'Elapsed wall time: {elapsed:.2f}s')
