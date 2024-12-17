"""
#########################################
ChromaPython - Design of Experiments
#########################################

Copyright (C) 2024 João Brinco

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

##########################################

The ff2n, full_factorial and plackett_burman functions were based on code originally licensed under:
    MIT License

    Copyright (c) 2020 James Marshall and Benedict Carling

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE

For the original code under the MIT License, please visit: https://github.com/JamesMarshall31/design-of-experiments/
Otherwise all code is licensed under GPL v3.


"""

import pandas as pd
import numpy as np
import itertools
import math
import os


def import_initial_csv(data):
    """
    The original code for ff2n and plackett-burnman requested a dictionary as input. This function provides an abstraction layer so that users can input a .csv or .xlsx file instead.
    """

    excel_extentions = [".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods", ".odt"]
    if data.lower().endswith('.csv'):
        inputdf = pd.read_csv(data)
    elif data.lower().endswith(tuple(excel_extentions)):
        inputdf = pd.read_excel(data)
    else:
        print("File extention not given or unrecognized. Please add it to the file name. Example: \"myawesomedata.csv\"")
        exit()
    dic_factors = inputdf.to_dict(orient="list")

    return dic_factors





def ff2n(data):
    """
    Creates a Two-level full factorial design from the dictionary of factors entered,
    if more than two levels are given for each factor the maximum and minimum values will be selected

    Parameters:
        data: The function calls import_initial_csv, so a csv or excel file can be provided

    Returns:
        df: A dataframe of the two-level full factorial resulting from the factors entered

    Example:
        >>> import design
        >>> Factors = {'Height':[1.6,2],'Width':[0.2,0.4],'Depth':[0.2,0.3]}
        >>> design.Factorial.full_factorial_2level(Factors)
           Height  Width  Depth
        0     1.6    0.2    0.2
        1     1.6    0.2    0.3
        2     1.6    0.4    0.2
        3     1.6    0.4    0.3
        4     2.0    0.2    0.2
        5     2.0    0.2    0.3
        6     2.0    0.4    0.2
        7     2.0    0.4    0.3
    """
    #Check if data is a dictionary or something else. If it's not a dictionary, will asume it to be a file name.
    if isinstance(data, dict):
        dic_factors = data
    else:
        dic_factors = import_initial_csv(data)


    # df is the dataframe that will be returned. matrix is the -1 and 1 matrix
    df = pd.DataFrame()
    matrix = pd.DataFrame()
    # factor_levels will be filled with the levels of each factor and
    # used when iterating through the runs of the design.
    factor_levels = []
    default_levels = []
    # factor_names is filled at the same time as factor_levels and
    # is used at the end to correctly name the columns of the dataframe.
    factor_names = []

    # This for loop fills up factor_levels with the maximum and minimum of each factor,
    # as well as filling up factor_names.
    for name in dic_factors:
        factor_names.append(name)
        factor_levels.append([min(dic_factors[name]), max(dic_factors[name])])
        default_levels.append([-1, 1])

    # This for loop will run through each combination(technically product) and build up
    # the dataframe df with each loop.
    for run in itertools.product(*factor_levels, repeat=1):
        run = list(run)
        s_add = pd.Series(run)
        df = pd.concat([df, s_add], axis=1, ignore_index=True)

    for run in itertools.product(*default_levels, repeat=1):
        run = list(run)
        s_add = pd.Series(run)
        matrix = pd.concat([matrix, s_add], axis=1, ignore_index=True)


    # The dataframe is made with the runs being the columns, we want them to be the rows
    # hence the need to transpose.
    df = df.transpose()
    matrix = matrix.transpose()
    # The column headers are initially labelled '0','1','2' etc.., the line below
    # renames them by relating them to the factor_names list made earlier
    df = df.rename(columns=lambda x: factor_names[x])
    matrix = matrix.rename(columns=lambda x: factor_names[x])

    return df, matrix


