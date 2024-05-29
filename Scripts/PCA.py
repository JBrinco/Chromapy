#!/bin/python

import argparse
import chromapy

parser = argparse.ArgumentParser(
        epilog="For simple PCA, just run with no options, and preferably a \"Type\" column in the data, to separate sample classes. Alternatively, use the -L option to add labels to samples. A \"Sample\" column in the csv is mandatory! You will probably also need to scale the loadings, with option -s.",
        )
parser.add_argument("CSV", help="The file with the input data. Can be .csv, .xlsx, .ods, etc.")
parser.add_argument("-c", "--loading_class", help="If you want to color PCA loadings according to a certain type, you need to provide a CSV file with that information.")
parser.add_argument("-L", "--labels", help="Add labels to the samples.", action="store_true")
parser.add_argument("-l", "--loadings", help="Remove loadings from the PCA, and show only samples. Will write loadings separately.", action="store_false")
parser.add_argument("-n", "--normalize", help="Type of normalization to perform. Default is none. Options: zscore, normalize, minmaxscaler (see documentation).")
parser.add_argument("-o", "--output", type=str, help="The name of the output file for PCA image. The extention (.png, .svg, etc.) determines file type. Default is no output.")
# parser.add_argument("-O", "--varoutput", type=str, help="Name of optional file for explained variance. Default is no output.")
parser.add_argument("-s", "--loading_scale", type=float, help="Scale for loadings (samples) in the graph. Default is 1.", default=1)
parser.add_argument("-V", "--variance", type=str, help="Name of optional file for explained variance. Default is no output.")
parser.add_argument("-v", "--verbose", help="Verbose output, showing all calculated values and internal variables", action="store_true")
parser.add_argument("-x", "--x_axis", type=float, help="Custom, centered x axis. Accepts a number, and will set x to [-number, number]")
parser.add_argument("-y", "--y_axis", type=float, help="Custom, centered y axis. Accepts a number, and will set y to [-number, number]")
args = parser.parse_args()


## Cannot remove loadings!!!!!!!

#Import the dataframe
df = chromapy.multivariate_import(args.CSV)
print(df)

df_normalized = chromapy.normalize(df, normalization='area')
print(df_normalized)

pca_result, loadings_df, loadings = chromapy.pca(df_normalized)

plot = chromapy.pca_plot(pca_result, loadings_df, loadings, output="sample_pca_output.svg", X=args.x_axis, Y=args.y_axis, loadings_scale=args.loading_scale, write_loadings=args.loadings, labels=args.labels)
