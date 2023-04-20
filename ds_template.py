import os
import json
from pathlib import Path
from prometheus_client import Gauge
from google.oauth2 import service_account
from google.cloud.datastore import Client
from datetime import date as date_function, datetime, timedelta

credentials = service_account.Credentials.from_service_account_file('gcp-creds.json')
project_id  = os.getenv('PROJECT_ID', default='<your-project-id>')

gauges = []
is_initiated = False

def initAllGuages():
    file_list = []
    ds_files_path = './ds'
    for root, dirs, files in os.walk(ds_files_path):
        for file in files:
            file_path = os.path.join(root, file)
            ds_file_name = os.path.basename(file_path)
            ds_file_name = ds_file_name.split('.json')
            ds_file_name = ds_file_name[0]
            file_list.append({
                'filename': ds_file_name,
                'ds': json.loads(Path(file_path).read_text()),
            })

    for file in file_list:
        gauges.append({
            'gauge': Gauge(file['filename'], file['filename']),
            'ds': file['ds'],
        })
    is_initiated = True


def queryTables():
    if not is_initiated:
        print('pre init')
        initAllGuages()
        print('post init')

    for gauge in gauges:
        current_date = date_function.today()
        project_id = '<your-project-id>'
        namespace = gauge['ds']['namespace']
        kind = gauge['ds']['kind']
        filters = gauge['ds']['filters']
        client = Client(
            credentials=credentials,
            namespace=namespace,
            project=project_id
        )
        query = client.query(
            kind=kind,
            filters=filters
        )
        query_iter  = query.fetch()
        tasks       = list(query_iter)

        dates = []
        for task in tasks:
            date = task['date']
            if date not in dates:
                dates.append(date)
        dates.sort()
        date_count = 0
        if len(dates) == 0:
            continue
        start_date = datetime.strptime(dates[0], "%Y-%m-%d")
        end_date = current_date - timedelta(days=1)
        end_date = str(end_date)
        if dates[len(dates) - 1] != end_date:
            dates = dates + [end_date]
            date_count += 1
        for date_str in dates:
            while True:
                if str(start_date).split(' ')[0] == date_str:
                    start_date = start_date + timedelta(days=1)
                    break
                else:
                    start_date = start_date + timedelta(days=1)
                    date_count += 1

        gauge['gauge'].set(date_count)

queryTables()