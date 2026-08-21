"""Train an EXGEP regression ensemble using the bundled sample data."""

from __future__ import annotations

import argparse
import os
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from exgep.data import datautils
from exgep.data.reg_metrics import (
    mae_score as mae,
    mape_score as mape,
    medae_score as medae,
    mse_score as mse,
    pcc_score as pcc,
    r2_score as r2,
    rmse_score as rmse,
    rmsle_score as rmsle,
)
from exgep.model import RegEXGEP


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--geno", default="data/genotype.csv")
    parser.add_argument("--phen", default="data/pheno.csv")
    parser.add_argument("--soil", default="data/soil.csv")
    parser.add_argument("--weather", default="data/weather.csv")
    parser.add_argument("--target", default="Yield")
    parser.add_argument("--test-size", type=float, default=0.1)
    parser.add_argument("--n-splits", type=int, default=10)
    parser.add_argument("--n-trial", type=int, default=5)
    parser.add_argument("--models-optimize", nargs="+", default=["XGBoost"])
    parser.add_argument("--models-assess", nargs="+", default=["XGBoost"])
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    job_id = datetime.now().strftime("%Y%m%d%H%M%S")
    output = args.output or Path.cwd() / job_id / "result"
    data = datautils.merge_data(args.geno, args.phen, args.soil, args.weather)
    if args.target not in data.columns:
        raise ValueError(f"Target column {args.target!r} not found")
    X = pd.DataFrame(data.iloc[:, 3:])
    y = pd.Series(data[args.target])
    regression = RegEXGEP(
        y=y,
        X=X,
        test_size=args.test_size,
        n_splits=args.n_splits,
        n_trial=args.n_trial,
        reload_study=True,
        reload_trial=True,
        write_folder=f"{output}{os.sep}",
        metric_optimise=r2,
        metric_assess=[mae, mse, rmse, pcc, rmsle, mape, medae],
        optimization_objective="maximize",
        models_optimize=args.models_optimize,
        models_assess=args.models_assess,
        early_stopping_rounds=5,
        random_state=2024,
    )
    started = time.time()
    regression.train()
    print(f"Training time: {time.time() - started:.2f} seconds")
    print(f"Job ID: {job_id}")


if __name__ == "__main__":
    main()
