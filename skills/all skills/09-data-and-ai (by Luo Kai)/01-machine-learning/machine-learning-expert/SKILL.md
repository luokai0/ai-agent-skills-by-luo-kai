---
author: luo-kai
name: machine-learning
description: Expert-level machine learning engineering. Use when building ML models, feature engineering, model training/evaluation, scikit-learn, XGBoost, hyperparameter tuning, cross-validation, or deploying ML models to production. Also use when the user mentions 'ML model', 'feature engineering', 'scikit-learn', 'overfitting', 'cross-validation', 'classification', 'regression', 'clustering', 'training data', or 'model accuracy'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Machine Learning Expert

You are an expert ML engineer who bridges research and production, building reliable, well-evaluated, and maintainable ML systems.

## Before Starting

1. **Problem type** — classification, regression, clustering, ranking, recommendation?
2. **Data** — tabular, text, image, time-series? How much data?
3. **Constraints** — latency requirements, interpretability needed, compute budget?
4. **Stage** — exploration, training, evaluation, deployment, monitoring?
5. **Framework** — scikit-learn, XGBoost, PyTorch, TensorFlow, LightGBM?

---

## Core Expertise Areas

- **Problem framing**: defining the ML problem, metrics, baselines, success criteria
- **Data preparation**: EDA, cleaning, feature engineering, train/val/test splits
- **Supervised learning**: linear models, trees, ensembles (RF, XGBoost, LightGBM)
- **Model evaluation**: metrics, cross-validation, learning curves, calibration
- **Hyperparameter tuning**: grid search, random search, Optuna, early stopping
- **Pipelines**: sklearn pipelines, preprocessing, feature unions, column transformers
- **Class imbalance**: SMOTE, class weights, threshold tuning, resampling
- **Production ML**: model serialization, serving, monitoring, drift detection

---

## Key Patterns & Code

### ML Workflow Overview
```
1. Define the problem
   - What are we predicting?
   - What metric matters? (business metric vs ML metric)
   - What is the baseline? (random, majority class, simple rule)

2. Explore the data (EDA)
   - Shape, dtypes, missing values
   - Target distribution (imbalance?)
   - Feature distributions and correlations
   - Outliers and anomalies

3. Prepare data
   - Train / validation / test split (BEFORE any preprocessing)
   - Feature engineering
   - Preprocessing pipeline (fit on train, transform all)

4. Train models
   - Start simple: logistic regression, decision tree
   - Try ensemble: Random Forest, XGBoost, LightGBM
   - Evaluate on validation set

5. Tune hyperparameters
   - Use cross-validation on training set only
   - Optuna for efficient search

6. Final evaluation
   - Evaluate ONCE on test set
   - Confusion matrix, calibration, error analysis

7. Deploy and monitor
   - Serialize model
   - Serve predictions
   - Monitor for data drift and performance degradation
```

### Exploratory Data Analysis
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def eda_report(df: pd.DataFrame, target: str) -> None:
    print(f"Shape: {df.shape}")
    print(f"\nDtypes:\n{df.dtypes}")
    print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    print(f"\nDuplicates: {df.duplicated().sum()}")

    # Target distribution
    if df[target].dtype in ['object', 'category', 'bool']:
        print(f"\nTarget distribution:\n{df[target].value_counts(normalize=True)}")
    else:
        print(f"\nTarget stats:\n{df[target].describe()}")

    # Numeric feature stats
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if target in numeric_cols:
        numeric_cols.remove(target)

    print(f"\nNumeric features ({len(numeric_cols)}):", numeric_cols)
    print(df[numeric_cols].describe())

    # Correlation with target
    if df[target].dtype != 'object':
        correlations = df[numeric_cols].corrwith(df[target]).abs().sort_values(ascending=False)
        print(f"\nTop correlations with target:\n{correlations.head(10)}")

def check_data_quality(df: pd.DataFrame) -> pd.DataFrame:
    report = pd.DataFrame({
        'dtype': df.dtypes,
        'missing': df.isnull().sum(),
        'missing_pct': df.isnull().mean() * 100,
        'unique': df.nunique(),
        'unique_pct': df.nunique() / len(df) * 100,
    })
    return report.sort_values('missing_pct', ascending=False)
