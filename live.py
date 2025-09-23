import subprocess

def run_livetiming():
    process = subprocess.Popen(
        ["python", "console.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    try:
        # Read lines as they come in
        for line in process.stdout:
            if not line:
                continue

            # Pass the line into your parser
            print(f"$#%: {line}")

    except KeyboardInterrupt:
        print("\nStopped manually.")
        process.terminate()

run_livetiming()