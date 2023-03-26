# File name: generate_dataset.py
# Author: Jorge Alejandro Rodriguez Aldana
# Date: 1mar2023

# Import libraries
# -----------------

import numpy as np
from .basic_linear_classifier import blc_predictor

# Generate dataset from weight
# ----------------------------

def generate_dataset(w:np.ndarray,n:int = 100,predictor = blc_predictor) -> list:
    """Generate a dataset using a "true width"

    Parameters
    ----------
    w : np.ndarray
        True width: you spect that the training width tends to this np.ndarray.
    n : int, optional
        Number of pairs in the training dataset, by default 100
    predictor : function, optional
        A predictor function, by default blc_predictor

    Returns
    -------
    list
        List containing training pairs (feauture vector, label).
    """
    dataset = []
    dimension = w.shape[0]

    for data_n in range(n):
        x = np.random.randn(dimension)
        # x = np.random.randint(0,2,dimension)
        y = predictor(w,x)

        dataset.append((x,y))
    
    return dataset

def generate_dataset_with_randomness(w:np.ndarray,n:int = 100,predictor = blc_predictor) -> list:
    """Generate a dataset using a "true width" and adding some error with randomness in the feauture vector.

    Parameters
    ----------
    w : np.ndarray
        True width: you spect that the training width tends to this np.ndarray.
    n : int, optional
        Number of pairs in the training dataset, by default 100
    predictor : function, optional
        A predictor function, by default blc_predictor

    Returns
    -------
    list
        List containing training pairs (feauture vector (with randomness), label).
    """
    dataset = []
    dimension = w.shape[0]

    for data_n in range(n):
        x = np.random.randn(dimension)
        y = predictor(w,x)

        for i in range(len(x)):
            x[i] = x[i] + (np.random.randn()*0.1)

        dataset.append((x,y))
    
    return dataset

def generate_binary_features_dataset(w:np.ndarray,n:int = 100,predictor = blc_predictor) -> list:
    """Generate a dataset using a "true width", but the feauture vector has only three posible values in each coordinate: `[-1,0,1]`.

    Parameters
    ----------
    w : np.ndarray
        True width: you spect that the training width tends to this np.ndarray.
    n : int, optional
        Number of pairs in the training dataset, by default 100
    predictor : function, optional
        A predictor function, by default blc_predictor

    Returns
    -------
    list
        List containing training pairs (feauture vector (with integers), label).
    """
    dataset = []
    dimension = w.shape[0]

    for data_n in range(n):
        x = np.random.randint(-1,2,dimension)
        y = predictor(w,x)

        if not np.isnan(y):
            dataset.append((x,y))
    
    return dataset

def generate_binary_features_dataset_with_randomness(w:np.ndarray,n:int = 100,predictor = blc_predictor) -> list:
    """Generate a dataset using a "true width", but the feauture vector has only three posible values in each coordinate: `[-1,0,1]`. Also the label has a random error.

    Parameters
    ----------
    w : np.ndarray
        True width: you spect that the training width tends to this np.ndarray.
    n : int, optional
        Number of pairs in the training dataset, by default 100
    predictor : function, optional
        A predictor function, by default blc_predictor

    Returns
    -------
    list
        List containing training pairs (feauture vector (with integers), label (with error)).
    """
    dataset = []
    dimension = w.shape[0]

    for data_n in range(n):
        x = np.random.randint(-1,2,dimension)
        y = predictor(w,x) + np.random.randn()

        if not np.isnan(y):
            dataset.append((x,y))
    
    return dataset