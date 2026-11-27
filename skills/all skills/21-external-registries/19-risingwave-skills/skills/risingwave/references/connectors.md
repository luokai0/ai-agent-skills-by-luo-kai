# RisingWave Connectors Reference

## Sources (Ingestion)

### Message Queues
| Connector | `connector=` value | Notes |
|-----------|-------------------|-------|
| Apache Kafka | `kafka` | Most common; supports shared source |
| Redpanda | `kafka` | Kafka-compatible |
| Confluent Cloud | `kafka` | Use SASL/SSL properties |
| Apache Pulsar | `pulsar` | |
| AWS Kinesis | `kinesis` | |
| Google Pub/Sub | `google_pubsub` | |
| NATS JetStream | `nats` | |
| MQTT | `mqtt` | |

### Database CDC (must use `CREATE TABLE`, not `CREATE SOURCE`)
| Database | `connector=` value | Notes |
|----------|-------------------|-------|
| PostgreSQL | `postgres-cdc` | v10–17, RDS, Neon, Supabase |
| MySQL | `mysql-cdc` | |
| SQL Server | `sqlserver-cdc` | |
| MongoDB | `mongodb-cdc` | |
| TiDB | `mysql-cdc` | MySQL-compatible |

### Cloud Storage & Data Lakes
| Source | `connector=` value |
|--------|-------------------|
| AWS S3 | `s3` |
| Google Cloud Storage | `gcs` |
| Azure Blob Storage | `azblob` |
| Apache Iceberg | `iceberg` |

### HTTP & Testing
| Source | `connector=` value | Notes |
|--------|-------------------|-------|
| Webhooks | `http_push` | RisingWave acts as HTTP server |
| Datagen | `datagen` | Built-in mock data generator |
| Nexmark | `nexmark` | Streaming benchmark data |

---

## FORMAT and ENCODE Options

```sql
FORMAT { PLAIN | UPSERT | DEBEZIUM | MAXWELL | CANAL | DEBEZIUM_MONGO }
ENCODE { JSON | AVRO | PROTOBUF | CSV | BYTES }
```

| FORMAT | When to use |
|--------|-------------|
| `PLAIN` | Append-only streams (Kafka events, logs) |
| `UPSERT` | Key-value streams with updates (Kafka compacted topics) |
| `DEBEZIUM` | CDC from Debezium connector |
| `MAXWELL` | CDC from Maxwell's Daemon (MySQL) |
| `CANAL` | CDC from Canal (Alibaba MySQL CDC) |
| `DEBEZIUM_MONGO` | MongoDB CDC via Debezium |

---

## Sinks (Output)

### Message Queues
| Destination | `connector=` value |
|-------------|-------------------|
| Apache Kafka | `kafka` |
| AWS Kinesis | `kinesis` |
| Apache Pulsar | `pulsar` |
| Google Pub/Sub | `google_pubsub` |
| NATS | `nats` |
| MQTT | `mqtt` |

### Data Warehouses
| Destination | `connector=` value |
|-------------|-------------------|
| Snowflake | `snowflake` |
| BigQuery | `bigquery` |
| Amazon Redshift | `redshift` |
| ClickHouse | `clickhouse` |
| Apache Doris | `doris` |
| StarRocks | `starrocks` |

### Databases
| Destination | `connector=` value |
|-------------|-------------------|
| PostgreSQL | `jdbc` |
| MySQL | `jdbc` |
| SQL Server | `sqlserver` |
| CockroachDB | `jdbc` |
| TiDB | `jdbc` |
| Cassandra / ScyllaDB | `cassandra` |

### Data Lakes & Object Storage
| Destination | `connector=` value | Notes |
|-------------|-------------------|-------|
| Apache Iceberg | `iceberg` | Exactly-once with `is_exactly_once = true` |
| Delta Lake | `deltalake` | |
| AWS S3 | `s3` | Parquet or JSON |
| Google Cloud Storage | `gcs` | |
| Azure Blob Storage | `azblob` | |

### Search & Cache
| Destination | `connector=` value |
|-------------|-------------------|
| Elasticsearch | `elasticsearch` |
| Redis | `redis` |

---

## Common Sink Options

```sql
CREATE SINK my_sink FROM my_mv
WITH (
    connector = '...',
    snapshot = false,          -- skip backfilling existing MV data
    force_compaction = true    -- emit at most 1 update per key per barrier
)
FORMAT PLAIN ENCODE JSON;
```
