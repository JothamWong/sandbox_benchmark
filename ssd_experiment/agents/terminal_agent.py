import time
import os

PMEM_DIR = os.getenv("SHARED_PATH", "/mnt/shared_ssd")
PPTX_FILENAME = "presentation.pptx"


def run():
    print(f"--- [Terminal] Processing Job ---")

    pptx_path = os.path.join(PMEM_DIR, PPTX_FILENAME)

    # 1. Transfer In (Read from PMEM)
    print(f"Reading from PMEM: {pptx_path}...")
    start_read = time.time()

    if not os.path.exists(pptx_path):
        print("Error: Artifact not found on PMEM mount.")
        return

    with open(pptx_path, "rb") as f:
        while chunk := f.read(8192):
            pass

    end_read = time.time()

    size = os.path.getsize(pptx_path)
    print(f"SUCCESS: Received Artifact ({size} bytes).")
    print(f"METRIC_TRANSFER_READ: {end_read - start_read:.6f} seconds")


if __name__ == "__main__":
    run()
