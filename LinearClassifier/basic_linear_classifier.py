# File name: basic_linear_classifier.py
# Author: Jorge Alejandro Rodriguez Aldana

# Import libraries
# -----------------

import numpy as np
from collections.abc import Iterable

# Define predictor
# ----------------

def blc_predictor(w:np.ndarray,x:np.ndarray):
    """([b]inary) [l]inear [c]lassifier predictor. Returns the sign and score of a prediction given a weigth (w) and a feauture vector (x).

    Args:
        w (np.ndarray): n-dimensional weight vector
        x (np.ndarray): n-dimensional feauture vector

    Returns:
        float, float: sign value, score value
    """

    score = w.dot(x)

    if score > 0:
        sign = 1
    elif score < 0:
        sign = -1
    else:
        sign = np.nan
    
    return sign, score

# Define margin
# -------------

def margin(w:np.ndarray,x:np.ndarray,y:float):
    """Return the margin value for a given weight (w), feauture vector (x) and true prediction value (y).

    Args:
        w (np.ndarray): n-dimensional weight vector
        x (np.ndarray): n-dimensional feauture vector
        y (float): true prediction value for x
    Returns:
        float: Margin value
    """
    return (w.dot(x)) * y

# Define loss and derivatives
# ---------------------------

def zero_one_loss(w:np.ndarray,x:np.ndarray,y:float):
    """0-1 loss. Returns the 0-1 loss for a given weight (w), feauture vector (x) and true prediction value (y).

    Args:
        w (np.ndarray): n-dimensional weight vector
        x (np.ndarray): n-dimensional feauture vector
        y (float): true prediction value for x

    Returns:
        float: 0-1 loss value
    """
    margin = margin(w,x,y)

    if margin <= 0:
        return 1
    else:
        return 0

def hinge_loss(w:np.ndarray,x:np.ndarray,y:float):
    """Hinge loss. Returns the hinge loss for a given weight (w), feauture vector (x) and true prediction value (y).

    Args:
        w (np.ndarray): n-dimensional weight vector
        x (np.ndarray): n-dimensional feauture vector
        y (float): true prediction value for x

    Returns:
        float: Hinge loss value
    """

    margin = margin(w,x,y)

    hinge = max([0,1-margin])

    return hinge

def hinge_loss_derivative(w:np.ndarray,x:np.ndarray,y:float):
    """Hinge loss derivative. Returns the derivative of the hinge loss for a given weight (w), feauture vector (x) and true prediction value (y).

    Args:
        w (np.ndarray): n-dimensional weight vector
        x (np.ndarray): n-dimensional feauture vector
        y (float): true prediction value for x

    Returns:
        float: Hinge loss derivative value
    """

    margin = margin(w,x,y)

    if margin < 1:
        return - x * y
    if margin >= 1:
        return 0

# Gradient descent
# ----------------

def gradient_descent(loss:function,dd_loss:function,training_dataset:Iterable,eta:float = 0.01,iterations = 500,verbose:bool = True):
    
    dimension = training_dataset[0][0].shape[0]
    w = np.zeros(dimension)

    for iteration in range(iterations):
        loss_value = sum(loss(w,x,y) for x,y in training_dataset)/len(training_dataset)
        gradient = sum(dd_loss(w,x,y) for x,y in training_dataset)/len(training_dataset)
        w = w - (eta * gradient)

        if verbose:
            print('iteration {}:'.format(iteration),'w = {},'.format(w),'Loss(w) = {}'.format(loss_value))
        
    return w


