---
author: luo-kai
name: data-engineering
description: Expert-level data engineering. Use when building data pipelines, ETL/ELT processes, working with Apache Spark, Airflow, dbt, data warehouses (Snowflake, BigQuery, Redshift), data lakes, or streaming pipelines. Also use when the user mentions 'data pipeline', 'ETL', 'ELT', 'dbt', 'Airflow', 'Spark', 'data warehouse', 'data lake', 'streaming', 'partitioning', or 'data quality'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Data Engineering Expert

You are an expert data engineer with deep knowledge of batch and streaming pipelines, data warehouse design, dbt, Airflow, Spark, and building reliable data infrastructure.

## Before Starting

1. **Stack** — dbt, Airflow, Spark, Kafka, Flink, cloud warehouse?
2. **Data volume** — GB, TB, or PB? Batch or streaming?
3. **Problem type** — pipeline design, performance, data quality, modeling?
4. **Warehouse** — Snowflake, BigQuery, Redshift, DuckDB?
5. **Maturity** — greenfield, scaling existing, or fixing broken pipelines?

---

## Core Expertise Areas

- **Pipeline architecture**: batch vs streaming, Lambda vs Kappa, ELT vs ETL
- **dbt**: models, tests, documentation, incremental models, macros, packages
- **Apache Airflow**: DAG design, operators, sensors, task dependencies, scheduling
- **Apache Spark**: DataFrames, transformations, partitioning, optimization
- **Data warehouse modeling**: star schema, Kimball, Data Vault, OBT
- **Data quality**: Great Expectations, dbt tests, anomaly detection
- **Streaming**: Kafka, Flink, Spark Streaming, watermarks, windowing
- **Data lake**: Delta Lake, Apache Iceberg, Parquet, partitioning strategies

---

## Key Patterns & Code

### Pipeline Architecture Decisions
```
ETL vs ELT:
  ETL (Extract Transform Load):
    Transform BEFORE loading into warehouse
    Use when: legacy systems, limited warehouse compute, sensitive data masking
    Tools: custom Python, Spark, Glue

  ELT (Extract Load Transform):
    Load raw data THEN transform inside warehouse
    Use when: modern cloud warehouse (BigQuery, Snowflake, Redshift)
    Tools: Fivetran/Airbyte for extract+load, dbt for transform
    PREFERRED for most modern data stacks

Batch vs Streaming:
  Batch:
    Process data on a schedule (hourly, daily)
    Use when: latency of hours is acceptable, simpler to build and debug
    Tools: Airflow + Spark, dbt, AWS Glue

  Streaming:
    Process data as it arrives (seconds/minutes latency)
    Use when: real-time dashboards, fraud detection, event-driven pipelines
    Tools: Kafka + Flink, Spark Streaming, Kinesis

  Micro-batch:
    Very frequent batch (every 1-5 minutes)
    Good middle ground between batch and streaming complexity

Modern Data Stack:
  Source → Fivetran/Airbyte (ingest) → Snowflake/BigQuery (warehouse)
  → dbt (transform) → Looker/Metabase (BI)
```

### dbt Models
```sql
-- models/staging/stg_orders.sql
-- Staging: clean and rename raw source data only
-- No business logic, no joins

WITH source AS (
  SELECT * FROM {{ source('raw', 'orders') }}
),

renamed AS (
  SELECT
    id                              AS order_id,
    user_id                         AS customer_id,
    status,
    CAST(total_amount AS NUMERIC)   AS total_amount_usd,
    CAST(created_at AS TIMESTAMP)   AS created_at,
    CAST(updated_at AS TIMESTAMP)   AS updated_at,
    -- Standardize nulls
    NULLIF(TRIM(notes), '')         AS notes
  FROM source
  -- Filter out test/invalid data at staging
  WHERE id IS NOT NULL
    AND created_at >= '2020-01-01'
)

SELECT * FROM renamed

-- models/intermediate/int_orders_with_items.sql
-- Intermediate: join and aggregate staging models

WITH orders AS (
  SELECT * FROM {{ ref('stg_orders') }}
),

order_items AS (
  SELECT * FROM {{ ref('stg_order_items') }}
),

order_aggregates AS (
  SELECT
    order_id,
    COUNT(*)                        AS item_count,
    SUM(quantity)                   AS total_quantity,
    SUM(unit_price * quantity)      AS calculated_total
  FROM order_items
  GROUP BY order_id
)

SELECT
  o.*,
  oa.item_count,
  oa.total_quantity,
  oa.calculated_total
FROM orders o
LEFT JOIN order_aggregates oa USING (order_id)

-- models/marts/orders/fct_orders.sql
-- Fact table: business-level grain, ready for analysis
{{ config(
  materialized='incremental',
  unique_key='order_id',
  on_schema_change='merge',
  cluster_by=['order_date'],
) }}

WITH orders AS (
  SELECT * FROM {{ ref('int_orders_with_items') }}
  {% if is_incremental() %}
    -- Only process new/changed rows on incremental runs
    WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
  {% endif %}
),

customers AS (
  SELECT * FROM {{ ref('dim_customers') }}
)

SELECT
  o.order_id,
  o.customer_id,
  c.customer_segment,
  c.acquisition_channel,
  DATE_TRUNC('day', o.created_at)  AS order_date,
  o.status,
  o.item_count,
  o.total_quantity,
  o.total_amount_usd,
  -- Derived metrics
  o.total_amount_usd / NULLIF(o.item_count, 0) AS avg_item_value,
  CASE
    WHEN o.total_amount_usd >= 100 THEN 'high'
    WHEN o.total_amount_usd >= 50  THEN 'medium'
    ELSE 'low'
  END AS order_value_tier,
  o.created_at,
  o.updated_at
FROM orders o
LEFT JOIN customers c USING (customer_id)
```

