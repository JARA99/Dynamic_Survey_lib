# File name: generate_dataset.py
# Author: Jorge Alejandro Rodriguez Aldana
# Date: 1mar2023

# Import libraries
# -----------------

import numpy as np
from basic_linear_classifier import blc_predictor

# Generate dataset from weight
# ----------------------------

def generate_dataset(w:np.ndarray,n:int = 100):
    dataset = []
    dimension = w.shape[0]

    for data_n in range(n):
        # x = np.random.randint(dimension)
        x = np.random.randint(1,3,dimension)
        y, score = blc_predictor(w,x)

        dataset.append((x,y))
    
    return dataset

def generate_dataset_with_randomness(w:np.ndarray,n:int = 100):
    dataset = []
    dimension = w.shape[0]

    for data_n in range(n):
        x = np.random.randn(dimension)
        y, score = blc_predictor(w,x)

        for i in range(len(x)):
            x[i] = x[i] + np.random.randn()

        dataset.append((x,y))
    
    return dataset

