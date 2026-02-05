import time
import os

NAS_DIR = "/mnt/nas"
PPTX_FILENAME = "presentation.pptx"


def run():
    print(f"--- [Terminal] Processing Job ---")

    pptx_path = os.path.join(NAS_DIR, PPTX_FILENAME)

    # 1. Transfer In (Read from NAS)
    print(f"Reading from NAS: {pptx_path}...")
    start_read = time.time()

    if not os.path.exists(pptx_path):
        print("Error: Artifact not found on NAS mount.")
        return

    with open(pptx_path, "rb") as f:
        # Read chunks to ensure full network retrieval
        while chunk := f.read(8192):
            pass

    end_read = time.time()

    size = os.path.getsize(pptx_path)
    print(f"SUCCESS: Received Artifact ({size} bytes).")
    print(f"METRIC_TRANSFER_READ: {end_read - start_read:.6f} seconds")


if __name__ == "__main__":
    run()
