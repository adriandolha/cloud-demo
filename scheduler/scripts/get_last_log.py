from scripts.scheduler_service import SchedulerService

service = SchedulerService('http://34.207.74.29:8080')
last_log = service.get_last_log('connector_hello', 'run_report')
print(last_log)
