import requests
import time
import os
import sys

SHARED_PATH = os.environ["SHARED_PATH"]
PDF_FILENAME = "paper.pdf"
PDF_URL = "https://arxiv.org/pdf/1706.03762.pdf"


def run():
    print(f"--- [Browser] Processing Job ---")

    if not os.path.isdir(SHARED_PATH):
        print(
            f"CRITICAL ERROR: {SHARED_PATH} is not a directory. The NFS mount probably failed."
        )
        sys.exit(1)

    print(f"Downloading {PDF_URL}...")
    try:
        # Arxiv blocks requests without a User-Agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        resp = requests.get(PDF_URL, headers=headers, timeout=30)
        resp.raise_for_status()
        content = resp.content
        print(f"Downloaded {len(content)} bytes from Web.")

    except Exception as e:
        print(f"Web Download Error: {e}")
        sys.exit(1)

    target_path = os.path.join(SHARED_PATH, PDF_FILENAME)

    print(f"Writing to NAS mount: {target_path}...")
    start = time.time()

    try:
        with open(target_path, "wb") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
    except OSError as e:
        print(f"Write Error: {e}")
        sys.exit(1)
    duration = time.time() - start
    print(f"METRIC_TRANSFER_WRITE: {duration:.6f} seconds")


if __name__ == "__main__":
    run()
