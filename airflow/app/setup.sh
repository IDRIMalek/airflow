#!/bin/bash
# shutting down previous containers
docker-compose down 

# deleting previous docker-compose
rm docker-compose.yaml

# downloading new docker-compose.yml file
wget https://dst-de.s3.eu-west-3.amazonaws.com/airflow_avance_fr/eval/docker-compose.yaml

# creating directories
mkdir ./dags ./logs ./plugins
mkdir clean_data
mkdir raw_files

echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

#Donner tous les droits sur le dossier logs.
sudo chmod -R 777 dags/
sudo chmod -R 777 logs/
sudo chmod -R 777 plugins/
sudo chmod -R 777 clean_data/
sudo chmod -R 777 raw_files/

#initaliser les containers
docker-compose up airflow-init

# starting docker-compose
docker-compose up -d


git config --global user.email "idri.malek@gmail.com"
git config --global user.name "IDRIMalek"