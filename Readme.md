The task requires automating the setup of a development environment, which includes running a PostgreSQL database and an API service. We will use Docker and Docker Compose to achieve this, following Infrastructure as Code (IaC) principles.

## Tools Used
Docker: Containerizes both the PostgreSQL database and the API service to ensure consistency across environments.
Docker Compose: Orchestrates both services (PostgreSQL and the API) with a single command.
PostgreSQL: The relational database system where the data is stored.
Python + Gunicorn: The API service runs on Python and uses Gunicorn as the WSGI server.


# Development Environment Setup

## Prerequisites
- Docker
- Docker Compose

## Steps to Run the Environment

## 1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/deployable-env.git
   cd deployable-env


## 2. Build and start the containers:
   
       docker-compose up --build

## 3. Access the API by running the following command:

       curl "http://127.0.0.1:3000/rates?date_from=2021-01-01&date_to=2021-01-31&orig_code=CNGGZ&dest_code=EETLL"


## 4. To verify the database is running:

     docker exec -it <db_container_id> psql -U postgres -c "SELECT 'alive'"


This will set up the database and the API service, which can be accessed at http://localhost:3000.



##  Part 2: Theoretical Case - Evolving a Data Ingestion Pipeline

The second part of the task involves evolving a data ingestion pipeline for processing large batches of data while ensuring high availability and atomicity (all-or-nothing batch processing).

## Assumptions:

Each batch contains tens of thousands of data items.
The system must handle unpredictable spikes in incoming data and maintain high availability.
The entire batch must be processed as a single unit: either all items are inserted, or none are (atomicity).
Both ingestion and retrieval traffic can be sporadic but sometimes very high.


## Proposed Solution

## Architecture Overview

We will design a highly scalable, decoupled pipeline using AWS services. The architecture components are:

API Gateway: The entry point for batch submissions. It provides a managed, scalable interface to receive incoming data.

AWS SQS (Simple Queue Service): Acts as a buffer between the API and the processing service. It ensures scalability and smooth handling of sporadic traffic spikes by queuing incoming data.

AWS Lambda: Processes batches from the SQS queue. Lambda functions can scale horizontally, handling large volumes of incoming data without provisioning or managing servers.

PostgreSQL (RDS): Stores the processed data. RDS ensures transactional consistency, allowing batch insertion within transactions.
