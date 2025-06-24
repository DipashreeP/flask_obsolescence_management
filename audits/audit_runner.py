import subprocess

def run_audits():
    print("🔍 Running pip-audit...")
    subprocess.run(["pip-audit"], check=True)

    print("🔐 Running safety check...")
    subprocess.run(["safety", "check"], check=True)

if __name__ == "__main__":
    run_audits()
