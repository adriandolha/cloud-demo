const resume = {
    personalDetails: {
        name: 'Adrian Dolha',
        jobTitle: 'Senior Software Engineer',
        description: `Accomplished and energetic Senior Architect with a solid history of achievement in Enterprise Software.
        Motivated leader with strong organizational and prioritization abilities.
        Seeking to leverage his technical and professional expertise in the latest technologies such as AWS serverless,
        cloud native microservices and event driven architectures.`,
        picture: window.location.origin + '/img/me.jpeg',
        contact: {
            email: 'adrian.dolha1@gmail.com',
            phone: '+40743389452',
            location: 'Cluj-Napoca, Romania',
            github: { link: 'https://github.com/adriandolha', placeholder: 'github.com/in/adriandolha' },
            linkedin: { link: 'https://www.linkedin.com/in/adrian-dolha-562578b8/', placeholder: 'linkedin.com/in/adrian-dolha-562578b8' },
        }
    },
    skillsTitle: 'Skills',
    skills: {
        backend: {
            name: 'Backend',
            level: 5, items: [
                ['Python',
                    'Flask',
                    'Airflow',
                    'Pandas'],
                ['Java',
                    'Spring',
                    'Spring Boot',
                    'Spring JPA',
                    'Spring WebFlow',
                    'Spring Web MVC'],
                ['SQL Server', 'Oracle', 'Postgres', 'DynamoDb', 'Redis', 'RabbitMQ']
            ]
        },
        cloud: {
            name: 'Cloud',
            level: 5, items: [
                ['AWS'],
                ['Azure']
            ]
        },
        devops: {
            name: 'Devops',
            level: 4, items: [
                ['Jenkins',
                    'Terraform',
                    'Tekton',
                    'ArgoCD']
            ]
        },
        frontend: {
            name: 'Frontend',
            level: 3, items: [
                ['React',
                    'Material UI',
                    'Bootstrap'],
                ['Javascript',
                    'HTML',
                    'CSS'],
                ['Knockout']
            ]
        }
    },
    achievementsTitle: 'Achievements',
    achievements: [{
        title: 'AWS Certified Solutions Architect – Associate',
        name: 'aws_saa',
        badge: window.location.origin + '/img/aws_saa.png',
        from: '09/2021',
        to: '09/2024'
    }],
    languagesTitle: 'Languages',
    languages: [{
        title: 'English',
        level: 'Full Profesional Proficiency'
    }, {
        title: 'Romanian',
        level: 'Native'
    }
    ],
    educationTitle: 'Education',
    education: [{
        title: 'Technical University of Cluj-Napoca',
        specialization: 'Computer Science',
        from: '09/2004',
        to: '07/2009',
        location: 'Cluj-Napoca'
    }, {
        title: 'Tiberiu Popovici High Scool',
        specialization: 'Computer Science',
        from: '09/2000',
        to: '07/2004',
        location: 'Cluj-Napoca'
    }
    ],
    workExperienceTitle: 'Work Experience',
    tasksTitle: 'Achievements/Tasks',
    workExperiences: [
        {
            jobTitle: 'Head of Development',
            company: 'Endava',
            from: '01/2019',
            to: '04/2021',
            tasks: [
                'Coordinated Development Discipline with 10 Discipline Leads and over 400 developers.',
                'Built 6 technical communities for Java, .NET, Android, iOS, Frontend, Python',
                'Growed the Discipline from 300 to 400 members',
                'Doubled Frontend developers.',
                'Responsible for workforce planning, hiring, juniors intake, technical interviews.',
                'Involved in presales.',
            ],
            techStack: ['Management', 'Workforce Planning', 'Salary Reviews', 'Technical Communities', 'Presales',
                'People Development', 'Career Coach']
        },
        {
            jobTitle: 'Senior Architect',
            company: 'Endava',
            from: '05/2018',
            to: '05/2019',
            tasks: [
                'Coordinated the development effort for the team.',
                'Created on-boarding procedure for new team members.',
                'Trained new team members.',
                'Proposed architectural solutions for serverless AWS and Azure microservices.',
                'Created code structure and templates according to best practices.',
                'Developed a strategy to migrate from AWS to Azure.',
                'Documented application architecture.'
            ],
            techStack: ['Python', 'Flask', 'Apache Airflow', 'AWS', 'S3', 'DynamoDB', 'SQS', 'AWS Lambda', 'EKS', 'Azure', 'AKS']
        },
        {
            jobTitle: 'Product Architect',
            company: 'SDL',
            from: '01/2016',
            to: '04/2018',
            tasks: [
                'Designed the integration of new services.',
                'Improved availability from 95 to 99.',
                'Migrated from ANT to MAVEN and built Jenkins pipelines.',
                'Implemented monitoring using ELK stack.',
                'Provided support for the adoption of APM tool.',
                'Automated release process and increased test coverage with 20% on unit tests and 50% on e2e tests.',
                'Provided support to migrate from on-prem to AWS.',
                'Split the monolith and worked to containerize the application using Docker/ Kubernetes - developed demo projects based on Spring Boot/Kafka/ ElasticSearch /Redis, etc.',
                'Collaborated closely with different stakeholders from PM, PO, Dev Manager, DEV QA to OPS and Professional Support.'
            ],
            techStack: ['Java', 'Spring', 'Spring Boot', 'Docker', 'Kubernetes', 'AWS', 'Elastic Beanstalk', 'Jenkins', 'Maven', 'SQL Server', 'Oracle', 'Knockout']
        },
        {
            jobTitle: 'Technical Lead',
            company: 'SDL',
            from: '01/2014',
            to: '01/2016',
            tasks: [
                'Designed and implemented REST APIs from scratch.',
                'Worked closely on the integration and adoption of Spring stack: DI, REST, MVC, AOP, JPA (Hibernate).',
                'Lead the adoption of QueryDSL and migrated from Java 6 to Java 8, from Tomcat 7 to Tomcat 8.',
                'Fixed critical outages and performance issues.',
                'Provided continuous support for OPS, DEV and Professional Services and outstanding technical support to clients.'
            ],
            techStack: ['Java', 'Spring', 'SQL Server', 'Oracle', 'JSP']
        },
        {
            jobTitle: 'Software Developer',
            company: 'SDL',
            from: '01/2013',
            to: '01/2014',
            tasks: [
                'Worked on world leading translation software. The application offered both translation and translation projects management capabilities, being used by top companies over the world.',
                'Implemented new features.',
                'Provided maintenance on a large Enterprise product.',
                'Introduced new libraries.',
                'Started working on application refresh.',
                'Documented the application after KT and helped with the on boarding process for new comers.'
            ],
            techStack: ['Java', 'Spring', 'SQL Server', 'Oracle', 'JSP']
        },
        {
            jobTitle: 'Software Engineer',
            company: 'HP',
            from: '10/2009',
            to: '01/2013',
            tasks: [
                'Developed and worked on dozens of integrations (Active Driectory , OpenStack , Exchange, Powershell , SCVMM , EC2 , VMWARE , etc.) in a product used to orchestrate datacenter operations. The integrations were developed in Java/C#.',
                'Migrated build from ANT to Maven.',
                'Developed key integrations.',
                'Fixed critical issues for major clients.'
            ],
            techStack: ['Java', 'C#']
        }

    ],
    personalProjectsTitle: 'Personal Projects',
    personalProjects: [{
        title: 'Lorem Ipsum',
        github: { link: 'https://github.com/adriandolha/cloud-demo/tree/master/lorem-ipsum', placeholder: 'Github Repo' },
        from: '10/2009',
        to: 'Present',
        description: '',
        tasks: [
            'Developed and worked on dozens of integrations (Active Driectory , OpenStack , Exchange, Powershell , SCVMM , EC2 , VMWARE , etc.) in a product used to orchestrate datacenter operations. The integrations were developed in Java/C#.',
            'Migrated build from ANT to Maven.',
            'Developed key integrations.',
            'Fixed critical issues for major clients.'
        ],
        techStack: ['Python', 'Flask', 'Kubernetes', 'Istio', 'Terraform', 'Tekton', 'ArgoCD']
    },
    ]
}

export default resume;