# ARCHIVO: secure-report-back/app/routers/auth.py

from fastapi import APIRouter, HTTPException, status
from app.models.user import RegisterRequest, LoginRequest, RegisterResponse, LoginResponse, ErrorResponse
from app.db.mongo import get_user_by_email, create_user, get_user_by_id
from app.core.config import settings
from bcrypt import hashpw, checkpw, gensalt
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

def hash_password(password: str) -> str:
    """Hashea contraseña con bcrypt"""
    return hashpw(password.encode(), gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Verifica contraseña contra hash"""
    return checkpw(password.encode(), hashed.encode())

def create_access_token(user_id: str) -> str:
    """Crea JWT token"""
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest):
    """Registra nuevo usuario"""
    
    existing_user = get_user_by_email(request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "El correo ya está registrado"}
        )
    
    hashed_password = hash_password(request.password)
    
    user_id = create_user(
        nombre=request.nombre,
        apellido=request.apellido,
        fecha_nacimiento=request.fecha_nacimiento,
        direccion=request.direccion,
        email=request.email,
        hashed_password=hashed_password
    )
    
    return {"message": "Usuario registrado correctamente"}

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login de usuario"""
    
    user = get_user_by_email(request.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Credenciales inválidas"}
        )
    
    if not verify_password(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Credenciales inválidas"}
        )
    
    token = create_access_token(str(user["_id"]))
    
    return {
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "email": user["email"],
            "nombre": user["nombre"]
        }
    }