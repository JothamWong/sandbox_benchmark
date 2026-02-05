import os
import time
import subprocess
from fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("Sandbox Benchmark (PMEM Edition)")

# Configuration for PMEM
PMEM_PATH = os.getenv("PMEM_PATH", "/mnt/pmem0")


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
def download_pdf_task() -> str:
    """
    [Browser Sandbox] Downloads PDF and writes it to the NFS Mount (/mnt/nas).
    """
    return run_container_task("browser-agent")


@mcp.tool
def convert_pdf_task() -> str:
    """
    [Code Sandbox] Reads PDF from NFS Mount, converts, writes PPTX to NFS Mount.
    """
    return run_container_task("code-agent")


@mcp.tool
def verify_pptx_task() -> str:
    """
    [Terminal Sandbox] Reads PPTX from NFS Mount for verification.
    """
    return run_container_task("terminal-agent")


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
