#!/usr/bin/python3.6

# A simple template script to clean any given dataset
# argv[1] is the file name in csv format
# argv[2] is whether to drop rows or columns where null is found. Default is row
# argv[3+] columns to drop

# TO-DO
# duplicates -- very hard
# You can't throw away the data, you should store it somewhere else for review
# If you have quotes, you should load it into a single string variable
# Wouldn't it be nice for a ml algorithm to clean the data for me

import pandas as pd
import sys

df = pd.read_csv(sys.argv[1])
df = df.drop_duplicates()

if (len(sys.argv) <= 2) or (sys.argv[2] == "-r"):
    err = df[df.isna()]
    corrected = df[df.notna()]
    err.to_csv(str(sys.argv[1][:-4]) + str("_bad_rows.csv"))
    corrected.to_csv(str(sys.argv[1][:-4]) + str("_row_cleaned.csv"))

elif sys.argv[2] == "-c":
    df = df.dropna(axis = "columns")
    df.to_csv(str(sys.argv[1][:-4]) + str("_column_cleaned.csv"))

else:
    df = df.dropna(subset = sys.argv[2:]).sort_values(by = sys.argv[2:])
    df.to_csv(str(sys.argv[1][:-4]) + str("_column_cleaned.csv"))
