"""POST /api/v1/remodel — headless API entrypoint."""

from __future__ import annotations

from fastapi import FastAPI

from remodel_engine.engine import RemodelEngine
from remodel_engine.schema import RemodelRequest, RemodelResponse

app = FastAPI(title="dbt-remodel-engine", version="0.1.0")
_engine = RemodelEngine()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/remodel", response_model=RemodelResponse)
def remodel(request: RemodelRequest) -> RemodelResponse:
    return _engine.remodel(request)
