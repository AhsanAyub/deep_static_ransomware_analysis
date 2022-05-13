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


''' This is the utility function to populate the virus total info in a
a dataframe and return back the concat version of dataframes. '''
def ReadVirusTotalReportInfo(dataset_year):

    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_DLL_virus_total_report.pkl", "rb") as f:
        vt_report1 = pickle.load(f)
        
    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_EXE_virus_total_report.pkl", "rb") as f:
        vt_report2 = pickle.load(f)
    
    return pd.concat([vt_report1, vt_report2])

''' This is the utility function to populate the sections info in a
a dataframe and return back the concat version of dataframes. '''
def ReadSectionsInfo(dataset_year):

    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_DLL_sections.pkl", "rb") as f:
        sections1 = pickle.load(f)
        
    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_EXE_sections.pkl", "rb") as f:
        sections2 = pickle.load(f)
    
    return pd.concat([sections1, sections2])

''' This is the utility function to populate the exports used in a
a dataframe and return back the concat version of dataframes. '''
def ReadExportsInfo(dataset_year):

    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_DLL_exports.pkl", "rb") as f:
        exports1 = pickle.load(f)
        
    with open("./samples/processed_data/" + dataset_year + "/" + dataset_year + "_WIN32_EXE_exports.pkl", "rb") as f:
        exports2 = pickle.load(f)
    
    return pd.concat([exports1, exports2])


# Driver program
if __name__ == '__main__':

    years = ["2017", "2018", "2019", "2020", "2021"]
    
    for year in years:
       
        print(year)
        
        library_imports = ReadLibraryImportsInfo(year)
        library_counts = library_imports.groupby(['md5']).size()
        print("Library Counts\nMax: ", np.max(library_counts))
        print("Mean: ", np.mean(library_counts))
        print("Median: ", np.mean(library_counts))
        print("Min: ", np.min(library_counts))
        
        function_names = ReadFunctionNamesInfo(year)
        function_names_count = function_names.groupby(['md5']).size()
        print("Function Name Counts\nMax: ", np.max(function_names_count))
        print("Mean: ", np.mean(function_names_count))
        print("Median: ", np.mean(function_names_count))
        print("Min: ", np.min(function_names_count))
        
        vt_report = ReadVirusTotalReportInfo(year)
        vt_report["ratio"] = (vt_report["number_of_pos"] / vt_report["total"]) * 100
        print("VT Reprot Ratio\nMax: ", vt_report["ratio"].max())
        print("Mean: ", vt_report["ratio"].mean())
        print("Median: ", vt_report["ratio"].median())
        print("Min: ", vt_report["ratio"].min())
        
        sections_info = ReadSectionsInfo(year)
        section_names_count = sections_info.groupby(['md5']).size()
        print("Section Names Count\nMax: ", np.max(section_names_count))
        print("Mean: ", np.mean(section_names_count))
        print("Median: ", np.mean(section_names_count))
        print("Min: ", np.min(section_names_count))
        
        exports_info = ReadExportsInfo(year)
        exports_count = exports_info.groupby(['md5']).size()
        print("Exports Count\nMax: ", np.max(exports_count))
        print("Mean: ", np.mean(exports_count))
        print("Median: ", np.mean(exports_count))
        print("Min: ", np.min(exports_count))
        
        print("==============")
        
    del (library_imports, library_counts, function_names, function_names_count,
         vt_report, sections_info, section_names_count, exports_info, exports_count)