---
name: grafana-dashboard-engineer
description: Design, implement, and maintain professional Grafana dashboards following industry-standard observability patterns like RED and USE. Use when creating monitoring dashboards for microservices, infrastructure, or databases. Triggers on requests for Grafana dashboards, observability, monitoring, or infrastructure visualization.
---

# Grafana Dashboard Engineer

Build production-ready observability dashboards with industry best practices.

## Core Capabilities

- **Dashboard-as-Code** — JSON configurations for version control
- **RED/USE Methods** — Standard observability frameworks
- **Dynamic Variables** — Templating for multi-environment support
- **Alerting Integration** — Thresholds and notifications built-in
- **Provisioning Ready** — Terraform/Ansible compatible

## Observability Frameworks

### RED Method (For Services)
- **Rate** — Requests per second
- **Errors** — Error rate percentage
- **Duration** — Request latency (p50, p95, p99)

### USE Method (For Resources)
- **Utilization** — % of resource used
- **Saturation** — Queue length / wait time
- **Errors** — Error count / rate

## Dashboard Types

### API Monitoring
- Request rate and latency
- Error rate by endpoint
- Status code distribution
- Dependency health

### Infrastructure
- CPU/Memory/Disk utilization
- Network I/O
- Container metrics
- Host health

### Database
- Query performance
- Connection pooling
- Replication lag
- Storage metrics

## Quick Start

```json
{
  "dashboard": {
    "title": "API Service Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "timeseries",
        "targets": [{"expr": "rate(http_requests_total[5m])"}]
      }
    ]
  }
}
```

## Best Practices

1. **Consistent naming** — Use clear, descriptive panel titles
2. **Logical grouping** — Related metrics together
3. **Appropriate time ranges** — Default to last 6 hours
4. **Color consistency** — Green=good, Yellow=warning, Red=critical
5. **Annotations** — Mark deployments and incidents

## References

- [RED Method Guide](references/red-method.md)
- [USE Method Guide](references/use-method.md)
- [Terraform Provisioning](references/terraform.md)
- [Alerting Setup](references/alerting.md)
