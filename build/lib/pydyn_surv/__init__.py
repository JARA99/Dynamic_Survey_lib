# File name: __init__.py
# Author: Jorge Alejandro Rodriguez Aldana
# Date: 20mar2023

"""

`pydyn_surv` it's a simple library for creating a **dyn**amic **surv**ey using basic tools in python. This can be incorporated to a user inteface with the flexibility that Python offers.

## Submodules:

`pydyn_surv` it's made with the following submodules:

* **pydyn_surv.classes**: This submodule contains the clases for building a survey.
* **pydyn_surv.LinearClassifier**: This submodule contains the functions related to the Machine Learning process.
"""

from .LinearClassifier import *
from .classes import *