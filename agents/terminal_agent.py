import time
import os

SHARED_PATH = os.environ["SHARED_PATH"]
PPTX_FILENAME = "presentation.pptx"


def run():
    print(f"--- [Terminal] Processing Job ---")

    pptx_path = os.path.join(SHARED_PATH, PPTX_FILENAME)

    print(f"Reading from mount: {pptx_path}...")
    start_read = time.time()
    if not os.path.exists(pptx_path):
        print("Error: Artifact not found on mount.")
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
