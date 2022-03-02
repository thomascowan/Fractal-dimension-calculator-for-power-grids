# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:42:34 2022

@author: Thomas
"""


import pandas as pd
import os

df = {}
MW = {}

directory = ".\Data\Energex-Network-Substation-Load-Data-2020-21"
for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".csv"): 
         df[filename] = pd.read_csv(os.path.join(directory,filename))
         for row in df[filename].iterrows():    
             MW[]
     

print(df)