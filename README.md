# CPSC571 - Carmichael DB
## Authors
- Gustavo Bravo
- Jonathan Webster

A comprehensive database performance analysis and web application for storing and querying Carmichael numbers, comparing SQL and NoSQL database approaches to determine optimal performance for large-scale mathematical data.

## Web Access to Application

The web application can be accessed at: https://blue.butler.edu/~gbravo/

**Disclaimer:** Due to the absence of an SSL certificate (we are currently in the process of obtaining one from Butler University), the backend API is only accessible when running on a local machine. For our demonstration to the TA, we will show the complete system running end-to-end. The system can also be tested locally by following the setup instructions below.

## Overview

This project is a two-step process designed to analyze and serve Carmichael number data efficiently:

1. **Performance Testing Phase:** Automated performance tests compare SQL (PostgreSQL) and NoSQL (MongoDB) database approaches using standardized test cases. These tests measure query execution times to determine which database schema provides the fastest performance for our specific use case.

2. **Web Application Phase:** Based on performance test results, the winning database schema is deployed in a production web application that allows users to query Carmichael numbers by their prime factors and retrieve prime factorizations.

This dual-phase approach ensures that the web application uses the most optimized database structure for handling complex queries on large mathematical datasets.

## Performance Test Overview

The performance testing system automatically benchmarks three different database schemas to determine optimal query performance:

**Database Implementations Tested:**
1. **PostgreSQL - Single Table with GIN Index:** All Carmichael numbers stored in one table with a GIN (Generalized Inverted Index) on the factors array
2. **PostgreSQL - Multi-Table Partitioning:** Carmichael numbers partitioned across multiple tables (3-14) based on the number of prime factors
3. **MongoDB - Multi-Key Index:** All Carmichael numbers stored in a single collection with a multi-key index on the factors array

**Tech Stack:**
- **Python 3:** Test orchestration and execution
- **PostgreSQL:** Relational database with array support and specialized indexing
- **MongoDB:** NoSQL document database with multi-key indexing
- **psycopg2 / psql:** PostgreSQL client libraries and command-line interface
- **pymongo:** MongoDB Python driver
- **Test Framework:** Custom Python test runner with EXPLAIN ANALYZE queries

**Testing Methodology:**
- Executes standardized test cases from the `performance_testing/test_cases/` directory
- Runs each test multiple times for statistical reliability
- Captures query execution plans and timing data
- Generates detailed performance reports for comparison

## Web Application Overview

The web application provides an interactive interface for querying the Carmichael number database using the best-performing schema identified through performance testing.

**Tech Stack:**

**Backend Server:**
- **Node.js:** Runtime environment
- **Express.js:** Web application framework
- **PostgreSQL (pg):** Database client for the one-table schema (winner of performance tests)
- **CORS:** Cross-origin resource sharing middleware
- **dotenv:** Environment variable management
- **HTTPS:** Secure server with self-signed certificates (temporary)

**Frontend:**
- **HTML5:** Semantic markup and structure
- **CSS3:** Custom styling and responsive design
- **Vanilla JavaScript:** Client-side logic and API communication
- **REST API:** Communication between frontend and backend

**Features:**
- Query Carmichael numbers by multiple prime factors
- Retrieve prime factorization for specific Carmichael numbers
- Pagination support for large result sets
- Server-side caching for improved performance
- Responsive user interface

## Setting It Up Locally

### Prerequisites

Before setting up the project, ensure you have the following installed:
- **PostgreSQL** (version 12 or higher)
- **MongoDB** (version 4.4 or higher)
- **Python 3.8+** with pip
- **Node.js** (version 16 or higher) with npm

### Step 1: Download the Carmichael Numbers Dataset

Download the complete list of Carmichael numbers from:
https://blue.butler.edu/~jewebste/new_table.txt

Save this file as `new_table.txt` in the `database/` directory of the project.

**Note:** This file is too large to be stored on GitHub and is included in `.gitignore`.

### Step 2: Setup Environment Variables

1. Copy the example environment file:
```bash
cp .env-example .env
```

2. Edit the `.env` file and fill in your configuration:
```env
# For Data Parsing
FILE_LOCATION=new_table.txt

# General Database
DATABASE=your_database_name

# PostGres Connection
HOST=127.0.0.1
PQ_USER=your_postgres_username
PQ_USER_PASSWORD=your_postgres_password
PQ_PORT=5432

# MongoDB Connection
MONGO_USER=your_mongo_username
MONGO_PASSWORD=your_mongo_password
MONGO_HOST=localhost
MONGO_PORT=27017

# Express Function
WEB_PORT=5433
```

3. Copy the same `.env` file to the backend directory:
```bash
cp .env app/backend/.env
```

### Step 3: Setup Performance Testing Databases

#### PostgreSQL Setup:

1. Create the database tables by running the SQL schema:
```bash
psql -h 127.0.0.1 -U your_username -d your_database -f database/create_tables.sql
```

2. Insert data into the single-table schema:
```bash
cd database
python pq_one_table_insert.py
```

3. Insert data into the multi-table schema:
```bash
python pq_multi_table_insert.py
```

#### MongoDB Setup:

1. Run the MongoDB insertion script:
```bash
cd database
python mongo_insert.py
```

This script will:
- Create the `carmichael_number` collection
- Insert all Carmichael numbers with their factors
- Create a multi-key index on the factors array

