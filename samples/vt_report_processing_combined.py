#!/usr/bin/env python3

__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@tntech.edu"
__status__ = "Prototype"


#import libraries
import os
import glob
import json
import pandas as pd

from container import (FileGenericInfo, Imports, Exports, SectionsInfo, VirusTotal, PeInfo)

# Driver program
if __name__ == '__main__':

    # This dictionary will store information of all the JSON files
    processed_data = {}

    json_file = "vt_reports03142022.json"

    with open(json_file) as f:
        json_data = json.load(f)


    # Iterate through each object in the JSON file
    for vt_report in json_data:
        #print(vt_report)
        if vt_report['first_seen'][0:4] != "2018" and vt_report['first_seen'][0:4] != "2019" and vt_report['first_seen'][0:4] != "2020" and vt_report['first_seen'][0:4] != "2021" and vt_report['first_seen'][0:4] != "2022":

            # Initialize the containers of each class
            file_generic_info_obj = FileGenericInfo()
            imports_obj = Imports()
            exports_obj = Exports()
            sections_info_obj = SectionsInfo()
            virus_total_obj = VirusTotal()
            pe_info_obj = PeInfo()

            # Basic information of the sample
            processed_data[vt_report["md5"]] = {}
            processed_data[vt_report["md5"]]["data"] = []
            processed_data[vt_report["md5"]]["sample_size"] = vt_report["size"]
            processed_data[vt_report["md5"]]["collected_year"] = vt_report['first_seen'][0:4]

            # Information of Virus Total report Info container
            virus_total_obj.virus_total_info["scan_id"] = vt_report["scan_id"]
            virus_total_obj.virus_total_info["number_of_pos"] = vt_report["positives"]
            virus_total_obj.virus_total_info["total"] = vt_report["total"]

            for items in vt_report["additional_info"]:
                if items == "exiftool":
                    for exif_tool_keys in vt_report["additional_info"][items]:
                        
                        if exif_tool_keys == "MIMEType":
                            file_generic_info_obj.file_generic_info["mime_type"] = vt_report["additional_info"]["exiftool"][exif_tool_keys]

                        elif exif_tool_keys == "Subsystem":
                            pe_info_obj.pe_info["subsystem"] = vt_report["additional_info"]["exiftool"][exif_tool_keys]

                        elif exif_tool_keys == "MachineType":
                            pe_info_obj.pe_info["machine_type"] = vt_report["additional_info"]["exiftool"][exif_tool_keys]

                        elif exif_tool_keys == "FileType":
                            file_generic_info_obj.file_generic_info["file_type"] = vt_report["additional_info"]["exiftool"][exif_tool_keys]

                        elif exif_tool_keys == "TimeStamp":
                            pe_info_obj.pe_info["time_stamp"] = vt_report["additional_info"]["exiftool"][exif_tool_keys]
                        
                        elif exif_tool_keys == "PEType":
                            file_generic_info_obj.file_generic_info["pe_file"] = vt_report["additional_info"]["exiftool"][exif_tool_keys] 

                        elif exif_tool_keys == "FileTypeExtension":
                            file_generic_info_obj.file_generic_info["file_type_extension"] = vt_report["additional_info"]["exiftool"][exif_tool_keys]

                        elif exif_tool_keys == "CodeSize":
                            pe_info_obj.pe_info["code_size"] = vt_report["additional_info"]["exiftool"][exif_tool_keys]

                        elif exif_tool_keys == "InitializedDataSize":
                            pe_info_obj.pe_info["initialized_data_size"] = vt_report["additional_info"]["exiftool"][exif_tool_keys]

                        elif exif_tool_keys == "UninitializedDataSize":
                            pe_info_obj.pe_info["unitialized_data_size"] = vt_report["additional_info"]["exiftool"][exif_tool_keys]

                        elif exif_tool_keys == "SubsystemVersion":
                            pe_info_obj.pe_info["subsystem_version"] = vt_report["additional_info"]["exiftool"][exif_tool_keys]

                        elif exif_tool_keys == "OSVersion":
                            pe_info_obj.pe_info["os_version"] = vt_report["additional_info"]["exiftool"][exif_tool_keys]

                        else:
                            continue

                elif items == "pe-entry-point":
                    pe_info_obj.pe_info["pe_entry_point"] = vt_report["additional_info"][items]

                elif items == "magic":
                    pe_info_obj.pe_info["magic"] = vt_report["additional_info"][items]
                
                else:
                    continue

            try:
                imports_obj.imports_info = vt_report["additional_info"]["imports"]
            except:
                del processed_data[vt_report["md5"]]
                continue

            try:
                for export_functions in vt_report["additional_info"]["exports"]:
                    if export_functions != "":
                        exports_obj.exports_info.append(export_functions)
            except:
                exports_obj.exports_info = []

            for sections in vt_report["additional_info"]["sections"]:
                sections_info_obj.sections_info[sections[0]] = {}
                sections_info_obj.sections_info[sections[0]]["raw_size"] = sections[1]
                sections_info_obj.sections_info[sections[0]]["virtual_size"] = sections[3]
                sections_info_obj.sections_info[sections[0]]["entropy"] = sections[4]

            # Add the retrieved information to the main dictionary
            processed_data[vt_report["md5"]]["data"].append(file_generic_info_obj)
            processed_data[vt_report["md5"]]["data"].append(imports_obj)
            processed_data[vt_report["md5"]]["data"].append(exports_obj)
            processed_data[vt_report["md5"]]["data"].append(sections_info_obj)
            processed_data[vt_report["md5"]]["data"].append(virus_total_obj)
            processed_data[vt_report["md5"]]["data"].append(pe_info_obj)
        
        else:
            pass

    ''' All the data from the JSON files are fetched.
    Now, it's time to scan them appropriately to dump the information on both CSV and pickle files '''

    # Dataframes to process the information, as well as to save it on the files
    sample_info_df = pd.DataFrame(columns=['md5','sample_size','collected_year', 'is_malicious'])
    file_generic_info_df = pd.DataFrame(columns=['md5','sha1','sha256', 'vt_first_seen', 'mime_type', 'file_type', 'pe_file', 'file_type_extension'])
    virus_total_report_df = pd.DataFrame(columns=['scan_id','total','number_of_pos','md5'])
    pe_info_df = pd.DataFrame(columns=['subsystem', 'subsystem_version', 'machine_type', 'time_stamp', 'code_size', 'initialized_data_size', 'unitialized_data_size', 'os_version', 'magic', 'pe_entry_point', 'md5'])

    library_imports_dict = {}
    library_imports_dict['md5'] = []
    library_imports_dict['library_names'] = []
    
    function_names_imports_dict = {}
    function_names_imports_dict['md5'] = []
    function_names_imports_dict['function_names'] = []
    
    exports_dict = {}
    exports_dict['md5'] = []
    exports_dict['export_names'] = []
    
    sections_dict = {}
    sections_dict['md5'] = []
    sections_dict['section_name'] = []
    sections_dict['raw_size'] = []
    sections_dict['virtual_size'] = []
    sections_dict['entropy'] = []

    for md5_value in processed_data:
        sample_info_dict = {}
        sample_info_dict['md5'] = md5_value
        sample_info_dict['sample_size'] = int(processed_data[md5_value]['sample_size'])
        sample_info_dict['collected_year'] = int(processed_data[md5_value]['collected_year'])
        sample_info_dict['is_malicious'] = 1
        sample_info_df = sample_info_df.append(sample_info_dict, ignore_index = True)

        for objects in processed_data[md5_value]['data']:
            if (isinstance(objects, FileGenericInfo)):
                file_generic_info_df = file_generic_info_df.append(objects.get_file_info(), ignore_index = True)
            elif (isinstance(objects, PeInfo)):
                objects.pe_info["md5"] = md5_value
                pe_info_df = pe_info_df.append(objects.get_pe_info(), ignore_index = True)
            elif (isinstance(objects, VirusTotal)):
                objects.virus_total_info["md5"] = md5_value
                virus_total_report_df = virus_total_report_df.append(objects.get_virus_total_info(), ignore_index = True)
            elif (isinstance(objects, Imports)):
                for key in objects.get_imports_info():
                    library_imports_dict['library_names'].append(key)
                    library_imports_dict['md5'].append(md5_value)
                    for item in objects.get_imports_info()[key]:
                        function_names_imports_dict['md5'].append(md5_value)
                        function_names_imports_dict['function_names'].append(item)

            elif (isinstance(objects, Exports)):
                for item in objects.get_exports_info():
                    exports_dict['export_names'].append(item)
                    exports_dict['md5'].append(md5_value)
                
            elif (isinstance(objects, SectionsInfo)):
                for key in objects.get_sections_info():
                    sections_dict['md5'].append(md5_value)
                    sections_dict['section_name'].append(key)
                    for item in objects.get_sections_info()[key]:
                        if item == "raw_size":
                            sections_dict['raw_size'].append(int(objects.get_sections_info()[key][item]))
                        elif item == "virtual_size":
                            sections_dict['virtual_size'].append(int(objects.get_sections_info()[key][item]))
                        elif item == "entropy":
                            sections_dict['entropy'].append(float(objects.get_sections_info()[key][item]))
                        else:
                            pass
                
            else:
                pass
    
    library_imports_df = pd.DataFrame(library_imports_dict)
    function_names_imports_df = pd.DataFrame(function_names_imports_dict)
    exports_df = pd.DataFrame(exports_dict)
    sections_df = pd.DataFrame(sections_dict)

    '''print(sample_info_df)
    print(file_generic_info_df)
    print(virus_total_report_df)
    print(pe_info_df)
    print(library_imports_df)
    print(function_names_imports_df)
    print(exports_df)
    print(sections_df)'''

    # Dump the information to both pickle file and CSV file to work on it later on
    sample_info_df.to_csv("2017_sample_info.csv", sep='\t', index=False)
    sample_info_df.to_pickle("2017_sample_info.pkl")
    file_generic_info_df.to_csv("2017_file_generic_info.csv", sep='\t', index=False)
    file_generic_info_df.to_pickle("2017_file_generic_info.pkl")
    virus_total_report_df.to_csv("2017_virus_total_report.csv", sep='\t', index=False)
    virus_total_report_df.to_pickle("2017_virus_total_report.pkl")
    pe_info_df.to_csv("2017_pe_info.csv", sep='\t', index=False)
    pe_info_df.to_pickle("2017_pe_info.pkl")
    library_imports_df.to_csv("2017_library_imports.csv", sep='\t', index=False)
    library_imports_df.to_pickle("2017_library_imports.pkl")
    function_names_imports_df.to_csv("2017_function_names_imports.csv", sep='\t', index=False)
    function_names_imports_df.to_pickle("2017_function_names_imports.pkl")
    exports_df.to_csv("2017_exports.csv", sep='\t', index=False)
    exports_df.to_pickle("2017_exports.pkl")
    sections_df.to_csv("2017_sections.csv", sep='\t', index=False)
    sections_df.to_pickle("2017_sections.pkl")