# File name: __init__.py
# Author: Jorge Alejandro Rodriguez Aldana
# Date: 8mar2023

"""
This submodule contains the functions related to the Machine Learning process. It's made by two submodules:
* **pydyn_surv.LinearClassifier.basic_linear_classifier**: which contains the functions for processing datasets.
* **pydyn_surv.LinearClassifier.generate_dataset**: which contains functions for generating random datasets based on a "true weight".

"""

from . import basic_linear_classifier
from . import generate_dataset