#!/usr/bin/env python3

__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@tntech.edu"
__status__ = "Prototype"

import pandas as pd
import os
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

import binary_classification.data_preparation as data_preparation

if __name__ == '__main__':

    function_library_df = data_preparation.Processor(os.getcwd())
    Y = function_library_df.iloc[:,-1].values

    print("library_imports")
    library_imports_series = function_library_df["library_names"]
    
    library_imports_sparse = pd.get_dummies(library_imports_series.apply(pd.Series).stack()).sum(level=0)
    pca = PCA(n_components = 2)
    library_imports_pca = pca.fit_transform(library_imports_sparse)
    print(pca.explained_variance_ratio_)
    PrincipalComponents = pd.DataFrame(data = library_imports_pca, columns = ["PCA-1", "PCA-2"])
    library_imports_sparse["class"] = Y
    PrincipalComponents["class"] = Y
    library_imports_sparse.to_pickle("./samples/processed_data/library_imports_sparse.pkl", protocol=3)
    PrincipalComponents.to_pickle("./samples/processed_data/library_imports_pca.pkl", protocol=3)
    
    # 2D Visualization
    plt.clf() # Clear figure
    myFig = plt.figure(figsize=[12,12])
    plt.scatter(PrincipalComponents["PCA-1"][PrincipalComponents["class"] == 0],
                PrincipalComponents["PCA-2"][PrincipalComponents["class"] == 0],
                marker='o', alpha=0.7, color='blue')
    plt.scatter(PrincipalComponents["PCA-1"][PrincipalComponents["class"] == 1],
                PrincipalComponents["PCA-2"][PrincipalComponents["class"] == 1],
                marker='x', alpha=0.7, color='red')
    plt.title("PCA w/ Imports", fontsize=20, weight='bold')
    plt.xlabel('PCA-1', fontsize=18, weight='bold')
    plt.ylabel('PCA-2', fontsize=18, weight='bold')
    plt.yticks(fontsize=16)
    plt.legend(['Benign', 'Ransomware'], fontsize=16, loc='best')
    plt.show()
    myFig.savefig("./binary_classification/pca_with_imports.png", dpi = 150, format = 'png')
    myFig.savefig("./binary_classification/pca_with_imports.pdf", dpi = 300, format = 'pdf')
    
    del (PrincipalComponents, library_imports_pca, library_imports_series, library_imports_sparse)
    
    
    print("function names")
    function_names_series = function_library_df["function_names"]
    print(function_names_series.shape)
    
    function_names_sparse = pd.get_dummies(function_names_series.apply(pd.Series).stack()).sum(level=0)
    pca = PCA(n_components = 2)
    function_names_pca = pca.fit_transform(function_names_sparse)
    print(pca.explained_variance_ratio_)
    PrincipalComponents = pd.DataFrame(data = function_names_pca, columns = ["PCA-1", "PCA-2"])
    PrincipalComponents["class"] = Y
    function_names_sparse["class"] = Y
    function_names_sparse.to_pickle("./samples/processed_data/function_names_sparse.pkl", protocol=3)
    PrincipalComponents.to_pickle("./samples/processed_data/function_names_pca.pkl", protocol=3)
    
    # 2D Visualization
    plt.clf() # Clear figure
    myFig = plt.figure(figsize=[12,12])
    plt.scatter(PrincipalComponents["PCA-1"][PrincipalComponents["class"] == 0],
                PrincipalComponents["PCA-2"][PrincipalComponents["class"] == 0],
                marker='o', alpha=0.7, color='blue')
    plt.scatter(PrincipalComponents["PCA-1"][PrincipalComponents["class"] == 1],
                PrincipalComponents["PCA-2"][PrincipalComponents["class"] == 1],
                marker='x', alpha=0.7, color='red')
    plt.title("PCA w/ Function Names", fontsize=20, weight='bold')
    plt.xlabel('PCA-1', fontsize=18, weight='bold')
    plt.ylabel('PCA-2', fontsize=18, weight='bold')
    plt.yticks(fontsize=16)
    plt.legend(['Benign', 'Ransomware'], fontsize=16, loc='best')
    plt.show()
    myFig.savefig("./binary_classification/pca_with_functions.png", dpi = 150, format = 'png')
    myFig.savefig("./binary_classification/pca_with_functions.pdf", dpi = 300, format = 'pdf')
    
    del (PrincipalComponents, function_names_pca, function_names_series, function_names_sparse)
    
    
    print("function names and import libraries")
    function_library_series = function_library_df['function_names'] + function_library_df['library_names']
    print(function_library_series.shape)
    
    function_library_sparse = pd.get_dummies(function_library_series.apply(pd.Series).stack()).sum(level=0)
    pca = PCA(n_components = 2)
    function_library_pca = pca.fit_transform(function_library_sparse)
    print(pca.explained_variance_ratio_)
    PrincipalComponents = pd.DataFrame(data = function_library_pca, columns = ["PCA-1", "PCA-2"])
    PrincipalComponents["class"] = Y
    function_library_sparse["class"] = Y
    function_library_sparse.to_pickle("./samples/processed_data/function_library_sparse.pkl", protocol=3)
    PrincipalComponents.to_pickle("./samples/processed_data/function_library_pca.pkl", protocol=3)
    
    # 2D Visualization
    plt.clf() # Clear figure
    myFig = plt.figure(figsize=[12,12])
    plt.scatter(PrincipalComponents["PCA-1"][PrincipalComponents["class"] == 0],
                PrincipalComponents["PCA-2"][PrincipalComponents["class"] == 0],
                marker='o', alpha=0.7, color='blue')
    plt.scatter(PrincipalComponents["PCA-1"][PrincipalComponents["class"] == 1],
                PrincipalComponents["PCA-2"][PrincipalComponents["class"] == 1],
                marker='x', alpha=0.7, color='red')
    plt.title("PCA w/ Function Names and Imports", fontsize=20, weight='bold')
    plt.xlabel('PCA-1', fontsize=18, weight='bold')
    plt.ylabel('PCA-2', fontsize=18, weight='bold')
    plt.yticks(fontsize=16)
    plt.legend(['Benign', 'Ransomware'], fontsize=16, loc='best')
    plt.show()
    myFig.savefig("./binary_classification/pca_with_functions_imports.png", dpi = 150, format = 'png')
    myFig.savefig("./binary_classification/pca_with_functions_imports.pdf", dpi = 300, format = 'pdf')
    
    del (PrincipalComponents, function_library_pca, function_library_series, function_library_sparse)