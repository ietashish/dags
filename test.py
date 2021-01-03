import time
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

dag = DAG(
    'hello',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
)

task1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag,
    email='iet.ashish@gmail.com'
)

# task2 = BashOperator(
#     task_id='echo',
#     bash_command='ls ~',
#     retries=3,
#     dag=dag,
# )

task3 = BashOperator(
    task_id='sleep',
    bash_command='sleep 2',
    retries=3,
    dag=dag,
)
task3 >> task1
# task4 = EmailOperator(task_id="email",
#                       to='iet.ashish@gmail.com,ashishg@adobe.com',
#                       subject='Hello from Airflow',
#                       html_content='Some content',
#                       dag=dag)

# def sleep_function(random_base):
#     print(f'Sleeping for {random_base} seconds')
#     time.sleep(random_base)
#     if random_base == 4:
#         raise Exception

# task1 >> task2 >> task3

# for i in range(50):
#     pythonTask = PythonOperator(task_id=f'sleep_for_{i}_sec',
#                                 python_callable=sleep_function,
#                                 op_kwargs={'random_base': i},
#                                 dag=dag)
#     task3 >> pythonTask
#     pythonTask >> task4