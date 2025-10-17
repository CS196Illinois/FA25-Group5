import pandas as pd #work w tables 
import numpy as np #math lib
import matplotlib.pyplot as plt #graphing
import seaborn as sns #prettier graphs 
import warnings as wr
wr.filterwarnings('ignore')
#use: conda install pandas numpy matplotlib seaborn
# to ensure these libraries are installed 

import os
os.chdir("Cici Liu")
print(os.getcwd())

# #read excel file into pandas DataFrame(df)
df = pd.read_csv("course-catalog.csv")
#df = pd.read_csv(r"C:\Users\JL\Desktop\Python projects\CS124H\FA25-Group5\Cici Liu\course-catalog.csv")

# #view first few rows 
print(df.head())

print("Hello World ")