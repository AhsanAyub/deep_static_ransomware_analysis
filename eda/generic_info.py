#!/usr/bin/env python3

__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@tntech.edu"
__status__ = "Prototype"


#import libraries
import pandas as pd
import pickle5 as pickle


''' This is the utility function to populate the file generic info files in a 
a dataframe and return back the concat version of dataframes. '''
def ReadFileGenericInfo(dataset_year):

    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_DLL_file_generic_info.pkl", "rb") as f:
        file_generic_info1 = pickle.load(f)
        
    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_EXE_file_generic_info.pkl", "rb") as f:
        file_generic_info2 = pickle.load(f)
    
    return pd.concat([file_generic_info1, file_generic_info2])


''' This is the utility function to populate the sample info files in a 
a dataframe and return back the concat version of dataframes. '''
def ReadSampleInfo(dataset_year):

    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_DLL_sample_info.pkl", "rb") as f:
        sample_info1 = pickle.load(f)
        
    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_EXE_sample_info.pkl", "rb") as f:
        sample_info2 = pickle.load(f)
    
    return pd.concat([sample_info1, sample_info2])


''' This is the utility function to populate the pe info files in a 
a dataframe and return back the concat version of dataframes. '''
def ReadPeInfo(dataset_year):

    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_DLL_pe_info.pkl", "rb") as f:
        pe_info1 = pickle.load(f)
        
    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_EXE_pe_info.pkl", "rb") as f:
        pe_info2 = pickle.load(f)
    
    return pd.concat([pe_info1, pe_info2])


# Driver program
if __name__ == '__main__':
    
    years = ["2017", "2018", "2019", "2020", "2021"]
    
    for year in years:
        print(year)
        file_generic_info = ReadFileGenericInfo(year)
        sample_info = ReadSampleInfo(year)
        pe_info = ReadPeInfo(year)
        
        sample_info["sample_size"] = pd.to_numeric(sample_info["sample_size"])
        print("Sample Size\nMean: ", sample_info["sample_size"].mean() / 1000)
        print("Median: ", sample_info["sample_size"].median() / 1000)
        print("Maximum: ", sample_info["sample_size"].max() / 1000)
        print("Min: ", sample_info["sample_size"].min() / 1000)
        
        pe_info["code_size"] = pd.to_numeric(pe_info["code_size"])
        print("Code Size\nMean: ", pe_info["code_size"].mean() / 1000)
        print("Median: ", pe_info["code_size"].median() / 1000)
        print("Maximum: ", pe_info["code_size"].max() / 1000)
        print("Min: ", pe_info["code_size"].min() / 1000)
        
        pe_info["initialized_data_size"] = pd.to_numeric(pe_info["initialized_data_size"])
        print("Initialized Data Size\nMean: ", pe_info["initialized_data_size"].mean() / 1000)
        print("Median: ", pe_info["initialized_data_size"].median() / 1000)
        print("Maximum: ", pe_info["initialized_data_size"].max() / 1000)
        print("Min: ", pe_info["initialized_data_size"].min() / 1000)
        
        pe_info["unitialized_data_size"] = pd.to_numeric(pe_info["unitialized_data_size"])
        print("Uninitialized Data Size\nMean: ", pe_info["unitialized_data_size"].mean() / 1000)
        print("Median: ", pe_info["unitialized_data_size"].median() / 1000)
        print("Maximum: ", pe_info["unitialized_data_size"].max() / 1000)
        print("Min: ", pe_info["unitialized_data_size"].min() / 1000)
        
        print("Mime Type")
        print(file_generic_info["mime_type"].value_counts())
        
        print("Subsystem")
        print(pe_info["subsystem"].value_counts())  
        print("------------")