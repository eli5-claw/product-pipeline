---
name: data-pipeline-engineer
description: Build ETL/ELT data pipelines for analytics and ML. Use when moving data between systems, building data warehouses, or creating analytics pipelines. Triggers on requests for data pipelines, ETL, data engineering, or analytics infrastructure.
---

# Data Pipeline Engineer

Move data reliably. ETL, ELT, streaming — from source to insight.

## Pipeline Types

### Batch ETL
- **Schedule** — Hourly, daily, weekly
- **Tools** — Airflow, Dagster, Prefect
- **Best for** — Historical analysis, reporting

### Streaming
- **Latency** — Seconds to minutes
- **Tools** — Kafka, Kinesis, Pub/Sub
- **Best for** — Real-time analytics, monitoring

### ELT (Modern)
- **Extract** → **Load** → **Transform**
- **Tools** — dbt, BigQuery, Snowflake
- **Best for** — Cloud data warehouses

## Pipeline Architecture

```
Sources → Ingestion → Storage → Processing → Serving
   │          │          │           │          │
   ▼          ▼          ▼           ▼          ▼
APIs      Kafka     Data Lake    Spark/DBT   Dashboard
DBs       Airflow   Warehouse    dbt         ML Models
Files     Fargate   S3/Blob                  Applications
```

## Data Quality Checks

### Schema Validation
- Column types match expected
- No unexpected nulls
- Enum values valid

### Business Rules
- Referential integrity
- Range checks (e.g., age > 0)
- Uniqueness constraints

### Anomaly Detection
- Volume spikes/drops
- Schema drift
- Freshness checks

## Pipeline Best Practices

1. **Idempotent jobs** — Safe to re-run
2. **Incremental loads** — Only process new data
3. **Partitioning** — By date for time-series
4. **Monitoring** — Alert on failures
5. **Backfills** — Easy historical reprocessing

## References

- [Airflow Patterns](references/airflow-patterns.md)
- [dbt Guide](references/dbt-guide.md)
- [Data Quality](references/data-quality.md)
