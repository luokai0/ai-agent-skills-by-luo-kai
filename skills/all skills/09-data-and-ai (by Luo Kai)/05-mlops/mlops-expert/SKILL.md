---
author: luo-kai
name: mlops-expert
description: Expert-level MLOps and ML infrastructure. Use when setting up ML pipelines, model registries (MLflow, W&B), model serving (Triton, BentoML), A/B testing models, data versioning (DVC), feature stores, or monitoring ML models in production. Also use when the user mentions 'MLflow', 'model registry', 'model serving', 'feature store', 'concept drift', 'data drift', 'model monitoring', 'DVC', or 'ML pipeline'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# MLOps Expert

You are an expert in MLOps with deep knowledge of ML pipelines, experiment tracking, model serving, monitoring, and building reliable ML infrastructure.

## Before Starting

1. **Current state** — prototype, moving to production, or scaling existing?
2. **Stack** — MLflow, W&B, SageMaker, Vertex AI, custom?
3. **Problem type** — experiment tracking, model serving, monitoring, pipeline?
4. **Scale** — single model, multiple models, real-time vs batch inference?
5. **Team** — solo data scientist or ML platform team?

---

## Core Expertise Areas

- **Experiment tracking**: MLflow, Weights & Biases, logging metrics/params/artifacts
- **Model registry**: versioning, staging, promoting, lineage tracking
- **Model serving**: FastAPI, BentoML, Triton, SageMaker endpoints
- **Feature stores**: Feast, Hopsworks, online/offline feature serving
- **Data versioning**: DVC, lakeFS, dataset versioning and reproducibility
- **CI/CD for ML**: training pipelines, validation gates, automated retraining
- **Model monitoring**: data drift, concept drift, prediction monitoring, alerting
- **A/B testing**: shadow deployment, canary, champion/challenger patterns

---

## Key Patterns & Code

### MLflow Experiment Tracking
```python
import mlflow
import mlflow.sklearn
import mlflow.pytorch
from mlflow.models.signature import infer_signature
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score

# Configure MLflow
mlflow.set_tracking_uri('http://mlflow-server:5000')
mlflow.set_experiment('customer-churn-prediction')

def train_and_log(X_train, y_train, X_val, y_val, params: dict):
    with mlflow.start_run(run_name='gbm-' + str(params['n_estimators'])) as run:
        # Log parameters
        mlflow.log_params(params)
        mlflow.log_param('train_size', len(X_train))
        mlflow.log_param('val_size', len(X_val))
        mlflow.log_param('feature_count', X_train.shape[1])

        # Train model
        model = GradientBoostingClassifier(**params)
        model.fit(X_train, y_train)

        # Evaluate
        y_prob = model.predict_proba(X_val)[:, 1]
        y_pred = model.predict(X_val)

        metrics = {
            'val_roc_auc':   roc_auc_score(y_val, y_prob),
            'val_f1':        f1_score(y_val, y_pred),
            'val_precision': precision_score(y_val, y_pred),
            'val_recall':    recall_score(y_val, y_pred),
        }
        mlflow.log_metrics(metrics)

        # Log artifacts
        import matplotlib.pyplot as plt
        from sklearn.metrics import ConfusionMatrixDisplay
        fig, ax = plt.subplots()
        ConfusionMatrixDisplay.from_predictions(y_val, y_pred, ax=ax)
        mlflow.log_figure(fig, 'confusion_matrix.png')
        plt.close()

        # Log feature importance
        feat_importance = dict(zip(X_train.columns, model.feature_importances_))
        mlflow.log_dict(feat_importance, 'feature_importance.json')

        # Log model with signature and input example
        signature = infer_signature(X_val, y_prob)
        mlflow.sklearn.log_model(
            model,
            artifact_path='model',
            signature=signature,
            input_example=X_val.iloc[:3],
            registered_model_name='customer-churn-gbm',
        )

        print('Run ID:', run.info.run_id)
        print('ROC-AUC:', metrics['val_roc_auc'])
        return run.info.run_id, metrics

# Hyperparameter search with MLflow
param_grid = [
    {'n_estimators': 100, 'learning_rate': 0.1, 'max_depth': 3},
    {'n_estimators': 200, 'learning_rate': 0.05, 'max_depth': 5},
    {'n_estimators': 300, 'learning_rate': 0.01, 'max_depth': 6},
]

best_run_id = None
best_auc = 0
for params in param_grid:
    run_id, metrics = train_and_log(X_train, y_train, X_val, y_val, params)
    if metrics['val_roc_auc'] > best_auc:
        best_auc = metrics['val_roc_auc']
        best_run_id = run_id

print('Best run:', best_run_id, 'AUC:', best_auc)
```

