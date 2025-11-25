from dotenv import load_dotenv
from datetime import datetime
import sys
import os

sys.path.append(str(os.path.join(os.path.dirname(__file__), '..')))
from connection.psql_client import PSQLClient

ONE_TABLE_FILENAME = "one_table_results.txt"
MULTI_TABLE_FILENAME = "multi_table_results.txt"
TEST_DIR = "test_cases"
NUMBER_OF_EXECUTIONS = 3

load_dotenv(override=True)
db_client = PSQLClient()


def main () -> None:
    print("Database Tests Beginning!")
    print("...")
    for execution_number in range(NUMBER_OF_EXECUTIONS):
        print("Execution", execution_number + 1)
        execute_tests()


def execute_tests() -> None:
    """
    Test scrips. For SQL databases, it will run EXPLAIN ANALYZE queries.
    The scripts are ran and saved to a text file.

    We first create a directory for the tests based on the time this function begins.

    Then we create the files we will write to, this depends on how many tests we are running.

    For the current execution, there will be two tests ran every time. These tests run
    through all the test cases located in the TEST_DIR constant.

    The query output of the analyze queries is combined and then saved onto a master text file.
    """
    read_time = str(datetime.now()).replace(" ", "_")
    output_path = "results/" + read_time
    os.makedirs(output_path, exist_ok=True)

    one_table_path = output_path + "/" + ONE_TABLE_FILENAME
    multi_table_path = output_path + "/" + MULTI_TABLE_FILENAME

    with open(one_table_path, 'w') as one_out, open(multi_table_path, 'w') as multi_out:
        for filename in os.listdir(TEST_DIR):
            filepath = os.path.join(TEST_DIR, filename)

            if not os.path.isfile(filepath):
                raise ValueError(f"Invalid path name found while iterating inside the files of {TEST_DIR}")

            print(f"Reading {filename}...")
            one_out.write(f"TEST_NAME: {filename}\n")
            multi_out.write(f"TEST_NAME: {filename}\n")
            
            cases = read_test_case(filepath)
            print("Runnings tests on:", cases)
            print()

            for idx, case in enumerate(cases):
                print("Case:", case)
                read_and_write_case(one_out, 'One Table', idx, case)
                read_and_write_case(multi_out, 'Multi Table', idx, case)


def read_and_write_case(writer, name:str, index: int, test_case: str) -> None:
    """
    Controller function:
        Run the query and format the results nicely, passed into the io streamer to write.
    """
    print(f"Running {name.title()} Tests")
    writer.write('='*80 + '\n')
    writer.write(f"TEST_CASE_NUM: {index + 1}\n")
    writer.write('='*80 + '\n')
    writer.write(run_one_table_explain(test_case))
    writer.write('\n')


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
    
    Returns False if query failed to execute
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