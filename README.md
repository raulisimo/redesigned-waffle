cnmv-scraping-api
This project provides a FastAPI application that serves as an API for scraping financial data from the CNMV website.

Requirements
To run this project, you need to have the following installed on your system:

Docker
Running the Containers
To run the cnmv-scraping-api application, follow these steps:


Change to the project directory:
cd cnmv-scraping-api
Build the Docker image for the application:

docker build -t cnmv-scraping-api .
Start the Docker containers for the application and the MongoDB database:


docker-compose up
This command will start two containers: one for the FastAPI application and one for the MongoDB database.

Verify that the containers are running:

bash
Copy code
docker ps
This command should display the two containers that were started in the previous step.

Test the API:

You can test the API by sending requests to http://localhost:8080 in your web browser.

Stop the Docker containers:

To stop the Docker containers, press CTRL+C in the terminal where they are running.

Alternatively, you can run the following command in a separate terminal window:

docker-compose down
This command will stop and remove the containers.

Configuration
You can configure the application by setting environment variables in the docker-compose.yml file.

The following environment variables are available:

DB_HOST: The hostname or IP address of the MongoDB database. Default: db
DB_PORT: The port number of the MongoDB database. Default: 27017
You can change the values of these environment variables by editing the docker-compose.yml file.