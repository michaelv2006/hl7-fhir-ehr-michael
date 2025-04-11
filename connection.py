from pymongo import MongoClient
from pymongo.server_api import ServerApi


def connect_to_mongodb(db_name, collection_name):
    uri = "mongodb+srv://michaelvargas122006:ifmer2025@ifmer.bos2u.mongodb.net/?retryWrites=true&w=majority&appName=ifmer"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[db_name]
    collection = db[collection_name]
    return collection
