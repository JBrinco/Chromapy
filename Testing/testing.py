#!/bin/python

import chromapy
import numpy as np


y = np.array([90, 0])
x = np.array([0, 20])

result = chromapy.hplc_solvent("Examples/input_data/calculator_input.csv")

print(result)
