import json

from scheduler.scripts.scheduler_service import SchedulerService

service = SchedulerService('http://ec2-54-86-81-164.compute-1.amazonaws.com:8080')
response = service.get_task('connector_hello', 'run_connector')
print(response.status_code)
content = json.loads(response.content)
for k in content:
    print(k)
print(content)
