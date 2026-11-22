# Engineering notes: Containers and continuous verification

## Objective

Package an application with an observable health endpoint and a repeatable verification workflow.

## Design decisions

- Run the container under a numeric non-root user and publish its port on loopback in examples.
- Keep the service dependency-free so the exercise focuses on HTTP, packaging, and CI.
- Test successful health responses and unknown routes. Define an image build and smoke test in GitHub Actions.

## Verification performed

| Check | Observed result |
|---|---|
| `python3 -m unittest -v` | Passed; exit 0 as expected |

## What the evidence establishes

HTTP unit tests passed locally. GitHub Actions run 45067240967 then passed the unit tests, Docker image build, and running-container health check. The standard-library server is a learning implementation; the image and Actions tags are mutable.

## Next exercise

Explore pinned image digests, updated action runtimes, graceful shutdown, and a production application server.

## Published CI evidence

[Successful GitHub Actions run](https://github.com/sal-s-root/containerized-health-api/actions/runs/45067240967). Unit tests, image build, and container HTTP smoke test all passed. The runner reported a deprecation warning for the Node runtime declared by the selected action versions; it executed them using its newer runtime.
