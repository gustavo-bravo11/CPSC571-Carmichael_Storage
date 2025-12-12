import subprocess
from decimal import Decimal
from io import StringIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Constants
FILENAME = os.getenv('FILE_LOCATION', '')   # Must be in your .env file
BATCH_SIZE = 1000000                        # Commit every 1 million rows

def run_psql_query(query, input_data=None):
    """
    Execute a SQL query using psql command-line tool.
    Returns the output as a string.
    """
    # Build connection string
    host = os.getenv('HOST')
    database = os.getenv('DATABASE')
    user = os.getenv('PQ_USER')
    password = os.getenv('PQ_USER_PASSWORD', '')
    port = os.getenv('PQ_PORT')

    # Build psql command
    cmd = [
        'psql',
        '-h', host,
        '-U', user,
        '-d', database,
        '-p', port,
        '-t',  # Tuples only (no headers)
        '-A',  # Unaligned output
        '-c', query
    ]

    # Set password as environment variable
    env = os.environ.copy()
    if password:
        env['PGPASSWORD'] = password

    # Run the command
    result = subprocess.run(
        cmd,
        input=input_data,
        capture_output=True,
        text=True,
        env=env
    )

    if result.returncode != 0:
        raise Exception(f"psql command failed: {result.stderr}")

    return result.stdout.strip()

def insert_batch(data):
    """
    Insert batch data using COPY command via psql.
    Data should be tab-separated values ready for COPY FROM STDIN.
    """
    # Build connection parameters
    host = os.getenv('HOST')
    database = os.getenv('DATABASE')
    user = os.getenv('PQ_USER')
    password = os.getenv('PQ_USER_PASSWORD', '')
    port = os.getenv('PQ_PORT')

    # Build psql command for COPY
    cmd = [
        'psql',
        '-h', host,
        '-U', user,
        '-d', database,
        '-p', port,
        '-c', 'COPY carmichael_number (number, factors) FROM STDIN'
    ]

    # Set password as environment variable
    env = os.environ.copy()
    if password:
        env['PGPASSWORD'] = password

    # Run the command with data piped to stdin
    result = subprocess.run(
        cmd,
        input=data,
        capture_output=True,
        text=True,
        env=env
    )

    if result.returncode != 0:
        raise Exception(f"COPY command failed: {result.stderr}")

def main():
    """
        Insert data using batch processing!
        First query the database to find the starting point based on
        the batch size.
    """
    if FILENAME == '':
        raise ValueError(
            ("Please have a valid .env file and have the file containining ") +
            ("the carmichael numbers in the correct format.")
        )

    # Get the max value from database
    max_result = run_psql_query("SELECT MAX(number) FROM carmichael_number")

    # If query returns empty or null, set the value to 0 and skip the processing step
    last_inserted = Decimal(max_result) if max_result and max_result != '' else 0
    processing = last_inserted != 0

    batch_num = 0
    total_inserted = 0

    print(f"Beginning at carmichael numbers greater than {last_inserted}")
    if processing:
        print("Skipping...")

    # Skips rows already inserted inside get_batch (linearly)
    # File marker (f) maintains our spot after each batch
    with open(FILENAME, 'r', encoding='utf-8') as f:
        while True:
            batch_num += 1

            print(f"\nBatch {batch_num}: Reading up to {BATCH_SIZE} rows...")

            # Get batch data as StringIO buffer
            buffer, batch_count = get_batch(f, last_inserted, processing)

            # If no rows were read, we're done
            if batch_count == 0:
                print(f"\nImport complete!")
                break

            # Insert this batch using COPY command via psql
            insert_batch(buffer.getvalue())

            total_inserted += batch_count

            print(f"Batch {batch_num} complete: {batch_count} rows (Total: {total_inserted})")

            # If we got fewer rows than batch size, we're done
            if batch_count < (BATCH_SIZE):
                print(f"\nImport complete! Total inserted: {total_inserted}")
                break


def get_batch(file_handle, last_inserted, processing):
    """Read a batch of rows and return as StringIO buffer"""
    buffer = StringIO()
    batch_count = 0
    
    for line in file_handle:
        parts = line.strip().split()
        if not parts:
            continue
        
        cm_number = parts[0].strip()
        
        # Skip already processed
        if processing:
            if Decimal(cm_number) <= Decimal(last_inserted):
                continue
            else:
                processing = False
        
        factors = parts[1:]
        factors_psql = '{' + ','.join(factors) + '}'
        
        # Writes to STDIN, where copy reads from
        buffer.write(f"{cm_number}\t{factors_psql}\n")
        
        batch_count += 1
        
        # Stop after batch size
        if batch_count >= (BATCH_SIZE):
            break
    
    # IO pointer moves as you write new data to it, reset it
    buffer.seek(0)
    
    return buffer, batch_count

if __name__ == "__main__":
    main()