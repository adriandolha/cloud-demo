from scripts.scheduler_service import SchedulerService
service = SchedulerService('http://ec2-54-86-81-164.compute-1.amazonaws.com:8080')
response = service.run('dcmapireport-012ad701-57ca-453f-9733-1de1d77d2830')
print(response.status_code)
print(response.content)
