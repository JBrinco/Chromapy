"""
#########################################
ChromaPython - Multivariate Analysis
#########################################

Copyright (C) 2022-2024 João Brinco

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.

##########################################


TO-DO:
    - Area normalization not working for input with classes
    - In label plotting, remove extra column "labels", and acess index directly
    - Add option to graph only the loadings, separated by Type!
    - Fix code so it only needs to output pca_results and loadings once (not original loadings object plus loadings_dataframe)
    - Cleanup the Variance plot



"""

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn.cross_decomposition import PLSRegression, PLSCanonical

def multivariate_import (data):
    """
    Parse extention and import to dataframe accordingly. Will return the dataframe itself.
    """
    excel_extentions = [".xls", ".xlsx", ".xlsm", ".xlsb", ".odf", ".ods", ".odt"]
    if data.lower().endswith('.csv'):
        df = pd.read_csv(data, index_col="Sample")
    elif data.lower().endswith(tuple(excel_extentions)):
        df = pd.read_excel(data, index_col="Sample")
    else:
        print("File extention not given or unrecognized. Please add it to the file name. Example: \"myawesomedata.csv\"")
        exit()
    return df


def normalize (df, normalization="standard", output=""):
    """
    Normalization. Takes the dataframe as input

    NEDDS TO NORMALIZE BY ROW/INDEX/SAMPLE!!! NOT BY COLUMN!
    By default, preprocessing.normalize goes by rows (as it should be), but preprocessing.StandardScaler ("standard") and preprocessing.MinMaxScaler go by columns. Thus, the dataframe needs to be transposed before calculation (df.T), and again after, to retain its original shape.

    normalizaion=
        "area"  Will make the sum of all values in a sample equal to 100. Equivalent to using relative percentages of a chromatogram, ie. assuming the total area is 100%, and the area of each peak is a certain percentage of that.
    """

    # Check for Type column and classes row and drop them for calculations, if existent
    Type_col = False
    Class_col = False
    if "Type" in list(df.columns):
        type_list = df["Type"].tolist()
        df = (df.drop(columns=["Type"]))
        Type_col = True
    if "class" in list(df.index):
        class_list = list(df.loc['class'])
        df = df.drop('class', axis=0)
        if Type_col:
            type_list.remove("class")
        Class_col = True


    #Different normalization algorithms, implemented by sklearn.preprocessing submodule, and one of my own
    if normalization == "normalize":
        df = pd.DataFrame(
            preprocessing.normalize(df, copy=False), #copy=False
            columns=df.columns,
            index=df.index,
            )
    elif normalization == "standard":
        scaler = preprocessing.StandardScaler()
        df = pd.DataFrame(
                scaler.fit_transform(df.T).T,
                columns=df.columns,
                index=df.index,
                )
    elif normalization == "minmax":
        scaler = preprocessing.MinMaxScaler()
        df = pd.DataFrame(
            scaler.fit_transform(df.T).T,
            columns=df.columns,
            index=df.index,
            )
    elif normalization == "area":
        try:
            df_t = df.T
            df = ((df_t/df_t.sum())*100).T
            del(df_t)
        except:
            print("Area normalization not possible for data with classes. Defaulting to standard")
            scaler = preprocessing.StandardScaler()
            df = pd.DataFrame(
                    scaler.fit_transform(df.T).T,
                    columns=df.columns,
                    index=df.index,
                    )


    else:
        print("Error! normalization=\"OPTION\" unrecognized")


    #Adding Type column and class row back if present
    if Type_col:
        df["Type"] = type_list
    if Class_col:
        if Type_col:
            class_list.append("class")
        df.loc["class"] = class_list

    #Printing normalized dataframe if output is set:
    if output.lower().endswith('.csv'):
        df.to_csv(output)
    elif output.lower().endswith('.xlsx'):
        df.to_excel(output)

    return df



