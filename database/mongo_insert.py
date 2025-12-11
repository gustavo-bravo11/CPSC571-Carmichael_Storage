"""
File to insert data into mongoDB database.

This file will
1) Connect to the MongoDB server for thomas.butler.edu.
2) Create the relation of carmichael_number.
3) Convert the text data into a JSON format.
4) Insert the data into the carmichael_number database.
5) Adds an index to the factor array for querying efficiency.
"""
import urllib.parse
import os

from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv(override=True)

FILENAME = os.getenv('FILE_LOCATION', '')

def insert_data():
    user = urllib.parse.quote_plus(os.getenv('MONGO_USER', ''))
    password = urllib.parse.quote_plus(os.getenv('MONGO_PASSWORD', ''))
    uri = f"mongodb://{user}:{password}@localhost:27017/"

    db_name = os.getenv('DATABASE', '')
    if not db_name:
        raise ValueError("Provide a non-empty db name.")

    # Context manager handles closing if failure
    with MongoClient(uri) as client:
        with open(FILENAME, encoding='utf-8') as file:
            db = client[db_name]
            cn_collection = db['carmichael_number']

            for line in file:
                parts = line.strip().split(' ')

                cn_collection.insert_one({
                    "number": parts[0].strip(),
                    "factors": [factor for factor in parts[1:]]
                })
        
        # Create an index on factors in ascending order (default)
        cn_collection.create_index("factors")




if __name__ == "__main__":
    insert_data()