def full_factorial(data):
    """
    Creates a full factorial design from the dictionary of factors, but does not choose
    highest and lowest levels of each factor.

    Parameters:
        dic_factors: The dictionary of factors to be included in the full factorial's design

    Returns:
        df: A dataframe of the full factorial resulting from the factors entered

    Example:
        >>> import design
        >>> Factors = {'Height':[1.6,1.8,2],'Width':[0.2,0.3,0.4]}
        >>> design.Factorial.full_factorial(Factors)
            Height  Width
        0     1.6    0.2
        1     1.6    0.3
        2     1.6    0.4
        3     1.8    0.2
        4     1.8    0.3
        5     1.8    0.4
        6     2.0    0.2
        7     2.0    0.3
        8     2.0    0.4
    """

    #Check if data is a dictionary or something else. If it's not a dictionary, will asume it to be a file name.
    if isinstance(data, dict):
        dic_factors = data
    else:
        dic_factors = import_initial_csv(data)

    # The variables initialised below play the same role here as in the two level
    # full factorial above.
    df = pd.DataFrame()
    factor_levels = []
    factor_names = []
    # This for loop plays the same role as the for loop in the two level
    # but does not take the maximum and minimum factor levels, so does not reduce
    # the design to a two level design automatically.
    for name in dic_factors:
        factor_names.append(name)
        factor_levels.append(dic_factors[name])

    # This for loop functions the same as its two level counterpart.
    for run in itertools.product(*factor_levels, repeat=1):
        run = list(run)
        s_add = pd.Series(run)
        df = pd.concat([df, s_add], axis=1, ignore_index=True)
    # As in the two level, the dataframe must be transposed and renamed.
    df = df.transpose()
    df = df.rename(columns=lambda x: factor_names[x])

    return df




def plackett_burman(data, runs):
    """
    Returns a Plackett-Burman design where the number of runs is the next multiple of four higher than the number of runs entered if the runs given isn't a multiple of four. Will also return the matrix (-1 and 1).
    Example:
    Factors = {'Vent_Time':[30,90],'Vent_Pressure':[1,5],'Splitless_time':[60,120], 'Temp_Source':[250, 280], 'Start_Temp_Inlet':[60, 90]}
    design, matrix = chromapy.plackett_burman(Factors, 8)

    You can also input a file name:
    design, matrix = chromapy.plackett_burman("my_file_name.csv", 8)

    """
    #Check if data is a dictionary or something else. If it's not a dictionary, will asume it to be a file name.
    if isinstance(data, dict):
        dic_factors = data
    else:
        dic_factors = import_initial_csv(data)

    # Conditional changes run number to be a multiple of four
    if runs % 4 != 0:
        runs = runs + (4 - (runs % 4))

    #Check if the number of dictionary entries is larger than the required number of runs

    if len(dic_factors) > (runs -1):
        print("The required number of runs is too small for the number of variables. Please increase the number of runs.")
        exit()
    elif len(dic_factors) == (runs -1):
        print("Warning, you are using the maximum number of variables (factors) possible for this run number. For better results, use a larger design (the next multiple of four).")

    # Plackett-Burman designs are made using hadamard matrices
    factor_names = []
    factor_levels = []
    # this for loop fills up factor_levels and factor_names arrays
    for name in dic_factors:
        factor_names.append(name)
        factor_levels.append([min(dic_factors[name]), max(dic_factors[name])])


    #Grabs desired matrix from assets
    array = []
    handle = open("chromapy/assets/" + str(runs) + ".txt")
    for line in handle:
        line = line.strip()
        array.append(list(line.split(',')))
    handle.close()

    df = pd.DataFrame(array[(runs - len(dic_factors)):])
    df = df.transpose()
    matrix = pd.DataFrame.copy(df)

    # The dataframe is currently '+' and '-' so this for loop converts to the factor levels entered in the dictionary
    for i in range(len(dic_factors)):
        df[i] = df[i].apply(lambda y: factor_levels[i][0] if y == '-1' else factor_levels[i][1])
    df = df.rename(columns=lambda y: factor_names[y])
    matrix = matrix.rename(columns=lambda y: factor_names[y])
    # # df["Index"] = range(len(df))
    # df.insert(0, "Index", (range(len(df))))
    # df.set_index("Index")

    # matrix.insert(0, "Index", (range(len(matrix))))
    # # matrix["Index"] = range(len(matrix))
    # matrix.set_index("Index")

    return df, matrix






