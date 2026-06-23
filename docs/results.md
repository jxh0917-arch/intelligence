# Reproduced Results

The end-to-end workflow was run with the submitted model configuration:

- `MLPRegressor`
- hidden layers: `(200, 200)`
- activation: `tanh`
- solver: `lbfgs`
- `max_iter`: `15000`
- random state: `1`

The reproduced metrics were:

| Metric | Value |
| --- | ---: |
| Task-space RMSE | `0.0035456263 m` |
| Catch probability, radius `0.01 m` | `0.90` |
| Estimated tongue mass | `0.5488135039 kg` |

These results are consistent with the marking feedback: the evaluation and dynamics-estimation stages are highly accurate, while the inverse-kinematics model would benefit from follow-up model selection to reduce neural-network capacity.
