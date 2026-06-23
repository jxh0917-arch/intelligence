"""Reusable implementation of the chameleon tongue coursework solution."""

from .coursework import (
    estimate_mass,
    estimate_model,
    estimate_probability,
    estimate_rmse,
)
from .plant import ChameleonTongue, chameleon

__all__ = [
    "ChameleonTongue",
    "chameleon",
    "estimate_mass",
    "estimate_model",
    "estimate_probability",
    "estimate_rmse",
]