def pca (df):

    # Check for Type column and classes row and drop them for calculations, if existent
    Type_col = False
    Class_col = False
    if "Type" in list(df.columns):
        type_list = df["Type"].tolist()
        df = (df.drop(columns=["Type"]))
        Type_col = True
    if "class" in list(df.index):
        class_list = list(df.loc['class'])
        df = df.drop('class', axis = 'index')
        if Type_col == True:
            type_list.remove("class")
        Class_col = True


    # Calculate PCA and put it into pandas dataframe
    pca = PCA(n_components=5)
    pca_result = pd.DataFrame(
        pca.fit_transform(df),
        columns=["PC1", "PC2", "PC3", "PC4", "PC5",],
        index=df.index,
        )

    #Calculate loadings object, to be used in plotting
    loadings = pca.fit(df)

    #Make pandas dataframe from principal components
    loadings_df = pd.DataFrame(
             (loadings).components_.T,
             columns=["PC1", "PC2", "PC3", "PC4", "PC5"],
             index=df.columns,
             )
    #Adding Type to pca_result and classes to loadings_df
    if Type_col == True:
        pca_result["Type"] = type_list
    if Class_col == True:
        loadings_df["class"] = class_list


    return pca_result, loadings_df, loadings




def pca_plot (pca_result, loadings_df, loadings, write_loadings=True, output=False, colors=True, PC=("PC1","PC2"), loadings_scale=1, X=False, Y=False, variance=False, labels=False, grid = False):
    """
    Plotting of PCA. Will output a Biplot by default (samples AND loadings).
    OPTIONS:
    write_loadings - If set to false, will omit loadings and produce a sample-only plot.
    output - Will output a file whose name is the string given: output="myawesomegraph.svg"
    colors - If given an input file with the classes for each loading, will color them accordingly. CURRENTLY NOT WORKING
    PC - Plot the principal components as described. Example: PC=("PC3", "PC5") will plot x as principal component 3 and y as 5. CURRENTLY NOT WORKING FULLY!
    loadings_scale - The scaling factor for loadings, so that they fit well in the byplot.
    X and Y - If set, will center the axis on the number (integer or float) given. So: X=4.5 will set the x axis between -4.5 and 4.5
    variance -
    labels - if set to True, will add labels above each sample. Usually not pretty, but it will show you where each sample is.
    """
    if grid:
        sns.set_theme(style="whitegrid")

    if variance:
        variance_df = pd.DataFrame(
             np.cumsum(loadings.explained_variance_ratio_)*100,
             index=[1, 2, 3, 4, 5])
        var_graph = sns.lineplot(data = variance_df)
        plt.xlabel('Principal Component')
        plt.ylabel('Variance Explained (%)')
        plt.show()

    #Create a "colors" list according to the loading classes, if present.
    if colors:
        classes_present=False
        if "class" in list(loadings_df.columns):
            classes_present=True
            colors_list = ["#F00000", "#09FF00", "#00FF00", "#000080", "#800080", "#959559", "#FF5FFF", "#FFE600", "#552200", "#00E5FF", "#FF6600", "#FF742E", "#FF5959", "#3091FF", "#6E6EFF", "#434932"]
            class_list = loadings_df["class"].tolist()
            #Iterator that asigns color per class value, creating the colors list
            class_color_dict ={}
            i = 0
            colors = []
            for value in class_list:
                if value not in list(class_color_dict.keys()):
                    class_color_dict[value] = colors_list[i]
                    i += 1
                colors.append(class_color_dict[value])


    if "Type" in list(pca_result.columns):
        graph = sns.scatterplot(data=pca_result, x=PC[0], y=PC[1], hue="Type", style="Type", s=300)
    else:
        graph = sns.scatterplot(data=pca_result, x=PC[0], y=PC[1], s=300)

    #Write loadings into the plot. Will take into account the scale and color diferenciation, if set
    if write_loadings:
        for i, label in enumerate(loadings_df.index):
            plt.text(
                    (loadings_df[["PC1", "PC2"]].values)[i, 0] * loadings_scale,
                    (loadings_df[["PC1", "PC2"]].values)[i, 1] * loadings_scale,
                    label,
                    color="#000" if classes_present is False else colors[i],
                    fontweight="bold",
                    ha="center",
                    va="center",
                    )

    #Write sample labels on top of each sample point
    if labels:
        pca_result["label"] = pca_result.index
        for i in range(pca_result.shape[0]):
            plt.text(x=pca_result.PC1[i]+0.05,y=pca_result.PC2[i]+0.05,s=pca_result.label[i],
                       fontdict=dict(color='red',size=10),
                       bbox=dict(facecolor='yellow',alpha=0.3),
                       )
        pca_result = pca_result.pop("label")

    graph.set_xlabel(f"PC1 ({loadings.explained_variance_ratio_[0]*100:.2f} %)")
    graph.set_ylabel(f"PC2 ({loadings.explained_variance_ratio_[1]*100:.2f} %)")

    if X:
        graph.set_xlim(-X, X)
    if Y:
        graph.set_ylim(-Y, Y)

    if output:
        plt.savefig(output, dpi=500)

    # Print the plot and return the graph object.
    plt.show()
    return graph





