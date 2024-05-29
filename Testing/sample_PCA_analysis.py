#!/bin/python

import chromapy

#Import the dataframe
df = chromapy.multivariate_import("Examples_Templates/input_data/wine_data.csv")

#Normalize by area and output the normalized dataframe as an excel spreadsheet
#df = chromapy.normalize(df, normalization='area', output="out.xlsx")

#Run PCA analysis
pca_result, loadings_df, loadings = chromapy.pca(df)

#Plot the results!
plot = chromapy.pca_plot(pca_result, loadings_df, loadings, output="sample_pca_output.svg", loadings_scale=1250000000, labels=False, variance=False)