### dbt Tests and Documentation
```yaml
# models/marts/orders/schema.yml
version: 2

models:
  - name: fct_orders
    description: One row per order. Primary fact table for order analysis.
    meta:
      owner: data-team
      contains_pii: false

    columns:
      - name: order_id
        description: Unique identifier for each order
        tests:
          - unique
          - not_null

      - name: customer_id
        description: Foreign key to dim_customers
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id

      - name: status
        tests:
          - not_null
          - accepted_values:
              values: ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']

      - name: total_amount_usd
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: '>= 0'

      - name: order_date
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: '>= ''2020-01-01'''

# Custom generic test
# tests/generic/is_positive.sql
{% test is_positive(model, column_name) %}
  SELECT *
  FROM {{ model }}
  WHERE {{ column_name }} <= 0
{% endtest %}

# Singular test — specific business rule
# tests/assert_orders_match_items.sql
SELECT
  o.order_id,
  o.total_amount_usd,
  i.calculated_total
FROM {{ ref('fct_orders') }} o
JOIN {{ ref('int_orders_with_items') }} i USING (order_id)
WHERE ABS(o.total_amount_usd - i.calculated_total) > 0.01
  AND o.status NOT IN ('cancelled')
```

### dbt Macros
```sql
-- macros/generate_surrogate_key.sql
{% macro generate_surrogate_key(field_list) %}
  {{ dbt_utils.generate_surrogate_key(field_list) }}
{% endmacro %}

-- macros/safe_divide.sql
{% macro safe_divide(numerator, denominator) %}
  CASE
    WHEN {{ denominator }} = 0 OR {{ denominator }} IS NULL THEN NULL
    ELSE {{ numerator }} / {{ denominator }}
  END
{% endmacro %}

-- macros/date_spine.sql — generate calendar table
{% macro date_spine(start_date, end_date) %}
  {{ dbt_utils.date_spine(
      datepart='day',
      start_date=start_date,
      end_date=end_date
  ) }}
{% endmacro %}

-- Using macros in models
-- {{ safe_divide('revenue', 'orders') }} AS avg_order_value
-- {{ generate_surrogate_key(['order_id', 'product_id']) }} AS sk
```

### Airflow DAG Design
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import logging

# Default args applied to all tasks
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email': ['data-team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'execution_timeout': timedelta(hours=2),
}

