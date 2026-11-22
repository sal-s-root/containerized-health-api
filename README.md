# Containerized health API

## Purpose

Package a small service, add a health endpoint, run it as a non-root user, and define CI checks.

## Run locally

```sh
python3 -m unittest -v
python3 app.py
# In a separate terminal: curl --fail http://127.0.0.1:8080/healthz
# Container alternative:
# docker build -t health-api:lab .
# docker run --rm -p 127.0.0.1:8080:8080 health-api:lab
```

## Scope and limitations

The standard-library HTTP server is for a lab, not production traffic. Dependencies use mutable version tags. Local unit tests are separate from a container build and hosted CI execution.

## Engineering notes

See [LEARNING.md](LEARNING.md) for the design decisions, verification evidence,
and next steps. Never commit credentials, private hostnames, or real incident data.

## Version inspection

`GET /version` returns `APP_VERSION` or `development` when unset. Set a release identifier when launching a container, then compare the endpoint with the intended deployment manifest. This reports a configured value, not cryptographic build provenance.
