# Ostrich-AI/genAI_without_UI

Sample headless GenAI workload. Use synthetic inputs and an explicitly selected model/provider.

## Source baseline

| Field | Value |
| --- | --- |
| Reviewed branch | main |
| Reviewed SHA | bb7a17bcfef1168dea85afe8214ac38f3d2debba |
| GitHub default | main |
| Source class | Wider platform / sample / tooling |
| Validation | Source/manifests inspected; application execution not claimed |

The reviewed branch is a concrete coding baseline, not proof of the staging image. Reproduce a deployed issue using its actual image/source manifest. A different default branch may contain older code.

## Clone the right repository

```sh
git clone https://github.com/Ostrich-AI/genAI_without_UI.git
cd genAI_without_UI
git switch main
git switch -c feature/your-change
```

## Install, run and check

| Task | Observed command / requirement | Evidence |
| --- | --- | --- |
| Install | python -m pip install -r requirements.txt | requirements.txt; activated local virtual environment |

Commands are derived from the selected manifests/entrypoints. Configure only isolated local or approved sandbox dependencies before running tests or migrations. A semicolon in a table separates sequential commands; run them separately in your shell.

## Dependencies

- See the package/image manifest and code map; this component may be documentation, infrastructure, UI or a sample rather than a standalone API.

## Where to change code

### Build and deployment

- [Dockerfile](https://github.com/Ostrich-AI/genAI_without_UI/blob/bb7a17bcfef1168dea85afe8214ac38f3d2debba/Dockerfile)

## Configuration, tests and issues

Read [CONFIGURATION.md](docs/onboarding/CONFIGURATION.md) before starting the process. Use [MAINTAINERS.md](MAINTAINERS.md) for issue and access routing. Unit/contract/integration are different boundaries; tests listed in package metadata have not been executed by this documentation task.

Before a pull request: run the available checks, add a focused regression, update affected API/data/worker documentation and name any blocked dependency. No shared root credential is required to submit code. Product defects remain engineering issues rather than hidden documentation omissions.

## Provenance

[Selected source tree](https://github.com/Ostrich-AI/genAI_without_UI/tree/bb7a17bcfef1168dea85afe8214ac38f3d2debba) was inspected on 24 November 2026. Old README clone names and feature claims are not adopted without matching source evidence.

## Contributor navigation

- [Contribution workflow](CONTRIBUTING.md)
- [Component architecture](docs/onboarding/ARCHITECTURE.md)
- [Security reporting](SECURITY.md)
- [Previous README](docs/legacy/README.before-20261124-main.md)

## Concrete sample or installer entry point

The checked Dockerfile starts Ollama, pulls tinyllama, runs `python inference.py` and writes `output/output.csv`. Review the included synthetic input and parameters before running.

```sh
docker build -t genai-headless-local .
docker run --name genai-headless-check genai-headless-local
docker cp genai-headless-check:/app/output ./local-output
docker rm genai-headless-check
```

These source-derived commands require Docker, network/model download capacity and a clean execution check. The container is retained until output is copied.

- [inference.py](https://github.com/Ostrich-AI/genAI_without_UI/blob/bb7a17bcfef1168dea85afe8214ac38f3d2debba/inference.py)
- [Dockerfile](https://github.com/Ostrich-AI/genAI_without_UI/blob/bb7a17bcfef1168dea85afe8214ac38f3d2debba/Dockerfile)
- [parameters.json](https://github.com/Ostrich-AI/genAI_without_UI/blob/bb7a17bcfef1168dea85afe8214ac38f3d2debba/parameters.json)
- [Existing docs/HANDOVER.md](docs/HANDOVER.md)
- [Existing docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Branch and release boundary

This README is installed on `main`. The reviewed implementation branch is `main`; use it for the setup commands above. Source pins identify the pre-documentation code baseline. Documentation updates do not establish the image running at any portal.

This is a public sample/distribution repository. Its existing license and notices govern reuse; no new license is introduced here.
