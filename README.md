# Enterprise DevOps ML Platform

## Overview

Modern machine learning projects fail not because models are bad, but because they cannot be reliably deployed, monitored, secured, or operated at scale. This project addresses that gap.

**Enterprise DevOps ML Platform** is an end-to-end, DevOps-first machine learning system that demonstrates how data ingestion, model training, model serving, CI/CD, infrastructure-as-code, and observability come together in a production-grade workflow.

This repository is intentionally opinionated: it prioritizes **operability, reproducibility, and clarity** over model complexity.

---

## Problem Statement

Most ML demos stop at notebooks. Enterprises need:

* Repeatable deployments
* CI/CD pipelines
* Infrastructure defined as code
* Observable and testable services
* Clear failure handling and tradeoffs

This project solves the problem of **"How do we deploy and operate ML systems like real software?"**

---

## High-Level Architecture

```
Developer Push
   │
   ▼
GitHub Repository
   │
   ├── CI Pipeline (tests, lint, build)
   ├── Docker Image Build
   └── CD Pipeline
        │
        ▼
Terraform (IaC)
   │
   ├── Azure / AWS / GCP
   ├── Network
   ├── Compute
   └── Monitoring
        │
        ▼
Containerized ML API (FastAPI)
   │
   ├── /predict
   ├── /health
   └── /metrics
        │
        ▼
Prometheus Monitoring
```

---

## Key Capabilities

* Containerized ML training and inference
* FastAPI-based prediction service
* CI/CD with GitHub Actions
* Infrastructure-as-Code using Terraform
* Prometheus metrics for observability
* Cloud-agnostic design (Azure, AWS, GCP)

---

## How to Run Locally

### Prerequisites

* Docker
* Docker Compose
* Python 3.10+

### Steps

```bash
# Clone repository
git clone https://github.com/yourname/enterprise-devops-ml-platform.git
cd enterprise-devops-ml-platform

# Train model
python src/training/train.py

# Build and run API
docker-compose up --build
```

### Verify

* Health check: [http://localhost:8000/health](http://localhost:8000/health)
* Metrics: [http://localhost:8000/metrics](http://localhost:8000/metrics)
* Prediction: POST [http://localhost:8000/predict](http://localhost:8000/predict)

---

## CI/CD Pipeline (How It Works)

### Continuous Integration

Triggered on every push or pull request:

1. Code checkout
2. Python dependency installation
3. Unit tests execution
4. Docker image build

### Continuous Deployment

On merge to main:

1. Terraform plan
2. Terraform apply
3. Deployment to target cloud environment

This enforces **repeatability and safety**.

---

## Failure Scenarios & Handling

| Scenario           | Handling                    |
| ------------------ | --------------------------- |
| Model file missing | API fails fast on startup   |
| Prediction error   | HTTP 500 + logged exception |
| Container crash    | Restart via orchestrator    |
| Bad deployment     | Terraform rollback          |
| High latency       | Prometheus alerting         |

Failures are visible, not silent.

---

## Tradeoffs (Honest Assessment)

* Simple ML model chosen over complex models to emphasize infrastructure
* No real-time streaming to keep scope focused
* Manual Terraform apply instead of GitOps (for clarity)

These tradeoffs are intentional for demonstration purposes.

---

## What I Would Do Next in a Real Enterprise

1. Introduce GitOps (ArgoCD / Flux)
2. Add secrets management (Vault / Cloud Secrets)
3. Add model registry (MLflow)
4. Implement blue-green or canary deployments
5. Add alerting (PagerDuty / Opsgenie)
6. Introduce data validation (Great Expectations)
7. Enforce security scanning (Snyk, Trivy)

---

# ARCHITECTURE.md

## Design Principles

1. **Infrastructure is Code** – no manual setup
2. **CI/CD is Mandatory** – no direct deployments
3. **Observability by Default** – metrics before scale
4. **Cloud Portability** – no vendor lock-in
5. **Failure is Expected** – systems must surface it

---

## Component Breakdown

### ML Training

* Offline batch training
* Versioned artifacts
* Reproducible via scripts

### Model Serving

* FastAPI
* Stateless containers
* Horizontal scalability

### CI/CD

* GitHub Actions
* Automated testing
* Automated builds

### Infrastructure

* Terraform modules
* Environment isolation
* Declarative provisioning

---

## Security Considerations

* No secrets committed
* Environment variable injection
* Minimal container base images
* Network boundaries enforced via IaC

---

## Scalability Considerations

* Stateless API enables horizontal scaling
* Metrics-driven performance tuning
* Cloud-native compute

---

## Why This Architecture

This architecture mirrors how real enterprise teams build ML platforms:

* ML is treated as a **service**, not a notebook
* DevOps is first-class, not an afterthought
* Tradeoffs are explicit

PYTHON CODE 

1️ FastAPI inference service 

src/serving/api.py

from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest
import time
import joblib

app = FastAPI(title="Enterprise ML API")

REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total API requests",
    ["endpoint"]
)

REQUEST_LATENCY = Histogram(
    "api_request_latency_seconds",
    "API request latency"
)

model = joblib.load("model/model.joblib")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
@REQUEST_LATENCY.time()
def predict(payload: dict):
    REQUEST_COUNT.labels(endpoint="/predict").inc()
    features = [payload["value"]]
    prediction = model.predict([features])[0]
    return {"prediction": int(prediction)}


@app.get("/metrics")
def metrics():
    return generate_latest()


This is deployable, observable, and testable.

2️ Training pipeline (REAL)

src/training/train.py

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

def train():
    data = load_iris()
    X, y = data.data, data.target

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    joblib.dump(model, "model/model.joblib")

if __name__ == "__main__":
    train()


Simple on purpose.
We prove pipeline correctness first.

3️ Dockerfile for API (REAL)

docker/Dockerfile.api

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY model/ ./model/

EXPOSE 8000

CMD ["uvicorn", "src.serving.api:app", "--host", "0.0.0.0", "--port", "8000"]

4️ Docker Compose (LOCAL DEVOPS PARITY)
version: "3.8"

services:
  api:
    build:
      context: .
      dockerfile: docker/Dockerfile.api
    ports:
      - "8000:8000"


This matches enterprise dev parity practices.

 CI PIPELINE (REAL, STRICT)

.github/workflows/ci.yml

name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest

      - name: Build Docker image
        run: docker build -f docker/Dockerfile.api .




 Terraform (Azure example — REAL)

infra/terraform/azure/main.tf

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "ml-platform-rg"
  location = "West Europe"
}

resource "azurerm_container_group" "api" {
  name                = "ml-api"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"

  container {
    name   = "api"
    image  = "yourdockerhub/ml-api:latest"
    cpu    = "1"
    memory = "2"

    ports {
      port     = 8000
      protocol = "TCP"
    }
  }
}


