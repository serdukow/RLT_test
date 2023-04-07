import os
from pymongo import MongoClient

from dotenv import load_dotenv


def connect_to_mongodb():
    load_dotenv()
    db_conn = os.getenv('DB_CONN')
    client = MongoClient(db_conn, tlsAllowInvalidCertificates=True)
    db = client['salary']
    collection = db['sample_collection']
    return collection