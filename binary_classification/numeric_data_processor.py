#!/usr/bin/env python3

__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@tntech.edu"
__status__ = "Prototype"

import os
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler

import binary_classification.ml_utils as utils
import binary_classification.data_preparation as data_preparation

if __name__ == '__main__':
    
    function_library_df = data_preparation.Processor(os.getcwd())
    section_names = data_preparation.ProcessSectionNames(os.getcwd())
    
    overlay = pd.read_pickle("./samples/processed_data/benign_data/overlay.pkl")
    resource_lang = pd.read_pickle("./samples/processed_data/benign_data/resource_language.pkl")
    
    pe_info = data_preparation.ProcessPeInfo(os.getcwd())
    sample_info = data_preparation.ProcessSampleInfo(os.getcwd()).drop(columns = ['collected_year'])
    
    function_library_df = function_library_df.reset_index(drop=True)
    counter = 0
    for items in function_library_df["library_names"]:
        function_library_df["library_names"][counter] = len(items)
        counter += 1
        
    counter = 0
    for items in function_library_df["function_names"]:
        function_library_df["function_names"][counter] = len(items)
        counter += 1
    
    del items    
    function_library_df.rename({'library_names': 'library_names_count', 'function_names': 'function_names_count'}, axis=1, inplace=True)

    section_names = section_names.reset_index(drop=True)
    counter = 0
    for items in section_names["section_names"]:
        try:
            section_names["section_names"][counter] = len(items)
        except:
            print(counter)
            
        counter += 1
    
    del items
    section_names.rename({'section_names': 'section_names_count'}, axis=1, inplace=True)

    columns = set() 
    resource_lang_series = resource_lang["resource_langs"]
    for items in resource_lang_series:
        for item in items:
            columns.add(str(item).lower())
    
    columns = list(columns)
    columns.append("md5")
    columns.append("is_malicious")
    
    md5s = resource_lang["md5"].to_list()
    classes = resource_lang["is_malicious"].to_list()
    
    counter = 0
    resource_lang_sparse = pd.DataFrame(columns=columns)
    for items in resource_lang_series:
        resource_lang_sparse.loc[counter] = [0 for i in range(len(columns))]
        
        for item in items:
            s = str(item).lower()
            resource_lang_sparse[s][counter] = 1
        
        resource_lang_sparse["md5"][counter] = md5s[counter]
        resource_lang_sparse["is_malicious"][counter] = classes[counter]
        
        counter += 1
    
    del (resource_lang_series, resource_lang, s, md5s)
    
    resource_lang_counts = resource_lang_sparse
    resource_lang_counts = resource_lang_counts.drop(columns = ["md5", "is_malicious"])
    resource_lang_counts = resource_lang_counts.sum(axis=1)
    resource_lang_counts = pd.DataFrame({"counts" : resource_lang_counts,
                                        "md5" : resource_lang_sparse["md5"],
                                        "is_malicious" : resource_lang_sparse["is_malicious"]})
    pca = PCA(n_components = 2)
    resource_lang_pca = resource_lang_sparse
    resource_lang_pca = resource_lang_pca.drop(columns = ["md5", "is_malicious"])
    resource_lang_pca = pca.fit_transform(resource_lang_pca)
    print(pca.explained_variance_ratio_)
    resource_lang_pca = pd.DataFrame(data = resource_lang_pca, columns = ["PCA-1", "PCA-2"])
    resource_lang_pca["is_malicious"] = resource_lang_sparse["is_malicious"]
    resource_lang_pca["md5"] = resource_lang_sparse["md5"].str.lower()
    

    function_library_df["md5"] = function_library_df["md5"].str.lower()
    section_names["md5"] = section_names["md5"].str.lower()
    dataset = pd.merge(function_library_df, section_names, on="md5", how="left")
    dataset = dataset.dropna()
    dataset.rename({'is_malicious_x': 'is_malicious'}, axis=1, inplace=True)
    dataset = dataset.drop(columns=["is_malicious_y"])
    
    sample_info["md5"] = sample_info["md5"].str.lower()
    dataset = pd.merge(dataset, sample_info, on="md5", how="left")
    dataset = dataset.dropna()
    dataset.rename({'is_malicious_x': 'is_malicious'}, axis=1, inplace=True)
    dataset = dataset.drop(columns=["is_malicious_y"])
    
    dataset = pd.merge(dataset, resource_lang_pca, on="md5", how="left")
    dataset.rename({'is_malicious_x': 'is_malicious'}, axis=1, inplace=True)
    dataset = dataset.drop(columns=["is_malicious_y"])
    dataset = dataset.dropna()
    
    scaler = MinMaxScaler()
    dataset[["sample_size"]] = scaler.fit_transform(dataset[["sample_size"]])
    
    Y = dataset["is_malicious"].values
    dataset = dataset.drop(columns=["is_malicious", "md5"])
    X = dataset.iloc[:,:].values
    utils.RunModels(X, Y)
    
    del (X, Y, dataset, overlay, pe_info, sample_info, section_names)
    del (function_library_df, resource_lang_sparse, resource_lang_pca)