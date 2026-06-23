"""Run the end-to-end chameleon tongue workflow."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chameleon_tongue import estimate_mass, estimate_model, estimate_probability, estimate_rmse


def parse_hidden_layers(value: str) -> tuple[int, ...]:
    parts = [part.strip() for part in value.replace("x", ",").split(",") if part.strip()]
    if not parts:
        raise argparse.ArgumentTypeError("Provide at least one hidden layer size.")
    try:
        layers = tuple(int(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Hidden layer sizes must be integers.") from exc
    if any(size <= 0 for size in layers):
        raise argparse.ArgumentTypeError("Hidden layer sizes must be positive.")
    return layers


def load_csv(data_dir: Path, name: str) -> np.ndarray:
    return np.loadtxt(data_dir / name, delimiter=",")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "raw")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs")
    parser.add_argument("--hidden-layer-sizes", type=parse_hidden_layers, default=(200, 200))
    parser.add_argument("--max-iter", type=int, default=15000)
    parser.add_argument("--random-state", type=int, default=1)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    random.seed(args.random_state)
    np.random.seed(args.random_state)

    data = {
        "R": load_csv(args.data_dir, "R.csv"),
        "Q": load_csv(args.data_dir, "Q.csv"),
        "Qdot": load_csv(args.data_dir, "Qdot.csv"),
        "Qddot": load_csv(args.data_dir, "Qddot.csv"),
        "Tau": load_csv(args.data_dir, "Tau.csv"),
        "Rd": load_csv(args.data_dir, "Rd.csv"),
    }

    model = estimate_model(
        data["R"],
        data["Q"],
        hidden_layer_sizes=args.hidden_layer_sizes,
        max_iter=args.max_iter,
        random_state=args.random_state,
    )

    metrics = {
        "model": {
            "type": "sklearn.neural_network.MLPRegressor",
            "hidden_layer_sizes": list(args.hidden_layer_sizes),
            "activation": "tanh",
            "solver": "lbfgs",
            "max_iter": args.max_iter,
            "random_state": args.random_state,
        },
        "data": {
            "training_samples": int(data["R"].shape[1]),
            "target_samples": int(data["Rd"].shape[1]),
        },
        "rmse_m": estimate_rmse(data["Rd"], model),
        "catch_probability_radius_0_01_m": estimate_probability(data["Rd"], model),
        "estimated_mass_kg": estimate_mass(data["Q"], data["Qdot"], data["Qddot"], data["Tau"]),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = args.output_dir / "metrics.json"
    output_path.write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
