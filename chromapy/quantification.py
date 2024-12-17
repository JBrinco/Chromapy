"""
#########################################
ChromaPython - Quantification
#########################################

Copyright (C) 2024 João Brinco

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

##########################################




"""

import sys
import os
import datetime

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from matplotlib.backends.backend_pdf import PdfPages


def quant_import(calibration_file, samples_file):
    """
    calibration_file has the calibration data for all compounds, samples_file has the sample signals. Should ideally be .csv, but can also be any of the excel or open document spreadsheet formats
    """

    excel_extentions = [".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods", ".odt"]
    if calibration_file.lower().endswith('.csv'):
        calibration_df = pd.read_csv(calibration_file)
    elif calibration_file.lower().endswith(tuple(excel_extentions)):
        calibration_df = pd.read_excel(calibration_file)
    else:
        print("Calibration file extention not given or unrecognized. Please add it to the file name. Example: \"myawesomedata.csv\"")
        exit()

    if samples_file.lower().endswith('.csv'):
        samples_df = pd.read_csv(samples_file)
    elif samples_file.lower().endswith(tuple(excel_extentions)):
        samples_df = pd.read_excel(samples_file)
    else:
        print("Calibration file extention not given or unrecognized. Please add it to the file name. Example: \"myawesomedata.csv\"")
        exit()

    return calibration_df, samples_df







