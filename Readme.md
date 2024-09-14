The task requires automating the setup of a development environment, which includes running a PostgreSQL database and an API service. We will use Docker and Docker Compose to achieve this, following Infrastructure as Code (IaC) principles.

Tools Used
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


2. Build and start the containers:
   
       docker-compose up --build

3. Access the API by running the following command:

       curl "http://127.0.0.1:3000/rates?date_from=2021-01-01&date_to=2021-01-31&orig_code=CNGGZ&dest_code=EETLL"


4. To verify the database is running:

     docker exec -it <db_container_id> psql -U postgres -c "SELECT 'alive'"
