import os
import subprocess
import sys

def setup():
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    if os.name == "nt":
        pip_cmd = os.path.join("venv", "Scripts", "pip")
    else:
        pip_cmd = os.path.join("venv", "bin", "pip")
        
    subprocess.run([pip_cmd, "install", "-r", "requirements.txt"])

if __name__ == "__main__":
    setup()