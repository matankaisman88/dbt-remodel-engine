FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY remodel_engine/ ./remodel_engine/

RUN pip install --no-cache-dir .

EXPOSE 8001

CMD ["uvicorn", "remodel_engine.api:app", "--host", "0.0.0.0", "--port", "8001"]
