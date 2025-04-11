from pymongo import MongoClient
from pymongo.server_api import ServerApi

def connect_to_mongodb(db_name, collection_name):
    uri = "mongodb+srv://michaelvargas122006:ifmer2025@ifmer.bos2u.mongodb.net/?retryWrites=true&w=majority&appName=ifmer"
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        db = client[db_name]
        collection = db[collection_name]
        
        # Prueba la conexión listando las colecciones
        print("✅ Conexión a MongoDB establecida correctamente")
        print("📂 Bases de datos disponibles:", client.list_database_names())
        print("📄 Colecciones en la BD:", db.list_collection_names())
        
        return collection
    except Exception as e:
        print("❌ Error al conectar con MongoDB:", str(e))
        return None
