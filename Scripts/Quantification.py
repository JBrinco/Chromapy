#!/bin/python

import argparse
import chromapy

parser = argparse.ArgumentParser(
        epilog="Quantification module. Requires a calibration CSV and a Samples csv (passed with the -s option).",
        )
parser.add_argument("CSV", help="The file with the input data. Can be .csv, .xlsx, .ods, etc. Even for calculating the RSM, this file should be the first one, without the design or the results.")
parser.add_argument("-s", "--samples", type=str, help="REQUIRED! The .csv with the samples.")
parser.add_argument("-v", "--verbose", help="Verbose output, showing all calculated values and internal variables", action="store_true", default=False)
parser.add_argument("-p", "--print", type=str, help="The name of the .csv with the quantification results. Default is \"Quantification_results.csv\"", default="Quantification_results.csv")
parser.add_argument("-q", "--quantification_parameters", type=str, help="The name of the file where the calibration parameters (LOQ, R2, etc) are printed. Default is \"Quantification_parameters.txt\"", default="Quantification_parameters.txt")
parser.add_argument("-i", "--int_standard", help="Use this option if you want to calculate values with an internal standard.", action="store_true", default=False)
args = parser.parse_args()



if not args.samples:
    print("You must give me the file with the samples! Example: -s \"samples_file.csv\"")
    exit()

calibration_df, samples_df = chromapy.quant_import(args.CSV, args.samples)

quant_results = chromapy.quantification(calibration_df, samples_df, int_standard = args.int_standard, verbose = args.verbose, print_results =args.quantification_parameters)

quant_results.to_csv(args.print)
