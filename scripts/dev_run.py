import os
import sys
import time
import subprocess
from datetime import datetime

def get_last_modified_time(root_dir):
    max_mtime = 0
    for root, dirs, files in os.walk(root_dir):
        if any(ignored in root for ignored in ['.git', '__pycache__', 'venv', '.gemini']):
            continue
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(path)
                    if mtime > max_mtime:
                        max_mtime = mtime
                except OSError:
                    pass
    return max_mtime

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    main_script = os.path.join(root_dir, 'main.py')
    
    print(f"--- MediTrack Hot-Reload Started ---")
    print(f"Watching directory: {root_dir}")
    print(f"Press Ctrl+C to stop.\n")

    process = None
    last_mtime = get_last_modified_time(root_dir)

    try:
        while True:
            if process is None:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting application...")
                process = subprocess.Popen([sys.executable, main_script], cwd=root_dir)

            time.sleep(1)
            
            current_mtime = get_last_modified_time(root_dir)
            if current_mtime > last_mtime:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Change detected! Restarting...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                
                process = None
                last_mtime = current_mtime
                
            if process and process.poll() is not None:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Application exited. Waiting for changes...")
                process = None

    except KeyboardInterrupt:
        print("\nStopping watcher...")
        if process:
            process.terminate()

if __name__ == "__main__":
    main()
