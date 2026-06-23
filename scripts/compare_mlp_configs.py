"""Compare inverse-kinematics MLP configurations on a validation split."""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
import warnings
from pathlib import Path

import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chameleon_tongue.coursework import estimate_model
from chameleon_tongue.plant import ChameleonTongue


DEFAULT_CONFIGS = [
    {
        "name": "submitted",
        "hidden_layer_sizes": (200, 200),
        "max_iter": 15000,
        "alpha": 1e-7,
    },
    {
        "name": "compact_single_layer",
        "hidden_layer_sizes": (80,),
        "max_iter": 4000,
        "alpha": 1e-5,
    },
    {
        "name": "compact_two_layer",
        "hidden_layer_sizes": (50, 50),
        "max_iter": 4000,
        "alpha": 1e-5,
    },
    {
        "name": "regularised_small",
        "hidden_layer_sizes": (30,),
        "max_iter": 3000,
        "alpha": 1e-4,
    },
]


def load_csv(data_dir: Path, name: str) -> np.ndarray:
    return np.loadtxt(data_dir / name, delimiter=",")


def parameter_count(model) -> int:
    return int(sum(weights.size for weights in model.coefs_) + sum(bias.size for bias in model.intercepts_))


def task_space_rmse(targets: np.ndarray, predicted_q: np.ndarray) -> float:
    plant = ChameleonTongue()
    predicted_r = np.vstack([plant.forward_kinematics(q) for q in predicted_q])
    return float(np.sqrt(mean_squared_error(targets, predicted_r)))


def evaluate_config(config: dict, train_r: np.ndarray, val_r: np.ndarray, train_q: np.ndarray, val_q: np.ndarray) -> dict:
    convergence_warning = False
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ConvergenceWarning)
        model = estimate_model(
            train_r.T,
            train_q.T,
            hidden_layer_sizes=config["hidden_layer_sizes"],
            max_iter=config["max_iter"],
            alpha=config["alpha"],
        )
        convergence_warning = any(isinstance(item.message, ConvergenceWarning) for item in caught)

    train_pred_q = model.predict(train_r)
    val_pred_q = model.predict(val_r)

    return {
        "name": config["name"],
        "hidden_layer_sizes": "x".join(str(size) for size in config["hidden_layer_sizes"]),
        "max_iter": config["max_iter"],
        "alpha": config["alpha"],
        "parameters": parameter_count(model),
        "train_mse_q": float(mean_squared_error(train_q, train_pred_q)),
        "validation_mse_q": float(mean_squared_error(val_q, val_pred_q)),
        "validation_rmse_r_m": task_space_rmse(val_r, val_pred_q),
        "convergence_warning": convergence_warning,
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "raw")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs")
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--random-state", type=int, default=1)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    random.seed(args.random_state)
    np.random.seed(args.random_state)

    r = load_csv(args.data_dir, "R.csv").T
    q = load_csv(args.data_dir, "Q.csv").T
    train_r, val_r, train_q, val_q = train_test_split(
        r,
        q,
        test_size=args.test_size,
        random_state=args.random_state,
    )

    rows = [evaluate_config(config, train_r, val_r, train_q, val_q) for config in DEFAULT_CONFIGS]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.output_dir / "model_comparison.csv", rows)
    (args.output_dir / "model_comparison.json").write_text(
        json.dumps(rows, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(rows, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
