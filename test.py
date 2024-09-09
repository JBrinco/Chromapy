#!/bin/python

import chromapy

file = "stuff"
quant_df = chromapy.quantification("Examples_Templates/Quantification/calibration.csv", "Examples_Templates/Quantification/samples.csv", file_input = True, int_standard = True, print_results = "My_Results.txt")
