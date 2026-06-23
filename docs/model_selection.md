# Model-Selection Analysis

The original submission used a high-capacity MLP with two hidden layers of 200 units. Instructor feedback noted that the model was accurate but larger than necessary. The repository therefore includes `scripts/compare_mlp_configs.py`, which evaluates smaller alternatives using a deterministic train/validation split.

The comparison reports:

- number of trainable parameters;
- configuration-space MSE on the training split;
- configuration-space MSE on the validation split;
- task-space validation RMSE after forward kinematics;
- convergence-warning status.

Run the analysis with:

```powershell
python scripts/compare_mlp_configs.py
```

This analysis is intended as model-selection evidence rather than a replacement for the submitted coursework solution. It keeps the original method visible while documenting a clear path toward a more compact model.

## Reproduced Comparison

Using `random_state=1` and an `80/20` train/validation split, the comparison produced:

| Model | Hidden layers | Parameters | Train MSE in `q` | Validation MSE in `q` | Validation RMSE in task space |
| --- | ---: | ---: | ---: | ---: | ---: |
| Submitted | `200x200` | `41202` | `2.75e-05` | `4.24e-04` | `0.006144 m` |
| Compact single layer | `80` | `402` | `2.41e-04` | `2.05e-03` | `0.007578 m` |
| Compact two layer | `50x50` | `2802` | `1.88e-05` | `5.72e-04` | `0.004803 m` |
| Regularised small | `30` | `152` | `9.71e-04` | `4.57e-03` | `0.014131 m` |

The compact two-layer model is a useful candidate for future work: it uses around `6.8%` of the submitted model's parameters while achieving the best validation task-space RMSE in this split. This does not invalidate the submitted model, but it supports the feedback that a smaller architecture could provide a better accuracy-complexity trade-off.
