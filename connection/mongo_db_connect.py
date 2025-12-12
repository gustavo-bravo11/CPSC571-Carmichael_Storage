import urllib.parse
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import os
from dotenv import load_dotenv


load_dotenv(override=True)

MONGO_INITDB_ROOT_USERNAME=os.getenv('MONGO_USER', '')
MONGO_INITDB_ROOT_PASSWORD=os.getenv('MONGO_PASSWORD', '')

def main():
    u = urllib.parse.quote_plus( MONGO_INITDB_ROOT_USERNAME )
    p = urllib.parse.quote_plus( MONGO_INITDB_ROOT_PASSWORD )

    uri = f"mongodb://{u}:{p}@localhost:27017/"
    client = MongoClient(uri)

    try:
        client.admin.command("ping")
        print("Connected successfully")
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
