#!/bin/python
import chromapy
import pandas as pd

calibration_df, samples_df = chromapy.quant_import("calibration.csv", "results.csv")

print(calibration_df)
print("-----")
print(samples_df)
print("-----")

quant_results = chromapy.quantification(calibration_df, samples_df, int_standard = True, verbose = True)


print(quant_results)



# sample_list = []
# for sample in quant_results['Sample']:
#     if not sample in sample_list:
#         sample_list.append(str(sample))

# quant_df = pd.DataFrame(index = sample_list)



# compounds = ['Captan', 'Metolachlor']

# # This for loop will go through each analyte in the compound list, create a series for each sample name (in the sample_list), and then calculate the mean and standard deviation
# for analyte in compounds:
#     for sample in sample_list:
#        sample_values_series = quant_results.loc[quant_results['Sample'] == sample, analyte]
#        quant_df.at[sample, (str(analyte) + " mean")] = (sample_values_series.to_numpy()).mean()
#        quant_df.at[sample, (str(analyte) + " st.dev")] = (sample_values_series.to_numpy()).std()


# series_test = quant_results.loc[quant_results['Sample'] == '6B', 'Captan']
# narray = series_test.to_numpy()
# print("---")
# print(quant_df)
# print("---")
