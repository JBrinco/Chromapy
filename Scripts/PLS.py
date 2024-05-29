#!/bin/python

import argparse
import chromapy

parser = argparse.ArgumentParser(
        epilog="For simple PLS, just run with no options, and preferably a \"Type\" column in the data, to separate sample classes. Alternatively, use the -L option to add labels to samples. A \"Sample\" column in the csv is mandatory! You will probably also need to scale the loadings, with option -s.",
        )
parser.add_argument("CSV", help="The file with the input data. Can be .csv, .xlsx, .ods, etc.")
# parser.add_argument("-c", "--loading_class", help="If you want to color PCA loadings according to a certain type, you need to provide a CSV file with that information.")
parser.add_argument("-L", "--labels", help="Add labels to the samples.", action="store_true")
parser.add_argument("-l", "--loadings", help="Remove loadings from the PLS plot, and show only samples. Will write loadings separately.", action="store_true")
parser.add_argument("-n", "--normalize", type=str, help="Type of normalization to perform. Default is none. Options: \"standard\", \"normalize\", \"minmax\" and \"area\" (see documentation in the code).")
parser.add_argument("-o", "--output", type=str, help="The name of the output file for plot image. The extention (.png, .svg, etc.) determines file type. Default is no output.")
parser.add_argument("-s", "--loading_scale", type=float, help="Scale for loadings (samples) in the graph. Default is 1.", default=1)
parser.add_argument("-r", "--response", type=int, help="The number of response variable columns. Default is one. Response columns should be named \"Response1\", \"Response2\", etc. If you want different names, you must call the function directly in python, not using this script.", default=1)
parser.add_argument("-x", "--x_axis", type=float, help="Custom, centered x axis. Accepts a number, and will set x to [-number, number]")
parser.add_argument("-y", "--y_axis", type=float, help="Custom, centered y axis. Accepts a number, and will set y to [-number, number]")
args = parser.parse_args()



# Import the dataframe
df = chromapy.multivariate_import(args.CSV)

# Normalize if wanted
if args.normalize:
    df_normalized = chromapy.normalize(df, normalization=args.normalize)

if args.response == 1:
    responses = ["Response1"]
elif args.response == 2:
    responses = ["Response1", "Response2"]
elif args.response == 3:
    responses = ["Response1", "Response2", "Response3"]
elif args.response == 4:
    responses = ["Response1", "Response2", "Response3", "Response4"]
elif args.response == 5:
    responses = ["Response1", "Response2", "Response3", "Response4", "Response5"]
elif args.response == 6:
    responses = ["Response1", "Response2", "Response3", "Response4", "Response5", "Response6"]
else:
    print("Number of responses not supported")

pls_result, pls_loadings, response_df = chromapy.pls(df, responses)

if args.output:
    plot = chromapy.pls_plot(pls_result, pls_loadings, response=response_df, labels=args.labels, loadings_scale=args.loading_scale, write_loadings = (not args.loadings), output=args.output, X=args.x_axis, Y=args.y_axis)
else:
    plot = chromapy.pls_plot(pls_result, pls_loadings, response=response_df, labels=args.labels, loadings_scale=args.loading_scale, write_loadings = (not args.loadings), X=args.x_axis, Y=args.y_axis)