### Model Registry — Promotion Workflow
```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient('http://mlflow-server:5000')
MODEL_NAME = 'customer-churn-gbm'

# Promote model through stages
def promote_model(run_id: str, model_name: str) -> str:
    # Register model version from run
    model_uri = 'runs:/' + run_id + '/model'
    mv = client.create_model_version(
        name=model_name,
        source=model_uri,
        run_id=run_id,
    )
    version = mv.version
    print('Created version:', version)

    # Transition to Staging
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage='Staging',
        archive_existing_versions=False,
    )
    print('Promoted to Staging')
    return version

def validate_and_promote_to_production(model_name: str, version: str):
    # Load staging model
    model_uri = 'models:/' + model_name + '/Staging'
    model = mlflow.sklearn.load_model(model_uri)

    # Run validation on held-out test set
    y_prob = model.predict_proba(X_test)[:, 1]
    test_auc = roc_auc_score(y_test, y_prob)
    print('Test AUC:', test_auc)

    # Gate: only promote if above threshold
    AUC_THRESHOLD = 0.80
    if test_auc < AUC_THRESHOLD:
        raise ValueError('Model failed validation: AUC ' + str(test_auc) + ' < ' + str(AUC_THRESHOLD))

    # Promote to Production
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage='Production',
        archive_existing_versions=True,  # archive old production model
    )

    # Add description
    client.update_model_version(
        name=model_name,
        version=version,
        description='Test AUC: ' + str(test_auc) + '. Promoted on ' + str(datetime.now().date()),
    )
    print('Promoted to Production!')

# Load production model for inference
def load_production_model(model_name: str):
    model_uri = 'models:/' + model_name + '/Production'
    return mlflow.sklearn.load_model(model_uri)
```

### Model Serving with FastAPI
```python
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import mlflow.sklearn
import numpy as np
import pandas as pd
from typing import Optional
import time
import logging
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI(title='Churn Prediction API', version='1.0.0')

# Load model at startup
model = None
model_version = None

@app.on_event('startup')
async def load_model():
    global model, model_version
    model = mlflow.sklearn.load_model('models:/customer-churn-gbm/Production')
    model_version = '1.0'
    logging.info('Model loaded successfully')

# Metrics
PREDICTIONS_TOTAL = Counter('predictions_total', 'Total predictions', ['model_version'])
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Prediction latency')
PREDICTION_SCORES = Histogram('prediction_score', 'Distribution of prediction scores',
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

class PredictionRequest(BaseModel):
    customer_id: str
    features: dict
    model_version: Optional[str] = None

class PredictionResponse(BaseModel):
    customer_id: str
    churn_probability: float
    churn_prediction: bool
    model_version: str
    latency_ms: float

@app.post('/predict', response_model=PredictionResponse)
async def predict(request: PredictionRequest, background_tasks: BackgroundTasks):
    if model is None:
        raise HTTPException(status_code=503, detail='Model not loaded')

    start = time.time()

    try:
        # Convert to DataFrame
        df = pd.DataFrame([request.features])

        with PREDICTION_LATENCY.time():
            prob = float(model.predict_proba(df)[0, 1])

        latency_ms = (time.time() - start) * 1000

        PREDICTIONS_TOTAL.labels(model_version=model_version).inc()
        PREDICTION_SCORES.observe(prob)

        # Log prediction asynchronously for monitoring
        background_tasks.add_task(
            log_prediction,
            customer_id=request.customer_id,
            features=request.features,
            probability=prob,
        )

        return PredictionResponse(
            customer_id=request.customer_id,
            churn_probability=round(prob, 4),
            churn_prediction=prob >= 0.5,
            model_version=model_version,
            latency_ms=round(latency_ms, 2),
        )
    except Exception as e:
        logging.error('Prediction error: ' + str(e))
        raise HTTPException(status_code=500, detail='Prediction failed')

@app.get('/metrics')
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get('/health')
async def health():
    return {'status': 'healthy', 'model_loaded': model is not None}
```

