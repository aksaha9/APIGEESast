import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--repo-url', required=True)
args = parser.parse_args()

# Invoke Smithy (assuming installed or Dockerized)
subprocess.run(["smithy", "run", "smithy/workflow.yaml", f"--input=repo_url={args.repo_url}"])