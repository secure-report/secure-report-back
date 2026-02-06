from pymongo import MongoClient, ReturnDocument
from pymongo.errors import ServerSelectionTimeoutError
from app.core.config import settings
from bson.objectid import ObjectId
from datetime import datetime
from urllib.parse import urlparse

def _mask_mongo_uri(uri: str) -> str:
    """
    Oculta usuario y password del URI para logs seguros
    """
    try:
        parsed = urlparse(uri)
        return f"{parsed.scheme}://***:***@{parsed.hostname}/{parsed.path.lstrip('/')}"
    except Exception:
        return "***"

try:
    print("> Iniciando conexión MongoDB...")
    print(f"> URI: {_mask_mongo_uri(settings.MONGODB_URI)}")
    print(f"> DB: {settings.MONGODB_DB_NAME}")

    client = MongoClient(
        settings.MONGODB_URI,
        serverSelectionTimeoutMS=5000
    )

    client.admin.command("ping")

    print("> Conexión MongoDB establecida correctamente")

except ServerSelectionTimeoutError as e:
    print("X ERROR: No se pudo conectar a MongoDB")
    print(f"Detalle: {e}")
    raise

# Base de datos activa (ÚNICA)
db = client[settings.MONGODB_DB_NAME]

# Colecciones activas
users_collection = db["users"]
reports_collection = db["reports"]

# Índices
users_collection.create_index("email", unique=True)
reports_collection.create_index("anonymousUserId")

print("> Colecciones activas: users, reports")

# ===== FUNCIONES USUARIOS =====

def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})


def create_user(nombre, apellido, fecha_nacimiento, direccion, email, hashed_password):
    user_data = {
        "nombre": nombre,
        "apellido": apellido,
        "fecha_nacimiento": fecha_nacimiento,
        "direccion": direccion,
        "email": email,
        "password": hashed_password,
        "role": "admin",
        "created_at": datetime.utcnow()
    }
    result = users_collection.insert_one(user_data)
    return str(result.inserted_id)


def get_user_by_id(user_id: str):
    try:
        return users_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None


# ===== FUNCIONES REPORTES =====


def generate_report_id() -> str:
    import secrets
    return f"rep_{secrets.token_hex(3)}"


def create_report(
    anonymous_user_id: str,
    category: str,
    description: str,
    location: dict,
    address_reference: str,
    media: list
) -> str:
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
    return reports_collection.find_one({"_id": report_id})


def get_reports_by_user(anonymous_user_id: str):
    return list(
        reports_collection
        .find({"anonymousUserId": anonymous_user_id})
        .sort("createdAt", -1)
    )


def get_all_reports():
    return list(
        reports_collection
        .find({})
        .sort("createdAt", -1)
    )


def update_report_status(report_id: str, status: str):
    try:
        now = datetime.utcnow()
        return reports_collection.find_one_and_update(
            {"_id": report_id},
            {"$set": {"status": status, "updatedAt": now}},
            return_document=ReturnDocument.AFTER
        )
    except Exception:
        return None


def close_connection():
    print("> Cerrando conexión MongoDB")
    client.close()
