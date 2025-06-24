import sys
import os
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_audits():
    print("🔍 Running pip-audit...")
    try:
        result = subprocess.run(["pip-audit"], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running pip-audit:")
        print(e.stdout)
        print(e.stderr)

    print("🔐 Running safety check...")
    try:
        result = subprocess.run(["safety", "check"], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running safety check:")
        print(e.stdout)
        print(e.stderr)

if __name__ == "__main__":
    run_audits()
