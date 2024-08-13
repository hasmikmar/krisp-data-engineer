# krisp-data-engineer
# Data Ingestion Pipeline for User Metrics

## Project Overview

This project sets up a data ingestion pipeline for streaming user metrics, including `talked_time`, `microphone_used`, `speaker_used`, and `voice_sentiment`. The pipeline ingests data into a PostgreSQL database using a Flask application. The solution is containerized with Docker, and Docker Compose is used to orchestrate the application and database containers.

## Features

- **User Metrics Ingestion:** Collects and stores user metrics, along with session and user information.
- **Database Setup:** Automatically creates necessary tables and indices for efficient data storage and retrieval.
- **Containerized Environment:** Utilizes Docker for easy setup and deployment.
- **Persistence:** Ensures data persistence by storing PostgreSQL files on the host machine.

## Technologies Used

- **Docker**: Containerization platform to run the application and database.
- **Docker Compose**: Tool for defining and running multi-container Docker applications.
- **PostgreSQL**: Relational database for storing user metrics and session data.
- **Flask**: Python web framework for handling API requests.
- **psycopg2**: PostgreSQL adapter for Python.

## Project Structure

```
.
├── app.py                 # Main Flask application
├── Dockerfile             # Dockerfile for the Flask application
├── docker-compose.yaml    # Docker Compose configuration
├── init.sql               # SQL script to initialize the database
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation (this file)
```

## Database Schema

The database consists of three main tables:

1. **users**: Stores user information.
   - `user_id` (Primary Key)
   - `name`
   - `email`
   - `created_at` (Timestamp)

2. **sessions**: Stores session data, linked to users.
   - `session_id` (Primary Key)
   - `user_id` (Foreign Key)
   - `device_id`
   - `platform`
   - `location`
   - `start_time` (Timestamp)
   - `end_time` (Timestamp)
   - `created_at` (Timestamp)

3. **user_metrics**: Stores metrics data for each session.
   - `metric_id` (Primary Key)
   - `session_id` (Foreign Key)
   - `talked_time` (Interval)
   - `microphone_used` (Boolean)
   - `speaker_used` (Boolean)
   - `voice_sentiment` (String)
   - `timestamp` (Timestamp)
   - `created_at` (Timestamp)

Indices are created for performance optimization on relevant columns.

## Setup Instructions

### Prerequisites

- Docker installed on your machine.
- Docker Compose installed on your machine.

### Steps to Run the Project

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/hasmikmar/krisp-data-engineer.git
   cd <repository-directory>
   ```

2. **Build and Run the Containers:**
   ```bash
   docker-compose up --build
   ```

3. **Access the Application:**
   - The Flask application will be available at `http://localhost:855`.
   - The PostgreSQL database will be accessible at `localhost:5432`.

### Database Initialization

The database is automatically initialized with the schema defined in `init.sql` when the application starts. This includes creating the necessary tables (`users`, `sessions`, and `user_metrics`) and setting up indices.

## API Endpoints

- **POST `/data`**: Ingest user metrics data.
  - **Request Body**:
    ```json
    {
      "user_id": 1,
      "name": "John Doe",
      "email": "john.doe@example.com",
      "session_id": 1,
      "talked_time": 120,
      "microphone_used": true,
      "speaker_used": true,
      "voice_sentiment": "positive",
      "timestamp": 1622558400
    }
    ```
  - **Response**:
    - `200 OK` on success
    - `400 Bad Request` if data is invalid
    - `500 Internal Server Error` on failure

## Maintenance and Extensions

### Future Improvements

- **Scaling:** Implementing horizontal scaling to handle increased load.
- **Data Validation:** Adding more rigorous data validation at the API level.
- **Logging and Monitoring:** Integrating logging and monitoring for better observability.

### Assumptions and Limitations

- **Data Consistency:** The application assumes that the incoming data is consistent and well-formed.
- **Single Database:** The current setup uses a single PostgreSQL instance. For high availability, a distributed database setup can be considered.
  
### Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.


# Part Two: Solutions for Coding Assignments

This section of the repository contains solutions to various coding assignments. All solutions can be found in the `Part2` folder, with each file named appropriately according to the problem it addresses.

## Table of Contents

1. [Code Review Assignments](#code-review-assignments)
2. [Solution for Find Min Pledge Problem](#solution-for-find-min-pledge-problem)
3. [Solution for Get Headlines](#solution-for-get-headlines)
4. [Solution for Process Payments](#solution-for-process-payments)
5. [Solution for Process Payments 2](#solution-for-process-payments-2)