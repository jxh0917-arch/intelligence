# Presentation Notes

## One-Minute Overview

This project studies a simplified chameleon tongue control problem as a combination of machine learning and physical modelling. The first part learns inverse kinematics: given a desired prey location, the model predicts the tongue angle and extension length required to reach it. The second part evaluates the prediction in Cartesian task space, estimates catch probability using a physical insect radius, and identifies the tongue mass from the system dynamics.

## Key Technical Points

- The inverse-kinematics model is an `MLPRegressor` trained to map tongue-tip positions `(r1, r2)` to configurations `(q1, q2)`.
- Evaluation is performed after forward kinematics, so the reported RMSE reflects physical targeting error rather than only configuration-space error.
- Catch probability is computed using a `0.01 m` radius threshold, which turns the regression output into a task-level performance measure.
- Mass estimation is formulated as a linear regression problem by rearranging the dynamics equation so that the unknown mass is the scalar parameter.
- A follow-up model-selection script compares smaller MLPs and demonstrates that a compact `50x50` network can reduce parameter count substantially while preserving strong validation performance.

## Results To Emphasise

| Result | Interpretation |
| --- | --- |
| RMSE `0.0035456263 m` | The predicted tongue configurations reach the desired targets with low task-space error. |
| Catch probability `0.90` | Nine out of ten target insects are caught under the `0.01 m` radius assumption. |
| Mass `0.5488135039 kg` | The linear dynamics formulation recovers the unknown mass from observed motion and force data. |
| Compact `50x50` MLP | Reduces parameters from `41202` to `2802` in the validation comparison. |

## Suggested Narrative

1. Start with the physical system: a two-degree-of-freedom tongue model with angle and extension length.
2. Explain why inverse kinematics is learned rather than hard-coded: the model maps observed target locations to required configurations.
3. Stress that the evaluation returns to physics: predictions are passed through forward kinematics before RMSE and catch probability are computed.
4. Explain the dynamics identification step as a separate but complementary problem: using motion and force observations to estimate mass.
5. Close with the model-complexity reflection: the original MLP performed well, and the follow-up comparison shows how the workflow can be extended toward a more compact model.

## Possible Questions And Answers

**Why use task-space RMSE rather than only comparing predicted `q` values?**

Because the practical goal is to hit a target in Cartesian space. Two configuration errors can have different physical consequences, so evaluating the reached tongue-tip location is more meaningful.

**Why is the mass estimation solved with linear regression?**

After rearranging the dynamics, the unknown mass appears as a scalar multiplier of known feature terms. This makes the parameter estimation linear in the unknown mass, even though the original dynamics contain nonlinear state terms.

**What is the main limitation of the submitted model?**

The neural network has high capacity relative to the data size. The model-selection analysis addresses this by comparing smaller architectures and showing a better accuracy-complexity trade-off for a compact two-layer model on the validation split.