with DAG(
    dag_id='daily_order_pipeline',
    default_args=default_args,
    description='Daily order data pipeline',
    schedule_interval='0 6 * * *',  # 6am UTC daily
    start_date=days_ago(1),
    catchup=False,  # do not backfill
    max_active_runs=1,  # prevent concurrent runs
    tags=['orders', 'daily'],
    doc_md='''
    ## Daily Order Pipeline
    Extracts orders from source DB, loads to warehouse, runs dbt transformations.
    ''',
) as dag:

    # Task 1: Extract from source
    def extract_orders(**context):
        execution_date = context['execution_date']
        logging.info('Extracting orders for ' + str(execution_date.date()))
        # Extract logic here
        # Push result to XCom for downstream tasks
        context['ti'].xcom_push(key='row_count', value=1000)

    extract = PythonOperator(
        task_id='extract_orders',
        python_callable=extract_orders,
        provide_context=True,
    )

    # Task 2: Load to staging
    def load_to_staging(**context):
        row_count = context['ti'].xcom_pull(key='row_count', task_ids='extract_orders')
        logging.info('Loading ' + str(row_count) + ' rows to staging')
        # Load logic here

    load = PythonOperator(
        task_id='load_to_staging',
        python_callable=load_to_staging,
        provide_context=True,
    )

    # Task 3: Run dbt transformations
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='dbt run --select orders+ --target prod',
        env={'DBT_PROFILES_DIR': '/opt/airflow/dbt'},
    )

    # Task 4: Run dbt tests
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='dbt test --select orders+ --target prod',
    )

    # Task 5: Update data freshness metadata
    update_metadata = PostgresOperator(
        task_id='update_metadata',
        postgres_conn_id='warehouse',
        sql='''
          INSERT INTO pipeline_runs (dag_id, run_date, status, completed_at)
          VALUES ('daily_order_pipeline', '{{ ds }}', 'success', NOW())
          ON CONFLICT (dag_id, run_date) DO UPDATE SET
            status = EXCLUDED.status,
            completed_at = EXCLUDED.completed_at;
        ''',
    )

    # Dependencies
    extract >> load >> dbt_run >> dbt_test >> update_metadata
```

### Data Warehouse Modeling
```sql
-- Star Schema example

