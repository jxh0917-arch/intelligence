"""Coursework functions in an importable form."""

from __future__ import annotations

import math

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor

from .plant import ChameleonTongue


def _as_samples(matrix: np.ndarray) -> np.ndarray:
    """Convert coursework arrays from `(features, samples)` to samples first."""

    return np.asarray(matrix, dtype=float).T


def estimate_model(
    R: np.ndarray,
    Q: np.ndarray,
    hidden_layer_sizes: tuple[int, ...] = (200, 200),
    activation: str = "tanh",
    solver: str = "lbfgs",
    max_iter: int = 15000,
    alpha: float = 1e-7,
    tol: float = 1e-9,
    random_state: int = 1,
) -> MLPRegressor:
    """Learn inverse kinematics from tip locations to tongue configurations."""

    model = MLPRegressor(
        hidden_layer_sizes=hidden_layer_sizes,
        activation=activation,
        solver=solver,
        max_iter=max_iter,
        alpha=alpha,
        tol=tol,
        random_state=random_state,
    )
    model.fit(_as_samples(R), _as_samples(Q))
    return model


def _predict_tip_locations(Rd: np.ndarray, model: MLPRegressor) -> np.ndarray:
    """Predict tongue-tip locations after inverse-kinematics inference."""

    targets = _as_samples(Rd)
    predicted_q = model.predict(targets)
    plant = ChameleonTongue()
    return np.vstack([plant.forward_kinematics(q) for q in predicted_q])


def estimate_rmse(Rd: np.ndarray, model: MLPRegressor) -> float:
    """Estimate Cartesian RMSE between desired and reached target locations."""

    targets = _as_samples(Rd)
    predicted_r = _predict_tip_locations(Rd, model)
    return math.sqrt(mean_squared_error(targets, predicted_r))


def estimate_probability(Rd: np.ndarray, model: MLPRegressor) -> float:
    """Estimate catch probability for insects with radius 0.01 m."""

    targets = _as_samples(Rd)
    predicted_r = _predict_tip_locations(Rd, model)
    errors = np.linalg.norm(targets - predicted_r, axis=1)
    return float(np.mean(errors <= 0.01))


def estimate_mass(Q: np.ndarray, Qdot: np.ndarray, Qddot: np.ndarray, Tau: np.ndarray) -> float:
    """Estimate tongue mass by solving the linearized dynamics relation."""

    q = _as_samples(Q)
    qdot = _as_samples(Qdot)
    qddot = _as_samples(Qddot)
    tau = _as_samples(Tau)

    q1 = q[:, 0]
    q2 = q[:, 1]
    qd1 = qdot[:, 0]
    qd2 = qdot[:, 1]
    qdd1 = qddot[:, 0]
    qdd2 = qddot[:, 1]
    tau1 = tau[:, 0]
    tau2 = tau[:, 1]

    gravity = 9.81
    torque_feature = (q2**2 * qdd1) + (2.0 * q2 * qd2 * qd1) + (gravity * q2 * np.cos(q1))
    force_feature = qdd2 - (q2 * qd1**2) + (gravity * np.sin(q1))

    features = np.concatenate([torque_feature, force_feature]).reshape(-1, 1)
    targets = np.concatenate([tau1, tau2])

    regressor = LinearRegression(fit_intercept=False)
    regressor.fit(features, targets)
    return float(regressor.coef_[0])
