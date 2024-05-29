#!/bin/python

import numpy as np
import pandas as pd
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages
from rpy2.robjects.vectors import StrVector

# import packages
base = rpackages.importr('base')
utils = rpackages.importr('utils')
rsm = rpackages.importr('rsm')

rsm.chooseCRANmirror(ind=1)

packnames = ('ggplot2', 'hexbin', 'rsm')

# Selectively install what needs to be install.
# We are fancy, just because we can.
names_to_install = [x for x in packnames if not rpackages.isinstalled(x)]
if len(names_to_install) > 0:
    rsm.install_packages(StrVector(names_to_install))

exit()
