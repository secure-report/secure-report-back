# ARCHIVO: secure-report-back/app/models/user.py

from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    fecha_nacimiento: str = Field(..., description="Formato YYYY-MM-DD")
    direccion: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    password: str = Field(..., min_length=6)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    nombre: str

class LoginResponse(BaseModel):
    token: str
    user: UserResponse

class RegisterResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    error: str