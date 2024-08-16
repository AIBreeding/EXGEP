## EXGEP
## EXGEP: a framework for predicting genotype-by-environment interactions using ensembles of explainable machine-learning models
<strong>Abstract:</strong> Phenotypic variation results from the combination of genotype, the environment, and their interaction. The ability to quantify the relative contributions of genes and environmental factors to complex traits can help in breeding crops with superior adaptability for growth in varied environments. Here, we developed and extensively evaluated the performance of an explainable machine learning framework named EXGEP (Explainable Genotype-by-Environment Interactions Prediction) to accurately predict crop yield values. To assess the performance of EXGEP, we applied it to a dataset comprising 70,693 phenotypic records of grain yield traits for 3,793 hybrids (also including both genotype and environmental condition data). EXGEP revealed 20 features and their interactions that affect yield prediction model performance; these features, including 11 soil features, 6 weather features, and 3 genotype features, contributed 52.87% of the mean total Shapley Additive Explanations (SHAP) sum contribution to yield prediction. When used with 4 different combinations of genotypes and environmental data, EXGEP exceeded the yield prediction performance of the classic model Bayesian ridge regression (BRR) model by 17.37-42.35%. And data from a series of tests support that EXGEP exhibits superior performance in terms of prediction accuracy, model stability, and explainability. Our development of EXGEP and comparisons of it against alternative models provide valuable insights into methods for accurately predicting complex traits in multiple environments.

<img src="EXGEP.png" alt="Your Image" style="max-width: 100%;">

### Table of Contents
- [Getting started](#Getting-started)
- [Usage](#usage)
- [Copyright and License](#copyright-and-license)

## Getting started


### Requirements
 
 - Python 3.9
 - pip

### Installation
Install packages:
```bash
conda create -n exgep python=3.9
conda activate exgep
cd exgep
pip install exgep
```

## Usage

```python
import os
import time
import argparse
import pandas as pd
from datetime import datetime
from exgep.model import RegEXGEP
from exgep.preprocess import datautils
from sklearn.metrics import r2_score, median_absolute_error, mean_squared_error

Geno = './data/genotype.csv'
Phen = './data/pheno.csv'
Soil = './data/soil.csv'
Weather = './data/weather.csv'

data = datautils.merge_data(Geno, Phen, Soil, Weather)
X = pd.DataFrame(data.iloc[:, 3:])
y = data['Yield']
y = pd.core.series.Series(y)
    
regression = RegEXGEP(
    y=y,
    X=X,
    test_frac=0.1,
    n_splits=10,
    n_trial=5,
    reload_study=True,
    reload_trial_cap=True,
    write_folder=os.getcwd()+'/result/',
    metric_optimise=r2_score,
    metric_assess=[median_absolute_error, mean_squared_error, r2_score],
    optimisation_direction='maximize',
    models_to_optimize=['xgboost'],
    models_to_assess=['xgboost'],
    boosted_early_stopping_rounds=5,
    random_state=2024
)

start = time.time()
regression.apply()
end = time.time()
print(end - start)
print(regression.summary)
```

### Training Example
```python
python test_exgep.py \
--Geno ./data/genotype.csv \
--Phen ./data/pheno.csv \
--Soil ./data/soil.csv \
--Weather ./data/weather.csv \
--Test_frac 0.2 \
--N_splits 5 \
--N_trial 5 \
--models_to_optimize xgboost \
--models_to_assess xgboost
```

 - Geno: Genotype data
 - Phen: Phenotype data
 - Soil: Soil data
 - Weather: Weather data
 - Test_frac: Test data division ratio
 - N_splits: Cross validation folds
 - N_trial: Number of model optimization evaluations
 - models_to_optimize: Selection of an optimized base models
 - models_to_assess: Base models for needs assessment
 
```bash
Alternative base models:
'dummy', 'lightgbm', 'xgboost', 'catboost', 'bayesianridge', 'lassolars', 'adaboost', 'gradientboost',
'histgradientboost', 'knn', 'sgd', 'bagging', 'svr', 'elasticnet', 'randomforest', 'gbdt'
```
In this study we chose lightgbm,xgboost,randomforest,and gbdt as the base models.
            
### Explainable Example
```
python test_explain.py \
--Geno ./data/genotype.csv \
--Phen ./data/pheno.csv \
--Soil ./data/soil.csv \
--Weather ./data/weather.csv \
--SSP 150 \
--IEF1 pc1 \
--IEF2 pc2 \
--job_id 20240813103950
```
 - Geno: Genotype data
 - Phen: Phenotype data
 - Soil: Soil data
 - Weather: Weather data
 - SSP: Sample number to be explained
 - IEF1: Features to be explained1
 - IEF2: Features to be explained2
 - job_id: Obtaining optimized parameters using model-trained job ID

## Copyright and License
This project is free to use for non-commercial purposes - see the [LICENSE](LICENSE) file for details.


