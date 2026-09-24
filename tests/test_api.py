from fastapi.testclient import TestClient

from remodel_engine.api import app

client = TestClient(app)


def test_remodel_api_minimal():
    payload = {
        "pipeline_id": "p1",
        "source_platform": "informatica",
        "raw_dbt_models": [
            {
                "model_name": "raw_stg",
                "sql": "SELECT id FROM {{ source('s', 't') }}",
                "materialization": "view",
            }
        ],
    }
    resp = client.post("/api/v1/remodel", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["pipeline_id"] == "p1"
    assert body["remodeled_models"]
