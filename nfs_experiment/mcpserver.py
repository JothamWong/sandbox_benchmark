from fastmcp import FastMCP
import subprocess

mcp = FastMCP("Sandbox Benchmark (NAS Edition)")


def run_container_task(service_name):
    """
    Executes the mapped 'agent.py' inside the specified container.
    """
    cmd = ["docker-compose", "exec", "-T", service_name, "python", "/app/agent.py"]

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
    return run_container_task("nfs-browser-agent")


@mcp.tool
def convert_pdf_task() -> str:
    """
    [Code Sandbox] Reads PDF from NFS Mount, converts, writes PPTX to NFS Mount.
    """
    return run_container_task("nfs-code-agent")


@mcp.tool
def verify_pptx_task() -> str:
    """
    [Terminal Sandbox] Reads PPTX from NFS Mount for verification.
    """
    return run_container_task("nfs-terminal-agent")


@mcp.tool
def get_metrics_guide() -> str:
    return "Sum the METRIC_TRANSFER_* lines. These represent 'os.fsync' times over the NFS network."


if __name__ == "__main__":
    mcp.run(transport="sse")
