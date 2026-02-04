# ARCHIVO: secure-report-back/app/models/report.py

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
from enum import Enum


class ReportCategory(str, Enum):
    """Categorías de reportes"""
    ACOSO = "acoso"
    PRECIOS_ABUSIVOS = "precios_abusivos"
    MALA_ATENCION = "mala_atencion"
    PRODUCTOS_DEFECTUOSOS = "productos_defectuosos"
    PUBLICIDAD_ENGANOSA = "publicidad_enganosa"
    FALTA_HIGIENE = "falta_higiene"
    OTROS = "otros"


class ReportStatus(str, Enum):
    """Estados del reporte"""
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    RESOLVED = "resolved"


class LocationPoint(BaseModel):
    """Modelo para coordenadas GeoJSON"""
    type: Literal["Point"] = "Point"
    coordinates: List[float] = Field(..., description="[longitud, latitud]")


class MediaItem(BaseModel):
    """Modelo para archivos multimedia"""
    type: Literal["image", "video"]
    url: str


class ReportBase(BaseModel):
    """Modelo base de reporte"""
    anonymousUserId: str
    category: ReportCategory
    description: str = Field(..., min_length=10, max_length=1000)
    location: LocationPoint
    addressReference: str = Field(..., min_length=5, max_length=200)
    media: Optional[List[MediaItem]] = []


class ReportCreate(ReportBase):
    """Modelo para crear un reporte (request)"""
    pass


class ReportUpdate(BaseModel):
    """Modelo para actualizar un reporte"""
    category: Optional[ReportCategory] = None
    description: Optional[str] = Field(None, min_length=10, max_length=1000)
    location: Optional[LocationPoint] = None
    addressReference: Optional[str] = Field(None, min_length=5, max_length=200)
    media: Optional[List[MediaItem]] = None
    status: Optional[ReportStatus] = None


class ReportInDB(ReportBase):
    """Modelo de reporte en base de datos"""
    id: str = Field(..., alias="_id")
    anonymousUserId: str
    status: ReportStatus = ReportStatus.PENDING
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "rep_98a21f",
                "anonymousUserId": "anon_7f93a2c1",
                "category": "acoso",
                "description": "Persona del establecimiento realizó comentarios y gestos de naturaleza sexual y/o intimidatoria hacia el denunciante.",
                "location": {
                    "type": "Point",
                    "coordinates": [-78.4678, -0.1807]
                },
                "addressReference": "Sector La Mariscal, Quito",
                "media": [
                    {
                        "type": "image",
                        "url": "https://cdn.app.com/reports/rep_98a21f/img1.jpg"
                    }
                ],
                "status": "pending",
                "createdAt": "2026-01-19T18:45:00Z",
                "updatedAt": "2026-01-19T18:45:00Z"
            }
        }


class ReportResponse(BaseModel):
    """Modelo de respuesta de reporte"""
    id: str = Field(..., alias="_id")
    anonymousUserId: str
    category: ReportCategory
    description: str
    location: LocationPoint
    addressReference: str
    media: List[MediaItem]
    status: ReportStatus
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True
