from pathlib import Path

from remodel_engine.engine import RemodelEngine
from remodel_engine.schema import RawDbtModel, RemodelRequest

_FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "informatica"
    / "informatica_xml_minimal_source_sq_exp_target"
)


def _base_request(**overrides):
    tgt_sql = (_FIXTURE / "models" / "tgt_orders.sql").read_text()
    seeds_sql = str(_FIXTURE / "seeds.sql")
    payload = {
        "pipeline_id": "entity_consolidation_demo",
        "source_platform": "informatica",
        "raw_dbt_models": [
            RawDbtModel(
                model_name="tgt_orders",
                sql=tgt_sql,
            )
        ],
        "entity_consolidations": [
            {
                "new_entity": "dim_customer",
                "old_tables": ["legacy_cust_a", "legacy_cust_b"],
                "old_key_columns": {
                    "legacy_cust_a": "cust_id",
                    "legacy_cust_b": "cust_id",
                },
                "new_key_column": "customer_key",
                "timestamp_column": "updated_at",
                "conflict_fields": ["customer_name", "city"],
            }
        ],
        "parity_context": {
            "seeds_sql": seeds_sql,
            "model_table_map": {},
            "source_table_map": {},
            "entity_consolidation_clusters": [
                {
                    "spec_new_entity": "dim_customer",
                    "new_key": "cust-100",
                    "rows": [
                        {
                            "old_key": "1",
                            "old_table": "legacy_cust_a",
                            "timestamp": "2020-01-01T00:00:00",
                            "field_values": {
                                "customer_name": "Alice",
                                "city": "NY",
                                "updated_at": "2020-01-01",
                            },
                        },
                        {
                            "old_key": "2",
                            "old_table": "legacy_cust_b",
                            "timestamp": "2022-01-01T00:00:00",
                            "field_values": {
                                "customer_name": "Alicia",
                                "city": "NY",
                                "updated_at": "2022-01-01",
                            },
                        },
                    ],
                },
                {
                    "spec_new_entity": "dim_customer",
                    "new_key": "cust-200",
                    "rows": [
                        {
                            "old_key": "9",
                            "old_table": "legacy_cust_a",
                            "timestamp": "2021-06-01T00:00:00",
                            "field_values": {
                                "customer_name": "Bob",
                                "city": "SF",
                                "updated_at": "2021-06-01",
                            },
                        },
                        {
                            "old_key": "10",
                            "old_table": "legacy_cust_b",
                            "timestamp": "2021-06-01T00:00:00",
                            "field_values": {
                                "customer_name": "Robert",
                                "city": "SF",
                                "updated_at": "2021-06-01",
                            },
                        },
                    ],
                },
            ],
        },
    }
    payload.update(overrides)
    return RemodelRequest(**payload)


def test_entity_consolidation_emits_crosswalk_compat_and_audit_models():
    resp = RemodelEngine().remodel(_base_request())
    names = {m.model_name for m in resp.remodeled_models}
    assert "int_dim_customer__crosswalk" in names
    assert "int_dim_customer__survivorship_audit" in names
    assert "stg_legacy_cust_a__compat" in names
    assert "stg_legacy_cust_b__compat" in names
    assert "dim_customer" in names
    assert len(resp.remodeled_models) == 1 + 5


def test_entity_consolidation_needs_survivorship_review_on_ambiguous_tie():
    resp = RemodelEngine().remodel(_base_request())
    assert resp.status == "needs_survivorship_review"
    audit = next(
        m for m in resp.remodeled_models if m.model_name == "int_dim_customer__survivorship_audit"
    )
    assert audit.parity_check.status == "pass"
    assert audit.merge_audits
