import urllib.parse
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


MONGO_INITDB_ROOT_USERNAME='jewebste'
MONGO_INITDB_ROOT_PASSWORD='gKxkyDja39PLZLBLjr4J'

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
