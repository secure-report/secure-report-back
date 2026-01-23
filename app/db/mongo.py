# ARCHIVO: secure-report-back/app/db/mongo.py

from pymongo import MongoClient, ReturnDocument
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
reports_collection = db["reports"]

users_collection.create_index("email", unique=True)
reports_collection.create_index("anonymousUserId")

def get_user_by_email(email: str):
    """Obtiene usuario por email"""
    return users_collection.find_one({"email": email})

def create_user(nombre: str, apellido: str, fecha_nacimiento: str, 
                direccion: str, email: str, hashed_password: str) -> str:
    """Crea nuevo usuario y retorna su ID"""
    user_data = {
        "nombre": nombre,
        "apellido": apellido,
        "fecha_nacimiento": fecha_nacimiento,
        "direccion": direccion,
        "email": email,
        "password": hashed_password,
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


# ===== FUNCIONES PARA REPORTES =====

def generate_report_id() -> str:
    """Genera un ID único para el reporte"""
    import secrets
    return f"rep_{secrets.token_hex(3)}"


def create_report(anonymous_user_id: str, category: str, description: str,
                 location: dict, address_reference: str, media: list) -> str:
    """Crea un nuevo reporte y retorna su ID"""
    report_id = generate_report_id()
    now = datetime.utcnow()
    
    report_data = {
        "_id": report_id,
        "anonymousUserId": anonymous_user_id,
        "category": category,
        "description": description,
        "location": location,
        "addressReference": address_reference,
        "media": media,
        "status": "pending",
        "createdAt": now,
        "updatedAt": now
    }
    
    reports_collection.insert_one(report_data)
    return report_id


def get_report_by_id(report_id: str):
    """Obtiene un reporte por ID"""
    return reports_collection.find_one({"_id": report_id})


def get_reports_by_user(anonymous_user_id: str):
    """Obtiene todos los reportes de un usuario anónimo"""
    return list(reports_collection.find({"anonymousUserId": anonymous_user_id}).sort("createdAt", -1))


def get_all_reports():
    """Obtiene todos los reportes sin filtro, ordenados por fecha de creación descendente"""
    return list(reports_collection.find({}).sort("createdAt", -1))


def update_report_status(report_id: str, status: str):
    """Actualiza el estado de un reporte y retorna el documento actualizado."""
    try:
        now = datetime.utcnow()
        updated = reports_collection.find_one_and_update(
            {"_id": report_id},
            {"$set": {"status": status, "updatedAt": now}},
            return_document=ReturnDocument.AFTER
        )
        return updated
    except Exception:
        return None


def close_connection():
    """Cierra conexión a MongoDB"""
    client.close()