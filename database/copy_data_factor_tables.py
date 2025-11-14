import psycopg2

from decimal import Decimal
from io import StringIO

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Constants
FILENAME = os.getenv('FILE_LOCATION', '')   # Must be in your .env file
BATCH_SIZE = 1000000                        # Commit every 1 million rows

def main():
    """
        Insert data using batch processing!
        First query the database to find the starting point based on
        the batch size. Data is distributed to tables carmichael_number_3
        through carmichael_number_14 based on the number of factors.
    """
    if FILENAME == '':
        raise ValueError(
            ("Please have a valid .env file and have the file containining ") +
            ("the carmichael numbers in the correct format.")
        )

    with psycopg2.connect(
        host=os.getenv('HOST'),
        database=os.getenv('DATABASE'),
        user=os.getenv('PQ_USER'),
        password=os.getenv('PQ_USER_PASSWORD', ''),
        port=os.getenv('PQ_PORT')
    ) as conn:
        with conn.cursor() as cur:

            # Get the max value from all tables and keep the largest
            last_inserted = 0
            for num_factors in range(3, 15):
                table_name = f"carmichael_number_{num_factors}"
                cur.execute(f"SELECT MAX(number) FROM {table_name}")
                numb_qr = cur.fetchall()[0]
                max_val = numb_qr[0] if numb_qr[0] is not None else 0
                if max_val > last_inserted:
                    last_inserted = max_val

            processing = last_inserted != 0

            batch_num = 0
            total_inserted = {i: 0 for i in range(3, 15)}  # Track inserts per table

            print(f"Beginning at carmichael numbers greater than {last_inserted}")
            if processing:
                print("Skipping...")

            # Skips rows already inserted inside get_batch (linearly)
            # File marker (f) maintains our spot after each batch
            with open(FILENAME, 'r', encoding='utf-8') as f:
                while True:
                    batch_num += 1

                    print(f"\nBatch {batch_num}: Reading up to {BATCH_SIZE} rows...")

                    # Get batch data as dictionary of StringIO buffers (one per table)
                    buffers, batch_counts = get_batch(f, last_inserted, processing)

                    # If no rows were read, we're done
                    if sum(batch_counts.values()) == 0:
                        print(f"\nImport complete!")
                        break

                    # Insert batches for each table
                    for num_factors in range(3, 15):
                        if batch_counts[num_factors] > 0:
                            table_name = f"carmichael_number_{num_factors}"
                            cur.copy_expert(
                                f"COPY {table_name} (number, factors) FROM STDIN",
                                buffers[num_factors]
                            )
                            total_inserted[num_factors] += batch_counts[num_factors]

                    conn.commit()

                    # Print batch summary
                    batch_total = sum(batch_counts.values())
                    print(f"Batch {batch_num} complete: {batch_total} rows")
                    for num_factors in range(3, 15):
                        if batch_counts[num_factors] > 0:
                            print(f"  - {num_factors} factors: {batch_counts[num_factors]} rows (Total: {total_inserted[num_factors]})")

                    # If we got fewer rows than batch size, we're done
                    if batch_total < BATCH_SIZE:
                        print(f"\nImport complete!")
                        print("Final totals:")
                        for num_factors in range(3, 15):
                            if total_inserted[num_factors] > 0:
                                print(f"  - carmichael_number_{num_factors}: {total_inserted[num_factors]} rows")
                        break

    cur.close()


def get_batch(file_handle, last_inserted, processing):
    """Read a batch of rows and return as dictionary of StringIO buffers"""
    buffers = {i: StringIO() for i in range(3, 15)}
    batch_counts = {i: 0 for i in range(3, 15)}
    total_batch_count = 0

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
        num_factors = len(factors)

        # Only process if number of factors is between 3 and 14 (inclusive)
        if not (3 <= num_factors <= 14):
            continue

        factors_psql = '{' + ','.join(factors) + '}'

        # Write to appropriate buffer based on number of factors
        buffers[num_factors].write(f"{cm_number}\t{factors_psql}\n")
        batch_counts[num_factors] += 1
        total_batch_count += 1

        # Stop after batch size
        if total_batch_count >= BATCH_SIZE:
            break

    # Reset IO pointers for all buffers
    for buffer in buffers.values():
        buffer.seek(0)

    return buffers, batch_counts

if __name__ == "__main__":
    main()
