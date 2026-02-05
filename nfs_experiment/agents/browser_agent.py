import requests
import time
import os
import sys

# NAS Path (Standard File System)
NAS_DIR = "/mnt/nas"
PDF_FILENAME = "paper.pdf"
PDF_URL = "https://arxiv.org/pdf/1706.03762.pdf"


def run():
    print(f"--- [Browser] Processing Job ---")

    # Pre-flight check: Is the NAS accessible?
    if not os.path.isdir(NAS_DIR):
        print(
            f"CRITICAL ERROR: {NAS_DIR} is not a directory. The NFS mount probably failed."
        )
        sys.exit(1)

    # 1. Processing (Download from Web)
    print(f"Downloading {PDF_URL}...")
    try:
        # FIX: Arxiv blocks requests without a User-Agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        resp = requests.get(PDF_URL, headers=headers, timeout=30)
        resp.raise_for_status()
        content = resp.content
        print(f"Downloaded {len(content)} bytes from Web.")

    except Exception as e:
        print(f"Web Download Error: {e}")
        print(
            "Note: If Arxiv is blocking, check your internet connection or the User-Agent."
        )
        sys.exit(1)

    # 2. Transfer (Write to NAS)
    target_path = os.path.join(NAS_DIR, PDF_FILENAME)

    print(f"Writing to NAS mount: {target_path}...")
    start = time.time()

    try:
        with open(target_path, "wb") as f:
            f.write(content)
            f.flush()  # Flush Python buffer
            os.fsync(f.fileno())  # Force Kernel -> Network -> NAS flush
    except OSError as e:
        print(f"NAS Write Error: {e}")
        print(
            "Hint: This usually means permissions on the NFS share are incorrect or the mount is read-only."
        )
        sys.exit(1)

    duration = time.time() - start

    print(f"SUCCESS: Written to NAS File System.")
    print(f"METRIC_TRANSFER_WRITE: {duration:.6f} seconds")


if __name__ == "__main__":
    run()