```

### Feature Engineering
```python
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

# Custom transformer — fits into sklearn Pipeline
class DateFeatureExtractor(BaseEstimator, TransformerMixin):
    def __init__(self, date_column: str):
        self.date_column = date_column

    def fit(self, X, y=None):
        return self  # nothing to fit

    def transform(self, X):
        X = X.copy()
        dt = pd.to_datetime(X[self.date_column])
        X[f'{self.date_column}_year']      = dt.dt.year
        X[f'{self.date_column}_month']     = dt.dt.month
        X[f'{self.date_column}_day']       = dt.dt.day
        X[f'{self.date_column}_dayofweek'] = dt.dt.dayofweek
        X[f'{self.date_column}_is_weekend']= dt.dt.dayofweek.isin([5, 6]).astype(int)
        X[f'{self.date_column}_quarter']   = dt.dt.quarter
        return X.drop(columns=[self.date_column])

# Interaction features
class InteractionFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, feature_pairs: list[tuple[str, str]]):
        self.feature_pairs = feature_pairs

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        for f1, f2 in self.feature_pairs:
            X[f'{f1}_x_{f2}'] = X[f1] * X[f2]
            X[f'{f1}_div_{f2}'] = X[f1] / (X[f2] + 1e-8)
        return X

# Target encoding (leak-safe using cross-val mean)
class TargetEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, columns: list[str], smoothing: float = 10.0):
        self.columns = columns
        self.smoothing = smoothing
        self.encodings_ = {}

    def fit(self, X, y):
        for col in self.columns:
            stats = pd.DataFrame({'target': y, 'feature': X[col]})
            global_mean = y.mean()
            agg = stats.groupby('feature')['target'].agg(['count', 'mean'])
            # Smoothed encoding reduces overfitting on rare categories
            smooth = (agg['count'] * agg['mean'] + self.smoothing * global_mean) /                      (agg['count'] + self.smoothing)
            self.encodings_[col] = smooth.to_dict()
        return self

    def transform(self, X):
        X = X.copy()
        for col in self.columns:
            X[col] = X[col].map(self.encodings_[col]).fillna(
                np.mean(list(self.encodings_[col].values()))
            )
        return X
```

### Full Training Pipeline
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report, roc_auc_score, confusion_matrix,
    average_precision_score, f1_score
)
import xgboost as xgb
import optuna
import joblib

# 1. Split data FIRST — before any preprocessing
X = df.drop(columns=['target'])
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y  # preserve class ratio
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train,
    test_size=0.2,
    random_state=42,
    stratify=y_train
)

# 2. Define feature groups
num_features = X.select_dtypes(include=[np.number]).columns.tolist()
cat_features = X.select_dtypes(include=['object', 'category']).columns.tolist()

# 3. Build preprocessing pipeline
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler()),
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
])

preprocessor = ColumnTransformer([
    ('num', numeric_transformer, num_features),
    ('cat', categorical_transformer, cat_features),
])

# 4. Build model pipeline
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', xgb.XGBClassifier(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric='auc',
        early_stopping_rounds=50,
        random_state=42,
        n_jobs=-1,
    )),
])

# 5. Fit with early stopping (XGBoost specific)
X_val_preprocessed = preprocessor.fit_transform(X_train)
model.fit(
    X_train, y_train,
    classifier__eval_set=[(preprocessor.transform(X_val), y_val)],
    classifier__verbose=100,
)

# 6. Evaluate
y_pred = model.predict(X_val)
y_prob = model.predict_proba(X_val)[:, 1]

print(classification_report(y_val, y_pred))
print(f"ROC-AUC:  {roc_auc_score(y_val, y_prob):.4f}")
print(f"PR-AUC:   {average_precision_score(y_val, y_prob):.4f}")
print(f"F1 Score: {f1_score(y_val, y_pred):.4f}")
```

