from prometheus_client import start_http_server
import threading
import bq_template

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    bq_template.queryTables()
    set_interval(bq_template.queryTables, 86400)
    start_http_server(8000)
    
    