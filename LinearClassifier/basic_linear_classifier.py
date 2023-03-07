# File name: basic_linear_classifier.py
# Author: Jorge Alejandro Rodriguez Aldana
# Date: 1mar2023

# Import libraries
# -----------------

import numpy as np
from collections.abc import Iterable
import random as rnd

# Define blc predictor
# --------------------

def blc_predictor(w:np.ndarray,x:np.ndarray):
    """([b]inary) [l]inear [c]lassifier predictor. Returns the sign of a prediction given a weigth (w) and a feauture vector (x).

    Args:
        w (np.ndarray): n-dimensional weight vector
        x (np.ndarray): n-dimensional feauture vector

    Returns:
        float: sign value
    """

    score = w.dot(x)

    if score > 0:
        sign = 1
    elif score < 0:
        sign = -1
    else:
        sign = np.nan
    
    return sign

# Define regression predictor
# ---------------------------

def reg_predictor(w:np.ndarray,x:np.ndarray):
    """([reg]ression predictor. Returns the sign of a prediction given a weigth (w) and a feauture vector (x).

    Args:
        w (np.ndarray): n-dimensional weight vector
        x (np.ndarray): n-dimensional feauture vector

    Returns:
        float: sign value
    """

    sign = w.dot(x)
    
    return sign

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
    mar = margin(w,x,y)

    if mar <= 0:
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

    mar = margin(w,x,y)

    hinge = max([0,1-mar])

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

    mar = margin(w,x,y)

    if mar < 1:
        return - x * y
    if mar >= 1:
        return 0

def squared_loss(w:np.ndarray,x:np.ndarray,y:float):
    """Squared loss. Returns the squared loss for a given weight (w), feauture vector (x) and true prediction value (y).

    Args:
        w (np.ndarray): n-dimensional weight vector
        x (np.ndarray): n-dimensional feauture vector
        y (float): true prediction value for x

    Returns:
        float: Squared loss value
    """

    score = w.dot(x)
    residual = score - y

    return residual**2

def squared_loss_derivative(w:np.ndarray,x:np.ndarray,y:float):
    """Squared loss. Returns the squared loss derivative for a given weight (w), feauture vector (x) and true prediction value (y).

    Args:
        w (np.ndarray): n-dimensional weight vector
        x (np.ndarray): n-dimensional feauture vector
        y (float): true prediction value for x

    Returns:
        float: Squared loss derivative value
    """

    score = w.dot(x)
    residual = score - y

    return 2*residual*x

# Gradient descent
# ----------------

def gradient_descent(loss,dd_loss,training_dataset:Iterable,eta:float = 0.01,iterations = 500,verbose:bool = True):
    
    dimension = training_dataset[0][0].shape[0]
    w = np.zeros(dimension)

    for iteration in range(iterations):
        loss_value = sum(loss(w,x,y) for x,y in training_dataset)/len(training_dataset)
        gradient = sum(dd_loss(w,x,y) for x,y in training_dataset)/len(training_dataset)
        w = w - (eta * gradient)

        if verbose:
            print('iteration {}:'.format(iteration+1),'w = {},'.format(w),'Loss(w) = {}'.format(loss_value))

        if loss_value == 0:
            break
        
    return w



# Stocastic Gradient descent
# --------------------------

def stocastic_gradient_descent(loss,dd_loss,training_dataset:Iterable,init_eta:float = 0.1,iterations = 500,verbose:bool = True):
    
    dimension = training_dataset[0][0].shape[0]
    w = np.zeros(dimension)

    n = 0

    dataset_len = len(training_dataset)

    for iteration in range(iterations):
        n += 1
        eta = init_eta/np.sqrt(n)
        # eta  = init_eta

        indexlist = np.arange(dataset_len)
        rnd.shuffle(indexlist)

        for i in indexlist:

            x = training_dataset[i][0]
            y = training_dataset[i][1]

            sample_loss = loss(w,x,y)

            if sample_loss:

                gradient = dd_loss(w,x,y)
                w = w - (eta * gradient)


            loss_value = sum(loss(w,x,y) for x,y in training_dataset)/dataset_len

            if verbose:
                print('iteration {}, index {}:    w = {}, Loss(w) = {}'.format(iteration+1,i,w,loss_value))

        if loss_value == 0:
            break
        
    return w