def pls(df, responses):
    """
    Partial least squares model
    Besides the dataframe, also needs a list with the response column names.
    """

    #Check if "Type" Column is present
    Type_col = False
    if "Type" in list(df.columns):
        Type_col = True

    # Fill x_values and y_values dataframes with the data needed for calculation
    if Type_col:
        x_values = df.drop(columns=['Type'])
    else:
        x_values = df.copy()
    y_values = df[[responses[0]]]

    i = 0
    for column in responses:
        x_values = x_values.drop(columns=[column])
        if i > 0:
            y_values[column] = df.loc[:, column]
        i += 1

    #Run PLS and write output dataframes
    components = 2
    pls = PLSRegression(n_components=components)
    xscores, yscores = pls.fit_transform(x_values, y=y_values)
    pls_result = pd.DataFrame(
            xscores,
        columns=["PC1", "PC2"],
        index=df.index)

    loadings_df = pd.DataFrame(
            pls.x_loadings_,
            columns=["PC1", "PC2"],
            index=x_values.columns)

    response_df = pd.DataFrame(
            pls.y_loadings_,
            columns=["PC1", "PC2"],
            index=y_values.columns)


    if Type_col:
        pls_result['Type']= df['Type']

    return pls_result, loadings_df, response_df


def pls_plot(pls_result, loadings_df, response, loadings_scale=1, labels=False, write_loadings=True, output=False, PC=("PC1","PC2"), grid=False, X=False, Y=False):
    """
    Graphing a PLS regression, very similar to PCA, but with small diferences.
    will take an optional response dataframe that maps the response variables onto the space

    """

    if grid:
        sns.set_theme(style="whitegrid")

    #Make the graph
    if "Type" in list(pls_result.columns):
        graph = sns.scatterplot(data=pls_result, x=PC[0], y=PC[1], hue="Type", style="Type", s=300)
    else:
        graph = sns.scatterplot(data=pls_result, x=PC[0], y=PC[1], s=300)


    #Write loadings into the plot. Will take into account the scale and color diferenciation, if set
    if write_loadings:
        for i, label in enumerate(loadings_df.index):
            plt.text(
                    (loadings_df[["PC1", "PC2"]].values)[i, 0] * loadings_scale,
                    (loadings_df[["PC1", "PC2"]].values)[i, 1] * loadings_scale,
                    label,
                    color="#000", #if classes_present is False else colors[i],
                    fontweight="bold",
                    ha="center",
                    va="center",
                    )
        for i, label in enumerate(response.index):
                plt.text(
                    (response[["PC1", "PC2"]].values)[i, 0] * loadings_scale,
                    (response[["PC1", "PC2"]].values)[i, 1] * loadings_scale,
                    label,
                    color="#FF0000", #if classes_present is False else colors[i],
                    fontweight="bold",
                    ha="center",
                    va="center",
                    )

    #Write sample labels on top of each sample point
    if labels:
        pls_result["label"] = pls_result.index
        for i in range(pls_result.shape[0]):
            plt.text(x=pls_result.PC1[i]+0.05,y=pls_result.PC2[i]+0.05,s=pls_result.label[i],
                       fontdict=dict(color='red',size=10),
                       bbox=dict(facecolor='yellow',alpha=0.3),
                       )
        pls_result = pls_result.pop("label")

    # graph.set_xlabel(f"PC1 ({loadings.explained_variance_ratio_[0]*100:.2f} %)")
    # graph.set_ylabel(f"PC2 ({loadings.explained_variance_ratio_[1]*100:.2f} %)")

    if X:
        graph.set_xlim(-X, X)
    if Y:
        graph.set_ylim(-Y, Y)

    if output:
        plt.savefig(output, dpi=500)


    # Print the plot and return the graph object.
    plt.show()
    return graph
