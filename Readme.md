# Description:
The Weather application lets you ingest data into database and accordingly lets you perform api calls to fetch respective weather records and weather stats data from their respective api's.

# Framework used:
- Fastapi

# Weather API with fastAPI.
There are 3 endpoints in this project:-
  1. `/api/weather/`
  2. `/api/weather/stats/`
  3. `/docs`

# Project Setup and Installation.
1. Clone the git repository.
2. Move to project directory using below command (project directory:: weather-api):-
```bash
cd weather-api
```
3. Create and activate a virtual environment using the below commands:-
```bash
  python -m venv venv
  source venv/bin/activate #(For Mac and Linux)
  venv\Scripts\activate #(For Windows)
```
4. Run the below command to install the required packages:-
```bash 
  pip install -r requirements.txt
  ```

# Database Setup and Installation.
1. Download and Install PostgreSQL in your computer using this link `https://www.postgresql.org/download/`.
2. Create a database using below command:-
```bash
CREATE DATABASE database_name;
```

# Setup environment variables.
Create a .env file and store your database credentials in below format:-
```bash
DB_USER='user_name_for_db'
DB_PASSWORD='password_of_db'
DB_HOST='host_of_db'
DB_PORT='port_number_of_db'
DB_NAME='name_of_db'
MAIN_DATABASE_URL='f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"'
TESTING_DATABASE_URL='f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"'
```

# Run project.

1. Run the below command to load the data and run the project:-
```bash
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000 
```

# Data Ingestion Information:
- Now when application starts running, data ingestion process starts automatically.
- Entire information regarding ingestion process will be logged into log file which is generated automatically at runtime.
- Also, to verify ingestion process completion in terminal: 
- You can see following logs in the terminal:
  - INFO:     Waiting for application startup -> Once this is received, ensures ingestion process is started.
  - INFO:     Application startup complete -> Once this is received, ensures ingestion process is completed and application is started successfully.
<br><br>

![Alt text](static/application-start.png?raw=true "application start")

#### This step will take few minutes as it will dump the data in the initial setup.

# To access the API endpoints:
```bash
/api/weather/  #for weather records
/api/weather/stats/  #for weather stats
/docs #for accessing swagger api documentation

- Rest of our functionalities can be easily accessed through the API links:
  http://127.0.0.1:8000/api/swagger/
  http://127.0.0.1:8000/api/weather/
  http://127.0.0.1:8000/api/weather/stats/

  
```
# Troubleshoot to application startup if any: Kill port if port already in use:
```bash
kill -9 $(lsof -t -i:8000)
```

# Testing:
To run the testcases use this command:-
```bash
pytest
```

### For Code Coverage:
```bash
pytest --cov
```
<br><br>
![Alt text](static/tests.png?raw=true "testing")

# Screenshots of Postman Collection

![Alt text](static/weather-all.png?raw=true "weather records all")
<br><br>
![Alt text](static/weather-date.png?raw=true "weather records date")
<br><br>
![Alt text](static/weather-station.png?raw=true "weather records station")
<br><br>
![Alt text](static/weather-page-limit.png?raw=true "weather records page limit")
<br><br>
![Alt text](static/weather-stats-all.png?raw=true "weather stats records all")
<br><br>
![Alt text](static/weather-stats-year.png?raw=true "weather stats records date")
<br><br>
![Alt text](static/weather-stats-station.png?raw=true "weather stats records station")
<br><br>
![Alt text](static/weather-stats-page-limit.png?raw=true "weather stats records page limit")

# Screenshots of Swagger API Collection

![Alt text](static/swagger-1-1.png?raw=true "swagger api weather records")
<br><br>
![Alt text](static/swagger-1-2.png?raw=true "swagger api weather records")
<br><br>
![Alt text](static/swagger-2-1.png?raw=true "swagger api weather stats")
<br><br>
![Alt text](static/swagger-2-2.png?raw=true "swagger api weather stats")

# AWS Deployment Approach
# Deploying FastAPI API on AWS

## Deployment Overview
Deploying a FastAPI API on AWS involves leveraging several key services to ensure scalability, security, and ease of management.

## Steps:

### 1. AWS Elastic Beanstalk Setup
- Utilize AWS Elastic Beanstalk for streamlined deployment and operation of your FastAPI web application.
- Elastic Beanstalk supports Python, the foundational language for FastAPI, making it ideal for hosting your API.

### 2. Load Balancer Implementation
- Implement a load balancer to efficiently manage incoming traffic.
- Distribute requests across multiple instances of your FastAPI application to ensure optimal performance and reliability.

### 3. Database Deployment with Amazon RDS
- Deploy a PostgreSQL database using Amazon RDS (Relational Database Service).
- RDS provides a fully managed, scalable database solution, ensuring robust data storage capabilities for your FastAPI application.
- Securely configure access between your FastAPI API and the RDS instance to protect sensitive data.

### 4. Data Storage Options
- Store text files using AWS EFS (Elastic File System) or S3 (Simple Storage Service).
- AWS EFS offers scalable, shared file storage for your application's file system needs.
- S3 provides durable object storage, suitable for storing large volumes of unstructured data.

### 5. Scheduling Data Ingestion Process
- Implement a data ingestion pipeline using AWS ECS FARGATE.
- Use AWS ECR (Elastic Container Registry) to store container images required for data processing tasks.
- Define Amazon CloudWatch Events rules to schedule and automate Fargate tasks at specified intervals.
- Facilitate seamless data ingestion into the PostgreSQL database hosted on Amazon RDS.

## Conclusion
This deployment approach ensures a scalable, secure, and manageable environment for your FastAPI API, database, and data ingestion processes.
By leveraging AWS Elastic Beanstalk, Amazon RDS, ECS FARGATE, and CloudWatch Events, you can effectively handle varying levels of traffic and automate data ingestion tasks without the complexities of infrastructure management.
