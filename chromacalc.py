#!/bin/python

import argparse
import chromapy

parser = argparse.ArgumentParser(
        epilog="Simple chromatography calculators.",
        )
parser.add_argument("CSV", help="The file with the input data or the column internal diameter in the case of -l and -f.")
parser.add_argument("-s", "--hplc_solvent", help="Calculate solvent consumption. Flow must be PER MINUTE! Result will be in the same volume units", action="store_true")
parser.add_argument("-l", "--linear_velocity", type=float, help="Calculate GC linear velocity. Instead of a CSV, takes in the column diameter and flow. Example for 0.25 mm column and 1 mL/min: chromacalc 0.25 -l 1.0", default=171.31)
parser.add_argument("-f", "--flow", type=float, help="Calculate GC flow. Instead of a CSV, takes in the column diameter and linear velocity. Example for 0.25 mm column and 30cm/sec: chromacalc 0.25 -f 30.0", default=171.31)
args = parser.parse_args()


# HPLC solvent consumption
if args.hplc_solvent:
    result = chromapy.hplc_solvent(args.CSV)
    print("That solvent\'s consumption (in the same volume units as the flow) is " + str('%.3f' % result)) # Print with only 3 decimal places

if args.linear_velocity != 171.31: #Dummy number. Helps in calling the script from the CLI with only one flag insted of two.
    result = chromapy.lin_velocity(args.linear_velocity, float(args.CSV))
    print("Linear velocity for " + str('%.3f' % float(args.CSV)) + " mm column and " + str('%.3f' % args.linear_velocity) + " mL/min flow is " + str('%.3f' % result) + " cm/sec.")

if args.flow != 171.31: #Dummy number. Helps in calling the script from the CLI with only one flag insted of two.
    result = chromapy.flow(args.flow, float(args.CSV))
    print("Flow for " + str('%.3f' % float(args.CSV)) + " mm column and " + str('%.3f' % args.flow) + " cm/sec linear velocity is " + str('%.3f' % result) + " mL/min.")
