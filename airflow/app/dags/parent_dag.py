from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.subdag import SubDagOperator
from airflow.operators.bash import BashOperator
# importing DAG generating function
#from my_subdag import create_sub_dag

my_parent_dag = DAG(
    dag_id="parent_to_subdag2",
    tags=['tutorial', 'datascientest'],
    schedule_interval=None,
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, 1)
    }
)

def create_sub_dag(dag_id, schedule_interval, start_date):
    my_sub_dag = DAG(
        dag_id=dag_id,
        schedule_interval=schedule_interval,

        default_args={
            'start_date': days_ago(0)
        }
    )

    task1 = BashOperator(
        bash_command="echo subdag task 1",
        task_id="my_sub_dag_task1",
        dag=my_sub_dag
    )

    task2 = BashOperator(
        bash_command="echo subdag task 2",
        task_id="my_sub_dag_task2",
        dag=my_sub_dag
    )

    task1 >> task2

    return my_sub_dag

task1 = SubDagOperator(
    task_id="my_subdag",
    subdag=create_sub_dag(
        dag_id=my_parent_dag.dag_id + '.' + 'my_subdag',
        schedule_interval=my_parent_dag.schedule_interval,
        start_date=my_parent_dag.start_date),
    dag=my_parent_dag
)


task2 = BashOperator(
    task_id="bash_task",
    bash_command="echo hello world from parent",
    dag=my_parent_dag
)

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago




task1 >> task2