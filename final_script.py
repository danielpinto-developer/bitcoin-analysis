import subprocess

scripts = [
    "dip_alert.py",
    "bitcoin_analysis.py",
    "top_crypto.py"
]

print("🚀 Running full crypto analysis pipeline...\n")

for script in scripts:
    print(f"▶️ Running {script}...")
    try:
        subprocess.run(["python", script], check=True)
        print(f"✅ Finished {script}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run {script}: {e}\n")

print("🎉 All scripts completed.")
