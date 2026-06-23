"""Planar chameleon tongue plant model."""

from __future__ import annotations

import math

import numpy as np


class ChameleonTongue:
    """Two-degree-of-freedom tongue model used by the coursework."""

    def __init__(self, mass: float = 0.1, gravity: float = 9.81) -> None:
        self.dimq = 2
        self.dimr = 2
        self.m = mass
        self.q = np.array([0.0, 0.0]).T
        self.qdot = np.array([0.0, 0.0]).T
        self.tau = np.array([0.0, 0.0]).T
        self.g = gravity

    def set_m(self, mass: float) -> None:
        """Set the plant mass to a non-default value."""

        self.m = mass

    def forward_kinematics(self, q: np.ndarray) -> np.ndarray:
        """Map tongue configuration `[q1, q2]` to tip position `[r1, r2]`."""

        q = np.asarray(q, dtype=float).ravel()
        return np.array([q[1] * math.cos(q[0]), q[1] * math.sin(q[0])])

    def get_MCG(self, q: np.ndarray, qdot: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return inertia, Coriolis/centrifugal, and gravity terms."""

        q = np.asarray(q, dtype=float).ravel()
        qdot = np.asarray(qdot, dtype=float).ravel()
        m = self.m
        g = self.g

        matrix_m = np.array(
            [
                [m * q[1] ** 2, 0.0],
                [0.0, m],
            ]
        )
        matrix_c = np.array(
            [
                [0.0, 2.0 * m * q[1] * qdot[0]],
                [-m * q[1] * qdot[0], 0.0],
            ]
        )
        vector_g = np.array(
            [
                m * g * q[1] * math.cos(q[0]),
                m * g * math.sin(q[0]),
            ]
        ).T

        return matrix_m, matrix_c, vector_g

    def get_joint_acceleration(self, q: np.ndarray, qdot: np.ndarray, tau: np.ndarray) -> np.ndarray:
        """Compute joint accelerations from state and generalized forces."""

        matrix_m, matrix_c, vector_g = self.get_MCG(q, qdot)
        qdot = np.asarray(qdot, dtype=float).ravel()
        tau = np.asarray(tau, dtype=float).ravel()
        return np.linalg.solve(matrix_m, tau - matrix_c @ qdot - vector_g).ravel()


chameleon = ChameleonTongue