def main_effect(results, matrix, dataframe = False, output = "main_effect_output.csv", print_to_terminal = True, return_dictionary = False):
    """
    Calculation of main effect. Will take in either tabular/spreadsheet files or pandas dataframes (set dataframe = True). Will return a dataframe or dictionary of main effect for each factor.
    Set output=False to supress .csv generation
    Check the example input files to understand the input format
    """

    #Read .csv or other if dataframe is set to false. Otherwise will already assume correctly formatted dataframes
    if dataframe == False:
        excel_extentions = [".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods", ".odt"]
        if results.lower().endswith('.csv'):
            results = pd.read_csv(results)
        elif results.lower().endswith(tuple(excel_extentions)):
            results = pd.read_csv(results)
        else:
            print("Results file extention not given or unrecognized. Please add it to the file name. Example: \"myawesomedata.csv\"")
            exit()

        if matrix.lower().endswith('.csv'):
            matrix = pd.read_csv(matrix)
        elif matrix.lower().endswith(tuple(excel_extentions)):
            matrix = pd.read_csv(matrix)
        else:
            print("Matrix file extention not given or unrecognized. Please add it to the file name. Example: \"myawesomedata.csv\"")
            exit()

    #Set values to float, to avoid problems
    matrix = matrix.astype('float')
    results = results.astype('float')

    #If the matrix and index dataframes have different numbers of rows, will throw an assertion error!
    assert len(matrix.index) == len(results.index), "The DOE matrix and Results do not have the same number of rows!"

    #Create empty numpy array, and fill it with the results, then multiply the matrix (-1 and 1) by the results, to get a dataframe with the results properly inverted. This is redundant, as results_np could be gotten directly from the .csv file. But if a dataframe is passed directly to the function (dataframe=True), it works.
    results_np = np.empty(0)
    for index, row in results.iterrows():
        results_np = np.append(results_np, row.iloc[0]) # row.iloc[0] used to be row[0], but it would get a futurewarning saying this type of indexing was deprecated
    results_multiplied = matrix.multiply(results_np, axis=0)


    #This calculates the main effect. The calculation is made difficult when there are different numbers of 1 and -1 for a given column (factor or variable), meaning no orthogonality. This double loop iterates over columns and rows of the multiplied results, finds which values are -1 and 1 in the matrix, and sums them and divides them accordingly. The result is a dictionary with the main effects. If the matrix had always the same amount of -1 and 1 for each factor, we could simply do:
    #results_sum = {column: results_multiplied[column].sum() for column in results_multiplied.columns.values}
    #matrix_sum = {column: matrix[column].sum() for column in matrix.columns.values}
    main_effect = {}
    for column in results_multiplied.columns.values:
        num_neg = 0
        sum_neg = 0
        num_pos = 0
        sum_pos = 0
        for index in results_multiplied.index.values:
            matrix_value = matrix.loc[index, column]
            value = results_multiplied.loc[index, column]
            if matrix_value < 0:
                num_neg = num_neg + 1
                sum_neg = sum_neg + value
            else:
                num_pos = num_pos + 1
                sum_pos = sum_pos + value
        main_effect[column] = (sum_pos/num_pos)+(sum_neg/num_neg)

    # Turn dictionary back into dataframe, print values
    main_effect_df = pd.DataFrame(main_effect.values(), index = main_effect.keys())
    if print_to_terminal == True:
        print("Main Effect:")
        print("----------")
        print(main_effect_df.to_string(header=False))
    # main_effect_df = main_effect_df.transpose()

    #Create .csv if wanted. THIS SHOULD GO INTO THE SCRIPT!!!!
    if output != False:
        main_effect_df.to_csv(output, index = True)

    if return_dictionary == True:
        return main_effect
    else:
        return main_effect_df



######## Response Surface Modeling ########