### Hyperparameter Tuning with Optuna
```python
import optuna
from sklearn.model_selection import cross_val_score

optuna.logging.set_verbosity(optuna.logging.WARNING)

def objective(trial):
    params = {
        'classifier__n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'classifier__max_depth': trial.suggest_int('max_depth', 3, 10),
        'classifier__learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'classifier__subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'classifier__colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'classifier__min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'classifier__reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10.0, log=True),
        'classifier__reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10.0, log=True),
    }

    model.set_params(**params)

    scores = cross_val_score(
        model, X_train, y_train,
        cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
        scoring='roc_auc',
        n_jobs=-1,
    )

    return scores.mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100, show_progress_bar=True)

print(f"Best AUC: {study.best_value:.4f}")
print(f"Best params: {study.best_params}")

# Apply best params
model.set_params(**{f'classifier__{k}': v for k, v in study.best_params.items()})
model.fit(X_train, y_train)
```

### Class Imbalance Handling
```python
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.utils.class_weight import compute_class_weight

# Option 1: Class weights (simplest, often best)
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train),
    y=y_train
)
weight_dict = dict(zip(np.unique(y_train), class_weights))

model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        class_weight='balanced',  # or weight_dict
        n_estimators=200,
        random_state=42,
    )),
])

# Option 2: SMOTE oversampling (use with caution, only on training set)
pipeline_with_smote = ImbPipeline([
    ('preprocessor', preprocessor),
    ('smote', SMOTE(random_state=42, k_neighbors=5)),
    ('classifier', LogisticRegression(random_state=42)),
])

# Option 3: Threshold tuning (best for calibrated classifiers)
from sklearn.metrics import precision_recall_curve

precision, recall, thresholds = precision_recall_curve(y_val, y_prob)

# Find threshold that maximizes F1
f1_scores = 2 * precision * recall / (precision + recall + 1e-8)
best_threshold = thresholds[f1_scores[:-1].argmax()]

y_pred_tuned = (y_prob >= best_threshold).astype(int)
print(f"Best threshold: {best_threshold:.3f}")
print(f"F1 at best threshold: {f1_score(y_val, y_pred_tuned):.4f}")
```

### Model Evaluation — Comprehensive
```python
from sklearn.metrics import (
    confusion_matrix, classification_report,
    roc_auc_score, roc_curve,
    average_precision_score, precision_recall_curve,
    calibration_curve, brier_score_loss
)
import matplotlib.pyplot as plt

def evaluate_classifier(model, X, y, threshold=0.5):
    y_prob = model.predict_proba(X)[:, 1]
    y_pred = (y_prob >= threshold).astype(int)

    print("=" * 50)
    print("CLASSIFICATION REPORT")
    print("=" * 50)
    print(classification_report(y, y_pred))

    print(f"ROC-AUC:       {roc_auc_score(y, y_prob):.4f}")
    print(f"PR-AUC:        {average_precision_score(y, y_prob):.4f}")
    print(f"Brier Score:   {brier_score_loss(y, y_prob):.4f}")

    # Confusion matrix
    cm = confusion_matrix(y, y_pred)
    tn, fp, fn, tp = cm.ravel()
    print(f"\nConfusion Matrix:")
    print(f"  True Positives:  {tp}")
    print(f"  True Negatives:  {tn}")
    print(f"  False Positives: {fp} (Type I error)")
    print(f"  False Negatives: {fn} (Type II error)")

    # Calibration
    prob_true, prob_pred = calibration_curve(y, y_prob, n_bins=10)
    print(f"\nCalibration (predicted vs actual probability):")
    for pt, pp in zip(prob_true, prob_pred):
        print(f"  Predicted {pp:.2f} → Actual {pt:.2f}")

def plot_roc_pr_curves(models: dict, X, y):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    for name, model in models.items():
        y_prob = model.predict_proba(X)[:, 1]

        # ROC curve
        fpr, tpr, _ = roc_curve(y, y_prob)
        auc = roc_auc_score(y, y_prob)
        ax1.plot(fpr, tpr, label=f'{name} (AUC={auc:.3f})')

        # PR curve
        precision, recall, _ = precision_recall_curve(y, y_prob)
        pr_auc = average_precision_score(y, y_prob)
        ax2.plot(recall, precision, label=f'{name} (AP={pr_auc:.3f})')

    ax1.plot([0, 1], [0, 1], 'k--')
    ax1.set_xlabel('False Positive Rate')
    ax1.set_ylabel('True Positive Rate')
    ax1.set_title('ROC Curve')
    ax1.legend()

    ax2.set_xlabel('Recall')
    ax2.set_ylabel('Precision')
    ax2.set_title('Precision-Recall Curve')
    ax2.legend()

    plt.tight_layout()
    plt.savefig('model_evaluation.png', dpi=150, bbox_inches='tight')
```

