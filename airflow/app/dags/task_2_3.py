import os
import json
import pandas as pd

def transform_data_into_csv(n_files=None, filename='data.csv'):
    parent_folder = "/app/raw_files"
    files = sorted(os.listdir(parent_folder), reverse=True)
    print('ok')
    print(files)
    if n_files:
        files = files[:n_files]

    dfs = []

    for f in files:
        try:
            with open(os.path.join(parent_folder, f), "r") as file:
                data_temp = json.load(file)

            for data_city in data_temp:
                dfs.append(
                    {
                        "temperature": data_city["main"]["temp"],
                        "city": data_city["name"],
                        "pression": data_city["main"]["pressure"],
                        "date": f.split(".")[0],
                    }
                )
        except:
            print("Erreur sur le fichier ===>", os.path.join(parent_folder, f))

    df = pd.DataFrame(dfs)

    print('\n', df.head(10))
    df.to_csv(os.path.join('/app/clean_data', filename), index=False)

