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

HTTP unit tests ran directly in the existing container. The new Docker image was not built and the hosted Actions workflow has not run. The standard-library server is a learning implementation; the image and Actions tags are mutable.

## Next exercise

Run the workflow after publishing, inspect image health, then explore pinned image digests, graceful shutdown, and a production application server.
