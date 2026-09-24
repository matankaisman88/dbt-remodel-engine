# Remodeling Verification Report

Phase A headless engine run against copied corpora under `tests/fixtures/`.

> **Fixture provenance:** These manifests mirror the raw 1:1 dbt export layout
> consumed from `etl_to_dbt` (WWI star schema + DailyETLMain active diagnosis pipeline).
> Replace files under `tests/fixtures/` with a fresh copy from `ETL-Migration-Studio-main`
> to re-verify against your local export.

## WWI corpus (etl_to_dbt export format)

- **pipeline_id:** `wwi_sales_star`
- **overall status:** `needs_manual_review`
- **legacy transformations (manifest):** 11
- **modern models:** 6
- **CTEs collapsed:** 2
- **models NEEDS_MANUAL_REVIEW:** 2

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `stg_customers` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | ['source_rows', 'filtered'] |
| `int_sales_enriched` | `intermediate` | `pass` | matched rule #2: ref() upstream with join/window/aggregation/CASE | ['invoice_base', 'joined'] |
| `dim_tgt_dim_customer` | `marts` | `pass` | matched rule #3: direct 1:1 target mapping to DIM_CUSTOMER, update_strategy_scd | — |
| `fct_tgt_fct_invoice_lines` | `marts` | `pass` | matched rule #3: direct 1:1 target mapping to FCT_INVOICE_LINES, aggregator_fact_load | — |
| `raw_passthrough_ref_only` | `needs_manual_review` | `pass` | rule #2 incomplete: has ref() but no join/window/aggregation/CASE — cannot classify as intermediate; not a legacy target | — |
| `raw_multi_consumer_window` | `needs_manual_review` | `pass` | failed rule #1 (sources only but disallowed transforms) and no other rule matched | — |

## DailyETLMain / Informatica corpus (etl_to_dbt export format)

- **pipeline_id:** `daily_etl_main_active_diagnosis`
- **overall status:** `success`
- **legacy transformations (manifest):** 14
- **modern models:** 4
- **CTEs collapsed:** 0
- **models NEEDS_MANUAL_REVIEW:** 0

### Per-model results

| Model | Layer | Parity | Classification reason | CTE merges |
| --- | --- | --- | --- | --- |
| `stg_diagnosis` | `staging` | `pass` | matched rule #1: staging rule: source-only upstream with allowed transforms | — |
| `int_diagnosis_enriched` | `intermediate` | `pass` | matched rule #2: ref() upstream with join/window/aggregation/CASE | — |
| `int_m_active_diagnosis` | `intermediate` | `pass` | matched rule #2: ref() upstream with join/window/aggregation/CASE | — |
| `int_lookup_ambiguous` | `intermediate` | `pass` | matched rule #2: ref() upstream with join/window/aggregation/CASE | — |

## Failures (unfiltered)

_No parity failures._

## NEEDS_MANUAL_REVIEW (unfiltered)

- `wwi_sales_star` → `raw_passthrough_ref_only`: rule #2 incomplete: has ref() but no join/window/aggregation/CASE — cannot classify as intermediate; not a legacy target
- `wwi_sales_star` → `raw_multi_consumer_window`: failed rule #1 (sources only but disallowed transforms) and no other rule matched
