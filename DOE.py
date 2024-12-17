#!/bin/python

"""
This file is part of Chromapy (https://github.com/JBrinco/Chromapy).
Copyright (c) 2024 João Brinco.

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful, but 
WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import argparse
import chromapy

parser = argparse.ArgumentParser(
        epilog="Design of Experiments and Response Surface Modeling. For good results, always use the template files, and preferably .csv files.",
        )
parser.add_argument("CSV", help="The file with the input data. Can be .csv, .xlsx, .ods, etc. Even for calculating the RSM, this file should be the first one, without the design or the results.")
parser.add_argument("-p", "--plackett_burman", type=int, help="Plackett Burman design. Requires number of runs (4, 8, 16...) Example: -p 8.")
parser.add_argument("-f", "--ff2n", help="Full factorial with two levels.", action="store_true")
parser.add_argument("-F", "--ff", help="Full factorial", action="store_true")
parser.add_argument("-m", "--main_effect", type=str, help="Calculate main effect. Requires a file name where the results are. other input file must be the matrix with which the results were made. Example: python DOE.py \"DOE_matrix_used.csv\" -m \"DOE_Results_column.csv\"")
parser.add_argument("-b", "--box_behnken", help="Box-Behnken design. Can accept an argument with the name of the outputfile. Otherwise, default is \"BB-Design.csv\" ", action="store_true")
parser.add_argument("-R", "--randomize", help="Randomize Box-Behnken design.", action="store_true", default = False)
parser.add_argument("-r", "--rsm", type=str, help="Calculate Response Surface. Requires a file name where the box-behnken design and results are. Example: -r \"myfile.csv\"")
parser.add_argument("-t", "--text_name", type=str, help="Name of textfile for output. When used with -b, -p or -f will output a .csv with the design. When used with -r will output the summary of the RSM.", default="NULL")
parser.add_argument("-P", "--plot", help="Plot (pdf) output for rsm. Must be used with -r. Default is \"RSM_Plot.pdf\", but you can add a name with the -i option. Example: -P -i \"output_file_name.pdf\". CAUTION: if a pdf with the same name already exists, it will be OVERWRITTEN.", action = "store_true")
parser.add_argument("-i", "--image", type=str, help="Image (pdf) output for rsm. Must be used with -r. Default is \"RSM_Plot.pdf\", but you can add a name. Example: -i \"output_file_name.pdf\"", default = "NULL")
parser.add_argument("-d", "--two_d", help="Make output images 2D instead of 3D (default). Must be used with -P (and -r).", action = "store_true")
parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true", default = False)
args = parser.parse_args()


# Make Plackett-Burman Design
if args.plackett_burman:
    try:
        pb_design, matrix = chromapy.plackett_burman(args.CSV, args.plackett_burman)
    except:
        print("An error ocurred. You probably specified too small a number of runs. Try increasing it!")

    if args.text_name == "NULL":
        pb_design.to_csv('Plackett_Burman_design.csv', index = False)
    elif args.text_name != "NULL":
        pb_design.to_csv(args.textname, index = False)
    matrix.to_csv('Plackett_Burman_matrix.csv', index = False)

    if args.verbose == True:
        print("Plackett-Burman Design")
        print(pb_design)
        print("\nPlackett-Burman Matrix")
        print(matrix)

#Make Full Factorial (2 levels)
if args.ff2n:
    ff2n_design, matrix = chromapy.ff2n(args.CSV)

    if args.text_name == "NULL":
        ff2n_design.to_csv('Full_Factorial_2Level_design.csv', index = False)
    elif args.text_name != "NULL":
        ff2n_design.to_csv(args.textname, index = False)
    matrix.to_csv('Full_Factorial_2Level.csv', index = False)

    if args.verbose == True:
        print("Full-Factorial two-level Design")
        print(ff2n_design)
        print("\nFull-Factorial Matrix")
        print(matrix)

#Make Full Factorial (2 levels)
if args.ff:
    ff_design = chromapy.full_factorial(args.CSV)

    if args.text_name == "NULL":
        ff_design.to_csv('Full_Factorial_design.csv', index = False)
    elif args.text_name != "NULL":
        ff_design.to_csv(args.textname, index = False)

    if args.verbose == True:
        print("Full-Factorial Design")
        print(ff_design)



# Calculate Main Effect
if args.main_effect:
    main_effect_df = chromapy.main_effect(args.main_effect, args.CSV, output = False)
    with open("Main_effect.txt", "a") as f:
        print("----------", file=f)
        print("Main Effect:", file=f)
        print("----------", file=f)
        print(main_effect_df.to_string(header=False), file=f)

    if args.verbose == True:
        print("Main effect calculation")
        print(main_effect_df)


# Make Box-Behnken Design
if args.box_behnken:
    if args.text_name != "NULL":
        bb_design = chromapy.box_behnken(args.CSV, randomize = args.randomize, output = args.text_name)
    else:
        bb_design = chromapy.box_behnken(args.CSV, randomize = args.randomize)

# Calculate RSM
if args.rsm:
    if args.text_name != "NULL":
        design_rsm = chromapy.rsm(args.rsm, args.CSV, write_summary = args.text_name)
    else:
        design_rsm = chromapy.rsm(args.rsm, args.CSV)

    # Make Plots
    if args.plot:
        if args.image != "NULL":
            chromapy.rsm_plot(design_rsm, pdf = args.image, three_d = (not args.two_d), override_pdf = True) # if two_d is set to True, then three_d will be set to False, and the output will be 2D
        else:
            chromapy.rsm_plot(design_rsm, three_d = (not args.two_d), override_pdf = True) # if two_d is set to True, then three_d will be set to False, and the output will be 2D
