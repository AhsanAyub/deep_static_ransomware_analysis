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
from sklearn.metrics.pairwise import cosine_similarity

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


def ComputeCosineSimilarity(set1, set2):
    union_set = set1
    union_set.update(set2)
    l1 = []
    l2 = []
    for item in union_set:
        if(item in set1):
            l1.append(1)
        else:
            l1.append(0)
        if(item in set2):
            l2.append(1)
        else:
            l2.append(0)
    '''c = 0
    # cosine formula 
    for i in range(len(union_set)):
            c += l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    return cosine'''
    return cosine_similarity([l1], [l2])

# Driver program
if __name__ == '__main__':
    
    
    years = ["2017", "2018", "2019", "2020", "2021"]
    for year in years:
        library_imports = ReadLibraryImportsInfo(year)
        library_imports["library_names"] = library_imports["library_names"].str.lower()
        library_imports_per_md5 = {}
        md5_items = []
        i = 1
        for md5_item in library_imports["md5"].unique():
            md5_items.append(md5_item)
            temp_df = library_imports.loc[library_imports["md5"] == md5_item]
            library_imports_per_md5[i] = set(temp_df["library_names"])
            i += 1
        
        cosine_similarity_dic = {}
        md5_items_size = len(md5_items)
        for i in range(1,md5_items_size+1):
            cosine_similarity_dic[md5_items[i-1]] = []
            for j in range(1,md5_items_size+1):
                if(j == i):
                    continue
                cosine_value = ComputeCosineSimilarity(library_imports_per_md5[i], library_imports_per_md5[j])
                cosine_similarity_dic[md5_items[i-1]].append(cosine_value)
                
        cosine_similarity_df = {}
        for item in cosine_similarity_dic:
            cosine_similarity_df[item] = []
            cosine_similarity_df[item].append(np.max(cosine_similarity_dic[item]))
            cosine_similarity_df[item].append(np.quantile(cosine_similarity_dic[item], .75))
            cosine_similarity_df[item].append(np.mean(cosine_similarity_dic[item]))
            cosine_similarity_df[item].append(np.median(cosine_similarity_dic[item]))
            cosine_similarity_df[item].append(np.quantile(cosine_similarity_dic[item], .25))
            cosine_similarity_df[item].append(np.min(cosine_similarity_dic[item]))
            
        cosine_similarity_df = pd.DataFrame(cosine_similarity_df)
        cosine_similarity_df.to_csv(year + "_cosine_similarity_library.csv")
        
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
          
        cosine_similarity_dic = {}
        md5_items_size = len(md5_items)
        for i in range(1,md5_items_size+1):
            cosine_similarity_dic[md5_items[i-1]] = []
            for j in range(1,md5_items_size+1):
                if(j == i):
                    continue
                cosine_value = ComputeCosineSimilarity(function_names_per_md5[i], function_names_per_md5[j])
                cosine_similarity_dic[md5_items[i-1]].append(cosine_value)
                
        cosine_similarity_df = {}
        for item in cosine_similarity_dic:
            cosine_similarity_df[item] = []
            cosine_similarity_df[item].append(np.max(cosine_similarity_dic[item]))
            cosine_similarity_df[item].append(np.quantile(cosine_similarity_dic[item], .75))
            cosine_similarity_df[item].append(np.mean(cosine_similarity_dic[item]))
            cosine_similarity_df[item].append(np.median(cosine_similarity_dic[item]))
            cosine_similarity_df[item].append(np.quantile(cosine_similarity_dic[item], .25))
            cosine_similarity_df[item].append(np.min(cosine_similarity_dic[item]))
        
        cosine_similarity_df = pd.DataFrame(cosine_similarity_df)
        cosine_similarity_df.to_csv(year + "_cosine_similarity_functions.csv")
        print(year)