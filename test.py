#!/bin/python

import chromapy

dict = chromapy.import_initial_csv("DOE_Input.csv")

print(len(dict))

design, matrix = chromapy.plackett_burman("Examples_Templates/DOE/DOE_Input.csv", 12)

BBdesign = chromapy.box_behnken("Examples_Templates/DOE/BBD_Input.csv")
print(BBdesign)
