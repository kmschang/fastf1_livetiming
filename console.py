import time

def replay_cache(filename, delay=2):
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  # skip empty lines
                print(line)  # print to console
                time.sleep(delay)  # wait before next line
    except KeyboardInterrupt:
        print("\nReplay stopped manually.")

# Example usage
replay_cache("cache.txt", delay=2)
