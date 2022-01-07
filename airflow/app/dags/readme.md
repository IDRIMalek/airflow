
Explication de mes choix. 

J'ai tout d'abord travaillé les scripts un par un en dehors de airflow afin de m'assurer de leur fonctionnement. 
Puis je les ai regroupé en trois fichiers: 
-task_1.py ,pour ce qui concerne les fonctions de préparation des données  
-task_2_3.py ,pour ce qui concerne les fonctions de transformation des données sous format csv
-task_4_5.py pour le choix du meilleur model. 
Ainsi le fichier main comportant le dag est plus simple à comprendre car il ne comporte que les tâches et tout ce qui est relatif au DAG. 

