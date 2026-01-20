# ARCHIVO: secure-report-back/app/routers/media.py

from fastapi import APIRouter, File, UploadFile, HTTPException, status
from typing import List
import cloudinary
import cloudinary.uploader
from app.core.config import settings

router = APIRouter()

# Configurar Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_media(file: UploadFile = File(...)):
    """
    Sube una imagen o video a Cloudinary y retorna la URL
    
    - **file**: Archivo de imagen (jpg, png, gif) o video (mp4, mov, avi)
    """
    
    # Validar tipo de archivo
    allowed_types = {
        # Imágenes
        "image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp",
        # Videos
        "video/mp4", "video/quicktime", "video/x-msvideo", "video/x-ms-wmv"
    }
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no permitido. Tipos válidos: imágenes (jpg, png, gif, webp) o videos (mp4, mov, avi, wmv)"
        )
    
    try:
        # Determinar el tipo de recurso
        resource_type = "video" if file.content_type.startswith("video/") else "image"
        
        # Leer el archivo
        contents = await file.read()
        
        # Subir a Cloudinary
        upload_result = cloudinary.uploader.upload(
            contents,
            resource_type=resource_type,
            folder="secure-report",  # Carpeta en Cloudinary
            use_filename=True,
            unique_filename=True
        )
        
        return {
            "success": True,
            "type": resource_type,
            "url": upload_result["secure_url"],
            "public_id": upload_result["public_id"],
            "format": upload_result["format"],
            "size": upload_result["bytes"]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir el archivo: {str(e)}"
        )


@router.post("/upload/multiple", status_code=status.HTTP_201_CREATED)
async def upload_multiple_media(files: List[UploadFile] = File(...)):
    """
    Sube múltiples imágenes o videos a Cloudinary
    
    - **files**: Lista de archivos (máximo 10)
    """
    
    if len(files) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Máximo 10 archivos por solicitud"
        )
    
    results = []
    errors = []
    
    for file in files:
        try:
            # Validar tipo de archivo
            allowed_types = {
                "image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp",
                "video/mp4", "video/quicktime", "video/x-msvideo", "video/x-ms-wmv"
            }
            
            if file.content_type not in allowed_types:
                errors.append({
                    "filename": file.filename,
                    "error": "Tipo de archivo no permitido"
                })
                continue
            
            # Determinar el tipo de recurso
            resource_type = "video" if file.content_type.startswith("video/") else "image"
            
            # Leer el archivo
            contents = await file.read()
            
            # Subir a Cloudinary
            upload_result = cloudinary.uploader.upload(
                contents,
                resource_type=resource_type,
                folder="secure-report",
                use_filename=True,
                unique_filename=True
            )
            
            results.append({
                "filename": file.filename,
                "type": resource_type,
                "url": upload_result["secure_url"]
            })
        
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "success": len(errors) == 0,
        "uploaded": len(results),
        "failed": len(errors),
        "results": results,
        "errors": errors if errors else None
    }
