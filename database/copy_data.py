import psycopg2

from decimal import Decimal
from io import StringIO

import os
from dotenv import load_dotenv

# Constants
FILENAME = "carmichael_numbers.txt"         # Must be in your .env file
BATCH_SIZE = 1000000                        # Commit every 1 million rows

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


    load_dotenv(override=True)

    with psycopg2.connect(
        host=os.getenv('HOST'),
        database=os.getenv("DATABASE"),
        user=os.getenv('PQ_USER'),
        password=os.getenv('PQ_USER_PASSWORD', ''),
        port=os.getenv('PQ_PORT')
    ) as conn:
        with conn.cursor() as cur:

            # Get the max value
            cur.execute("SELECT MAX(number) FROM carmichael_number")
            numb_qr = cur.fetchall()[0]
            last_inserted = numb_qr[0] if numb_qr[0] is not None else 0
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
                    
                    # Insert this batch
                    cur.copy_expert(
                        "COPY carmichael_number (number, factors) FROM STDIN",
                        buffer
                    )
                    
                    conn.commit()
                    total_inserted += batch_count
                    
                    print(f"Batch {batch_num} complete: {batch_count} rows (Total: {total_inserted})")
                    
                    # If we got fewer rows than batch size, we're done
                    if batch_count < (BATCH_SIZE):
                        print(f"\nImport complete! Total inserted: {total_inserted}")
                        break
        
    cur.close()
    conn.close()


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