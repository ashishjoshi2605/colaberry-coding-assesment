# Weather Data API

![Build Status](https://github.com/ashishjoshi2605/colaberry-coding-assesment/actions/workflows/test.yml/badge.svg)

## Purpose

This project provides a RESTful API to manage and query weather data records. It allows users to retrieve weather records and statistics for different weather stations, ensuring robust data validation, error handling, and pagination.

## Project Structure

### Answer to Problem 1 - Data Modeling
- **src/models.py**: Contains SQLAlchemy models representing the weather records and statistics.

### Answer to Problem 2 - Ingestion
- **src/load_data.py**: Script to load weather data from `.txt` files into the SQLite database.

### Answer to Problem 3 - Data Analysis
- **src/calculate_statistics.py**: Script to calculate yearly weather statistics for each weather station and store them in the database.

### Answer to Problem 4 - REST API
- **src/resources.py**: Contains controllers for the API endpoints.
- **src/app.py**: Contains actual code to create API endpoints and swagger documentation.
- **src/test_app.py**: Contains unit tests to ensure the API endpoints function correctly and meet specified requirements.

### AWS Deployment Plan

#### Storage of Text Files
To store the tab-separated text files containing weather data, I will use **Amazon S3 (Simple Storage Service)**. S3 is ideal for storing large amounts of data due to its durability, scalability, and security.

#### Data Ingestion
For the data ingestion process, I will use **AWS Lambda**. I will write a Lambda function that reads data from the S3 bucket, processes it, and loads it into the database. This function will be triggered on a schedule using **Amazon CloudWatch Events**.

#### Database
Instead of using SQLite, I will use **Amazon RDS (Relational Database Service)** with a database engine like PostgreSQL or MySQL. RDS is fully managed, making it easier to set up, operate, and scale a relational database in the cloud.

#### API Deployment
I will containerize my Flask API using Docker and deploy it using **Amazon ECS (Elastic Container Service)** or **AWS Fargate**. Fargate allows me to run containers without managing the underlying infrastructure. To expose the API endpoints, I will set up **Amazon API Gateway**.

#### Scheduled Data Ingestion
I will use **Amazon CloudWatch Events** to schedule the Lambda function to run at specific intervals, automating the data ingestion process.

### Detailed Steps:

1. **Store Text Files in S3**
    - Create an S3 bucket and upload all the tab-separated text files.

2. **Data Ingestion with Lambda**
    - Write a Lambda function to read data from S3, process it, and insert it into an Amazon RDS database.
    - Use Amazon CloudWatch Events to trigger the Lambda function on a schedule.

3. **Set Up the Database in RDS**
    - Create an RDS instance with PostgreSQL or MySQL.
    - Set up the necessary tables in the RDS instance to store the weather data.

4. **Deploy Flask API with ECS or Fargate**
    - Create a Dockerfile for the Flask application.
    - Build the Docker image and push it to Amazon ECR (Elastic Container Registry).
    - Create an ECS cluster and set up a task definition using the Docker image.
    - Use Fargate to run the containers.

5. **API Gateway**
    - Set up Amazon API Gateway to expose the endpoints of the Flask application.
    - Configure API Gateway to integrate with the ECS/Fargate service.

### Architecture Diagram

Below is the architecture diagram illustrating the AWS services used:

![AWS Architecture Diagram](https://github.com/ashishjoshi2605/colaberry-coding-assesment/blob/dev/aws_architecture_diagram.png)

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/ashishjoshi2605/colaberry-coding-assesment.git
   ```

   ```bash
    cd colaberry-coding-assesment
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **Windows:**
     1. Open PowerShell as Administrator.
     2. Run the following command to allow script execution:
        ```powershell
        Set-ExecutionPolicy RemoteSigned
        ```
     3. Go back to the terminal where you cloned the repository to activate the virtual environment:
        ```bash
        venv\Scripts\activate
        ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Requirements**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run Data Ingestion (This will take about 5 minutes to execute.)**

   ```bash
   python src/load_data.py
   ```

6. **Perform Data Analytics Task**

   ```bash
   python src/calculate_statistics.py
   ```

7. **Launch the API**

   ```bash
   python src/app.py
   ```

8. **Access the Swagger UI**

   Open your web browser and navigate to `http://127.0.0.1:5000/apidocs` to access the Swagger UI for the API documentation.

## Running the Tests

To run the unit tests and check code coverage:

```bash
coverage run -m unittest discover -s src -p "test_app.py"
```

```bash
coverage report -m
```

## API Endpoints

### `/api/weather`
- **Description**: Retrieve weather records.
- **Method**: `GET`
- **Parameters**:
  - `page` (optional): Page number for pagination (integer).
  - `per_page` (optional): Number of records per page (integer).
  - `date` (optional): Filter by date in `YYYY-MM-DD` format (string).
  - `station_id` (optional): Filter by station ID (string).
- **Responses**:
  - `200 OK`: Successfully retrieved weather records.
    ```json
    {
      "total": 2,
      "page": 1,
      "per_page": 10,
      "items": [
        {
          "id": 1,
          "date": "20230101",
          "max_temp": 250,
          "min_temp": 150,
          "precipitation": 0,
          "weather_station_id": "STATION1",
          "ingestion_timestamp": "2023-01-01T00:00:00"
        }
      ]
    }
    ```
  - `400 Bad Request`: Invalid date format or illogical date.
    ```json
    {
      "error": "Invalid date format or illogical date. Use YYYY-MM-DD format."
    }
    ```
  - `404 Not Found`: No records matching the criteria.
    ```json
    {
      "error": "No records matching this criteria found."
    }
    ```

### `/api/weather/stats`
- **Description**: Retrieve weather statistics.
- **Method**: `GET`
- **Parameters**:
  - `page` (optional): Page number for pagination (integer).
  - `per_page` (optional): Number of records per page (integer).
  - `year` (optional): Filter by year in `YYYY` format (integer).
  - `station_id` (optional): Filter by station ID (string).
- **Responses**:
  - `200 OK`: Successfully retrieved weather statistics.
    ```json
    {
      "total": 1,
      "page": 1,
      "per_page": 10,
      "items": [
        {
          "id": 1,
          "year": 2023,
          "weather_station_id": "STATION1",
          "avg_max_temp": 25.0,
          "avg_min_temp": 15.0,
          "total_precipitation": 0.5
        }
      ]
    }
    ```
  - `400 Bad Request`: Invalid year format.
    ```json
    {
      "error": "Invalid year format. Use YYYY format."
    }
    ```
  - `404 Not Found`: No records matching the criteria.
    ```json
    {
      "error": "No records matching this criteria found."
    }
    ```

## Scripts

### models.py
Defines the SQLAlchemy models:
- `WeatherRecord`: Represents weather records with fields for date, temperatures, precipitation, and station ID.
- `WeatherStats`: Represents weather statistics with fields for year, average temperatures, and total precipitation.

### load_data.py
Loads weather data from `.txt` files into the SQLite database:
- Reads weather data files.
- Inserts data into the `WeatherRecord` table.
- Ensures no duplicate entries are inserted.

### calculate_statistics.py
Calculates and stores yearly weather statistics:
- Computes average maximum and minimum temperatures, and total precipitation for each weather station per year.
- Stores the results in the `WeatherStats` table.

### test_app.py
Contains unit tests for the API endpoints:
- Tests validation of date and year formats, ensuring `400 Bad Request` responses for invalid inputs.
- Tests responses for valid inputs and empty results, ensuring `404 Not Found` and `200 OK` statuses as appropriate.
- Verifies pagination functionality.
- Achieves more than 80% code coverage.
  
This project ensures robust handling and querying of weather data, with comprehensive validation and error handling, and thorough unit tests to maintain code quality.
