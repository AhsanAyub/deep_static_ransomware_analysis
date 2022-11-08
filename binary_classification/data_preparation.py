__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@tntech.edu"
__status__ = "Prototype"

import pandas as pd
import os
import glob

def ProcessFunctionNames(curr_dir):
        
    os.chdir("./samples/processed_data/function_names/")
    
    filenames = [i for i in glob.glob('*.pkl')]
    frames = []
    for filename in filenames:
        frames.append(pd.read_pickle(filename))
    
    os.chdir(curr_dir)    
    rw_function_names = pd.concat(frames)
    rw_function_names["is_malicious"] = 1
    #print(len(rw_function_names["function_names"].unique()))
    
    frames = []
    os.chdir("./samples/processed_data/benign_data/")
    filenames = [i for i in glob.glob('*function*')]
    for filename in filenames:
        frames.append(pd.read_pickle(filename))
    
    os.chdir(curr_dir)    
    benign_function_names = pd.concat(frames)
    benign_function_names["is_malicious"] = 0
    #print(len(benign_function_names["function_names"].unique()))
    
    function_names = pd.concat([benign_function_names, rw_function_names])
    function_names["function_names"] = function_names["function_names"].str.lower()
    function_names["md5"] = function_names["md5"].str.lower()
    return function_names
    

def ProcessLibraryImports(curr_dir):
    
    os.chdir("./samples/processed_data/library_imports/")
    
    filenames = [i for i in glob.glob('*.pkl')]
    frames = []
    for filename in filenames:
        df = pd.read_pickle(filename)
        df.columns = ["md5", "library_names"]
        frames.append(df)
        del df
    
    os.chdir(curr_dir)
    rw_library_imports = pd.concat(frames)
    rw_library_imports["is_malicious"] = 1
    #print(len(rw_library_imports["library_names"].unique()))
    
    frames = []
    os.chdir("./samples/processed_data/benign_data/")
    filenames = [i for i in glob.glob('*library*')]
    for filename in filenames:
        df = pd.read_pickle(filename)
        df.columns = ["md5", "library_names"]
        frames.append(df)
        del df
    
    os.chdir(curr_dir)    
    benign_library_imports = pd.concat(frames)
    benign_library_imports["is_malicious"] = 0
    #print(len(benign_library_imports["library_names"].unique()))
    
    library_imports = pd.concat([benign_library_imports, rw_library_imports])
    library_imports["library_names"] = library_imports["library_names"].str.lower()
    library_imports["md5"] = library_imports["md5"].str.lower()
    return library_imports


def ProcessSectionNames(curr_dir):
    
    os.chdir("./samples/processed_data/sections/")
    
    filenames = [i for i in glob.glob('*.pkl')]
    frames = []
    for filename in filenames:
        frames.append(pd.read_pickle(filename))
    
    os.chdir(curr_dir)    
    rw_section_names = pd.concat(frames)
    rw_section_names = rw_section_names.drop(columns=['raw_size', 'virtual_size', 'entropy'])
    rw_section_names = rw_section_names.groupby('md5')['section_name'].apply(list).reset_index(name="section_names")
    rw_section_names["is_malicious"] = 1
    
    benign_section_names_only = pd.read_pickle("./samples/processed_data/benign_data/benign_sections.pkl")
    benign_section_names = pd.read_pickle("./samples/processed_data/benign_data/benign_exe_sections.pkl")
    benign_section_names = benign_section_names.drop(columns=['raw_size', 'virtual_size', 'entropy'])
    benign_section_names = benign_section_names.groupby('md5')['section_name'].apply(list).reset_index(name="section_names")
    benign_section_names = pd.concat([benign_section_names_only, benign_section_names])
    benign_section_names["is_malicious"] = 0
    
    section_names = pd.concat([benign_section_names, rw_section_names])
    section_names["md5"] = section_names["md5"].str.lower()
    
    return section_names


def ProcessPeInfo(curr_dir):
    
    os.chdir("./samples/processed_data/pe_info")
    
    filenames = [i for i in glob.glob('*.pkl')]
    frames = []
    for filename in filenames:
        df = pd.read_pickle(filename)
        if 'unitialized_data_size' in df.columns:
            df = df.rename({'unitialized_data_size': 'uninitialized_data_size'}, axis=1, inplace=True)
        frames.append(df)
        
    os.chdir(curr_dir)    
    rw_pe_info = pd.concat(frames)
    rw_pe_info["is_malicious"] = 1
    
    bengin_pe_info = pd.read_pickle("./samples/processed_data/benign_data/benign_pe_info.pkl")
    bengin_pe_info["is_malicious"] = 0
    pe_info = pd.concat([bengin_pe_info, rw_pe_info])
    pe_info["md5"] = pe_info["md5"].str.lower()
    
    return pe_info
    #bengin_sample_info = pd.read_pickle("./samples/processed_data/benign_data/benign_sample_info.pkl")


def ProcessSampleInfo(curr_dir):
    
    os.chdir("./samples/processed_data/sample_info")
    
    filenames = [i for i in glob.glob('*.pkl')]
    frames = []
    for filename in filenames:
        df = pd.read_pickle(filename)
        print(df.columns)
        frames.append(df)
    
    os.chdir(curr_dir)    
    rw_sample_info = pd.concat(frames)
    
    bengin_sample_info = pd.read_pickle("./samples/processed_data/benign_data/benign_sample_info.pkl")
    return pd.concat([bengin_sample_info, rw_sample_info])
    
 
def Processor(curr_dir):
    
    function_names_df = ProcessFunctionNames(curr_dir)
    library_imports_df = ProcessLibraryImports(curr_dir)
    
    function_names_list_df = function_names_df.groupby('md5')['function_names'].apply(list).reset_index(name="function_names")
    function_names_list_df["is_malicious"] = function_names_df.groupby('md5').first()['is_malicious'].tolist()
    
    library_imports_list_df = library_imports_df.groupby('md5')['library_names'].apply(list).reset_index(name="library_names")
    
    return pd.merge(library_imports_list_df, function_names_list_df, on = "md5")