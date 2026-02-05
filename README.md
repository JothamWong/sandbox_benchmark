# Sandbox benchmark experiments

## NFS Experiment

The agent downloads a paper PDF from one sandbox (Docker container), transfers that to another sandbox to convert to pptx, then transfers it to another terminal sandbox for the final conclusion.

The pwd is assumed to be `nfs_experiment`.
Run `docker compose up`.
Run `uv run mcpserver.py`
Then run `uv run main.py`

## PMEM Experiment

First run `setup.sh` script.
The agent downloads a paper PDF from one sandbox (Docker container), writes that PDF file to the mounted /mnt/pmem0 XFS filesystem. The code agent reads it directly from the mounted filesystem and writes the ppt to the filesystem as well. The terminal agent also reads directly.

The pwd is assumed to be `pmem_experiment`.
Run `docker compose up`.
Run `uv run mcpserver.py`
Then run `uv run main.py`