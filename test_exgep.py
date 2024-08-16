import time
import os
import pandas as pd
from exgep.preprocess import datautils
from exgep.model import RegEXGEP
from sklearn.metrics import r2_score, median_absolute_error, mean_squared_error
import argparse
from datetime import datetime

jobnum = datetime.now().strftime('%Y%m%d%H%M%S')
print('Job number: ', jobnum)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Automated Regression with External Data')

    parser.add_argument('--Geno', type=str,
                        default='./data/genotype.csv', help='Path to genotype CSV file')
    parser.add_argument('--Phen', type=str,
                        default='./data/pheno.csv', help='Path to phenotype CSV file')
    parser.add_argument('--Soil', type=str,
                        default='./data/soil.csv', help='Path to soil CSV file')
    parser.add_argument('--Weather', type=str,
                        default='./data/weather.csv', help='Path to weather CSV file')
    parser.add_argument('--Test_frac', type=float, default=0.1,
                        help='Fraction of the data to be used for testing')
    parser.add_argument('--N_splits', type=int, default=10,
                        help='Number of splits for cross-validation')
    parser.add_argument('--N_trial', type=int, default=5,
                        help='Number of optimization trials')
    parser.add_argument(
        '--models',
        nargs='+', 
        choices=[
            'dummy', 'lightgbm', 'xgboost', 'catboost',
            'bayesianridge', 'lassolars', 'adaboost',
            'gradientboost', 'histgradientboost', 'knn',
            'sgd', 'bagging', 'svr', 'elasticnet'
        ], 
        default=['xgboost'],
        help='Select models (Options: dummy, lightgbm, xgboost, catboost, bayesianridge, lassolars, adaboost, gradientboost, histgradientboost, knn, sgd, bagging, svr, elasticnet)'
    )
    parser.add_argument(
        '--Emodels',
        nargs='+', 
        choices=[
            'dummy', 'lightgbm', 'xgboost', 'catboost',
            'bayesianridge', 'lassolars', 'adaboost',
            'gradientboost', 'histgradientboost', 'knn',
            'sgd', 'bagging', 'svr', 'elasticnet'
        ], 
        default=['xgboost'],
        help='Options are the same as --models'
    )

    return parser.parse_args()

def main():
    args = parse_args()
    data = datautils.merge_data(
        args.Geno, args.Phen, args.Soil, args.Weather)
    X = pd.DataFrame(data.iloc[:, 3:])
    y = data['Yield']
    y = pd.core.series.Series(y)
    models = args.models
    Emodels = args.Emodels

    regression = RegEXGEP(
        y=y,
        X=X,
        test_frac=args.Test_frac,
        n_splits=args.N_splits,
        n_trial=args.N_trial,  
        reload_study=True,
        reload_trial_cap=True,
        write_folder=f'{os.getcwd()}/{jobnum}/result/',
        metric_optimise=r2_score,
        metric_assess=[median_absolute_error, mean_squared_error, r2_score],
        optimisation_direction='maximize',
        models_to_optimize=models,  
        models_to_assess=Emodels, 
        boosted_early_stopping_rounds=5,
        random_state=2024  
    )

    start = time.time()
    regression.apply()
    end = time.time()

    print(end - start)
    print(regression.summary)
    print('Job ID: ', jobnum)


if __name__ == '__main__':
    main()
