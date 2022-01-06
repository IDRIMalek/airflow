import os
import requests
import json
import datetime


# définition de la fonction de récupération des données depuis OpenWeatherMap
def recup_data():
    # création du dossier  '/app/raw_files' de destination des fichiers résultats des requêtes
    filepath = '/app/raw_files'
    if os.path.exists(filepath) == False:
        os.makedirs(filepath, mode = 511, exist_ok= False)
    # positionnement dans le dossier 'app/raw_files'
    os.chdir(filepath)
    # création de la liste des villes pour lesquelles les données météo vont être demandées
    city_db = ['paris', 'london', 'washington']
    # pour chaque ville de la liste précédente
    # création du nom du fichier dont le nom correspond à la date et l'heure de la récolte
    filename = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')+'.json'

    liste=[]
    for n, city in enumerate(city_db):
        # requête des données météo
        r = requests.get('https://api.openweathermap.org/data/2.5/weather',
        params= {
        'q': city,
        'appid': 'fc56ae115f07d271b2c9808ce644e091'
            }
        )
        # Remplissage du fichier avec les données météos récoltées
        liste.append(r.json())

    with open(filename, 'a') as file:
        json.dump(liste, file)
        
    return r.status_code

