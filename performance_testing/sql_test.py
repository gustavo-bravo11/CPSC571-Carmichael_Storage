from dotenv import load_dotenv
import sys
import os

sys.path.append(str(os.path.join(os.path.dirname(__file__), '..')))
from connection.psql_client import PSQLClient


OUTPUT_PATH = "results/"        # Append the filename to this
load_dotenv(override=True)
db_client = PSQLClient()

def main() -> None:
    """
    Test scrips. For SQL databases, it will run EXPLAIN ANALYZE queries.
    The scripts are ran and saved to a text file.

    The output results will be hardcoded inside this file.
    """

    primes_1 = read_test_1('test_cases/1_primes.txt')
    run_one_table_explain(primes_1[-1])


def run_one_table_explain(factor_list:int|list[int]) -> str:
    """
    Run the EXPLAIN ANALYZE query for the one table.
    If it's one element, we assume we are only doing one test,
    if it's a list, then we check multiple values.

    Returns False if query failed to execute
    """

    if isinstance(factor_list, list):
        factor_str = ','.join(map(str, factor_list))
    else:
        factor_str = str(factor_list)

    query = f"""
        EXPLAIN ANALYZE
        SELECT number
        FROM carmichael_number
        WHERE factors @> ARRAY[{factor_str}]::BIGINT[];
    """

    return db_client.execute_query(query)

def read_test_1(file_path:str) -> list[int]:
    """
    Read the data from the first test case. Return a 1d array.
    """
    if not file_path or not file_path.endswith('.txt'):
        raise ValueError("Please pass in a real path of a text file for the test case.")
    
    primes = []
    with open(file_path) as f:
        for line in f.readlines():
            primes.append(int(line.strip()))

    return primes


if __name__ == "__main__":
    main()