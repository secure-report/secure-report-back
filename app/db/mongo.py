# ARCHIVO: secure-report-back/app/db/mongo.py

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from app.core.config import settings
from bson.objectid import ObjectId
from datetime import datetime

try:
    client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ Conectado a MongoDB Atlas")
except ServerSelectionTimeoutError as e:
    print("❌ No se pudo conectar a MongoDB Atlas")
    print(f"Error: {e}")
    raise

db = client[settings.MONGODB_DB_NAME]
users_collection = db["users"]

users_collection.create_index("email", unique=True)

def get_user_by_email(email: str):
    """Obtiene usuario por email"""
    return users_collection.find_one({"email": email})

def create_user(nombre, apellido, fecha_nacimiento, direccion, email, hashed_password):
    user_data = {
        "nombre": nombre,
        "apellido": apellido,
        "fecha_nacimiento": fecha_nacimiento,
        "direccion": direccion,
        "email": email,
        "password": hashed_password,
        "role": "admin",  # ← AGREGAR ESTO
        "created_at": datetime.utcnow()
    }
    result = users_collection.insert_one(user_data)
    return str(result.inserted_id)

def get_user_by_id(user_id: str):
    """Obtiene usuario por ObjectId"""
    try:
        return users_collection.find_one({"_id": ObjectId(user_id)})
    except:
        return None

def close_connection():
    """Cierra conexión a MongoDB"""
    client.close()