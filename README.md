# Xeneta_Devops_task

https://github.com/xeneta/operations-task

The task is two-fold:

A practical case of developing a deployable development environment based on a simple application.

A theoretical case describing and evolving a data ingestion pipeline.

You will be expected to present and discuss both solutions.

Some general points:

Provide the solution as a public git repository that can easily be cloned by our development team.

Provide any instructions needed to run the automation solution in README.md.

The configuration file rates/config.py has some defaults that will most likely change depending on the solution. It would be beneficial to have a way to more dynamically pass in config values.

List and describe the tool(s) used, and why they were chosen for the task.

If you have any questions, please don't hesitate to contact us.

Practical case: Deployable development environment
Premise
Provided are two simplified parts of the same application environment: A database dump and an API service. Your task is to automate setting up the development environment in a reliable and testable manner using "infrastructure as code" principles.

The goal is to end up with a limited set of commands that would install the different environments and run them using containers. You can use any software that you find suitable for the task. The code should come with instructions on how to run and deploy it.

Running the database
There’s an SQL dump in db/rates.sql that needs to be loaded into a PostgreSQL 13.5 database.

After installing the database, the data can be imported through:

createdb rates
psql -h localhost -U postgres < db/rates.sql
You can verify that the database is running through:

psql -h localhost -U postgres -c "SELECT 'alive'"
The output should be something like:

 ?column?
----------
 alive
(1 row)
Running the API service
Start from the rates folder.

1. Install prerequisites
DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y python3-pip
pip install -U gunicorn
pip install -Ur requirements.txt
2. Run the application
gunicorn -b :3000 wsgi
The API should now be running on http://localhost:3000.

3. Test the application
Get average rates between ports:

curl "http://127.0.0.1:3000/rates?date_from=2021-01-01&date_to=2021-01-31&orig_code=CNGGZ&dest_code=EETLL"
The output should be something like this:

{
   "rates" : [
      {
         "count" : 3,
         "day" : "2021-01-31",
         "price" : 1154.33333333333
      },
      {
         "count" : 3,
         "day" : "2021-01-30",
         "price" : 1154.33333333333
      },
      ...
   ]
}
Case: Data ingestion pipeline
In this section we are seeking:

Your high-level considerations for architecture and possible solutions
Diagram and description of one concrete solution
Please elaborate on advantages and limitations of your chosen solution
Please document your assumptions about the problem
Extended service
Imagine that for providing data to fuel this service, you need to receive and insert big batches of new prices, ranging within tens of thousands of items, conforming to a similar format. Each batch of items needs to be processed together, either all items go in, or none of them do.

Both the incoming data updates and requests for data can be highly sporadic - there might be large periods without much activity, followed by periods of heavy activity.

High availability is a strict requirement from the customers.

How would you design the system?
How would you set up monitoring to identify bottlenecks as the load grows?
How can those bottlenecks be addressed in the future?
Provide a high-level diagram, along with a few paragraphs describing the choices you've made and what factors you need to take into consideration.

Additional questions
Here are a few possible scenarios where the system requirements change or the new functionality is required:

The batch updates have started to become very large, but the requirements for their processing time are strict.

Code updates need to be pushed out frequently. This needs to be done without the risk of stopping a data update already being processed, nor a data response being lost.

For development and staging purposes, you need to start up a number of scaled-down versions of the system.

Please address at least one of the situations. Please describe:

Which parts of the system are the bottlenecks or problems that might make it incompatible with the new requirements?
How would you restructure and scale the system to address those?