def box_behnken(inputfile, randomize = True, output = "Box-Behnken_Design.csv"):
    '''
    Takes in a properly formatted csv or excel and returns a box-behnken design, randomized or not.
    Uses pandas to generate the lists required for the design because it is easier than doing it in native R.
    All the heavy work is done by the rsm package in R, interfaced by rpy2, which enables running an R instance and code directly from python.
    Check the example inputfile for an idea of the formatting required
    '''
    import rpy2.robjects as robjects # Imports R objects into python and other shenanigans
    import rpy2.robjects.packages as rpackages #Package management
    r = robjects.r # Makes things more readable. r is called only with r.

    #Check if rsm is installed, and if not install it! Will only load utils package if needed, so can be run with every box_behnken call because it will not take long to evaluate the if not.
    if not rpackages.isinstalled('rsm'):
        try:
            utils = rpackages.importr('utils') # import R's utility package and select a mirror
            utils.chooseCRANmirror(ind=1) #This will error if no internet connection exists
            utils.install_packages('rsm')
            print("An R package called rsm package has been installed for response surface modeling.")
        except:
            print("An error occured getting the required R package (rsm)\nPlease make sure you have an internet connection")

    #Import rsm package
    rsm = rpackages.importr('rsm')

    excel_extentions = [".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods", ".odt"]
    if inputfile.lower().endswith('.csv'):
        inputdf = pd.read_csv(inputfile)
    elif data.lower().endswith(tuple(excel_extentions)):
        inputdf = pd.read_excel(inputfile)
    else:
        print("File extention not given or unrecognized. Please add it to the file name. Example: \"myawesomedata.csv\"")
        exit()

    #Count number of columns and assume that is the number of factors
    Factors_number = int(len(inputdf.columns))

    #Generate py_vls (the center values), py_dvt (the deviations, +-) and py_var_names, the name of each factor. .values returns np array, .flatten makes the np array one dimentional. flatten is probably useless, but harmless...
    py_vls = inputdf.loc[0, :].values.flatten().tolist()
    py_dvt = inputdf.loc[1, :].values.flatten().tolist()
    py_var_names = inputdf.columns.values.flatten().tolist()

    # Create R variables (vectors) from the parsed lists
    vls = robjects.FloatVector(py_vls)
    dvt = robjects.FloatVector(py_dvt)
    var_names = robjects.StrVector(py_var_names)

    # Export those variables to the R global environment, so they can be used within the R code
    robjects.globalenv['vls'] = vls
    robjects.globalenv['dvt'] = dvt
    robjects.globalenv['var_names'] = var_names


    # Declares R functions.
    # "generate_bbd", for box-Behnken design generation. Needs an if elif for handling different number of factors. This has to be hardcoded because rsm is not built for this stuff. Will use vls and dvt already parsed and added to R's globalenv
    r('''
  generate_bbd <- function(Factors_number, random = TRUE) {
    if (Factors_number == 2) {
        design <- bbd(Factors_number, block = FALSE, randomize = random,  coding = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]] ))

    } else if (Factors_number == 3) {
        design <- bbd(Factors_number, block = FALSE, randomize = random,  coding = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] ))

    } else if  (Factors_number == 4) {
        design <- bbd(Factors_number, block = FALSE, randomize = random,  coding = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]], x4 ~ (d - vls[[4]])/dvt[[4]]))

    } else if (Factors_number == 5) {
        design <- bbd(Factors_number, block = FALSE, randomize = random,  coding = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] , x4 ~ (d - vls[[4]])/dvt[[4]] , x5 ~ (e - vls[[5]])/dvt[[5]]))

    } else if (Factors_number == 6) {
        design <- bbd(Factors_number, block = FALSE, randomize = random,  coding = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] , x4 ~ (d - vls[[4]])/dvt[[4]] , x5 ~ (e - vls[[5]])/dvt[[5]] , x6 ~ (f - vls[[6]])/dvt[[6]]))

    } else if (Factors_number == 7) {
        design <- bbd(Factors_number, block = FALSE, randomize = random,  coding = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] , x4 ~ (d - vls[[4]])/dvt[[4]] , x5 ~ (e - vls[[5]])/dvt[[5]] , x6 ~ (f - vls[[6]])/dvt[[6]] , x7 ~ (g - vls[[7]])/dvt[[7]]))

    } else{
        print("Unrecognized or unsuported number of Factors (variables)")}
        }



    rename_design <- function(design, var_names){
        first_var_names <- list("run.order", "std.order")
        variable_names <- c(first_var_names, var_names)
        truenames(design) <- variable_names
        design$Results <- 0

        return(design)
        }

    output_design <- function(design, output) {
        write.csv(decode.data(design), output, row.names=FALSE)
    }

    ''')

    #Pythonize the syntax
    generate_bbd = r['generate_bbd']
    rename_design = r['rename_design']
    output_design = r['output_design']

    # Create the design! Will be stored as an R object, not python!!!!
    if randomize == True:
        design = generate_bbd(Factors_number)
    else:
        design = generate_bbd(Factors_number, random = False)

    # Change standard design factor names by their actual names and add "Results" column so people know where to put them
    new_design = rename_design(design, var_names)

    if output != False:
        output_design(new_design, output = output)

    return(new_design)



