# ML Experiment

Scaffold a new model-training script or audit an existing one for the problems that make ML results unreproducible or quietly wrong — missing seeds, data leakage between train/val/test, and no baseline comparison. Framework-agnostic.

Trigger: `/ml-experiment`

## How It Works

1. **Mode and data shape first** — new script or audit an existing one, and is the data time-ordered or i.i.d.? This decides the split strategy and is the biggest source of silent leakage.
2. **Split strategy by data shape** — random split with a fixed seed for i.i.d. data; a time-based split or walk-forward for time-ordered data (reuse [MC Analysis](mc-analysis.md) if the project already has one).
3. **Leakage checks** — scalers/encoders fit on the full dataset before splitting, target-derived features, duplicate rows across splits, rolling windows that reach past the prediction point.
4. **Seeds fixed and logged** — numpy, framework, and split `random_state`, alongside hyperparameters and a data version/hash, so a run can be reproduced from its own logged settings.
5. **Baseline required** — every metric is logged next to a naive baseline (majority-class, mean, previous-value) so an improvement is a real comparison, not an isolated number.
6. **Audit mode greps for concrete bugs** — `fit_transform` before a split, `train_test_split` with no `random_state`, `shuffle=True` on dated data, target-derived features, metrics printed with no baseline.
7. **Report or generate accordingly** — scaffold mode produces a training script following the examples below; audit mode reports file:line findings in the same severity-style format as [Secrets Audit](secrets-audit.md).

## Leakage From Fitting on the Full Dataset

!!! warning "Bad: scaler sees the test set before the split \"happens\""
    ```python
    scaler = StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, random_state=42)
    ```

!!! example "Good: split first, fit only on train"
    ```python
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    ```

## Time-Ordered Data Split Randomly

!!! warning "Bad: shuffles away the thing you're trying to predict"
    ```python
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)
    ```

!!! example "Good: train on the past, test on the future"
    ```python
    split_date = "2026-01-01"
    train = df[df["date"] < split_date]
    test = df[df["date"] >= split_date]
    ```

## Reporting a Result With No Baseline

!!! warning "Bad: a number with nothing to compare it to"
    ```
    Model accuracy: 0.92
    ```

!!! example "Good: the number that actually tells you something"
    ```
    Model accuracy: 0.92  |  Majority-class baseline: 0.90  |  Seed: 42  |  Data hash: a1b2c3d
    ```

## Notes

- A model that beats its baseline by less than its run-to-run seed variance hasn't beaten anything — check under 2-3 seeds before claiming a real improvement.
- Suspiciously high accuracy/R² is a prompt to re-check the split for leakage, not a reason to celebrate.
- Framework-agnostic by design — a checklist, not a scaffold tied to any specific library. Existing project training conventions win over anything suggested here.
- Comparing a production model against its original backtest is [Trade Review](trade-review.md)'s job, not this skill's.
- Natural habit points: before trusting a metric improvement enough to act on it, before merging a new model into a pipeline, and whenever a training script reports a number that seems unusually good.
