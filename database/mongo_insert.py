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
from decimal import Decimal


load_dotenv(override=True)

FILENAME = os.getenv('FILE_LOCATION', '')
CHECKPOINT = 10000

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
    batch = []

    # Context manager handles closing if failure
    with MongoClient(uri) as client:
        db = client[db_name]

        if "carmichael_number" not in db.list_collection_names():
            # Enforce a schema for our new collection
            cn_collection = db.create_collection(
                "carmichael_number", 
                validator={
                        "_id": {"$type": "decimal"},
                        "factors": {"$type": "array"}
                },
                validationLevel="strict"
            )
            max_inserted = 0
        else: # Look for checkpoint
            cn_collection = db["carmichael_number"]
            max_query = cn_collection.aggregate([
                {
                    "$group": {
                        "_id": None,
                        "max_carmichael": {"$max": "$_id"}
                    }
                }
            ]).next()
            max_inserted = Decimal(str(max_query['max_carmichael']))

        with open(FILENAME, encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(' ')

                if max_inserted >= Decimal(parts[0].strip()):
                    continue

                batch.append({
                    "_id": Decimal128(parts[0].strip()),
                    "factors": [int(factor.strip()) for factor in parts[1:]]
                })

                if len(batch) == CHECKPOINT:
                    cn_collection.insert_many(batch, ordered=False)
                    row_count += len(batch)
                    batch = []
                    print(f"Inserted {row_count} rows.")
        
        # Create an index on factors in ascending order (default)
        cn_collection.create_index("factors")


if __name__ == "__main__":
    insert_data()