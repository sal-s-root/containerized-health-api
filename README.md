# Instrumented infrastructure service fixture

A small HTTP service for practicing image builds, reverse proxies, health probes,
rollouts, and monitoring. This is a lab fixture using Python's standard HTTP
server, not a production application framework.

| Endpoint | Purpose |
|---|---|
| `/healthz` | Process responds to requests |
| `/readyz` | Fixture is ready; no external dependencies are checked |
| `/version` | Configured `APP_VERSION`, default `development` |
| `/metrics` | Prometheus request counters with bounded route labels |

```sh
python3 -m unittest -v
docker build -t infra-demo:local .
docker run --rm --read-only --tmpfs /tmp -p 127.0.0.1:8080:8080 infra-demo:local
```

The image runs as UID 10001. The server handles SIGTERM for graceful shutdown.
Unknown routes share one metrics label to avoid user-controlled route cardinality.
No authentication or TLS is included: keep it in a lab or behind an appropriate
proxy. Health and readiness are deliberately separate interfaces even though this
fixture has no external dependencies.

The CI workflow tests the service, builds its image, and probes the running
container. Related labs: [Compose](https://github.com/sal-s-root/compose-platform-lab),
[Kubernetes](https://github.com/sal-s-root/kubernetes-platform-lab), and
[observability](https://github.com/sal-s-root/observability-platform-lab).

## Project history

See [history and scope](HISTORY.md) for the correction of earlier synthetic dates.