### Model Monitoring — Drift Detection
```python
import pandas as pd
import numpy as np
from scipy import stats
from dataclasses import dataclass
from typing import Optional

@dataclass
class DriftResult:
    feature: str
    drift_detected: bool
    statistic: float
    p_value: float
    drift_type: str

class DataDriftDetector:
    def __init__(self, reference_data: pd.DataFrame, threshold: float = 0.05):
        self.reference = reference_data
        self.threshold = threshold

    def detect_drift(self, current_data: pd.DataFrame) -> list[DriftResult]:
        results = []
        for col in self.reference.columns:
            if col not in current_data.columns:
                continue
            ref = self.reference[col].dropna()
            cur = current_data[col].dropna()

            if ref.dtype in ['object', 'category']:
                result = self._chi_squared_test(col, ref, cur)
            else:
                result = self._ks_test(col, ref, cur)
            results.append(result)
        return results

    def _ks_test(self, feature: str, ref: pd.Series, cur: pd.Series) -> DriftResult:
        stat, p_value = stats.ks_2samp(ref, cur)
        return DriftResult(
            feature=feature,
            drift_detected=p_value < self.threshold,
            statistic=stat,
            p_value=p_value,
            drift_type='KS',
        )

    def _chi_squared_test(self, feature: str, ref: pd.Series, cur: pd.Series) -> DriftResult:
        all_categories = set(ref.unique()) | set(cur.unique())
        ref_counts = ref.value_counts().reindex(all_categories, fill_value=0)
        cur_counts = cur.value_counts().reindex(all_categories, fill_value=0)
        stat, p_value = stats.chisquare(cur_counts, f_exp=ref_counts * len(cur) / len(ref))
        return DriftResult(
            feature=feature,
            drift_detected=p_value < self.threshold,
            statistic=stat,
            p_value=p_value,
            drift_type='Chi-squared',
        )

# Prediction drift monitoring
class PredictionDriftMonitor:
    def __init__(self, reference_predictions: np.ndarray):
        self.reference = reference_predictions

    def check_prediction_drift(self, current_predictions: np.ndarray) -> dict:
        stat, p_value = stats.ks_2samp(self.reference, current_predictions)

        ref_mean = float(np.mean(self.reference))
        cur_mean = float(np.mean(current_predictions))
        pct_high_risk_ref = float(np.mean(self.reference >= 0.5))
        pct_high_risk_cur = float(np.mean(current_predictions >= 0.5))

        return {
            'drift_detected':     p_value < 0.05,
            'ks_statistic':       stat,
            'p_value':            p_value,
            'ref_mean_score':     ref_mean,
            'current_mean_score': cur_mean,
            'score_change':       cur_mean - ref_mean,
            'pct_high_risk_ref':  pct_high_risk_ref,
            'pct_high_risk_cur':  pct_high_risk_cur,
        }

# Scheduled monitoring job
def run_monitoring_job(model_name: str, lookback_days: int = 7):
    # Load reference data (training data distribution)
    ref_data = load_reference_data(model_name)
    detector = DataDriftDetector(ref_data)

    # Load recent predictions
    recent_data = load_recent_predictions(model_name, lookback_days)

    drift_results = detector.detect_drift(recent_data)
    drifted_features = [r for r in drift_results if r.drift_detected]

    if drifted_features:
        alert_message = ('Data drift detected in model ' + model_name +
                         '. Features: ' + str([r.feature for r in drifted_features]))
        send_alert(alert_message)
        log_metric('drift_features_count', len(drifted_features))

    return drift_results
```

