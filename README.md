# 09_observability - Logging, Metrics & Tracing

> Production-grade observability stack demonstrating comprehensive monitoring, logging, and distributed tracing.

## 🎯 Overview

This module implements:

- **Structured Logging** - JSON logs with correlation
- **Metrics** - Prometheus metrics collection
- **Tracing** - OpenTelemetry distributed tracing
- **Alerting** - Alert rules and notifications

## 📁 Structure

```
09_observability/
├── src/
│   ├── logging/             # Structured logging
│   │   ├── logger.py        # Logger configuration
│   │   └── formatters.py    # Log formatters
│   ├── metrics/             # Prometheus metrics
│   │   ├── collectors.py    # Custom collectors
│   │   └── middleware.py    # Request metrics
│   └── tracing/             # Distributed tracing
│       ├── tracer.py        # Tracer config
│       └── propagation.py   # Context propagation
├── dashboards/              # Grafana dashboards
└── alerts/                  # Alert rules
```

## 🚀 Quick Start

```bash
pip install -e .
python -m src.main
```

## 📄 License

MIT
