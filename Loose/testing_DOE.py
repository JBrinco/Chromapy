#!/bin/python


import chromapy
# from sklearn.cross_decomposition import PLSRegression, PLSCanonical


output = chromapy.box_behnken("BBD_Input.csv", randomize = False)
# print(output)
# print(output)
# print("--------")

results = [7, 7, 6, 5, 9, 10, 8, 8, 6, 7, 6, 5, 13, 14, 13, 12] # Near Perfect-fit data, DO NOT RANDOMIZE BBD! It will be randomized in production, but for now it would loose it's perfect fit

design_out = chromapy.add_results(output, results)
# print(design_out)
# print("--------")

design_rsm = chromapy.rsm(design_out, "BBD_Input.csv", write_summary = "CRAZYNAME.txt")
# print(design_rsm)
chromapy.rsm_plot(design_rsm, pdf = "A_Beautiful_output.pdf", three_d = True, override_pdf = True)

dic_factors = chromapy.import_initial_csv("Examples_Templates/input_data/DOE_Input.csv")
design, matrix = chromapy.plackett_burman("Examples_Templates/input_data/DOE_Input.csv", 16)
print(design)
