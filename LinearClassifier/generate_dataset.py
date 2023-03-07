# File name: generate_dataset.py
# Author: Jorge Alejandro Rodriguez Aldana
# Date: 1mar2023

# Import libraries
# -----------------

import numpy as np
from basic_linear_classifier import blc_predictor

# Generate dataset from weight
# ----------------------------

def generate_dataset(w:np.ndarray,n:int = 100,predictor = blc_predictor):
    dataset = []
    dimension = w.shape[0]

    for data_n in range(n):
        x = np.random.randn(dimension)
        # x = np.random.randint(0,2,dimension)
        y = predictor(w,x)

        dataset.append((x,y))
    
    return dataset

def generate_dataset_with_randomness(w:np.ndarray,n:int = 100,predictor = blc_predictor):
    dataset = []
    dimension = w.shape[0]

    for data_n in range(n):
        x = np.random.randn(dimension)
        y = predictor(w,x)

        for i in range(len(x)):
            x[i] = x[i] + (np.random.randn()*0.1)

        dataset.append((x,y))
    
    return dataset

def generate_binary_features_dataset(w:np.ndarray,n:int = 100,predictor = blc_predictor):
    dataset = []
    dimension = w.shape[0]

    for data_n in range(n):
        x = np.random.randint(-1,2,dimension)
        y = predictor(w,x)

        if not np.isnan(y):
            dataset.append((x,y))
    
    return dataset

def generate_binary_features_dataset_with_randomness(w:np.ndarray,n:int = 100,predictor = blc_predictor):
    dataset = []
    dimension = w.shape[0]

    for data_n in range(n):
        x = np.random.randint(-1,2,dimension)
        y = predictor(w,x) + np.random.randn()

        if not np.isnan(y):
            dataset.append((x,y))
    
    return dataset