def quantification(calibration_df, samples_df, file_input = False, int_standard = False, verbose = False, print_results = "None"):
    """
    Calculates the results and merit parameters.
    Requires a dataframe with calibration values and one with samples (see example files).

    TO-DO:
    Put mean and st-dev calculation within the sample loop rather than at the end, and add the results to the print_results file.

    """
    ################PARSER###################

    #If file input is set to True, will assume calibration_df and samples_df to be file names, and will cal quant_inport function above

    if file_input == True:
        calibration_df, samples_df = quant_import(calibration_df, samples_df)


    #Parse the file header and find compound names!
    index = 0
    compounds = []
    concIS_index = None
    signalIS_index = None
    conc_index = None
    #Stores the position of each necessary column, and the names of the analytes. Also stores any other columns present
    for column in list(calibration_df.columns):
        if column == "ConcIS":
            concIS_index = index
        elif column == "SignalIS":
            signalIS_index = index
        elif column == "Conc":
            conc_index = index
        else:
            compounds.append(column)
        index += 1


    #If the int_standard option is set, but it can't find one of the required columns
    if int_standard == True and concIS_index == None:
        print ("I can't find the ConcIS column in your calibration data!")
        sys.exit()
    if int_standard == True and signalIS_index == None:
        print ("I can't find the SignalIS column in your calibration data!")
        sys.exit()
    if conc_index == None:
        print ("I can't find the Conc (Concentration) column in your calibration data!")
        sys.exit()
    if len(compounds) == 0:
        print("There are no compound signal columns in your calibration file! What's going on?")
        sys.exit()


    if verbose == True:
        print("I have found the following compounds:\n")
        for comp in compounds:
            print(comp)
        print("\nWARNING: If any of these is not a compound, it might be causing an error. Please remove that column from your calibration file!")
        print("Calculating with Internal standard set to " + str(int_standard))

    # Add a header to the file where the calibration parameters (r2, LOD, etc.) will be written
    if print_results != "None":
                with open(print_results, 'a') as outfile:
                    outfile.write('\n\n\n\n\n\n##############################\nChromapy Quantification ran on: ' + str(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')) + '\n##############################\n')


    ##################CALIBRATION AND CALCULATION#########################

    results_df = pd.DataFrame()

    #Calibration loop if internal standard option is set
    if int_standard == True:
        calibration_df['AdjustedConc'] = calibration_df['Conc'] / calibration_df['ConcIS']
        results_df["Sample"] = samples_df["Sample"]

        for analyte in compounds: #Per analyte found in the parser above, run the calibration steps
            string = str(analyte) + "Adj" #Set a name for the adjusted signal column
            calibration_df[string] = calibration_df[analyte] / calibration_df['SignalIS']
            slope, intercept, rvalue, pvalue, stderr = stats.linregress(calibration_df['AdjustedConc'],calibration_df[string]) #stats.linregress returns an object with these atributes: slope, intercept, rvalue, pvalue, stderr and intercept_stderr. I could also pull them one by one.
            r2 = rvalue * rvalue
            ConcIS = float(calibration_df.at[1, 'ConcIS'])
            LOD = ((3.3 * stderr) / slope) * ConcIS
            LOQ = ((10 * stderr) / slope) * ConcIS

            if verbose == True:
                print('\n---------------------\n' + analyte + '\n---------------------\n')
                print("Model parameters:\n")
                print("Slope: " + str(format(slope, '.5f')))
                print("Intercept: " + str(format(intercept, '.5f')))
                print("Coeficient of determination: " + str(format(r2, '.5f')))
                print("Limit of Detection: " + str(format(LOD, '.5f')))
                print("Limit of Quantification: " + str(format(LOQ, '0.5f')))

            if print_results != "None":
                with open(print_results, 'a') as outfile:
                    outfile.write('\n---------------------\n' + analyte + '\n---------------------\n')
                    outfile.write("Model parameters:\n")
                    outfile.write("\nSlope: " + str(format(slope, '.5f')))
                    outfile.write("\nIntercept: " + str(format(intercept, '.5f')))
                    outfile.write("\nCoeficient of determination: " + str(format(r2, '.5f')))
                    outfile.write("\nLimit of Detection: " + str(format(LOD, '.5f')))
                    outfile.write("\nLimit of Quantification: " + str(format(LOQ, '0.5f')))


            #PLOT####

            if intercept > 0:
                plot = sns.regplot(x="AdjustedConc", y=analyte, data=calibration_df,
                line_kws={'label':"y={0:.5f}x+{1:.5f}".format(slope,intercept)})
            else:
                plot = sns.regplot(x="AdjustedConc", y=analyte, data=calibration_df,
                line_kws={'label':"y={0:.5f}x{1:.5f}".format(slope,intercept)})
            plot.legend()
            plt.show()



            #Calculate the sample signal!
            results_df[analyte] = (((samples_df[analyte] / samples_df['SignalIS']) - intercept) / slope) * samples_df['ConcIS']







    else:
        results_df["Sample"] = samples_df["Sample"]

        for analyte in compounds: #Per analyte found in the parser above, run the calibration steps
            slope, intercept, rvalue, pvalue, stderr = stats.linregress(calibration_df['Conc'],calibration_df[analyte]) #stats.linregress returns an object with these atributes: slope, intercept, rvalue, pvalue, stderr and intercept_stderr. I could also pull them one by one.
            r2 = rvalue * rvalue
            LOD = ((3.3 * stderr) / slope)
            LOQ = ((10 * stderr) / slope)

            if verbose == True:
                print('\n---------------------\n' + analyte + '\n---------------------\n')
                print("Model parameters:\n")
                print("Slope: " + str(format(slope, '.5f')))
                print("Intercept: " + str(format(intercept, '.5f')))
                print("Coeficient of determination: " + str(format(r2, '.5f')))
                print("Limit of Detection: " + str(format(LOD, '.5f')))
                print("Limit of Quantification: " + str(format(LOQ, '0.5f')))

            if print_results != "None":
                with open(print_results, 'a') as outfile:
                    outfile.write('\n---------------------\n' + analyte + '\n---------------------\n')
                    outfile.write("Model parameters:\n")
                    outfile.write("\nSlope: " + str(format(slope, '.5f')))
                    outfile.write("\nIntercept: " + str(format(intercept, '.5f')))
                    outfile.write("\nCoeficient of determination: " + str(format(r2, '.5f')))
                    outfile.write("\nLimit of Detection: " + str(format(LOD, '.5f')))
                    outfile.write("\nLimit of Quantification: " + str(format(LOQ, '0.5f')))


            #PLOT####

            if intercept > 0:
                plot = sns.regplot(x="Conc", y=analyte, data=calibration_df,
                line_kws={'label':"y={0:.5f}x+{1:.5f}".format(slope,intercept)})
            else:
                plot = sns.regplot(x="Conc", y=analyte, data=calibration_df,
                line_kws={'label':"y={0:.5f}x{1:.5f}".format(slope,intercept)})
            plot.legend()
            plt.show()





            #Calculate the sample signal!
            results_df[analyte] = ((samples_df[analyte] - intercept) / slope)



    ############Calculate the sample values with mean and stdev###############

    #Retrieve sample names into sample list
    sample_list = []
    for sample in results_df['Sample']:
        if not sample in sample_list:
            sample_list.append(str(sample))

    quant_df = pd.DataFrame(index = sample_list)


    # This for loop will go through each analyte in the compound list, create a series for each sample name (in the sample_list), and then calculate the mean and standard deviation
    for analyte in compounds:
        for sample in sample_list:
           sample_values_series = results_df.loc[results_df['Sample'] == sample, analyte]
           quant_df.at[sample, (str(analyte) + " mean")] = (sample_values_series.to_numpy()).mean()
           quant_df.at[sample, (str(analyte) + " st.dev")] = (sample_values_series.to_numpy()).std()


    return quant_df
