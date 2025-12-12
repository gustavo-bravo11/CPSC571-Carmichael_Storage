"""
File to insert data into mongoDB database.

This file will
1) Connect to the MongoDB server for thomas.butler.edu.
2) Create the relation of carmichael_number.
3) Convert the text data into a JSON format.
4) Insert the data into the carmichael_number database.
5) Adds an index to the factor array for querying efficiency.

@author Gustavo Bravo
@date December 11, 2025
"""
import urllib.parse
import os

from dotenv import load_dotenv
from pymongo import MongoClient
from bson import Decimal128


load_dotenv(override=True)

FILENAME = os.getenv('FILE_LOCATION', '')
CHECKPOINT = 1000000

def insert_data():
    user = urllib.parse.quote_plus(os.getenv('MONGO_USER', ''))
    password = urllib.parse.quote_plus(os.getenv('MONGO_PASSWORD', ''))
    host = urllib.parse.quote_plus(os.getenv('MONGO_HOST', ''))
    port = urllib.parse.quote_plus(os.getenv('MONGO_PORT', '8000'))

    uri = f"mongodb://{user}:{password}@{host}:{port}/"

    db_name = os.getenv('DATABASE', '')
    if not db_name:
        raise ValueError("Provide a non-empty db name.")
    
    row_count = 0

    # Context manager handles closing if failure
    with MongoClient(uri) as client:
        db = client[db_name]

        # Enforce a schema for our new collection
        cn_collection = db.create_collection(
            "carmichael_number", 
            validator={
                    "_id": {"$type": "decimal"},
                    "factors": {"$type": "array"}
            },
            validationLevel="strict"
        )

        with open(FILENAME, encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(' ')

                cn_collection.insert_one({
                    "_id": Decimal128(parts[0].strip()),
                    "factors": [int(factor.strip()) for factor in parts[1:]]
                })

                row_count += 1
                if row_count % CHECKPOINT == 0:
                    print(f"Inserted {row_count/CHECKPOINT} million rows.")
        
        # Create an index on factors in ascending order (default)
        cn_collection.create_index("factors")


if __name__ == "__main__":
    insert_data()