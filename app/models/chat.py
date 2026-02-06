from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    respuesta: str

class UploadResponse(BaseModel):
    document_id: str
    file_name: str
    mensaje: str