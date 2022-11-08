import pandas as pd
import requests
import json

if __name__ == '__main__':
    benign_hashes = pd.read_csv("hashes.csv")
    benign_hashes = benign_hashes["id"].tolist()

    vt_api_key = ""
    headers = {
        "accept": "application/json",
        "x-apikey": vt_api_key
    }

    # dataframes to store the information
    sample_info = pd.DataFrame(columns = ["md5", "sample_size","collected_year", "is_malicious"])
    function_names_import = pd.DataFrame(columns = ["md5", "function_names"])
    library_import = pd.DataFrame(columns = ["md5", "library_name"])

    counter = 0

    for benign_hash in benign_hashes:
        try:
            url = "https://www.virustotal.com/api/v3/files/" + benign_hash
            response = requests.get(url, headers=headers)
            json_data = json.loads(response.text)

            sample_info_list = []
            sample_info_list.append(benign_hash)
            sample_info_list.append(json_data["data"]["attributes"]["size"])
            sample_info_list.append(2022)
            sample_info_list.append(0)
            sample_info.loc[counter] = sample_info_list

            function_names_import_set = set()
            library_import_set = set()

            for item in json_data["data"]["attributes"]["pe_info"]["import_list"]:
                library_import_set.add(item["library_name"])
                function_names_import_set.update(item["imported_functions"])

            temp_dict = {}
            temp_dict = {"md5" : [benign_hash for i in range(len(library_import_set))],
                        "library_name" : list(library_import_set)}
            library_import = library_import.append(pd.DataFrame(temp_dict))

            temp_dict = {"md5" : [benign_hash for i in range(len(function_names_import_set))],
                        "function_names" : list(function_names_import_set)}
            function_names_import = function_names_import.append(pd.DataFrame(temp_dict))
            
            counter += 1
            print(counter)
        
        except:
            print(benign_hash)
            continue

    sample_info.to_csv("benign_exe_sample_info.csv")
    sample_info.to_pickle("benign_exe_sample_info.pkl", protocol = 3)

    function_names_import.to_csv("benign_exe_function_names_import.csv")
    function_names_import.to_pickle("benign_exe_function_names_import.pkl", protocol = 3)
    
    library_import.to_csv("benign_exe_library_import.csv")
    library_import.to_pickle("benign_exe_library_import.pkl", protocol = 3)
