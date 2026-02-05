import os
import time
import requests
import sys

PMEM_PATH = os.getenv("PMEM_PATH", "/mnt/pmem0")
PDF_FILENAME = "paper.pdf"
PDF_URL = "https://arxiv.org/pdf/1706.03762.pdf"


def main():
    print(f"--- [Browser Agent] Starting Task ---")

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

    target_path = os.path.join(PMEM_PATH, PDF_FILENAME)
    start_time = time.time()
    with open(target_path, "wb") as f:
        f.write(content)
        f.flush()
        # Ensure it hits the pmem device
        os.fsync(f.fileno())

    duration = time.time() - start_time
    print(f"METRIC_TRANSFER_FSYNC_MS: {duration:.6f}")
    print(f"Task Complete: PDF written to PMEM.")


if __name__ == "__main__":
    main()
