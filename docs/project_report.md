# Project Report

## Abstract

This project investigates a simplified model of chameleon tongue control using supervised learning and dynamics-based parameter estimation. The work combines an inverse-kinematics neural network with physically grounded evaluation metrics and a linear regression formulation for identifying tongue mass. The resulting workflow is reproducible from the provided CSV data and is supported by automated tests.

## Problem Formulation

The tongue is represented as a two-degree-of-freedom planar system. The first coordinate is the launch angle, and the second is the tongue extension length. Given an observed tongue-tip position `(r1, r2)`, the inverse-kinematics task is to infer the configuration `(q1, q2)` required to reach that point.

The evaluation is carried out in task space. Instead of measuring only the error between predicted and observed configurations, predicted configurations are passed through forward kinematics and compared with the desired target locations. This makes the RMSE and catch-probability metrics directly interpretable in terms of physical performance.

## Methods

The inverse-kinematics model uses `MLPRegressor` with two hidden layers of 200 units, `tanh` activation, the `lbfgs` optimizer, and a fixed random state. This high-capacity configuration was effective for the submitted task, although model-selection analysis is included to explore smaller alternatives.

The probability calculation treats each target as a successful catch when the tongue-tip error is within `0.01 m`, matching the assumed insect radius.

For mass estimation, the two equations of motion are rearranged so that the unknown mass appears as a scalar parameter in a linear system. Stacking the torque and force equations produces an overdetermined regression problem, which is solved with a zero-intercept linear model.

## Reproduced Results

The end-to-end workflow reproduced the following values:

| Quantity | Value |
| --- | ---: |
| Task-space RMSE | `0.0035456263 m` |
| Catch probability | `0.90` |
| Estimated tongue mass | `0.5488135039 kg` |

The instructor feedback confirms that the RMSE, probability, and mass estimates were extremely accurate. The principal limitation was model complexity: the neural network used more hidden units than necessary for the scale of the data.

## Reflection

The main strength of the solution is the connection between machine-learning prediction and the physical system. The model is not judged only by numerical loss in the learned inverse map; it is evaluated by the actual tongue-tip location after forward kinematics. This gives a clearer engineering interpretation of the output.

The main follow-up is systematic model selection. A smaller network with stronger regularisation and lower iteration budget may generalise better while keeping the same physical evaluation framework. In the included validation split, a compact `50x50` model reduced the trainable parameter count from `41202` to `2802` while improving validation task-space RMSE from `0.006144 m` to `0.004803 m`. The comparison script in `scripts/compare_mlp_configs.py` supports further exploration.
