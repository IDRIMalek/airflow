from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from task_1 import *
from task_2_3 import *
from task_4_5 import *
from airflow.operators.subdag import SubDagOperator
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import os

with DAG(
    dag_id='EvaluationAirflow14',
    description='EvaluationAirflow : featching data from OpenWeatherMap api, ',
    tags=['Evaluation', 'datascientest'],
    schedule_interval= '* * * * *',
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0),
    },
    catchup=False
) as my_dag:

    task1  = PythonOperator(
        task_id='fetchdatas',
        python_callable=recup_data,
    )

    task2 = PythonOperator(
        task_id='datas_to_dashboard',
        python_callable=transform_data_into_csv,
        op_kwargs= {'n_files':20},
        provide_context=True,
    )

    task3 = PythonOperator(
        task_id='datas_to_ML',
        python_callable=transform_data_into_csv,
        op_kwargs={'filename': "fulldata.csv"},
        provide_context=True,
    )

    task4p = PythonOperator(
        task_id="LinearRegression",
        python_callable=func_4p,
    )

    task4pp = PythonOperator(
        task_id="DecisionTreeRegressor",
        python_callable=func_4pp,
    )

    task4ppp = PythonOperator(
        task_id="RandomForestRegressor",
        python_callable=func_4ppp,
    )


    task5 = PythonOperator(
        task_id='best_model_finder',
        python_callable=func_5,
    )


    task1 >> [task2, task3]
    task3 >> [task4p, task4pp, task4ppp] 
    [task4p, task4pp, task4ppp]  >> task5

