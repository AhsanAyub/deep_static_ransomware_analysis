import pandas as pd
import requests
import json

if __name__ == '__main__':
    benign_hashes = pd.read_pickle("benign_sample_info.pkl")
    benign_hashes = benign_hashes["md5"].tolist()

    vt_api_key = ""
    headers = {
        "accept": "application/json",
        "x-apikey": vt_api_key
    }

    df = pd.DataFrame(columns=["sha256", "md5", "name", "magic", "file_type"])
    counter = 0

    for benign_hash in benign_hashes:
        try:
            url = "https://www.virustotal.com/api/v3/files/" + benign_hash
            response = requests.get(url, headers=headers)
            json_data = json.loads(response.text)

            temp = []
            temp.append(json_data["data"]["attributes"]["sha256"])
            temp.append(json_data["data"]["attributes"]["md5"])
            temp.append(json_data["data"]["attributes"]["meaningful_name"])
            temp.append(json_data["data"]["attributes"]["magic"]) 
            temp.append(json_data["data"]["attributes"]["type_description"])
            df.loc[counter] = temp
            
            counter += 1
            print(counter)
        
        except:
            print(benign_hash)
            continue

    df.to_csv("benign_sample_information.csv")
