#!/bin/python


import chromapy

quant_results = chromapy.quantification("Examples_Templates/Quantification/calibration_test.csv", "Examples_Templates/Quantification/samples.csv", file_input = True, int_standard = True, print_results = "My_Results.txt")
quant_results.to_csv("Quantification_results.csv")

print(quant_results)
