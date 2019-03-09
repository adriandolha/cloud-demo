import datetime
import json
from datetime import timezone

import boto3

if __name__ == "__main__":
    print('main')
    client = boto3.client('eks')
    cluster = client.describe_cluster(name='cloud-demo')
    print(cluster)
    created_at = cluster['cluster']['createdAt']
    print(created_at)
    dateu = created_at.replace(tzinfo=timezone.utc)
    print(dateu)
    duration=datetime.datetime.utcnow() - created_at
    print(duration)
