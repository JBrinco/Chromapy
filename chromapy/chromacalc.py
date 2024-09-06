"""
#########################################
ChromaPython - Chromatography-related Calculators
#########################################

Copyright (C) 2022-2024 João Brinco

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

##########################################

FUNCTIONS:

-HPLC SOLVENT CALCULATOR
Will calculate how much of a given eluent is used in a run. Flow and time must be in the SAME UNIT! Result will be in the same volume unit as flow.
You can use hplc_solvent_manual, where you have to create numpy arrays yourself, such as:
    y = np.array([90, 0])
    x = np.array([0, 20])
and then feed them to the function. Althernatively, you can just use the simpler hplc_solvent, which takes in a correctly formatted dataframe.
"""

import numpy as np
import pandas as pd
from scipy import integrate
from math import pi


def hplc_solvent_manual (flow, y_array, x_array):
    """
    Input: y is percentage of that solvent, x is the time. Flow must be per MINUTE. Works with numpy arrays
    """

    y = y_array*flow/100
    result = integrate.trapezoid(y, x_array)

    return result


def hplc_solvent(data):
    """
    data is a csv, excel, etc, with the data. See example in the input files.
    """
    #Parse extention and import to dataframe accordingly. Will return the dataframe itself.

    excel_extentions = [".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods", ".odt"]
    if data.lower().endswith('.csv'):
        df = pd.read_csv(data)
    elif data.lower().endswith(tuple(excel_extentions)):
        df = pd.read_excel(data)
    else:
        print("File extention not given or unrecognized. Please add it to the file name. Example: \"myawesomedata.csv\"")
        exit()

    #After parsing, calculates as above. Flow must be per MINUTE.
    flow = df["Flow"].iloc[0]
    y = df["Percent"].values
    x = df["Time"].values

    y = y*flow/100
    result = integrate.trapezoid(y, x)

    return result

def lin_velocity(flow, diameter):
    """
    Flow in mL/min, and column diameter in mm (what says on the box, generally 0.1, 0.18, 0.25 or 0.32). Outputs linear velocity in cm/sec.
    """
    linear_velocity = (flow *4) / (60 * pi * ((diameter * 0.1)**2))
    return linear_velocity

def flow(lin_vel, diameter):
    """
    Linear velocity in cm/sec and column diameter same as above. Outputs flow in mL/min.
    """
    Flow = lin_vel * 60 * ((pi * ((diameter * 0.1)**2))/4)
    return Flow