def add_results(design, results):
    '''
    This is used when you handle everything internally within python. You can generate a design, save it somehow as an R object, and then add the results directly.
    This function takes a design (an R object) and a list of results (usually floats), and adds those results to the R object (which is actually a coded dataframe from rsm), so that it can be used to calculate the response surface.
    '''
    import rpy2.robjects as robjects # Imports R objects into python and other shenanigans
    import rpy2.robjects.packages as rpackages #Package management
    r = robjects.r # Makes things more readable. r is called only with r.
    rsm = rpackages.importr('rsm')

    # Make Results (capital R!) which is a vector of floats, and export it to R globalenvironment.
    Results = robjects.FloatVector(results)
    robjects.globalenv['Results'] = Results
    robjects.globalenv['design'] = design

    r('''
       design$Results <- Results
    ''')
    design_out = r['design']

    return design_out


def rsm(data, inputfile, print_summary = True, write_summary = True):
    '''
    Calculate/generate the response surface model
    The input can be either an R object or a .csv file. Excel is currently not supported, but it might be in the future (imported directly by R)
    data is the csv or R dataframe with the complete design plus the Results
    inputfile is the same as in the box_behnken function: it is the csv or excel with the initial values, before the design was made.
    Use write_summary = "filename.txt" to write the summary to a specific file. Alternativly just write_summary = True will output it with a standard name.
    '''

    #Explained in box_behnken above
    import rpy2.robjects as robjects # Imports R objects into python and other shenanigans
    import rpy2.robjects.packages as rpackages #Package management
    r = robjects.r # Makes things more readable. r is called only with r.
    if not rpackages.isinstalled('rsm'):
        try:
            utils = rpackages.importr('utils') # import R's utility package and select a mirror
            utils.chooseCRANmirror(ind=1) #This will error if no internet connection exists
            utils.install_packages('rsm')
            print("An R package called rsm package has been installed for response surface modeling.")
        except:
            print("An error occured getting the required R package (rsm)\nPlease make sure you have an internet connection")

    rsm = rpackages.importr('rsm')
    # Factors_number = int(factors) #Factors_number is used to call the R code. It has the same name inside the R code.

    ########## Parse the design. and recode data if necessary #########

    #file names will always be passed as strings, so check if "design" is a string
    if isinstance(data, str):
        if data.lower().endswith('.csv'):
           r('''
           read_csv <- function(csv_name) {
           designdf <- read.csv(csv_name)
           return(designdf)
           }
           ''')
           read_csv = r['read_csv']
           designdf = read_csv(data)

           ###### Generate vls, dvt and var_names. This code is the same as above in the box-behnken function, but making a single outside function made it confusing, so it is repeated
           #Parse the inputfile
           excel_extentions = [".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods", ".odt"]
           if inputfile.lower().endswith('.csv'):
               inputdf = pd.read_csv(inputfile)
           elif data.lower().endswith(tuple(excel_extentions)):
               inputdf = pd.read_excel(inputfile)
           else:
               print("File extention not given or unrecognized. Please add it to the file name. Example: \"myawesomedata.csv\"")
               exit()

           #Generate py_vls (the center values), py_dvt (the deviations, +-) and py_var_names, the name of each factor. .values returns np array, .flatten makes the np array one dimentional. flatten is probably useless, but harmless...
           py_vls = inputdf.loc[0, :].values.flatten().tolist()
           py_dvt = inputdf.loc[1, :].values.flatten().tolist()
           py_var_names = inputdf.columns.values.flatten().tolist()
           # Create R variables (vectors) from the parsed lists
           vls = robjects.FloatVector(py_vls)
           dvt = robjects.FloatVector(py_dvt)
           var_names = robjects.StrVector(py_var_names)
           # Export those variables to the R global environment, so they can be used within the R code
           robjects.globalenv['vls'] = vls
           robjects.globalenv['dvt'] = dvt
           robjects.globalenv['var_names'] = var_names
           #Count number of columns and assume that is the number of factors
           Factors_number = int(len(inputdf.columns))

           #Recode data function. needs vls and dvt. Needs also to return the factor names to a, b, c, d, etc before recoding, and then turning them back to their true names. Otherwise colnames and coded data will be different, and it will be impossible to set truenames
           r('''
        recode_data <- function(data, Factors_number) {
            first_var_names <- list("run.order", "std.order")
            last_var_name <- list("Results")
            if (Factors_number == 2) {
                var_names <- list("a", "b")
                colnames(data) <- c(first_var_names, var_names, last_var_name)
                design_results <- coded.data(data, formulas = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]]))

            } else if (Factors_number == 3) {
                var_names <- list("a", "b", "c")
                colnames(data) <- c(first_var_names, var_names, last_var_name)
                design_results <- coded.data(data,  formulas = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] ))

            } else if  (Factors_number == 4) {
                var_names <- list("a", "b", "c", "d")
                colnames(data) <- c(first_var_names, var_names, last_var_name)
                design_results <- coded.data(data, formulas = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]], x4 ~ (d - vls[[4]])/dvt[[4]]))

            } else if (Factors_number == 5) {
                var_names <- list("a", "b", "c", "d", "e")
                colnames(data) <- c(first_var_names, var_names, last_var_name)
                design_results <- coded.data(data, formulas = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] , x4 ~ (d - vls[[4]])/dvt[[4]] , x5 ~ (e - vls[[5]])/dvt[[5]]))

            } else if (Factors_number == 6) {
                var_names <- list("a", "b", "c", "d", "e", "f")
                colnames(data) <- c(first_var_names, var_names, last_var_name)
                design_results <- coded.data(data, formulas = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] , x4 ~ (d - vls[[4]])/dvt[[4]] , x5 ~ (e - vls[[5]])/dvt[[5]] , x6 ~ (f - vls[[6]])/dvt[[6]]))

            } else if (Factors_number == 7) {
                var_names <- list("a", "b", "c", "d", "e", "f", "g")
                colnames(data) <- c(first_var_names, var_names, last_var_name)
                design_results <- coded.data(data, formulas = list(x1 ~ (a - vls[[1]])/dvt[[1]], x2 ~ (b - vls[[2]])/dvt[[2]], x3 ~ (c - vls[[3]])/dvt[[3]] , x4 ~ (d - vls[[4]])/dvt[[4]] , x5 ~ (e - vls[[5]])/dvt[[5]] , x6 ~ (f - vls[[6]])/dvt[[6]] , x7 ~ (g - vls[[7]])/dvt[[7]]))

            } else{
                print("Unrecognized or unsuported number of Factors (variables)")}
            return(design_results)
                }

             rename_design <- function(design_results){
                first_var_names <- list("run.order", "std.order")
                last_var_name <- list("Results")
                variable_names <- c(first_var_names, var_names, last_var_name)
                truenames(design_results) <- variable_names

                return(design_results)
                }
                           ''')
           recode_data = r['recode_data']
           rename_design = r['rename_design']
           design_results = recode_data(designdf, Factors_number)
           coded_design = rename_design(design_results)

        else:
           print("File extention not given or unrecognized. Please add it to the file name. Only CSV currently suported. Example: \"myawesomedata.csv\"")
           exit()

    #If its not a string, must be an R object, and just needs to get the number of factors. Will assume "Results" tab is already full. vls and dvt are also not needed
    else:
        coded_design = data
        robjects.globalenv['coded_design'] = coded_design # export to R globalenv
        Factors_number = int(len(r('''colnames(coded_design)'''))-3) # Count number of columns, remove 3 (run.order, std.order and Results) and assume that is the number of factors



