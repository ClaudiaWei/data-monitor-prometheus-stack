import os
from prometheus_client import Gauge
from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('gcp-creds.json')
project_id = os.getenv('PROJECT_ID', default='<your-project-id>')
client = bigquery.Client(credentials=credentials,project=project_id)

file_name_list = []

def initAllGuages():
    sql_files_path = './bq_sql'
    for root, dirs, files in os.walk(sql_files_path):
        for file in files:
            file_path = os.path.join(root, file)
            folder_name = os.path.basename(os.path.dirname(file_path))
            sql_file_name = os.path.basename(file_path)
            sql_file_name = sql_file_name.split('.sql')
            sql_file_name = sql_file_name[0]
            file_name_list.append(sql_file_name)
    print(file_name_list)
    for file_name in file_name_list:
        file_name = Gauge(file_name, '')
        print(file_name + ' = Guage("' + file_name + '", " ")')

  