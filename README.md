# 09_observability

> Python observability foundation for structured logs, metrics, distributed traces, dashboards, and actionable alerts.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Prometheus](https://img.shields.io/badge/Metrics-Prometheus-E6522C?logo=prometheus&logoColor=white)](https://prometheus.io/)
[![OpenTelemetry](https://img.shields.io/badge/Tracing-OpenTelemetry-000000?logo=opentelemetry&logoColor=white)](https://opentelemetry.io/)
[![License](https://img.shields.io/badge/License-Custom%20Commercial-orange)](./LICENSE)

This repository provides a reusable observability toolkit for Python services. It combines structured JSON logging, Prometheus metrics, OpenTelemetry tracing, Grafana dashboards, and alert rules so teams can understand system health, investigate failures, and operate services reliably.

## What this project includes

- structured JSON logging with contextual fields
- correlation and request identifiers
- Prometheus-compatible application metrics
- request and middleware instrumentation
- OpenTelemetry distributed tracing
- OTLP exporter support
- Grafana dashboard organization
- alert-rule and notification extension points
- Pydantic-based configuration patterns
- FastAPI instrumentation support

## Repository structure

```text
09_observability/
├── src/
│   ├── logging/
│   │   ├── logger.py
│   │   └── formatters.py
│   ├── metrics/
│   │   ├── collectors.py
│   │   └── middleware.py
│   ├── tracing/
│   │   ├── tracer.py
│   │   └── propagation.py
│   └── main.py
├── dashboards/
├── alerts/
├── tests/
├── pyproject.toml
├── README.md
├── LICENSE
├── .env.example
└── .gitignore
```

## Observability architecture

```text
┌──────────────────────────────────────────────────────────────────┐
│                         Python Service                            │
│   application logs │ request metrics │ trace instrumentation      │
└──────────────────────────────────────────────────────────────────┘
              │                    │                    │
              ▼                    ▼                    ▼
┌─────────────────┐   ┌────────────────────┐   ┌─────────────────┐
│ Structured Logs  │   │ Prometheus Metrics │   │ OpenTelemetry  │
│ JSON + context   │   │ counters, gauges  │   │ spans + context │
└─────────────────┘   └────────────────────┘   └─────────────────┘
              │                    │                    │
              ▼                    ▼                    ▼
┌──────────────────────────────────────────────────────────────────┐
│              Collection, Dashboards, and Alerting                 │
│       log platform │ Prometheus │ Grafana │ OTLP backend          │
└──────────────────────────────────────────────────────────────────┘
```

## The three pillars

### Logs

Structured logs make events searchable and machine-readable. Include fields such as:

- timestamp
- service and environment
- request or correlation ID
- trace and span IDs
- event name
- severity
- duration
- safe error context

Never log passwords, tokens, authorization headers, private keys, or unnecessary personal data.

### Metrics

Prometheus metrics support operational questions such as:

- Is the service available?
- Are request errors increasing?
- What are latency percentiles?
- Are queues, workers, or databases saturated?
- Is a dependency failing?

Prefer stable, low-cardinality labels. Avoid user IDs, request IDs, or unrestricted URL values as metric labels.

### Traces

OpenTelemetry traces connect work across service boundaries. Propagate context through HTTP, messaging, and asynchronous jobs so a single request can be investigated end to end.

## Quick start

### Prerequisites

- Python 3.10+
- pip and virtual environment support
- optional Prometheus and Grafana instances
- optional OTLP-compatible tracing backend

### Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

### Configure environment

```bash
cp .env.example .env
```

Example configuration:

```env
APP_ENVIRONMENT=development
SERVICE_NAME=observability-demo
LOG_LEVEL=INFO
OTEL_SERVICE_NAME=observability-demo
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
PROMETHEUS_PORT=8000
TRACE_SAMPLE_RATE=1.0
```

Use a lower trace sample rate in high-volume production environments unless full sampling is required for a controlled investigation.

### Run the example

```bash
python -m src.main
```

## Development commands

Install the package in editable mode:

```bash
pip install -e .
```

Run tests when available:

```bash
pytest
```

Build package metadata:

```bash
python -m build
```

## Production-readiness assessment

### Current maturity: strong observability foundation

This repository provides useful instrumentation building blocks. Production deployments should connect them to a complete collection and incident-response stack, with defined ownership and retention policies.

### Strengths

- covers logs, metrics, and traces together
- uses standard Prometheus and OpenTelemetry ecosystems
- supports structured context and correlation
- provides dashboard and alerting extension points
- suitable for Python services and API platforms

### Production gaps to address

1. Define service-level indicators and SLOs.
2. Add alert ownership, routing, and escalation policies.
3. Configure log, metric, and trace retention deliberately.
4. Add instrumentation tests and telemetry health checks.
5. Protect telemetry endpoints and collector traffic.
6. Remove sensitive data and control high-cardinality fields.
7. Add dashboards for dependencies, saturation, and business signals.
8. Document sampling, cost controls, and incident workflows.

## Recommended SLO signals

Track service-level indicators such as:

- availability and successful request rate
- error rate by endpoint and dependency
- p50, p95, and p99 latency
- saturation of CPU, memory, workers, queues, and databases
- background job success and processing delay
- dependency timeout and retry rates

Alerts should represent actionable symptoms rather than every individual error.

## Security and privacy

Before production deployment:

- redact secrets and personal data before export
- restrict access to logs, dashboards, and traces
- use TLS for collector and backend communication
- protect metrics endpoints from public exposure
- apply retention and deletion policies
- review third-party exporters and collectors
- avoid placing authorization data in metric labels

## Monetization opportunities

This toolkit supports several commercial directions:

| Business model | Best use case |
| --- | --- |
| managed observability service | monitoring for small and mid-sized teams |
| reliability consulting toolkit | instrumenting client applications |
| internal platform module | standard telemetry across engineering teams |
| alerting and SLO product | operational reliability workflows |
| Python instrumentation package | reusable service monitoring foundation |

## GitHub discoverability

This repository is positioned around:

- Python structured logging
- Prometheus metrics toolkit
- OpenTelemetry tracing
- distributed tracing Python
- Grafana observability dashboards
- SRE monitoring foundation
- application performance monitoring

To improve discoverability:

- add screenshots of dashboards
- document a complete local Prometheus/Grafana setup
- show trace propagation across services
- publish example alert rules and SLO dashboards
- include telemetry cost and privacy guidance

## Roadmap ideas

- add a Docker Compose observability demo stack
- add OpenTelemetry Collector configuration
- add log correlation examples
- add standard RED and USE dashboards
- add SLO and error-budget templates
- add exporters for common cloud backends
- add automatic PII redaction middleware
- add CI checks for instrumentation regressions

## License

This repository contains a custom commercial license in `LICENSE`.

Review the full license before personal earning, commercial, enterprise, redistribution, or client deployment use.
