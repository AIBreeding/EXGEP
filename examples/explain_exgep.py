"""Inspect a completed EXGEP job and prepare data for explainability analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib

from exgep.data import datautils


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_id", type=Path, help="Training job directory")
    parser.add_argument("--geno", default="data/genotype.csv")
    parser.add_argument("--phen", default="data/pheno.csv")
    parser.add_argument("--soil", default="data/soil.csv")
    parser.add_argument("--weather", default="data/weather.csv")
    parser.add_argument("--target", default="Yield")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = datautils.merge_data(args.geno, args.phen, args.soil, args.weather)
    if args.target not in data.columns:
        raise ValueError(f"Target column {args.target!r} not found")
    model_path = args.job_id / "result" / "EXGEP_model.joblib"
    if not model_path.is_file():
        raise FileNotFoundError(f"Model not found: {model_path}")
    model = joblib.load(model_path)
    print(f"Loaded {type(model).__name__} from {model_path}")
    print(f"Merged sample shape: {data.shape}")
    print("Use SHAP with the fitted estimator and the same processed feature set used during training.")


if __name__ == "__main__":
    main()