### DVC — Data Version Control
```yaml
# dvc.yaml — define ML pipeline stages
stages:
  prepare:
    cmd: python src/prepare.py
    deps:
      - src/prepare.py
      - data/raw/events.csv
    outs:
      - data/processed/features.parquet
      - data/processed/labels.parquet
    params:
      - prepare.test_size
      - prepare.random_seed

  train:
    cmd: python src/train.py
    deps:
      - src/train.py
      - data/processed/features.parquet
      - data/processed/labels.parquet
    outs:
      - models/model.pkl
    params:
      - train.n_estimators
      - train.learning_rate
      - train.max_depth
    metrics:
      - metrics/train_metrics.json:
          cache: false

  evaluate:
    cmd: python src/evaluate.py
    deps:
      - src/evaluate.py
      - models/model.pkl
      - data/processed/features.parquet
    metrics:
      - metrics/eval_metrics.json:
          cache: false
    plots:
      - plots/roc_curve.csv
      - plots/confusion_matrix.csv

# params.yaml
# prepare:
#   test_size: 0.2
#   random_seed: 42
# train:
#   n_estimators: 200
#   learning_rate: 0.05
#   max_depth: 5
```

```bash
# DVC commands
dvc init                          # initialize DVC in git repo
dvc remote add -d myremote s3://mybucket/dvc-store
dvc add data/raw/events.csv       # track large file
dvc push                          # push data to remote
dvc pull                          # pull data from remote
dvc repro                         # run pipeline (only changed stages)
dvc params diff                   # compare params
dvc metrics show                  # show metrics
dvc metrics diff                  # compare metrics between commits
dvc plots show plots/roc_curve.csv
```

### CI/CD for ML Pipeline
```yaml
# .github/workflows/ml-pipeline.yml
name: ML Training Pipeline

on:
  push:
    paths:
      - 'src/**'
      - 'params.yaml'
  schedule:
    - cron: '0 2 * * 1'  # weekly retraining

jobs:
  train-and-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Pull DVC data
        run: |
          dvc remote modify myremote access_key_id ${{ secrets.AWS_ACCESS_KEY_ID }}
          dvc remote modify myremote secret_access_key ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          dvc pull

      - name: Run pipeline
        run: dvc repro

      - name: Check metrics gate
        run: |
          python scripts/check_metrics.py --min-auc 0.80
        # This script reads metrics/eval_metrics.json and fails if below threshold

      - name: Push model to registry
        if: github.ref == 'refs/heads/main'
        run: python scripts/register_model.py
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_URI }}

      - name: Commit DVC artifacts
        run: |
          dvc push
          git add dvc.lock metrics/
          git commit -m 'Update model artifacts [skip ci]' || true
          git push
```

---

## Best Practices

- Track every experiment — parameters, metrics, and artifacts — from day one
- Treat ML pipelines like software — version control code AND data AND models
- Define validation gates before promoting models to production
- Monitor both data drift AND prediction drift — they indicate different problems
- Log predictions to a feature store for future retraining and analysis
- Use shadow deployments before full canary — compare outputs without user impact
- Automate retraining triggers based on drift detection, not just schedules
- Make pipelines idempotent — re-running should produce the same result

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| No experiment tracking | Cannot reproduce results or compare models | Use MLflow or W&B from the start |
| Training-serving skew | Different preprocessing in training vs serving | Package preprocessing with model |
| No data versioning | Cannot reproduce model trained on old data | Use DVC or Delta Lake snapshots |
| Promoting without validation | Bad model silently degrades production | Add metric gates to promotion pipeline |
| No monitoring | Model silently degrades over time | Monitor drift and prediction quality |
| Manual deployments | Inconsistent, error-prone, no history | Automate with CI/CD pipeline |
| Model without signature | Input/output contract unclear | Always log model with MLflow signature |
| No rollback plan | Bad deploy = extended outage | Keep previous model in registry, automate rollback |

---

## Related Skills

- **machine-learning**: For building and evaluating ML models
- **deep-learning**: For training and fine-tuning neural networks
- **docker-expert**: For containerizing ML training and serving
- **kubernetes-expert**: For deploying ML workloads at scale
- **monitoring-expert**: For ML-specific observability patterns
- **cicd-expert**: For ML pipeline CI/CD automation