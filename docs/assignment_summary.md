# Assignment Summary

The coursework asks for four functions to be completed in the provided Python template.

1. `estimate_model(R, Q)`

   Learn the inverse kinematics mapping from tongue-tip position `(r1, r2)` to tongue configuration `(q1, q2)` using an artificial neural network. The recommended model family is `sklearn.neural_network.MLPRegressor`.

2. `estimate_rmse(Rd, model)`

   Predict tongue configurations for target insect locations and evaluate the resulting tongue-tip positions with forward kinematics. The required metric is root mean squared error in task space.

3. `estimate_probability(Rd, model)`

   Estimate the probability of catching insects when each insect has radius `0.01 m`. A prediction is successful when the Euclidean distance between the target and predicted tongue-tip location is within that radius.

4. `estimate_mass(Q, Qdot, Qddot, Tau)`

   Rearrange the tongue dynamics into a linear parameter-estimation problem and infer the unknown tongue mass from observed positions, velocities, accelerations, and generalized forces.

The submitted code was required to use only the imports already present in the original template and to preserve all template code outside the marked answer regions.
