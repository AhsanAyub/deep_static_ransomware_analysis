#!/usr/bin/env python3

__author__ = "Md. Ahsan Ayub"
__license__ = "GPL"
__credits__ = ["Ayub, Md. Ahsan", "Siraj, Ambareen"]
__maintainer__ = "Md. Ahsan Ayub"
__email__ = "mayub42@tntech.edu"
__status__ = "Prototype"


from typing import Dict, List


class FileGenericInfo(object):
    ''' A class to hold a few basic pieces of information of
    both ransomware samples and benign software. '''

    def __init__(self) -> None:
        ''' Intialize the container with the required piece
        of information about the file '''
        self.file_generic_info = {}

        # Storing the hash values
        self.file_generic_info["md5"] = ""
        self.file_generic_info["sha1"] = ""
        self.file_generic_info["sha256"] = ""

        # The scan reports from the Virus Total mainly
        self.file_generic_info["vt_first_seen"] = ""

        # The result obtained from the exiftool
        self.file_generic_info["mime_type"] = ""
        self.file_generic_info["file_type"] = ""
        self.file_generic_info["pe_file"] = ""
        self.file_generic_info["file_type_extension"] = ""

    def get_file_info(self) -> Dict:
        ''' Return the dictioary container for the file'''
        return self.file_generic_info

    def __str__(self) -> str:
        ''' This special method will be called to print the
        dictioary container for the file. '''
        return str(self.file_generic_info)


class Imports(object):
    ''' A class to hold the imports of both ransomware samples
    and benign software. It obtains information regarding the
    library names and function names. Function names are grouped
    into one library name. '''

    def __init__(self) -> None:
        ''' Library name will be the keys of the dictionary while
        its value will be a list of function names. '''
        self.imports_info = {}

    def get_imports_info(self) -> Dict:
        ''' Return the dictioary container for the imports'''
        return self.imports_info

    def __str__(self) -> str:
        ''' This special method will be called to print the
        dictioary container for the imports '''
        return str(self.imports_info)


class Exports(object):
    ''' A class to hold the exports of both ransomware samples
    and benign software. It obtains information regarding the
    export function names. '''

    def __init__(self) -> None:
        ''' Export function names will be stored in a list. '''
        self.exports_info = []

    def get_exports_info(self) -> List:
        ''' Return the list container for the exports'''
        return self.exports_info

    def __str__(self) -> str:
        ''' This special method will be called to print the
        dictioary container for the exports'''
        return str(self.exports_info)


class SectionsInfo(object):
    '''A class to hold the section info. It comprises of the name
    of the section, its raw size, its virtual size, and its entropy.'''
    
    def __init__(self) -> None:
        ''' Section name will be the keys of the dictionary while
        its value will be raw size, virtual size, and entropy '''
        self.sections_info = {}

    def get_sections_info(self) -> Dict:
        ''' Return the dictioary container for the sections info'''
        return self.sections_info

    def __str__(self) -> str:
        ''' This special method will be called to print the
        dictioary container for the sections info '''
        return str(self.sections_info)


class VirusTotal(object):
    '''A class to hold the information of VirusTotal scan reports'''

    def __init__(self) -> None:
        '''A dictionary container to store the scan id, the number
        of anti-virus engines labeling the sample as positive, the'''
        self.virus_total_info = {}

        self.virus_total_info["scan_id"] = ""
        self.virus_total_info["total"] = 0
        self.virus_total_info["number_of_pos"] = 0
        self.virus_total_info["md5"] = ""
        
    def get_virus_total_info(self) -> Dict:
        ''' Return the dictioary container for the virus total info'''
        return self.virus_total_info

    def __str__(self) -> str:
        ''' This special method will be called to print the
        dictioary container for the virustotal info '''
        return str(self.virus_total_info)


class PeInfo(object):
    '''A class to hold the pe file information of both ransomware
    and benign samples. '''

    def __init__(self) -> None:
        ''' A dictionary container to hold the information'''
        self.pe_info = {}

        self.pe_info["subsystem"] = ""
        self.pe_info["subsystem_version"] = ""
        self.pe_info["machine_type"] = ""
        self.pe_info["time_stamp"] = ""
        self.pe_info["code_size"] = 0
        self.pe_info["initialized_data_size"] = 0
        self.pe_info["unitialized_data_size"] = 0
        self.pe_info["os_version"] = ""
        self.pe_info["magic"] = ""
        self.pe_info["pe_entry_point"] = 0
        self.pe_info["md5"] = ""

    def get_pe_info(self) -> Dict:
        ''' Return the dictioary container for the pe info '''
        return self.pe_info

    def __str__(self) -> str:
        ''' This special method will be called to print the
        dictioary container for the pe info '''
        return str(self.pe_info)