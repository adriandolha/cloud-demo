from scheduler.scripts.scheduler_service import SchedulerService

service = SchedulerService('http://ec2-54-86-81-164.compute-1.amazonaws.com:8080')
response = service.run('connector_hello')
print(response.status_code)
print(response.content)