##### Calculate RSM ######
    r('''
    calculate_rsm <- function(coded_design, Factors_number, filename = "RSM_Summary.txt") {
    if (Factors_number == 2) {
        design_results.rsm <- rsm(Results ~ SO(x1, x2), data = coded_design)

    } else if (Factors_number == 3) {
        design_results.rsm <- rsm(Results ~ SO(x1, x2, x3), data = coded_design)

    } else if  (Factors_number == 4) {
        design_results.rsm <- rsm(Results ~ SO(x1, x2, x3, x4), data = coded_design)

    } else if (Factors_number == 5) {
        design_results.rsm <- rsm(Results ~ SO(x1, x2, x3, x4, x5), data = coded_design)

    } else if (Factors_number == 6) {
        design_results.rsm <- rsm(Results ~ SO(x1, x2, x3, x4, x5, x6), data = coded_design)

    } else if (Factors_number == 7) {
        design_results.rsm <- rsm(Results ~ SO(x1, x2, x3, x4, x5, x6, x7), data = coded_design)
    }
    if (filename != FALSE) {
        outtext<-capture.output(summary(design_results.rsm))
        cat(outtext, file = filename, sep="\n", append=TRUE)
    }
    return(design_results.rsm)

    }
        ''')
    # Call the calculate_rsm R function, and then export the result to R's globalenv so that we can get the summary
    calculate_rsm = r['calculate_rsm']
    if write_summary == False:
        design_rsm = calculate_rsm(coded_design, Factors_number, filename = False)
    elif write_summary != True:
        design_rsm = calculate_rsm(coded_design, Factors_number, filename = write_summary)
    else:
        design_rsm = calculate_rsm(coded_design, Factors_number)



    robjects.globalenv['design_results.rsm'] = design_rsm

    if print_summary == True:
        print("-----------------------")
        print("\nSUMMARY of Response Surface modelling.")
        print("Stationary point of response surface should be within -1 to 1, which means it is within the experiment boundaries.")
        print(r('''summary(design_results.rsm)'''))
        print("-----------------------")

    return (design_rsm)


