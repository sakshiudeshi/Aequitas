import pandas as pd
import os
print("inside utils.py", os.getcwd())

def get_input_bounds(input_file, sensitive_col_name):
    input_bounds = []
    df=pd.read_csv(f'{input_file}')
    for col in df:
        # exclude the column you're trying to predict
        if col == sensitive_col_name:
            continue
        numUniqueVals = df[col].nunique()
        input_bounds.append([0, numUniqueVals - 1]) # bound is inclusive
    return input_bounds

def get_column_names(input_file):
    df=pd.read_csv(f'{input_file}')
    return list(df.columns)

def get_idx_of_column(input_file, column):
    df=pd.read_csv(f'{input_file}')
    return list(df.columns).index(column)