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
    section_names = pd.DataFrame(columns = ["md5", "section_name", "raw_size", "virtual_size", "entropy"])
    overlay_information = pd.DataFrame(columns = ["md5", "overlay_entropy", "overlay_offset", "overlay_size", "overlay_filetype"])
    resource_language = pd.DataFrame(columns = ["md5", "resource_langs"])
    #pe_info = pd.DataFrame(columns = ["subsystem", "subsystem_version", "machine_type", "time_stamp", "code_size", "initialized_data_size", "unitialized_data_size", "os_version", "magic", "pe_entry_point", "md5"])

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

            overlay_information_list = []
            try:
                overlay_information_list.append(benign_hash)
                overlay_information_list.append(json_data["data"]["attributes"]["pe_info"]["overlay"]["entropy"])
                overlay_information_list.append(json_data["data"]["attributes"]["pe_info"]["overlay"]["offset"])
                overlay_information_list.append(json_data["data"]["attributes"]["pe_info"]["overlay"]["size"])
                overlay_information_list.append(json_data["data"]["attributes"]["pe_info"]["overlay"]["filetype"])
            except:
                overlay_information_list = [benign_hash, -1, -1, -1, ""]
                
            overlay_information.loc[counter] = overlay_information_list

            langs = []
            try:
                for item in json_data["data"]["attributes"]["pe_info"]["resource_langs"]:
                    langs.append(item)
            except:
                pass

            resource_language.loc[counter] = [benign_hash, langs]
            
            temp_dict = {   "md5" : [],
                            "section_name" : [],
                            "raw_size" : [],
                            "virtual_size" : [],
                            "entropy" : []}
            for item in json_data["data"]["attributes"]["pe_info"]["sections"]:
                temp_dict["md5"].append(benign_hash)
                temp_dict["section_name"].append(item["name"])
                temp_dict["raw_size"].append(item["raw_size"])
                temp_dict["virtual_size"].append(item["virtual_size"])
                temp_dict["entropy"].append(item["entropy"])

            section_names = section_names.append(pd.DataFrame(temp_dict))

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

    '''sample_info.to_csv("benign_exe_sample_info.csv")
    sample_info.to_pickle("benign_exe_sample_info.pkl", protocol = 3)

    function_names_import.to_csv("benign_exe_function_names_import.csv")
    function_names_import.to_pickle("benign_exe_function_names_import.pkl", protocol = 3)
    
    library_import.to_csv("benign_exe_library_import.csv")
    library_import.to_pickle("benign_exe_library_import.pkl", protocol = 3)'''

    section_names.to_csv("benign_exe_sections.csv")
    section_names.to_pickle("benign_exe_sections.pkl", protocol = 3)

    overlay_information.to_csv("benign_exe_overlay.csv")
    overlay_information.to_pickle("benign_exe_overlay.pkl", protocol = 3)

    resource_language.to_csv("benign_exe_resource_language.csv")
    resource_language.to_pickle("benign_exe_resource_language.pkl", protocol = 3)
