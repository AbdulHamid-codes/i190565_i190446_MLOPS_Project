from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
import subprocess

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 11),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('ride_ez_dag', default_args=default_args, schedule_interval=None)

def preprocess():
    subprocess.run(["python", "preprocess.py"], check=True)

def train():
    subprocess.run(["python", "train.py"], check=True)

def evaluate():
    subprocess.run(["python", "evaluate.py"], check=True)

def deploy():
    subprocess.run(["python", "app.py"], check=True)

preprocess_task = PythonOperator(
    task_id='preprocess_task',
    python_callable=preprocess,
    dag=dag
)

train_task = PythonOperator(
    task_id='train_task',
    python_callable=train,
    dag=dag
)

evaluate_task = PythonOperator(
    task_id='evaluate_task',
    python_callable=evaluate,
    dag=dag
)

deploy_task = BashOperator(
    task_id='deploy_task',
    bash_command='python app.py',
    dag=dag
)

preprocess_task >> train_task >> evaluate_task >> deploy_task
