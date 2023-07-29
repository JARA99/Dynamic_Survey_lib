# File name: __init__.py
# Author: Jorge Alejandro Rodriguez Aldana
# Date: 20mar2023

"""

`pydyn_surv` it's a simple library for creating a **dyn**amic **surv**ey using basic tools in python. This can be incorporated to a user inteface with the flexibility that Python offers.

## Modules:

`pydyn_surv` it's made with the following modules:

* **pydyn_surv.survey**: This module contains the class survey, which is used to create survey instances.
* **pydyn_surv.item**: This module contains the class item, which is used to create item instances.
* **pydyn_surv.ml**: This module contains the class ml, which contains the machine learning algorithms used in the library.
* **pydyn_surv.funcs**: This module contains default and custom functions for defining condition and probability.
* **pydyn_surv.other_classes**: By now, this module only contains the class pydyn_surv_list, which is used in the library to create lists with custom methods.
"""

from . import survey
from . import item
from . import ml
from . import funcs
from . import other_classes