#!/usr/bin/env python3

__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@tntech.edu"
__status__ = "Prototype"

#import libraries
import pandas as pd
import numpy as np
import pickle5 as pickle

''' This is the utility function to populate the libraries used in a
a dataframe and return back the concat version of dataframes. '''
def ReadLibraryImportsInfo(dataset_year):

    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_DLL_library_imports.pkl", "rb") as f:
        file_generic_info1 = pickle.load(f)
        
    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_EXE_library_imports.pkl", "rb") as f:
        file_generic_info2 = pickle.load(f)
    
    return pd.concat([file_generic_info1, file_generic_info2])

''' This is the utility function to populate the function names used in a
a dataframe and return back the concat version of dataframes. '''
def ReadFunctionNamesInfo(dataset_year):

    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_DLL_function_names_imports.pkl", "rb") as f:
        function_names_import1 = pickle.load(f)
        
    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_EXE_function_names_imports.pkl", "rb") as f:
        function_names_import2 = pickle.load(f)
    
    return pd.concat([function_names_import1, function_names_import2])

''' This is the utility function to compute and return the jaccard index of
two sets that are going to be passed as function arguments. '''
def ComputeJaccardIndex(set1, set2):
    common_items = set1.intersection(set2)
    return float(len(common_items) / (len(set1) + len(set2) - len(common_items)))

# Driver program
if __name__ == '__main__':
    
    years = ["2017", "2018", "2019", "2020", "2021"]
    for year in years:
        library_imports = ReadLibraryImportsInfo(year)
        library_imports_per_md5 = {}
        md5_items = []
        i = 1
        for md5_item in library_imports["md5"].unique():
            md5_items.append(md5_item)
            temp_df = library_imports.loc[library_imports["md5"] == md5_item]
            library_imports_per_md5[i] = set(temp_df["library_names"])
            i += 1
          
        jaccard_index_dic = {}
        md5_items_size = len(md5_items)
        for i in range(1,md5_items_size+1):
            jaccard_index_dic[md5_items[i-1]] = []
            for j in range(1,md5_items_size+1):
                if(j == i):
                    continue
                jaccard_index = ComputeJaccardIndex(library_imports_per_md5[i], library_imports_per_md5[j])
                jaccard_index_dic[md5_items[i-1]].append(jaccard_index)
                
        jaccard_index_df = {}
        for item in jaccard_index_dic:
            jaccard_index_df[item] = []
            jaccard_index_df[item].append(np.max(jaccard_index_dic[item]))
            jaccard_index_df[item].append(np.quantile(jaccard_index_dic[item], .75))
            jaccard_index_df[item].append(np.mean(jaccard_index_dic[item]))
            jaccard_index_df[item].append(np.median(jaccard_index_dic[item]))
            jaccard_index_df[item].append(np.quantile(jaccard_index_dic[item], .25))
            jaccard_index_df[item].append(np.min(jaccard_index_dic[item]))
            
        jaccard_index_df = pd.DataFrame(jaccard_index_df)
        jaccard_index_df.to_csv(year + "_jaccard_index_library.csv")
        
        function_names = ReadFunctionNamesInfo(year)
        function_names["function_names"] = function_names["function_names"].str.lower()
        function_names_per_md5 = {}
        md5_items = []
        i = 1
        for md5_item in function_names["md5"].unique():
            md5_items.append(md5_item)
            temp_df = function_names.loc[function_names["md5"] == md5_item]
            function_names_per_md5[i] = set(temp_df["function_names"])
            i += 1
          
        jaccard_index_dic = {}
        md5_items_size = len(md5_items)
        for i in range(1,md5_items_size+1):
            jaccard_index_dic[md5_items[i-1]] = []
            for j in range(1,md5_items_size+1):
                if(j == i):
                    continue
                jaccard_index = ComputeJaccardIndex(function_names_per_md5[i], function_names_per_md5[j])
                jaccard_index_dic[md5_items[i-1]].append(jaccard_index)
                
        jaccard_index_df = {}
        for item in jaccard_index_dic:
            jaccard_index_df[item] = []
            jaccard_index_df[item].append(np.max(jaccard_index_dic[item]))
            jaccard_index_df[item].append(np.quantile(jaccard_index_dic[item], .75))
            jaccard_index_df[item].append(np.mean(jaccard_index_dic[item]))
            jaccard_index_df[item].append(np.median(jaccard_index_dic[item]))
            jaccard_index_df[item].append(np.quantile(jaccard_index_dic[item], .25))
            jaccard_index_df[item].append(np.min(jaccard_index_dic[item]))
        
        jaccard_index_df = pd.DataFrame(jaccard_index_df)
        jaccard_index_df.to_csv(year + "_jaccard_index_functions.csv")