### Feature Importance & Explainability
```python
import shap

# Tree-based feature importance
feature_names = (
    num_features +
    model.named_steps['preprocessor']
        .named_transformers_['cat']
        .named_steps['encoder']
        .get_feature_names_out(cat_features).tolist()
)

importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': model.named_steps['classifier'].feature_importances_,
}).sort_values('importance', ascending=False)

print("Top 20 features by importance:")
print(importance_df.head(20))

# SHAP values for individual prediction explanation
X_transformed = model.named_steps['preprocessor'].transform(X_val)
explainer = shap.TreeExplainer(model.named_steps['classifier'])
shap_values = explainer.shap_values(X_transformed)

# Summary plot
shap.summary_plot(shap_values, X_transformed, feature_names=feature_names)

# Single prediction explanation
shap.force_plot(
    explainer.expected_value,
    shap_values[0],
    X_transformed[0],
    feature_names=feature_names
)
```

### Model Serialization & Serving
```python
import joblib
from pathlib import Path
from datetime import datetime
import json

def save_model(model, metadata: dict, output_dir: str):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save model
    model_path = output_dir / f'model_{timestamp}.joblib'
    joblib.dump(model, model_path)

    # Save metadata
    metadata['saved_at'] = timestamp
    metadata['model_path'] = str(model_path)
    metadata_path = output_dir / f'metadata_{timestamp}.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Model saved to {model_path}")
    return model_path

# FastAPI serving
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()
model = joblib.load('models/model_latest.joblib')

class PredictionRequest(BaseModel):
    features: dict

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    model_version: str

@app.post('/predict', response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    df = pd.DataFrame([request.features])
    prob = model.predict_proba(df)[0, 1]
    pred = int(prob >= 0.5)

    return PredictionResponse(
        prediction=pred,
        probability=float(prob),
        model_version='1.0.0',
    )
```

---

## Best Practices

- Split data BEFORE any preprocessing — data leakage is the most common ML mistake
- Always establish a simple baseline before building complex models
- Use stratified splits for imbalanced classification problems
- Fit preprocessors on training data only — transform validation/test separately
- Use cross-validation on training set for model selection — test set is for final eval only
- Evaluate test set ONCE — repeated evaluation on test set leads to overfitting
- Monitor feature drift in production — model performance degrades when data changes
- Use class weights before SMOTE — simpler and often just as effective
- Calibrate probabilities with CalibratedClassifierCV when probabilities matter

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Data leakage | Preprocessing fit on full dataset | Always fit preprocessors on training set only |
| No baseline | No reference to compare model against | Always build a naive baseline first |
| Test set used for tuning | Overfitting to test set | Use test set exactly once for final evaluation |
| Wrong metric | Accuracy on imbalanced data looks good | Use ROC-AUC, F1, PR-AUC for imbalanced problems |
| SMOTE before split | Synthetic samples in validation set | Apply SMOTE only inside cross-validation or on train set |
| Overfitting | High train score, low val score | Regularization, more data, simpler model |
| Underfitting | Low train AND val score | More features, more complex model, less regularization |
| No calibration | Predicted probabilities are wrong | Use CalibratedClassifierCV for probability outputs |

---

## Related Skills

- **deep-learning**: For neural network models
- **llm-engineering**: For LLM-based ML applications
- **mlops-expert**: For deploying and monitoring ML models
- **data-engineering**: For data pipelines feeding ML models
- **python-expert**: For Python ML ecosystem
- **sql-analytics**: For feature engineering with SQL
