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
    
    df = data_preparation.ProcessSectionNames(os.getcwd())

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
    
    
    unique_functions = data_preparation.ProcessFunctionNames(os.getcwd())
    unique_functions = unique_functions['function_names'].unique().tolist()
    unique_functions.append("class")
    unique_functions = sorted(unique_functions)
    
    functions_sparse = pd.DataFrame(columns = unique_functions)
    del unique_functions
    
    functions_df = function_library_df["function_names"]
    classes = function_library_df["is_malicious"]
    del function_library_df
    
    counter = 0
    old_counter = 4550
    col_size = functions_sparse.shape[-1]
    while(old_counter < 5124):
        functions_sparse.loc[counter] = [0 for i in range(col_size)]
        functions_sparse["class"][counter] = classes[old_counter]
        for item in functions_df[old_counter]:
            functions_sparse[item][counter] = 1
        counter += 1
        old_counter += 1
    print(counter)
        
    functions_sparse.to_pickle("./samples/processed_data/function_library_sparse_10.pkl", protocol=3)
    del functions_sparse
    
    filename = "./samples/processed_data/function_library_sparse_"
    filenames = []
    for i in range(1,11):
        filenames.append(filename + str(i) + ".pkl")
    frames = []
    for filename in filenames:
        frames.append(pd.read_pickle(filename))
        print(filename)
        
    functions_sparse = pd.concat(frames)
    del frames
    
    functions_sparse.to_pickle("./samples/processed_data/function_names_sparse.pkl", protocol=3)
    Y = functions_sparse["class"]
    functions_sparse = functions_sparse.drop(columns=["class"])
    
    pca = PCA(n_components = 2)
    function_names_pca = pca.fit_transform(functions_sparse)
    print(pca.explained_variance_ratio_)
    del functions_sparse
    PrincipalComponents = pd.DataFrame(data = function_names_pca, columns = ["PCA-1", "PCA-2"])
    del function_names_pca
    PrincipalComponents["class"] = Y.tolist()
    PrincipalComponents.to_pickle("./samples/processed_data/function_names_pca.pkl", protocol=3)
    
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
    
    del (PrincipalComponents, Y)
    
    
    unique_functions = data_preparation.ProcessFunctionNames(os.getcwd())
    unique_functions = unique_functions['function_names'].unique().tolist()
    unique_imports = data_preparation.ProcessLibraryImports(os.getcwd())
    unique_imports = unique_imports['library_names'].unique().tolist()
    unique_functions_imports = unique_functions + unique_imports
    del (unique_functions, unique_imports)
    unique_functions_imports.append("class")
    unique_functions_imports = sorted(unique_functions_imports)
    col_size = len(unique_functions_imports)
    
    functions_df = function_library_df["function_names"]
    imports_df = function_library_df["library_names"]
    classes = function_library_df["is_malicious"]
    del function_library_df
    
    function_library_sparse = pd.DataFrame(columns=unique_functions_imports)
    
    counter = 0
    old_counter = 4550
    while(old_counter < 5124):
        function_library_sparse.loc[counter] = [0 for i in range(col_size)]
        function_library_sparse["class"][counter] = classes[old_counter]
        
        for item in functions_df[old_counter]:
            function_library_sparse[item][counter] = 1
            
        for item in imports_df[old_counter]:
            function_library_sparse[item][counter] = 1 
        
        counter += 1
        old_counter += 1
        print(counter)
    
    function_library_sparse.to_pickle("./samples/processed_data/function_library_sparse_10.pkl", protocol=3)
    del function_library_sparse
    
    del (functions_df, imports_df, classes, unique_functions_imports)
    
    filename = "./samples/processed_data/function_library_sparse_"
    filenames = []
    for i in range(1,11):
        filenames.append(filename + str(i) + ".pkl")
    frames = []
    for filename in filenames:
        frames.append(pd.read_pickle(filename))
        print(filename)
        
    function_library_sparse = pd.concat(frames)
    del frames
    
    function_library_sparse.to_pickle("./samples/processed_data/function_library_sparse.pkl", protocol=3)
    Y = function_library_sparse["class"]
    function_library_sparse = function_library_sparse.drop(columns=["class"])
    
    pca = PCA(n_components = 2)
    function_library_pca = pca.fit_transform(function_library_sparse)
    print(pca.explained_variance_ratio_)
    del function_library_sparse
    PrincipalComponents = pd.DataFrame(data = function_library_pca, columns = ["PCA-1", "PCA-2"])
    del function_library_pca
    PrincipalComponents["class"] = Y.tolist()
    del Y
    PrincipalComponents.to_pickle("./samples/processed_data/function_library_pca.pkl", protocol=3)
    
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
    
    del PrincipalComponents