# APIGEESast: Static Analysis Framework for Apigee Bundles

## Overview
APIGEESast is a prototype framework for performing effective Static Application Security Testing (SAST) on Apigee proxies and shared flows. It addresses the challenge of securing native Apigee XML-based bundles by combining Apigee-specific linting with optional scanning for embedded Java code. The output is a unified SARIF report, enabling easy integration into CI/CD pipelines like GitHub Actions, GitLab CI, or Jenkins.

This tool-agnostic approach shifts security left, helping teams identify vulnerabilities early without disrupting development velocity. It's designed for API security engineers, DevSecOps practitioners, and organizations using Apigee in cloud or hybrid environments.

## Key Benefits
- **Comprehensive Coverage**: Scans Apigee XML policies with apigeelint and conditionally scans Java service callouts with Checkmarx (or alternatives).
- **CI/CD Integration**: Runs as a dedicated SAST stage, with gating based on severity thresholds.
- **Extensible Reporting**: Produces SARIF-compatible reports for tools like GitHub Security, DefectDojo, or custom dashboards.
- **Pragmatic Design**: Detects Java presence automatically; skips unnecessary scans to optimize performance.
- **Open-Source Friendly**: Built with Python, Docker, and existing tools for easy adaptation.

## Architecture
The framework uses Smithy Security for orchestration. See the sequence flow below (rendered from `docs/sequence.puml`):

![Sequence Diagram](https://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/yourusername/APIGEESast/main/docs/sequence.puml)

High-level components:
- **Git Clone**: Pulls the Apigee bundle from a provided repo URL.
- **apigeelint Scan**: Lints XML policies and outputs SARIF.
- **Java Detector**: Python script checks for Java files in `/resources/java`.
- **Checkmarx Scan** (Optional): Scans Java code if detected.
- **Report Aggregator**: Merges results into a single SARIF file.

## Quick Start
1. Clone this repo: `git clone https://github.com/yourusername/APIGEESast.git`
2. Install dependencies: See `setup_guide.md` for detailed steps.
3. Run locally: `python orchestrate.py --repo-url <your-apigee-repo>`
4. Integrate into CI: Add as a step in your pipeline (examples in `ci-examples/`).

For full setup, refer to `setup_guide.md`.

## Requirements
- Python 3.8+
- Docker (for tool containers)
- Access to Checkmarx (API token for scans)
- GitHub repo with flattened Apigee bundle structure

## Limitations
This is a PoC. For production, enhance with authentication, error handling, and tool alternatives (e.g., Snyk instead of Checkmarx).

## Contributing
Contributions welcome! Fork, create a branch, and submit a PR. Focus on improving extensibility or adding support for other SAST tools.

## License
MIT License - see `LICENSE` file.

## Author
Ashish Saha - Senior API Security Engineer | LinkedIn: [linkedin.com/in/ashish-saha-seniorengineeringmanager](https://linkedin.com/in/ashish-saha-seniorengineeringmanager)