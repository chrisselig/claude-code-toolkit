---
name: ml-experiment
description: Scaffold a new model-training script or audit an existing one for the problems that make ML results unreproducible or quietly wrong — missing seeds, data leakage between train/val/test, and no baseline comparison. Framework-agnostic (sklearn, xgboost, statsmodels, pytorch). Use when starting a new model-training script, adding a model to an existing pipeline, or reviewing a training script that reports suspiciously good results.
argument-hint: "[new | audit] [path]"
---

# ML Experiment

Make a model-training run reproducible and honest before trusting its metrics. This skill doesn't pick a framework or algorithm — it checks the three things that are wrong in almost every "it got 98% accuracy" training script: no fixed seed, leakage between splits, and no baseline to compare against.

## Steps

1. **Ask which mode**: starting a new training script (scaffold the checklist into code) or auditing an existing one (review for the failure modes below). Also ask: is the data time-ordered (forecasting, trading, any "predict the future from the past" problem) or i.i.d. (rows are independent)? This changes the split strategy and is the single most common source of silent leakage.

2. **Pick the split strategy by data shape**:
   - i.i.d. data: random train/val/test split with a fixed `random_state`.
   - Time-ordered data: a time-based split (train on earlier dates, test on later ones) or walk-forward validation — never a random shuffle. If this project already has a walk-forward setup for a specific domain (e.g. the forex bot), reuse [MC Analysis](../mc-analysis/SKILL.md)'s approach instead of inventing a new one.

3. **Check for leakage** — the thing that produces a great-looking metric and a useless model:
   - Scalers/encoders/imputers fit on the full dataset before splitting, instead of `fit` on train only and `transform` on val/test.
   - A feature derived from the target (or from something only known after the target is known).
   - Duplicate or near-duplicate rows landing in both train and test (common after a join or after oversampling).
   - For time-ordered data: any feature computed using a rolling/aggregate window that reaches past the prediction point.

4. **Fix every seed and log it** — numpy's, the framework's, and the split function's `random_state` — alongside the hyperparameters and a hash or version tag for the input data. A run that can't be reproduced from its own logged settings isn't a result, it's an anecdote.

5. **Require a baseline before trusting a metric.** Log the model's metric next to a naive baseline computed the same way (previous-value/mean for regression, majority-class for classification, a simple linear model if the real model is complex). "92% accuracy" means nothing on its own; "92% vs. a 90% majority-class baseline" means the model barely helps.

6. **In audit mode**, grep the script for the concrete bugs, not just the concepts: `fit_transform` called on a variable that is later split, a `train_test_split` call with no `random_state`, `shuffle=True` on data that has a date/time column, a feature column that's a transform of the target column, and any metric printed without a baseline nearby in the same output.

7. **Report or generate accordingly** — scaffold mode produces the training script structured per the examples below; audit mode reports findings as file:line plus which failure mode it matches, same severity-style format as [Secrets Audit](../secrets-audit/SKILL.md)'s report (not a redaction concern here, just "named and located").

## Examples

### Leakage from fitting on the full dataset

**BAD** — scaler sees the test set before the split "happens":
```python
scaler = StandardScaler().fit(X)
X_scaled = scaler.transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, random_state=42)
```

**GOOD** — split first, fit only on train:
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
scaler = StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
```

### Time-ordered data split randomly

**BAD** — shuffles away the thing you're trying to predict:
```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)
```

**GOOD** — train on the past, test on the future:
```python
split_date = "2026-01-01"
train = df[df["date"] < split_date]
test = df[df["date"] >= split_date]
```

### Reporting a result with no baseline

**BAD** — a number with nothing to compare it to:
```
Model accuracy: 0.92
```

**GOOD** — the number that actually tells you something:
```
Model accuracy: 0.92  |  Majority-class baseline: 0.90  |  Seed: 42  |  Data hash: a1b2c3d
```

## Notes

- A model that beats its baseline by less than its run-to-run variance (different seed, same everything else) hasn't beaten anything — run it under 2-3 seeds before claiming an improvement is real.
- Leakage usually produces a result that looks *too good* — treat suspiciously high accuracy/R² as a prompt to re-check the split, not a reason to celebrate.
- This skill is framework-agnostic by design: it's a checklist, not a scaffold tied to sklearn or any specific library. If the project already has training conventions, follow those over anything suggested here.
- For comparing a model already in production against its original backtest, that's [Trade Review](../trade-review/SKILL.md)'s job, not this skill's.
- Natural habit points: before trusting a metric improvement enough to act on it, before merging a new model into a pipeline, and whenever a training script reports a number that seems unusually good.
