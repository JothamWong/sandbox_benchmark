import os
import time
import subprocess
from fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("Sandbox Benchmark (PMEM Edition)")

# Configuration for PMEM
PMEM_PATH = os.getenv("PMEM_PATH", "/mnt/pmem0")
DAX_DEVICE = os.getenv("DAX_DEVICE", "/dev/dax0.0")


def run_container_task(service_name, script_path="/app/agent.py"):
    """
    Executes a script inside the specified container.
    """
    cmd = ["docker-compose", "exec", "-T", service_name, "python", script_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"ERROR in {service_name}:\n{e.stderr}"


@mcp.tool
def get_pmem_status() -> str:
    """
    Checks if the PMEM path and DAX device are accessible.
    """
    path_exists = os.path.exists(PMEM_PATH)
    device_exists = os.path.exists(DAX_DEVICE)

    status = (
        f"PMEM Mount Path: {PMEM_PATH} (Exists: {path_exists})\n"
        f"DAX Device: {DAX_DEVICE} (Exists: {device_exists})\n"
        f"Info: Ensure the device is formatted and mounted with -o dax on the host."
    )
    return status


@mcp.tool
def prepare_pmem_transfer(filename: str, size_mb: int) -> str:
    """
    Simulates preparing a file on the PMEM mount for benchmarking.
    """
    file_path = os.path.join(PMEM_PATH, filename)
    try:
        start_time = time.perf_counter()
        # Create a file on the PMEM filesystem with direct I/O simulation
        with open(file_path, "wb", buffering=0) as f:
            f.write(os.urandom(size_mb * 1024 * 1024))
            os.fsync(f.fileno())
        end_time = time.perf_counter()

        duration_ms = (end_time - start_time) * 1000
        return f"File {filename} ({size_mb}MB) ready at {file_path}. Prep time: {duration_ms:.2f}ms"
    except Exception as e:
        return f"Error preparing transfer: {str(e)}"


@mcp.tool
def cleanup_pmem_file(filename: str) -> str:
    """
    Removes a file from the PMEM mount.
    """
    file_path = os.path.join(PMEM_PATH, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return f"Deleted {filename} from PMEM."
    return f"File {filename} not found."


@mcp.tool
def run_pmem_agent_task(agent_type: str) -> str:
    """
    Runs the benchmark task on a specific agent (e.g., 'code-agent', 'terminal-agent').
    """
    return run_container_task(agent_type)


@mcp.tool
def get_pmem_metrics_guide() -> str:
    """
    Provides guidance on interpreting PMEM benchmark metrics.
    """
    return (
        "Focus on the 'os.fsync' and 'read' times. Since PMEM uses DAX, "
        "the latency should be significantly lower than NFS as it bypasses the network stack "
        "and the kernel page cache."
    )


if __name__ == "__main__":
    mcp.run(transport="sse")
