#!/bin/python

import chromapy
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn.cross_decomposition import PLSRegression, PLSCanonical

#Import the dataframe
df = chromapy.multivariate_import("Examples_Templates/input_data/wine_data_pls.csv")


responses = ["Response1", "Response2"]



pls_result, pls_loadings, response_df = chromapy.pls(df, responses)

print(pls_result)
print(pls_loadings)

plot = chromapy.pls_plot(pls_result, pls_loadings, response=response_df, labels=False, loadings_scale=15)






exit()

X = df.drop(columns=['Response1', 'Response2', 'Type'])
Y = df[['Response1', 'Response2']]
sns.set_theme(style="darkgrid")

i=2

pls = PLSRegression(n_components=i)
xscores, yscores = pls.fit_transform(X, y=Y)
pls_result = pd.DataFrame(
        xscores,
    columns=["PC1", "PC2"],
    index=df.index)

pls_loadings = pd.DataFrame(
        pls.x_loadings_,
        columns=["PC1", "PC2"],
        index=X.columns)


pls_result['Type']= df['Type']
print(pls_loadings)

exit()

# plot = chromapy.pls_plot(pls_result, pls_loadings, pls)

loadings_scale = 20
classes_present = False
graph = sns.scatterplot(data=pls_result, x="PC1", y="PC2", hue="Type", style="Type", s=300)

for i, label in enumerate(pls_loadings.index):
    plt.text(
            (pls_loadings[["PC1", "PC2"]].values)[i, 0] * loadings_scale,
            (pls_loadings[["PC1", "PC2"]].values)[i, 1] * loadings_scale,
            label,
            color="#000" if classes_present is False else colors[i],
            fontweight="bold",
            ha="center",
            va="center",
            )

plt.show()


print(pls_loadings)
print("-----------")
print(pls_result)
print("\n ---------------\n")

# df = chromapy.normalize(df)

# X = df.drop(columns=['Response1', 'Response2', 'Type'])
# Y = df[['Response1', 'Response2']]


# i=2

# pls = PLSRegression(n_components=i)
# xscores, yscores = pls.fit_transform(X, y=Y)
# pls_result = pd.DataFrame(
#         xscores,
#     columns=["PC1", "PC2"],
#     index=df.index)

# pls_loadings = pd.DataFrame(
#         pls.y_loadings_,
#         columns=["PC1", "PC2"],
#         index=Y.columns)

# print(pls_loadings)
# print("-----------")
# print(pls_result)




















exit()

pca_result, loadings_df, loadings = chromapy.pca(df)
plot = chromapy.pca_plot(pca_result, loadings_df, loadings, output="sample_pca_output.svg", loadings_scale=2, labels=True)

# Check for Type column and classes row and drop them for calculations, if existent
Type_col = False
Class_col = False
if "Type" in list(df.columns):
    type_list = df["Type"].tolist()
    df = (df.drop(columns=["Type"]))
    print(type_list)
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
print(df)
print("-------")
if Type_col:
    df["Type"] = type_list

print(df)


#Adding Type to pca_result and classes to loadings_df
if Type_col == True:
    pca_result["Type"] = type_list
if Class_col == True:
    loadings_df["class"] = class_list



exit()

# pca_result, loadings_df, loadings = chromapy.pca(df)


if df.iloc[0,0] == "class":
    classes_list = df.values[0, 1:].tolist()
    df = df.drop('class', axis = 'index')

# print(df.loc['class'])
classes_list = list(df.loc['class'])
del classes_list[0]


#Grabs the classes and makes a list with them
try:
    classes_list = list(df.loc['class'])
    del classes_list[0]
except:
    classes_list = False


# try:
#     print(df.loc['class'])
#     classes_list = df['class'].tolist()
#     print(classes_list)
# except:
#     # classes_list = False
#     print("Nowhere to be found!")


# df_normalized = chromapy.normalize(df, normalization='area')
# print(df_normalized)

# pca_result, loadings_df, loadings = chromapy.pca(df_normalized)

# plot = chromapy.pca_plot(pca_result, loadings_df, loadings, output="sample_pca_output.svg", loadings_scale=15, labels=True)
