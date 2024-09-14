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

 1. Clone the repository:
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


 Proposed Solution

## Architecture Overview

We will design a highly scalable, decoupled pipeline using AWS services. The architecture components are:

API Gateway: The entry point for batch submissions. It provides a managed, scalable interface to receive incoming data.

AWS SQS (Simple Queue Service): Acts as a buffer between the API and the processing service. It ensures scalability and smooth handling of sporadic traffic spikes by queuing incoming data.

AWS Lambda: Processes batches from the SQS queue. Lambda functions can scale horizontally, handling large volumes of incoming data without provisioning or managing servers.

PostgreSQL (RDS): Stores the processed data. RDS ensures transactional consistency, allowing batch insertion within transactions.


+-------------------+    +-----------------+    +------------------+
| Incoming Batch    | -> |  Data Ingestion  | -> |  Queue (SQS)     | 
| HTTP Requests     |    |  Microservice    |    |                  |
+-------------------+    +-----------------+    +------------------+
                                                      |
                                                      v
                                            +--------------------+
                                            |  Processing Worker  | 
                                            |  (AWS Lambda)       | 
                                            +--------------------+
                                                      |
                                                      v
                                            +--------------------+
                                            |  Database (RDS)     | 
                                            +--------------------+



Key Components

AWS SQS:

Decoupling: Acts as a buffer, allowing the system to handle sudden surges in incoming requests.
Scalability: Can handle large volumes of messages, ensuring that the backend is not overwhelmed by traffic spikes.
AWS Lambda:

Scalability: Automatically scales based on the number of messages in the SQS queue. Lambda can process multiple batches concurrently.
Atomicity: Batches are processed within a single Lambda invocation, and database transactions are used to ensure that either all data is inserted or none of it is.
PostgreSQL (RDS):

Transactional Integrity: Supports transactions, ensuring that all batch items are processed atomically.
Horizontal Scaling: If necessary, we can scale the RDS instance vertically or use read replicas to distribute query loads.
Monitoring and Bottleneck Identification
Monitoring Tools:

CloudWatch: Monitors the SQS queue length, Lambda execution duration, and RDS performance (CPU, memory, IOPS).
RDS Metrics: Monitor database performance using built-in RDS metrics.
Potential Bottlenecks:

Queue Backlogs: If the SQS queue grows consistently, it indicates that Lambda isn't processing batches quickly enough. Increase Lambda concurrency to process more batches simultaneously.
Database Performance: If the database becomes a bottleneck due to high write activity, consider upgrading the RDS instance or introducing sharding to spread the load.



Theoretical Case: Data Ingestion Pipeline
High-Level Considerations
We need to design a system to ingest and process large batches of data (e.g., tens of thousands of records) and serve requests for these records. High availability, scalability, and batch atomicity (all-or-nothing processing) are critical requirements.

Assumptions
Data batches can arrive sporadically, so the system must handle bursts of activity.
Batch updates must be processed atomically—if one record fails, none should be inserted.
The system must be highly available, with minimal downtime.
Both read and write requests should scale smoothly with the load.
Architecture
1. Batch Ingestion with Queues
Ingestion Layer: Ingest data batches via a REST API or file upload.
Queueing System: AWS SQS or Apache Kafka can be used to queue incoming batch updates. Each batch will be processed in the order it arrives. Using a message queue helps to decouple the ingestion process from the actual processing logic.
2. Processing Layer
Batch Processor: A Lambda function or containerized service (via Kubernetes) processes the batches. The service reads messages from the queue, validates the data, and writes to the database. If the batch is processed successfully, the message is removed from the queue. If an error occurs, the batch can be retried or sent to a "dead-letter queue" for manual review.
3. Atomic Database Transactions
PostgreSQL: Use PostgreSQL with support for transactional updates. Each batch is processed in a single transaction—either the entire batch is inserted successfully, or none of it is.
4. Serving Data
A separate API service (as in the practical case) can be used to serve data requests. This service will query the database, with indexes optimized for read-heavy operations.
Read Replicas: To scale read requests, read replicas of the primary database can be used.



       +------------+
                |   Client    |
                +-----+------+
                      |
                      v
               +--------------+
               | Ingestion API |
               +--------------+
                      |
                      v
                +-------------+                +--------------+
                | Message Queue| <------------ | Dead-Letter Q |
                +------+------+                +------+-------+
                       |                            |
                       v                            v
             +------------------+         +-------------------+
             | Batch Processor   |         | Manual Processing |
             +---------+---------+         +-------------------+
                       |
                       v
           +---------------------------+
           | PostgreSQL (with replicas) |
           +---------------------------+


Advantages and Limitations
Advantages:
The queue system decouples ingestion from processing, allowing for greater flexibility and fault tolerance.
Batch processing is atomic, ensuring data integrity.
The system is highly scalable, using read replicas and a message queue to handle increasing loads.
Limitations:
The processing system may experience delays if the message queue grows too large, leading to higher latencies during periods of heavy load.
Requires careful configuration of the queue to ensure proper back-off and retry strategies.
Monitoring and Bottleneck Detection
Metrics to Monitor:
Queue length (to detect growing backlogs).
Database query performance (e.g., slow queries).
CPU, memory, and I/O usage on the batch processing instances.
Addressing Bottlenecks:
If queue lengths grow too long, increase the number of consumers (batch processors).
Optimize database queries by adding indexes and scaling the database horizontally (read replicas).
Addressing Scaling and Processing Time
If batch updates become too large:

Horizontal Scaling: Increase the number of processing instances and parallelize the workload. Partition large batches into smaller chunks that can be processed concurrently.
Database Optimizations: Use database partitioning or sharding to spread the load across multiple nodes.
If code updates need to be pushed frequently:

Zero-Downtime Deployments: Implement rolling updates or blue-green deployments to ensure that updates are pushed without interrupting ongoing data processing.





