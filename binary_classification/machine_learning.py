#!/usr/bin/env python3

__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@tntech.edu"
__status__ = "Prototype"

import pandas as pd

import binary_classification.ml_utils as utils

def ProcessDataset(df):
    Y = df.iloc[:, -1].values
    df = df.drop(columns=["class"])
    X = df.iloc[:,:].values
    
    return X, Y


if __name__ == '__main__':

    # Get the dataset
    X, Y = ProcessDataset(pd.read_pickle("./samples/processed_data/library_imports_pca.pkl"))
    
    # Run the models
    print("Import Names as Feature")
    utils.RunModels(X, Y)
    
    # Get the dataset
    X, Y = ProcessDataset(pd.read_pickle("./samples/processed_data/function_names_pca.pkl"))
    
    # Run the models
    print("Function Names as Feature")
    utils.RunModels(X, Y)
    
    # Get the dataset
    X, Y = ProcessDataset(pd.read_pickle("./samples/processed_data/function_library_pca.pkl"))
    
    # Run the models
    print("Functions and Imports as Feature")
    utils.RunModels(X, Y)