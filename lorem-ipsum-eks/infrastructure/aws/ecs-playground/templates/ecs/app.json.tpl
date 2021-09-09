
[
  {
    "name": "lorem-ipsum-app",
    "image": "${app_image}",
    "cpu": ${fargate_cpu},
    "memory": ${fargate_memory},
    "networkMode": "awsvpc",
    "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/cb-app",
          "awslogs-region": "${aws_region}",
          "awslogs-stream-prefix": "ecs"
        }
    },
    "portMappings": [
      {
        "containerPort": ${app_port},
        "hostPort": ${app_port}
      }
    ],
    "secrets": [
      {
        "name": "aurora_password",
        "valueFrom": "${database_password}"
      },
      {
        "name": "aurora_user",
        "valueFrom": "${database_user}"
      },
      {
        "name": "admin_user",
        "valueFrom": "${admin_user}"
      },
      {
        "name": "admin_password",
        "valueFrom": "${admin_password}"
      },
      {
        "name": "password_encryption_key",
        "valueFrom": "${password_encryption_key}"
      },
      {
        "name": "auth0_public_key",
        "valueFrom": "${auth0_public_key}"
      }
    ],
    "environment": [
        {
          "name": "aurora_host",
          "value": "${database_host}"
        },
        {
          "name": "database_name",
          "value": "${database_name}"
        }
    ]
  }
]