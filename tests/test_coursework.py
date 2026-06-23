import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chameleon_tongue.coursework import estimate_mass, estimate_probability, estimate_rmse
from chameleon_tongue.plant import ChameleonTongue


class PolarInverseModel:
    def predict(self, targets):
        angles = np.arctan2(targets[:, 1], targets[:, 0])
        lengths = np.linalg.norm(targets, axis=1)
        return np.column_stack([angles, lengths])


def test_forward_kinematics_maps_polar_configuration_to_cartesian_position():
    plant = ChameleonTongue()
    result = plant.forward_kinematics(np.array([np.pi / 4.0, np.sqrt(2.0)]))
    np.testing.assert_allclose(result, np.array([1.0, 1.0]), atol=1e-12)


def test_probability_and_rmse_are_exact_for_analytic_inverse_model():
    targets = np.array(
        [
            [1.0, 0.0, -1.0, 0.0],
            [0.0, 1.0, 0.0, -1.0],
        ]
    )
    model = PolarInverseModel()
    assert estimate_probability(targets, model) == 1.0
    assert estimate_rmse(targets, model) < 1e-12


def test_estimate_mass_recovers_synthetic_plant_mass():
    plant = ChameleonTongue(mass=0.17)
    q_samples = np.array(
        [
            [0.2, 0.6],
            [0.4, 0.8],
            [0.7, 1.0],
            [1.0, 0.9],
        ]
    )
    qdot_samples = np.array(
        [
            [0.1, -0.2],
            [0.3, 0.1],
            [-0.2, 0.4],
            [0.5, -0.1],
        ]
    )
    qddot_samples = np.array(
        [
            [0.2, 0.3],
            [-0.1, 0.5],
            [0.4, -0.2],
            [0.1, -0.4],
        ]
    )

    tau_samples = []
    for q, qdot, qddot in zip(q_samples, qdot_samples, qddot_samples):
        matrix_m, matrix_c, vector_g = plant.get_MCG(q, qdot)
        tau_samples.append(matrix_m @ qddot + matrix_c @ qdot + vector_g)

    estimated_mass = estimate_mass(
        q_samples.T,
        qdot_samples.T,
        qddot_samples.T,
        np.asarray(tau_samples).T,
    )
    assert np.isclose(estimated_mass, 0.17, atol=1e-12)