def rsm_plot(design_rsm, pdf = "RSM_plot.pdf", three_d = True, override_pdf = False):
    '''
    Draw the plot. Will output several plots, you can choose which you like. Manually messing with the plots can be tricky, but you can change the R code if you are so inclined.
    Input is the rsm object returned from the chromapy.rsm function.
    three_d - Set to false to produce 2D plots
    pdf - name of the pdf output. Running R in script does not produce an interactive plot. It will simply output it to pdf. So you will not see the plot until you open the pdf file.
    override_pdf - Set to true if you want to write over the previous plot file (if the name is the same).
    '''

    #Explained in box_behnken above
    import rpy2.robjects as robjects # Imports R objects into python and other shenanigans
    import rpy2.robjects.packages as rpackages #Package management
    r = robjects.r # Makes things more readable. r is called only with r.
    if not rpackages.isinstalled('rsm'):
        try:
            utils = rpackages.importr('utils') # import R's utility package and select a mirror
            utils.chooseCRANmirror(ind=1) #This will error if no internet connection exists
            utils.install_packages('rsm')
            print("An R package called rsm package has been installed for response surface modeling.")
        except:
            print("An error occured getting the required R package (rsm)\nPlease make sure you have an internet connection")
    rsm = rpackages.importr('rsm')


    # If override_pdf was not set to true and the pdf file name already exists, exit with a message
    if override_pdf != True and os.path.isfile(pdf):
        print("A pdf file already exists with the same name as the output created by this call. To avoid rewriting, please change the pdf name with pdf = \"Filename\". Alternatively, you can use override_pdf = True, which will write over the previous file, deleting it.")
        exit()

    r('''
    rsm_plotting <- function(design_rsm, pdf_file, three_dimentions = TRUE) {
        pdf(file = pdf_file) # Sets the pdf file to where stuff is going
        xs <- canonical(design_results.rsm)$xs # Important variable, contains the stationary point
        Factors_number = length(xs) # Returns factor number from looking at the results

        # This generates a hook on the stationary point, so that we can plot around it!
        myhook <- list()
        myhook$post.plot <- function(lab) {
        idx <- sapply(lab[3:4], grep, names(xs))
        points (xs[idx[1]], xs[idx[2]], pch=2, col="red")}

        if (Factors_number == 2) {
            if (three_dimentions == FALSE){
                contour(design_results.rsm, ~ x1 + x2, image =TRUE) # Simple contour plot, 2D, default
                contour (design_results.rsm, ~ x1 + x2, image = TRUE, at = xs, hook = myhook) # Center on stationary point
                }
            else {
                persp (design_results.rsm, ~ x1 + x2, col = rainbow(50), contours = "colors") # Default output
                persp (design_results.rsm, ~ x1 + x2, at = xs, col = rainbow(50), contours = "colors", hook = myhook) #Center on stationary point
                }

        } else if (Factors_number == 3) {
            if (three_dimentions == FALSE){
                contour(design_results.rsm, ~ x1 + x2 + x3, image =TRUE) # Simple contour plot, 2D, default
                contour (design_results.rsm, ~ x1 + x2 + x3, image = TRUE, at = xs, hook = myhook) # Center on stationary point
                }
            else {
                persp (design_results.rsm, ~ x1 + x2 + x3, col = rainbow(50), contours = "colors") # Default output
                persp (design_results.rsm, ~ x1 + x2 + x3, at = xs, col = rainbow(50), contours = "colors", hook = myhook) #Center on stationary point
                }

        } else if  (Factors_number == 4) {
            if (three_dimentions == FALSE){
                contour(design_results.rsm, ~ x1 + x2 + x3 + x4, image =TRUE) # Simple contour plot, 2D, default
                contour (design_results.rsm, ~ x1 + x2 + x3 + x4, image = TRUE, at = xs, hook = myhook) # Center on stationary point
                }
            else {
                persp (design_results.rsm, ~ x1 + x2 + x3 + x4, col = rainbow(50), contours = "colors") # Default output
                persp (design_results.rsm, ~ x1 + x2 + x3 + x4, at = xs, col = rainbow(50), contours = "colors", hook = myhook) #Center on stationary point
                }

        } else if (Factors_number == 5) {
            if (three_dimentions == FALSE){
                contour(design_results.rsm, ~ x1 + x2 + x3 + x4 + x5, image =TRUE) # Simple contour plot, 2D, default
                contour (design_results.rsm, ~ x1 + x2 + x3 + x4 + x5, image = TRUE, at = xs, hook = myhook) # Center on stationary point
                }
            else {
                persp (design_results.rsm, ~ x1 + x2 + x3 + x4 + x5, col = rainbow(50), contours = "colors") # Default output
                persp (design_results.rsm, ~ x1 + x2 + x3 + x4 + x5, at = xs, col = rainbow(50), contours = "colors", hook = myhook) #Center on stationary point
                }

        } else if (Factors_number == 6) {
            if (three_dimentions == FALSE){
                contour(design_results.rsm, ~ x1 + x2 + x3 + x4 + x5 + x6, image =TRUE) # Simple contour plot, 2D, default
                contour (design_results.rsm, ~ x1 + x2 + x3 + x4 + x5 + x6, image = TRUE, at = xs, hook = myhook) # Center on stationary point
                }
            else {
                persp (design_results.rsm, ~ x1 + x2 + x3 + x4 + x5 + x6, col = rainbow(50), contours = "colors") # Default output
                persp (design_results.rsm, ~ x1 + x2 + x3 + x4 + x5 + x6, at = xs, col = rainbow(50), contours = "colors", hook = myhook) #Center on stationary point
                }

        } else if (Factors_number == 7) {
            if (three_dimentions == FALSE){
                contour(design_results.rsm, ~ x1 + x2 + x3 + x4 + x5 + x6 + x7, image =TRUE) # Simple contour plot, 2D, default
                contour (design_results.rsm, ~ x1 + x2 + x3 + x4 + x5 + x6 + x7, image = TRUE, at = xs, hook = myhook) # Center on stationary point
                }
            else {
                persp (design_results.rsm, ~ x1 + x2 + x3 + x4 + x5 + x6 + x7, col = rainbow(50), contours = "colors") # Default output
                persp (design_results.rsm, ~ x1 + x2 + x3 + x4 + x5 + x6 + x7, at = xs, col = rainbow(50), contours = "colors", hook = myhook) #Center on stationary point
                }
        }
    }


    ''')

    #Call the function, pass the arguments
    rsm_plotting = r['rsm_plotting']
    rsm_plotting(design_rsm, pdf, three_dimentions = three_d)

    # Print output path. If windows will be using different kind of slashes...
    if os.name == 'nt':
        print("Output written to " + os.getcwd() + "\\" + pdf )
    else:
        print("Output written to " + os.getcwd() + "/" + pdf )

    # No returns here. The plots will be written to a file directly
