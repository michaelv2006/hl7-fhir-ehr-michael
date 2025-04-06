import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi
 
# Función para conectar a la base de datos MongoDB
def connect_to_mongodb(uri, db_name, collection_name):
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[db_name]
    collection = db[collection_name]
    return collection
 
# Función para guardar el JSON en MongoDB
def save_patient_to_mongodb(patient_json, collection):
    try:
        # Convertir el JSON string a un diccionario de Pyt
