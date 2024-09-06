#!/bin/python

import chromapy
import pandas as pd

#From CSV
design, matrix = chromapy.plackett_burman("Examples_Templates/DOE/DOE_Input.csv", 12)
# matrix.to_csv('Plackett_Burman_matrix.csv', index = False) #convert matrix to .csv
# main_effect = chromapy.main_effect("Examples_Templates/DOE/DOE_results.csv", "Plackett_Burman_matrix.csv")


results = pd.read_csv("Examples_Templates/DOE/DOE_results.csv")
main_effect = chromapy.main_effect(results, matrix, dataframe = True)


# BBdesign = chromapy.box_behnken("Examples_Templates/DOE/BBD_Input.csv")
# print(BBdesign)
