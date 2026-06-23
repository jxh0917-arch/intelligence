# Instructor Feedback

Final total: `86/100`.

## Summary

The submission was assessed as excellent overall. The model was configured with `MLPRegressor`, and the numerical estimates for RMSE, catch probability, and mass were extremely accurate.

## Question-Level Feedback

- Q1: `11/25`
  - High training accuracy with MSE less than `1e-4`.
  - Moderate generalisation with MSE less than `1e-2`.
  - The model used a relatively large number of hidden units and a moderate number of hidden layers.
  - Suggested improvement: use a simpler architecture with fewer hidden units, lower `max_iter`, and additional hyperparameter tuning.

- Q2: `25/25`
  - RMSE estimate was extremely accurate, with negligible difference from the expected value.

- Q3: `25/25`
  - Catch-probability estimate was extremely accurate, with negligible difference from the expected value.

- Q4: `25/25`
  - Mass estimate was extremely accurate, with negligible difference from the expected value.

## Interpretation

The strongest parts of the work are the physically grounded evaluation steps and dynamics parameter identification. The main modelling trade-off is that the inverse-kinematics neural network is highly expressive. In a research workflow, this motivates a follow-up model-selection stage comparing smaller MLPs, regularisation settings, and validation-set performance.
