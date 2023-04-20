import os
from pathlib import Path
from prometheus_client import Gauge
from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('gcp-creds.json')
project_id = os.getenv('PROJECT_ID', default='<your-project-id>')
client = bigquery.Client(credentials=credentials,project=project_id)

gauges = []
is_initiated = False

def initAllGuages():
    file_list = []
    sql_files_path = './bq_sql'
    for root, dirs, files in os.walk(sql_files_path):
        for file in files:
            file_path = os.path.join(root, file)
            sql_file_name = os.path.basename(file_path)
            sql_file_name = sql_file_name.split('.sql')
            sql_file_name = sql_file_name[0]
            file_list.append({
                'filename': sql_file_name,
                'query': Path(file_path).read_text(),
            })

    for file in file_list:
        gauges.append({
            'gauge': Gauge(file['filename'], file['filename']),
            'query': file['query'],
        })
    is_initiated = True

def queryTables():
    if not is_initiated:
        print('pre init')
        initAllGuages()
        print('post init')
    
    for gauge in gauges:
        query_job = client.query(gauge['query'])
        results = query_job.result()

        for result in results:
            gauge['gauge'].set(result.resultValue)
