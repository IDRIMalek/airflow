from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from task_1 import recup_data
from task_2_3 import transform_data_into_csv
from task_4_5 import *
from airflow.operators.subdag import SubDagOperator
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import os

CUR_DIR = os.path.abspath(os.path.dirname(__file__))

my_dag = DAG(
    dag_id='EvaluationAirflow1',
    description='EvaluationAirflow : featching data from OpenWeatherMap api, ',
    tags=['Evaluation', 'datascientest'],
    schedule_interval='* * * * *',
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0),
    },
    catchup=False
)


task1  = PythonOperator(
    task_id='fetchdata',
    python_callable=recup_data,
    dag=my_dag
)

task2 = PythonOperator(
    task_id='datas_to_dashboard',
    python_callable=transform_data_into_csv,
    op_kwargs= 20,
    dag=my_dag
)

task3 = PythonOperator(
    task_id='datas_to_ML',
    python_callable=transform_data_into_csv,
    op_kwargs={'filename': "fulldata.csv"},
    dag=my_dag
)

X, y =prepare_data('/app/clean_data/fulldata.csv')

def func_4p(task_instance):
    score_lr = compute_model_score(LinearRegression(), X, y)
    task_instance.xcom_push(key='model_accuracy', value=score_lr)


def func_4pp(task_instance):
    score_dt = compute_model_score(DecisionTreeRegressor(), X, y)
    task_instance.xcom_push(key='model_accuracy', value=score_dt)


def func_4ppp(task_instance):
    score_rfr = compute_model_score(RandomForestRegressor(), X, y)
    task_instance.xcom_push(key='model_accuracy', value=score_rfr)

def func_5(task_instance):
    list_scores=task_instance.xcom_pull(
    key="model_accuracy",
    task_ids=["LinearRegression", "DecisionTreeRegressor", "RandomForestRegressor"]
    )
    score_max=max(list_scores)
    print('score_max =>',score_max)
    list_ml=[LinearRegression(),DecisionTreeRegressor(),RandomForestRegressor()]
    # using neg_mean_square_error
    train_and_save_model(
        list_ml[list_scores.index(score_max)],
        X,
        y,
        '../clean_data/best_model.pickle'
    )

task4p = PythonOperator(
    task_id="LinearRegression",
    python_callable=func_4p,
    dag=my_dag
)

task4pp = PythonOperator(
    task_id="DecisionTreeRegressor",
    python_callable=func_4pp,
    dag=my_dag
)

task4ppp = PythonOperator(
    task_id="RandomForestRegressor",
    python_callable=func_4ppp,
    dag=my_dag
)


task5 = PythonOperator(
    task_id='best_model_finder',
    python_callable=transform_data_into_csv,
    op_kwargs={'filename': "fulldata.csv"},
    dag=my_dag
)

task1 >> [task2, task3]
task3 >> [task4p, task4pp, task4ppp] 
[task4p, task4pp, task4ppp]  >> task5