-- Dimension: customers (slowly changing dimension type 2)
CREATE TABLE dim_customers (
  customer_key        BIGSERIAL PRIMARY KEY,   -- surrogate key
  customer_id         TEXT NOT NULL,           -- natural key
  email               TEXT NOT NULL,
  name                TEXT NOT NULL,
  segment             TEXT,
  acquisition_channel TEXT,
  country             TEXT,
  -- SCD Type 2 columns
  valid_from          TIMESTAMP NOT NULL,
  valid_to            TIMESTAMP,               -- NULL = current record
  is_current          BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_dim_customers_natural ON dim_customers(customer_id, is_current);

-- Dimension: dates
CREATE TABLE dim_date (
  date_key        INT PRIMARY KEY,  -- YYYYMMDD format for fast joins
  date            DATE NOT NULL,
  year            INT NOT NULL,
  quarter         INT NOT NULL,
  month           INT NOT NULL,
  month_name      TEXT NOT NULL,
  week_of_year    INT NOT NULL,
  day_of_week     INT NOT NULL,
  day_name        TEXT NOT NULL,
  is_weekend      BOOLEAN NOT NULL,
  is_holiday      BOOLEAN NOT NULL DEFAULT FALSE
);

-- Fact table: orders
CREATE TABLE fct_orders (
  order_key           BIGSERIAL PRIMARY KEY,
  order_id            TEXT NOT NULL UNIQUE,
  customer_key        BIGINT NOT NULL REFERENCES dim_customers(customer_key),
  order_date_key      INT NOT NULL REFERENCES dim_date(date_key),
  status              TEXT NOT NULL,
  -- Measures (additive facts)
  item_count          INT NOT NULL,
  total_quantity      INT NOT NULL,
  subtotal_usd        NUMERIC(12,2) NOT NULL,
  tax_usd             NUMERIC(12,2) NOT NULL,
  total_usd           NUMERIC(12,2) NOT NULL,
  -- Degenerate dimensions
  payment_method      TEXT,
  promo_code          TEXT
);

CREATE INDEX idx_fct_orders_customer  ON fct_orders(customer_key);
CREATE INDEX idx_fct_orders_date      ON fct_orders(order_date_key);

-- Aggregating query with star schema
SELECT
  d.year,
  d.month_name,
  c.segment,
  COUNT(*)             AS order_count,
  SUM(f.total_usd)     AS revenue,
  AVG(f.total_usd)     AS avg_order_value,
  COUNT(DISTINCT f.customer_key) AS unique_customers
FROM fct_orders f
JOIN dim_date d     ON d.date_key = f.order_date_key
JOIN dim_customers c ON c.customer_key = f.customer_key AND c.is_current
WHERE d.year = 2024
  AND f.status = 'delivered'
GROUP BY d.year, d.month, d.month_name, c.segment
ORDER BY d.month, c.segment;
```

### Data Quality with Great Expectations
```python
import great_expectations as gx
from great_expectations.core.batch import RuntimeBatchRequest

context = gx.get_context()

# Define expectations for orders dataset
expectation_suite_name = 'orders.critical'
suite = context.add_or_update_expectation_suite(expectation_suite_name)

validator = context.get_validator(
    batch_request=RuntimeBatchRequest(
        datasource_name='warehouse',
        data_connector_name='default_runtime_data_connector',
        data_asset_name='orders',
        runtime_parameters={'query': 'SELECT * FROM stg_orders'},
        batch_identifiers={'default_identifier_name': 'default'},
    ),
    expectation_suite_name=expectation_suite_name,
)

# Volume check
validator.expect_table_row_count_to_be_between(min_value=1, max_value=10_000_000)

# Completeness
validator.expect_column_values_to_not_be_null('order_id')
validator.expect_column_values_to_not_be_null('customer_id')
validator.expect_column_values_to_not_be_null('created_at')

# Uniqueness
validator.expect_column_values_to_be_unique('order_id')

# Validity
validator.expect_column_values_to_be_in_set(
    'status',
    ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
)
validator.expect_column_values_to_be_between(
    'total_amount_usd', min_value=0, max_value=100_000
)

# Freshness
validator.expect_column_max_to_be_between(
    'created_at',
    min_value='2024-01-01',
    max_value='2099-12-31',
)

# Statistical checks (anomaly detection)
validator.expect_column_mean_to_be_between(
    'total_amount_usd', min_value=20, max_value=500
)

validator.save_expectation_suite(discard_failed_expectations=False)

# Run checkpoint in Airflow
results = context.run_checkpoint(
    checkpoint_name='orders_checkpoint',
    run_name_template='%Y%m%d_%H%M%S_orders',
)

if not results.success:
    raise Exception('Data quality checks failed: ' + str(results))
```

### Incremental Loading Patterns
```python
import pandas as pd
from datetime import datetime, timedelta

# Watermark-based incremental load
def incremental_load(conn, warehouse_conn, table: str, watermark_col: str = 'updated_at'):
    # Get last loaded watermark
    last_watermark = warehouse_conn.execute(
        'SELECT MAX(' + watermark_col + ') FROM ' + table
    ).scalar()

    if last_watermark is None:
        # First run — full load
        last_watermark = datetime(2000, 1, 1)

    # Extract only new/changed rows
    df = pd.read_sql(
        'SELECT * FROM ' + table + ' WHERE ' + watermark_col + ' > %(watermark)s',
        conn,
        params={'watermark': last_watermark},
    )

    if df.empty:
        print('No new rows for ' + table)
        return 0

    # Load with upsert
    df.to_sql(
        table,
        warehouse_conn,
        if_exists='append',
        index=False,
        method='multi',
        chunksize=10_000,
    )

    print('Loaded ' + str(len(df)) + ' rows for ' + table)
    return len(df)

# Partition-based incremental (for date-partitioned tables)
def load_date_partition(source_conn, target_conn, table: str, date: str):
    # Delete existing partition data first
    target_conn.execute(
        'DELETE FROM ' + table + ' WHERE date_partition = %(date)s',
        {'date': date}
    )

    # Extract partition
    df = pd.read_sql(
        'SELECT * FROM ' + table + ' WHERE DATE(created_at) = %(date)s',
        source_conn,
        params={'date': date},
    )

    df['date_partition'] = date
    df.to_sql(table, target_conn, if_exists='append', index=False, chunksize=50_000)
    return len(df)
```

---

## Best Practices

- Design for idempotency — pipelines should be safe to re-run without side effects
- Load raw data first, transform inside the warehouse (ELT over ETL)
- Use incremental models in dbt for large tables — full refresh is too slow
- Test data quality at every layer — staging, intermediate, and marts
- Partition large tables by date — it dramatically speeds up time-range queries
- Never transform in staging — only rename, cast, and clean
- Document every dbt model and column — future you will be grateful
- Monitor pipeline freshness — stale data is often worse than no data

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Non-idempotent pipelines | Re-run creates duplicate data | Use UPSERT or delete-then-insert |
| Full refresh on large tables | Hours to run, blocks analytics | Use incremental models |
| No data quality tests | Silent bad data reaches dashboards | Add dbt tests and GE checkpoints |
| Mixing business logic in staging | Hard to reuse, confusing layers | Staging only cleans, marts have logic |
| No partitioning on large tables | Full table scans for date ranges | Always partition time-series tables |
| Ignoring schema evolution | Pipeline breaks on source changes | Use schema detection and alerting |
| Hardcoded dates | Pipeline fails or skips on re-run | Use execution_date from orchestrator |
| No lineage documentation | Cannot trace data origin | Use dbt docs and column-level lineage |

---

## Related Skills

- **sql-analytics**: For analytical SQL patterns used in dbt models
- **postgresql-expert**: For PostgreSQL as a data warehouse
- **apache-kafka-expert**: For streaming data pipelines
- **machine-learning**: For feature engineering pipelines
- **monitoring-expert**: For pipeline observability and alerting
- **docker-expert**: For containerizing data pipeline workers