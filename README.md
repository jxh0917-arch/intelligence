# Chameleon's Tongue: Inverse Kinematics and Dynamics Estimation

This repository presents a reproducible workflow for the chameleon tongue coursework problem from 7CCEMIAA Intelligence and Autonomy. The work combines inverse kinematics learning, task-space evaluation, catch-probability estimation, and linear dynamics parameter identification.

## Project Scope

The system models a simplified planar chameleon tongue with two generalized coordinates: tongue angle and extension length. The main objectives are:

- learn the inverse mapping from target location `(r1, r2)` to tongue configuration `(q1, q2)` using `MLPRegressor`;
- evaluate targeting accuracy as root mean squared error in Cartesian space;
- estimate the probability of catching an insect with radius `0.01 m`;
- identify the tongue mass from observed state, acceleration, and generalized force data.

## Repository Structure

```text
.
|-- data/raw/                     # Coursework CSV data used by the workflow
|-- docs/
|   |-- assignment_summary.md      # Summarised task requirements
|   |-- data_notice.md             # Publication note for coursework data
|   |-- github_publish_guide.md    # Steps for publishing the local repo
|   |-- project_report.md          # Concise academic report
|   |-- model_selection.md         # Follow-up analysis motivated by feedback
|   |-- teacher_feedback.md        # Marking feedback and interpretation
|   `-- original_submission/       # Original submission files kept for provenance
|-- scripts/compare_mlp_configs.py # Compact architecture comparison
|-- scripts/publish_to_github.ps1  # Helper for pushing to a new GitHub repo
|-- scripts/run_workflow.py        # End-to-end reproducibility script
|-- src/chameleon_tongue/          # Importable implementation
|-- tests/                         # Lightweight validation tests
|-- .github/workflows/python.yml   # GitHub Actions test workflow
|-- requirements.txt
`-- pyproject.toml
```

The original `work.py` submission is preserved under `docs/original_submission/`. The importable implementation in `src/chameleon_tongue/` keeps the same modelling logic while making the workflow easier to run, test, and present.

## Methodology

For inverse kinematics, the submitted model uses a two-layer MLP with `tanh` activations and the `lbfgs` optimizer. The model learns from observed end-effector locations and corresponding tongue configurations. Predicted configurations are then evaluated through forward kinematics, which gives a physically meaningful task-space error rather than only a configuration-space error.

For catch probability, each predicted tongue-tip location is compared with its desired insect location. A catch is counted when the Euclidean error is at most `0.01 m`.

For mass estimation, the tongue dynamics are rearranged into a linear regression problem. The two equations of motion are stacked into a single feature vector, and the mass is estimated with a zero-intercept linear model.

## Results Context

The marked submission received a final total of `86/100`. The RMSE, catch-probability, and mass-estimation components were assessed as extremely accurate. The main improvement area identified in feedback was the inverse-kinematics model complexity: the MLP achieved high accuracy, but the hidden-layer capacity was larger than necessary, so future work should compare smaller architectures and tune regularisation for generalisation.

The included model-selection script demonstrates this follow-up direction. On one deterministic validation split, a compact `50x50` MLP used `2802` trainable parameters compared with `41202` in the submitted `200x200` model, while improving validation task-space RMSE from `0.006144 m` to `0.004803 m`.

## Reproduced Metrics

Running `python scripts/run_workflow.py` on the included CSV data produced:

| Metric | Value |
| --- | ---: |
| Task-space RMSE | `0.0035456263 m` |
| Catch probability, radius `0.01 m` | `0.90` |
| Estimated tongue mass | `0.5488135039 kg` |

## Running the Workflow

Create an environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the full workflow:

```powershell
python scripts/run_workflow.py
```

The script writes `outputs/metrics.json` and prints the same metrics to the terminal.

To experiment with a smaller MLP:

```powershell
python scripts/run_workflow.py --hidden-layer-sizes 80,80 --max-iter 4000
```

To compare several model capacities on a validation split:

```powershell
python scripts/compare_mlp_configs.py
```

To publish after creating an empty GitHub repository:

```powershell
.\scripts\publish_to_github.ps1 -RepositoryUrl https://github.com/jxh0917-arch/chameleon-tongue-workflow.git
```

## Validation

Run the test suite:

```powershell
pytest -q
```

The tests validate the forward kinematics, catch-probability calculation, and mass-estimation formulation on controlled synthetic data. GitHub Actions runs the same checks on each push and pull request.

## Notes On Academic Use

The course handout itself is not committed here to avoid redistributing copyrighted module material. The repository instead includes a concise task summary and the preserved source files needed to understand and reproduce the submitted work.
