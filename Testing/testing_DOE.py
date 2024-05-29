#!/bin/python

import pandas as pd
import numpy as np
import chromapy
from sklearn.cross_decomposition import PLSRegression, PLSCanonical


matrix = pd.read_csv("DOE_matrix.csv")
results = pd.read_csv("DOE_results.csv")

print(matrix)
print("----")


main_effect = chromapy.main_effect("DOE_results.csv", "DOE_matrix.csv", dataframe=False, return_dictionary=True)

print(main_effect)


# # Factors = {'Vent_Time':[30,90],'Vent_Pressure':[1,5],'Splitless_time':[60,120], 'Temp_Source':[250, 280], 'Start_Temp_Inlet':[60, 90]}
# dic_factors = chromapy.import_initial_csv("DOE_Input.csv")

# design, matrix = chromapy.plackett_burman("DOE_Input.csv", 12)



# # print(dic_factors)
# # print("----")
# # print(design)
# # print("----")
# # print(design.index)
# # print("----")
# # print(matrix)
# # print(matrix.iloc[0,0])
# # matrix.iloc[0,0] = "Factor"
# # print(matrix.iloc[0,0])

# matrix.to_csv('matrix_out.csv', index = False)
# design.to_csv('design_out.csv', index = False)


# matrix = pd.read_csv("matrix_out.csv")
# results = pd.read_csv("results.csv")

# matrix = matrix.astype('float')
# results = results.astype('float')
# # matrix.apply(pd.to_numeric, errors='coerce').fillna(matrix)

# # multiplied = pd.DataFrame()

# # for label, table in matrix.items():
# #     multiplied[label] = matrix * table
# #     print(multiplied[label])

# print(matrix)
 # = chromapy.import_initial_csv("DOE_Input.csv")
# results_multiplied = chromapy.main_effect(results, matrix)

# results_np = np.empty(0)

# for index, row in results.iterrows():
#     results_np = np.append(results_np, row[0])
#     print(results_np)

# results_multiplied = matrix.multiply(results_np, axis=0)

# print(results_multiplied)

# print(main_effect)

# # print(results_multiplied)

# # df = pd.concat([pd.DataFrame(value) for value in main_effect.values()], ignore_index=True)
# output = "main_effect.csv"
# # Turn dictionary back into dataframe, print values and create .csv
# main_effect_df = pd.DataFrame(main_effect.values(), index = main_effect.keys())
# print(main_effect_df.transpose())
# main_effect_df = main_effect_df.transpose()

# main_effect_df.to_csv(output, index = False)


# # Sum values in both the matrix and results:
# results_sum = {column: results_multiplied[column].sum() for column in results_multiplied.columns.values}
# matrix_sum = {column: matrix[column].sum() for column in matrix.columns.values}
# print(results_sum)
# print("---")
# print(matrix_sum)

# sum_df = pd.DataFrame(results_sum, index=["Total"])


# number_negative = {column : matrix[column].sum() for column in matrix.columns.values}
# print(number_negative)

"""
This calculates the main effect. The calculation is made difficult when there are different numbers of 1 and -1 for a given column (factor or variable). This double loop iterates over columns and rows of the multiplied results, finds which values are -1 and 1 in the matrix, and sums them and divides them accordingly. The result is a dictionary with the main effects.
"""
# main_effect = {}
# for column in results_multiplied.columns.values:
#     num_neg = 0
#     sum_neg = 0
#     num_pos = 0
#     sum_pos = 0
#     for index in results_multiplied.index.values:
#         matrix_value = matrix.loc[index, column]
#         value = results_multiplied.loc[index, column]
#         if matrix_value < 0:
#             num_neg = num_neg + 1
#             sum_neg = sum_neg + value
#         else:
#             num_pos = num_pos + 1
#             sum_pos = sum_pos + value
#     main_effect[column] = (sum_pos/num_pos)+(sum_neg/num_neg)



# print(sum_df)

#main_effect = pd.DataFrame()
#for column in results_multiplied.columns.values:
#    temp = pd.DataFrame({column : results_multiplied[column].sum()})
#    main_effect = pd.concat([main_effect, temp])

#    print(column)
#    #Make a list of indexed entries
#    # main_effect[column].append(results_multiplied[column].sum())
#    # main_effect[column] = results_multiplied[column].sum()
#    print("---")
#    print(main_effect)

##Turn it into a dataframe
#main_effect = pd.DataFrame(main_effect)

#print(main_effect)



# print(results.columns)