### Step 4: Run Performance Tests (Optional)

To compare database performance:

```bash
cd performance_testing
python execution_time_test.py
```

This will generate timestamped result files in `performance_testing/database_results/` containing detailed execution statistics for each database implementation.

### Step 5: Setup and Run the Backend Server

1. Navigate to the backend directory:
```bash
cd app/backend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the backend server:
```bash
node server.js
```

The backend server will start on the port specified in your `.env` file (default: 5433).

**Note:** The server uses HTTPS with self-signed certificates. You may need to accept the security warning in your browser.

### Step 6: Access the Frontend

The frontend is a static HTML application that can be served in multiple ways:

**Option 1 - Using Live Server (Recommended for Development):**
1. Install the Live Server extension in VS Code
2. Right-click on `app/frontend/index.html`
3. Select "Open with Live Server"
4. The application will open at `http://localhost:5500`

**Option 2 - Using Python HTTP Server:**
```bash
cd app/frontend
python -m http.server 5500
```
Then navigate to `http://localhost:5500` in your browser.

**Option 3 - Direct File Access:**
Simply open `app/frontend/index.html` directly in your web browser.

### Verification

Once everything is running:
1. The backend should be accessible at `https://localhost:5433` (or your configured port)
2. The frontend should display the Carmichael number query interface
3. Try searching for Carmichael numbers with factors like `3, 5, 7` to verify the system is working

### Troubleshooting

**Database Connection Issues:**
- Verify PostgreSQL and MongoDB are running
- Check that credentials in `.env` are correct
- Ensure database names match in both `.env` files

**Backend CORS Errors:**
- The backend is configured to accept requests from `https://blue.butler.edu`, `http://127.0.0.1:5500`, and `http://localhost:5500`
- If using a different port, update the CORS configuration in `app/backend/server.js`

**HTTPS Certificate Warnings:**
- Self-signed certificates will trigger browser warnings
- This is expected for local development
- For production deployment, obtain a proper SSL certificate

## Architecture

### Web Application Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        WEB APPLICATION                          │
└─────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │   Frontend   │
    │              │
    │  HTML + CSS  │──────┐
    │      +       │      │
    │  JavaScript  │      │  HTTPS/REST API
    └──────────────┘      │  (Port 5433)
                          │
                          ↓
                    ┌─────────────┐
                    │   Backend   │
                    │             │
                    │  Express.js │
                    │   Node.js   │
                    └─────────────┘
                          │
                          │  PostgreSQL
                          │  Protocol
                          ↓
                ┌──────────────────────┐
                │  PostgreSQL Database │
                │                      │
                │  carmichael_number   │
                │  (One Table + GIN)   │
                └──────────────────────┘
```

### Performance Testing Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PERFORMANCE TESTING                          │
└─────────────────────────────────────────────────────────────────┘

    ┌────────────────────────┐
    │ execution_time_test.py │
    │  (Test Orchestrator)   │
    └────────────────────────┘
              │
              │  Reads test cases
              ↓
      ┌──────────────┐
      │  Test Cases  │
      │   (*.txt)    │
      └──────────────┘
              │
              │  Executes queries against
              ↓
    ┌─────────────────────────────────────┐
    │                                     │
    │   ┌────────────────────────────┐    │
    │   │  PostgreSQL - One Table    │    │
    │   │  (GIN Index)               │    │
    │   └────────────────────────────┘    │
    │                                     │
    │   ┌────────────────────────────┐    │
    │   │  PostgreSQL - Multi Table  │    │
    │   │  (Partitioned 3-14)        │    │
    │   └────────────────────────────┘    │
    │                                     │
    │   ┌────────────────────────────┐    │
    │   │  MongoDB Collection        │    │
    │   │  (Multi-Key Index)         │    │
    │   └────────────────────────────┘    │
    └─────────────────────────────────────┘
              │
              │  Outputs results
              ↓
      ┌──────────────────┐
      │ database_results │
      │  (Timestamped)   │
      └──────────────────┘
```

## Project Structure

```
CPSC571-Carmichael_Storage/
├── app/
│   ├── backend/
│   │   ├── db/                    # Database interface implementations
│   │   ├── utils/                 # Utility functions (caching, etc.)
│   │   ├── server.js              # Express.js backend server
│   │   ├── package.json           # Node.js dependencies
│   │   └── .env                   # Backend environment variables
│   └── frontend/
│       ├── index.html             # Main HTML interface
│       ├── style.css              # Frontend styling
│       └── script.js              # Client-side JavaScript
├── connection/
│   ├── psql_client.py             # PostgreSQL connection wrapper
│   └── mongo_db_connect.py        # MongoDB connection wrapper
├── database/
│   ├── create_tables.sql          # PostgreSQL table schemas
│   ├── pq_one_table_insert.py     # Single table data insertion
│   ├── pq_multi_table_insert.py   # Multi-table data insertion
│   ├── mongo_insert.py            # MongoDB data insertion
│   └── new_table.txt              # Carmichael numbers dataset (not in repo)
├── performance_testing/
│   ├── execution_time_test.py     # Performance test orchestration
│   ├── test_cases/                # Standardized query test cases
│   ├── database_results/          # Test result outputs
│   └── visualize.py               # Performance visualization tools
├── .env                           # Root environment variables
├── .env-example                   # Example environment configuration
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

Developed as part of CPSC 571 - Database Management Systems at the University of Calgary.
