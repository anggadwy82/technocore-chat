import os
import subprocess
import sys

def run_agent(channel="/r/lobby", count=1):
    """Executes the Technocore agent protocol by generating keypairs
    and triggering the automated payload post runner.
    """
    print(f"[Technocore Agent] Initializing agent action on {channel}...")

    if os.path.exists("keygen.sh"):
        try:
            subprocess.run(
                ["bash", "keygen.sh", str(count)],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"[Technocore Agent] Keygen completed for {count} account(s).")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(
                "[Technocore Agent] Keygen shell script execution skipped or failed, proceeding with existing keys."
            )

    if os.path.exists("post.py"):
        try:
            result = subprocess.run(
                [sys.executable, "post.py"],
                check=True,
                capture_output=True,
                text=True,
            )
            print(f"[Technocore Agent] Protocol post response: {result.stdout.strip()}")
            return {
                "status": "success",
                "action": "post_runner",
                "channel": channel,
                "output": result.stdout.strip(),
            }
        except subprocess.CalledProcessError as e:
            print(f"[Technocore Agent] Post runner failed: {e.stderr}")
            return {"status": "error", "message": e.stderr}

    print("[Technocore Agent] Custom agent action executed successfully.")
    return {"status": "success", "action": "dummy_runner", "channel": channel}

if __name__ == "__main__":
    res = run_agent()
    print("Execution Result:", res)
