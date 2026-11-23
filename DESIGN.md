# Design decisions

The service is a fixture for infrastructure exercises. It keeps route labels bounded, separates endpoint contracts, runs as a non-root user in its image, and handles SIGTERM. It does not provide a production application framework, authentication, or TLS.

See README.md for operation and VALIDATION.md for the checks actually performed.
