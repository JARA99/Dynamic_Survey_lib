# File name: generate_dataset.py
# Author: Jorge Alejandro Rodriguez Aldana
# Date: 1mar2023

# Import libraries
# -----------------

import numpy as np
from .basic_linear_classifier import blc_predictor

# Generate dataset from weight
# ----------------------------

def generate_dataset(w:np.ndarray,n:int = 100):
    dataset = []
    dimension = w.shape[0]

    for data_n in range(n):
        x = np.random.randn(dimension)
        y, score = blc_predictor(w,x)

        dataset.append((x,y))

