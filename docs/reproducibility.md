# Reproducibility

This repository is designed so that the main results can be regenerated from the committed source code and CSV data.

## Environment

Recommended Python version: `3.11` or newer.

Install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Commands

Run unit tests:

```powershell
pytest -q
```

Run the end-to-end workflow:

```powershell
python scripts/run_workflow.py
```

Run model-selection analysis:

```powershell
python scripts/compare_mlp_configs.py
```

## Expected Outputs

`scripts/run_workflow.py` should report:

| Metric | Expected value |
| --- | ---: |
| Task-space RMSE | `0.0035456263 m` |
| Catch probability | `0.90` |
| Estimated mass | `0.5488135039 kg` |

`scripts/compare_mlp_configs.py` should identify the compact `50x50` model as a strong validation candidate for this deterministic split, with validation task-space RMSE near `0.004803 m`.

## Continuous Integration

The GitHub Actions workflow installs dependencies, runs tests, executes the end-to-end workflow, and runs the model-selection script. This checks both the reusable package code and the reproducibility scripts.
