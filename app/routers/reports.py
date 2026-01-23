# ARCHIVO: secure-report-back/app/routers/reports.py

from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.report import ReportCreate, ReportResponse
from app.db.mongo import create_report, get_reports_by_user, get_all_reports
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_new_report(request: ReportCreate):
    """Crea un nuevo reporte"""
    
    try:
        report_id = create_report(
            anonymous_user_id=request.anonymousUserId,
            category=request.category,
            description=request.description,
            location=request.location.model_dump(),
            address_reference=request.addressReference,
            media=[m.model_dump() for m in request.media] if request.media else []
        )
        
        report = get_report_by_id(report_id)
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al recuperar el reporte creado"
            )
        
        return format_report_response(report)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el reporte: {str(e)}"
        )


@router.get("/user/{anonymous_user_id}", response_model=List[ReportResponse])
async def list_user_reports(anonymous_user_id: str):
    """Lista todos los reportes de un usuario anónimo"""
    
    try:
        reports = get_reports_by_user(anonymous_user_id)
        return [format_report_response(report) for report in reports]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los reportes: {str(e)}"
        )


def format_report_response(report: dict) -> dict:
    """Formatea un reporte de MongoDB para la respuesta"""
    return {
        "_id": str(report["_id"]),
        "anonymousUserId": report["anonymousUserId"],
        "category": report["category"],
        "description": report["description"],
        "location": report["location"],
        "addressReference": report["addressReference"],
        "media": report.get("media", []),
        "status": report["status"],
        "createdAt": report["createdAt"],
        "updatedAt": report["updatedAt"]
    }


@router.get("/", response_model=List[ReportResponse])
async def list_all_reports():
    """Lista todos los reportes sin filtro"""
    try:
        reports = get_all_reports()
        return [format_report_response(report) for report in reports]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los reportes: {str(e)}"
        )


def get_report_by_id(report_id: str):
    """Obtiene un reporte por ID - importado desde mongo.py"""
    from app.db.mongo import get_report_by_id as mongo_get_report
    return mongo_get_report(report_id)


@router.get("/{report_id}", response_model=ReportResponse)
async def retrieve_report(report_id: str):
    """Obtiene un reporte por su ID"""
    try:
        report = get_report_by_id(report_id)

        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reporte no encontrado"
            )

        return format_report_response(report)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el reporte: {str(e)}"
        )
