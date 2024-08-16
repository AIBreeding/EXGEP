#!/usr/bin/env python
from setuptools import setup, find_packages
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    
setup(
    name="EXGEP", 
    version="0.1.1", 
    packages=find_packages(), 
    description="A framework for predicting genotype-by-environment interactions using ensembles of explainable machine-learning models", 
    long_description_content_type="text/markdown",
    url="https://github.com/AIBreeding/exgep",
    python_requires='>=3.9',
    install_requires=requirements,
    
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: CentOS :: Linux",
    ],
)
