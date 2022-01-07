import os
import json
import pandas as pd
from airflow.models import Variable

def prepare_data(path_to_data='/app/clean_data/fulldata.csv'):
    # reading data
    df = pd.read_csv(path_to_data)
    # ordering data according to city and date
    df = df.sort_values(['city', 'date'], ascending=True)

    dfs = []

    for c in df['city'].unique():
        df_temp = df[df['city'] == c]

        # creating target
        df_temp.loc[:, 'target'] = df_temp['temperature'].shift(1)

        # creating features
        for i in range(1, 10):
            df_temp.loc[:, 'temp_m-{}'.format(i)
                        ] = df_temp['temperature'].shift(-i)

        # deleting null values
        df_temp = df_temp.dropna()

        dfs.append(df_temp)

    # concatenating datasets
    df_final = pd.concat(
        dfs,
        axis=0,
        ignore_index=False
    )

    # deleting date variable
    df_final = df_final.drop(['date'], axis=1)

    # creating dummies for city variable
    df_final = pd.get_dummies(df_final)

    features = df_final.drop(['target'], axis=1)
    target = df_final['target']

    return features, target

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
    
    if filename=='fulldata.csv':
        X, y =prepare_data('/app/clean_data/fulldata.csv')
        Variable.set(key="X", value=X)
        Variable.set(key="y", value=y)

