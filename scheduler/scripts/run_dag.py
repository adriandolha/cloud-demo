from scripts.scheduler_service import SchedulerService

service = SchedulerService('http://34.207.74.29:8080')
response = service.run('connector_hello')
print(response.status_code)
print(response.content)
