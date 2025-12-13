"""
Python SQL and NoSQL Tester

Run scripts required to analyze the query time using the EXPLAIN
ANALYZE keywords or .explain() pymongo function.

The script will connect to the database, and then execute the test
cases found in the TEST_DIR path director. Requirements for file:
- Database Setup with Carmichael table implementations.
- Implementation of PSQLClient.
- Connection to PyMongo client.
- Environment variables for establishing a connection.
- Test cases found in the TEST DIR path.

Currently there are two SQL implementations created that this file
will test. They are:
1) One table with GIN - All CN numbers in one table.
2) Multi table - All CN numbers split by the number of factors.
3) MongoDB collection with Multi Key Index - All CN numbers in one collection.

@author Gustavo Bravo
@date November 21, 2025
    Revised December 11, added MongoDB tests
"""

from dotenv import load_dotenv
from datetime import datetime
import json
import sys
import os

sys.path.append(str(os.path.join(os.path.dirname(__file__), '..')))
from connection.psql_client import PSQLClient
from urllib.parse import quote_plus
from pymongo import MongoClient

ONE_TABLE_FILENAME = "one_table_results.txt"
MULTI_TABLE_FILENAME = "multi_table_results.txt"
MONGO_DB_FILENAME = "mongodb_results.txt"

TEST_DIR = "test_cases"
NUMBER_OF_EXECUTIONS = 3
OUTPUT_DIR = "database_results"


load_dotenv(override=True)
db_client = PSQLClient()
mongo_client = MongoClient(
    f"mongodb://{quote_plus(os.getenv('MONGO_USER', ''))}" +
    f":{quote_plus(os.getenv('MONGO_PASSWORD', ''))}" +
    f"@{quote_plus(os.getenv('MONGO_HOST', ''))}:" + 
    f"{quote_plus(os.getenv('MONGO_PORT', ''))}/"
)


def main () -> None:
    print("Database Tests Beginning!")
    print("...")
    try:
        for execution_number in range(NUMBER_OF_EXECUTIONS):
            print("Execution", execution_number + 1)
            execute_tests()
    finally:
        mongo_client.close()
        

def execute_tests() -> None:
    """
    Test scrips. For databases, it will run EXPLAIN ANALYZE or .explain() queries.
    The scripts are ran and saved to a text file.

    We first create a directory for the tests based on the time this function begins.

    Then we create the files we will write to, this depends on how many tests we are running.

    For the current execution, there will be three tests ran every time. These tests run
    through all the test cases located in the TEST_DIR constant.

    The query output of the analyze queries is combined and then saved onto a master text file.
    """
    read_time = str(datetime.now()).replace(" ", "_")
    output_path = OUTPUT_DIR + "/" + read_time
    os.makedirs(output_path, exist_ok=True)

    one_table_path = output_path + "/" + ONE_TABLE_FILENAME
    multi_table_path = output_path + "/" + MULTI_TABLE_FILENAME
    mongo_collection_path = output_path + "/" + MONGO_DB_FILENAME

    with open(one_table_path, 'w') as one_out, \
         open(multi_table_path, 'w') as multi_out, \
         open(mongo_collection_path, 'w') as mongo_out:
        
        for filename in os.listdir(TEST_DIR):
            filepath = os.path.join(TEST_DIR, filename)

            if not os.path.isfile(filepath):
                raise ValueError(f"Invalid path name found while iterating inside the files of {TEST_DIR}")

            print(f"Reading {filename}...")

            one_out.write('='*80 + '\n')
            one_out.write(f"TEST_NAME: {filename}\n")
            
            multi_out.write('='*80 + '\n')
            multi_out.write(f"TEST_NAME: {filename}\n")

            mongo_out.write('='*80 + '\n')
            mongo_out.write(f"TEST_NAME: {filename}\n")
            
            cases = read_test_case(filepath)
            print("Runnings tests on:", cases)
            print()

            for idx, case in enumerate(cases):
                print("Case:", case)
                read_and_write_case(one_out, 'One Table', idx, case, run_one_table_explain)
                read_and_write_case(multi_out, 'Multi Table', idx, case, run_multi_table_explain)
                read_and_write_case(mongo_out, 'Mongo NoSQL', idx, case, run_mongo_col_explain)


def read_and_write_case(writer, name:str, index: int, test_case: str, func:callable) -> None:
    """
    Controller function:
        Run the query and format the results nicely, passed into the io streamer to write.
    """
    print(f"Running {name.title()} Tests")
    writer.write('='*80 + '\n')
    writer.write(f"TEST_CASE_NUM: {index + 1}\n")
    writer.write('='*80 + '\n')
    writer.write(func(test_case))
    writer.write('\n')


def run_mongo_col_explain(factor_str:str) -> str:
    """
    Runs test query on mongo DB, returns the executionStats parameter
    """
    factors = [int(factor) for factor in factor_str.split(',')]
    result = mongo_client[os.getenv('DATABASE', '')]['carmichael_number']\
        .find({"factors": {"$all": factors}}).explain()

    return json.dumps(result, indent=2, default=str)
    

def run_multi_table_explain(factor_str:str) -> str:
    """
    Run the EXPLAIN ANALYZE for multi-table.
    The size of the string matters here.
    
    To save time processing we will count the
    number of commas in the string.
    So the number of factors is always number of commas + 1.
    
    Remember, the search starts at three, so before 3, 
    we don't really care!
    """
    prime_count = max(3, factor_str.count(',') + 1)

    query = "EXPLAIN ANALYZE"
    for i in range(prime_count, 14):
        query += f"""
            SELECT number FROM carmichael_number_{i} WHERE factors @> ARRAY[{factor_str}]::BIGINT[]
            UNION ALL
        """
    query += f"""
    SELECT number FROM carmichael_number_14 WHERE factors @> ARRAY[{factor_str}]::BIGINT[]
    """

    return db_client.execute_query(query)


def run_one_table_explain(factor_str:str) -> str:
    """
    Run the EXPLAIN ANALYZE query for the one table.
    The values passed in should be a either a comma
    separated list of numbers, or one number.
    """
    query = f"""
        EXPLAIN ANALYZE
        SELECT number
        FROM carmichael_number
        WHERE factors @> ARRAY[{factor_str}]::BIGINT[];
    """

    return db_client.execute_query(query)


def read_test_case(file_path:str) -> list[str]:
    """
    Read the data from the first test case. Return a 1d array.
    The first file does not include the CN in the test,
    but every other file does, so the skip boolean is used here
    to omit the first number if required.
    """
    if not file_path or not file_path.endswith('.txt'):
        raise ValueError("Please pass in a real path of a text file for the test case.")
    
    first_file = file_path.endswith('1_primes.txt')
    cases = []

    with open(file_path) as f:
        for line in f.readlines():
            if first_file:
                cases.append(line.strip())
            else:
                cases.append(', '.join(line.split(" ")[1:]).strip())
        
    return cases


if __name__ == "__main__":
    main()