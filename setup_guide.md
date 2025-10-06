# Setup Guide for APIGEESast

This guide provides steps to set up and run the framework locally or in your organization. It assumes access to a GitHub repo with an Apigee bundle (e.g., /apiproxy folder).

## Prerequisites
- Python 3.8+ installed.
- Docker for containerized tools.
- Node.js not required (handled via Docker).
- Checkmarx account/API token (set as env: `export CX_TOKEN=your_token`).
- Git installed.

## Step 0: Build Docker Images (Prep Step)
Build the apigeelint image once:
```bash
docker build -t apigeelint:latest -f apigeelint/Dockerfile apigeelint/

This installs apigeelint in a container, avoiding global npm installs.

## Step 1: Clone the Repo
Clone the APIGEESast repository to your local machine:

```bash
git clone https://github.com/aksaha9/APIGEESast.git
cd APIGEESast

## Step 2: Install Dependencies
Install Smithy Security for workflow orchestration: pip install smithy-security (or use the Dockerized version if preferred).
For Checkmarx: Download the CxCLI from the Checkmarx portal and add it to your system PATH for Java scanning capabilities.

## Step 3:Configure Environment
Create a .env file in the repo root:

```text
CX_TOKEN=your_checkmarx_token

## Step 4: Run Locally
Execute the framework locally to test with a sample Apigee bundle:

```bash
python orchestrate.py --repo-url https://github.com/example/apigee-bundle.git

This command triggers the Smithy workflow, cloning the repo, running apigeelint, optionally scanning Java code with Checkmarx, and generating a unified SARIF report in /workspace/unified.sarif. Adjust the repo-url to point to your target Apigee bundle repository.

## Step 5: Integrate into CI/CD
ncorporate APIGEESast into your CI/CD pipeline for automated SAST. Examples are provided below:

GitHub Actions (ci-examples/github_workflow.yaml):

```yaml
name: Apigee SAST
on: [push]
jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - run: docker build -t apigeelint:latest -f apigeelint/Dockerfile apigeelint/
    - run: python orchestrate.py --repo-url ${{ github.repositoryUrl }}
    - uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: unified.sarif

Jenkins: Add the following shell steps in your pipeline:

```bash
docker build -t apigeelint:latest -f apigeelint/Dockerfile apigeelint/
python orchestrate.py --repo-url $REPO_URL

Define REPO_URL as a parameter in your Jenkins job.

GitLab CI: Use a .gitlab-ci.yml file with a similar structure, including a before_script for the Docker build:


```yaml

stages:
  - sast
sast_job:
  stage: sast
  before_script:
    - docker build -t apigeelint:latest -f apigeelint/Dockerfile apigeelint/
  script:
    - python orchestrate.py --repo-url $CI_PROJECT_URL
  artifacts:
    paths:
      - unified.sarif

## Step 6: Customize

Tailor the framework to your needs:

Add Thresholds: Modify smithy/aggregate_sarif.py to implement severity-based gating (e.g., fail on high-severity issues).
Replace Checkmarx: Update checkmarx/run_cx_scan.sh to use an alternative tool like Snyk by adjusting the scan command.
Test with Sample Repo: Clone a public Apigee example repository (e.g., from Apigee’s GitHub) and run the framework to validate the setup.

# Troubleshooting

No Java Detected: The workflow skips the Checkmarx scan automatically if no Java files are found in /resources/java.
Errors: Check logs in /workspace. Ensure the apigeelint Docker image is built successfully.
SARIF Conversion: If apigeelint JSON output varies (e.g., due to different rule structures), tweak the convert_apigeelint_to_sarif function in smithy/aggregate_sarif.py to handle the differences.