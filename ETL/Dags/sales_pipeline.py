from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import DummyOperator
from pathlib import Path
import sys
sys.path.append('/../Extract)
from SalesOrderDetailETL import ETL as sodetl
from SalesOrderHeaderETL import ETL as sohetl
from SalesTerritoryETL import ETL as stetl
from SalesTerritoryHistory import ETL as sthetl
sys.path.append('/../Load')
from DataLoad import main as load

default_args = {
    'owner': 'Diego Gonzalez',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 25),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'sales_pipeline',
    default_args=default_args,
    description='ETL de sales',
    schedule_interval=timedelta(days=1),  # se corre diariamente
)

# Tasks
start = (DummyOperator, task_id = 'start')
end = (DummyOperator, task_id = 'end')
clean_csv1 = PythonOperator(
    task_id='run_sodetl',
    python_callable=sodetl,
    dag=dag
)
clean_csv2 = PythonOperator(
    task_id='run_sohetl',
    python_callable=sodetl,
    dag=dag
)
clean_csv3 = PythonOperator(
    task_id='run_stetl',
    python_callable=stetl,
    dag=dag
)
clean_csv4 = PythonOperator(
    task_id='run_sthetl',
    python_callable=sthetl,
    dag=dag
)
load_data = PythonOperator(
    task_id='run_load',
    python_callable=load,
    dag=dag)


# Flujo
start >> [clean_csv1, clean_csv2, clean_csv3, clean_csv4] >> load_data >> end