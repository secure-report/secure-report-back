from fastapi import APIRouter, UploadFile, File, HTTPException, Header, status
from urllib.parse import unquote
from uuid import uuid4
from datetime import datetime
import time
import fitz
import google.generativeai as genai
from app.core.config import settings
from app.db.mongo import db
from app.models.chat import ChatRequest, ChatResponse, UploadResponse

router = APIRouter()

# Configurar Google AI
genai.configure(api_key=settings.GOOGLE_API_KEY)

SALUDO_INICIAL = "Hola, soy ChatSeguro. Estoy acá para escucharte y ayudarte con lo que necesites. Todo lo que me digas es privado y seguro. ¿En qué puedo apoyarte?"

PROMPT_INICIAL = """
Eres ChatSeguro, una asistente de confianza que ayuda a personas en Ecuador que enfrentan situaciones difíciles.

TU OBJETIVO:
- Escuchar sin juzgar
- Dar información clara y práctica
- Generar confianza y seguridad
- Empoderar a la persona para que tome decisiones

COMO HABLAR:
- Habla como un amigo cercano que entiende - cálido, cercano, sin formalismos
- Usa "tú" y "yo" - es conversación, no clase
- Si alguien comparte algo difícil (violencia, miedo), muestra empatía PRIMERO
- Valida sus sentimientos: "Entiendo que tengas miedo", "Es totalmente válido lo que sientes"
- Después ayuda con opciones prácticas

QUE EVITAR:
- NO digas "los documentos dicen..." o "según la información..."
- NO suenes robótico ni formal
- NO repitas mucho la misma respuesta
- NO minimices lo que la persona dice
- NO prometas cosas que no puedes cumplir

INFORMACION DISPONIBLE (usa esta como referencia, pero no la menciones):
La información incluye: números de emergencia en Ecuador, derechos del consumidor, cómo denunciar, consejos de seguridad, información sobre justicia y salud mental.

ESTRUCTURA DE RESPUESTA:
1. Si comparten algo difícil → EMPATIA primero
2. Valida su experiencia
3. Da información útil si aplica (sin decir "según los documentos")
4. Ofrece opciones o siguientes pasos
5. Pregunta si necesita más ayuda

RECUERDA:
- La persona merece sentirse segura
- Tu tono determina si confía o no
- Una buena respuesta hace que se sienta menos sola
- Responde natural, como si chalearas con alguien de confianza
"""

def limpiar_respuesta(texto):
    """Limpia la respuesta del modelo de formatos innecesarios"""
    texto = texto.replace("**", "").replace("*", "")
    texto = texto.replace("##", "").replace("#", "")
    lineas = texto.split("\n")
    lineas_limpias = []
    for linea in lineas:
        linea = linea.strip()
        if linea.startswith("-") or linea.startswith("*"):
            linea = linea[1:].strip()
        lineas_limpias.append(linea)
    texto = "\n".join(lineas_limpias)
    while "\n\n\n" in texto:
        texto = texto.replace("\n\n\n", "\n\n")
    return texto.strip()

def save_message(document_id, role, content):
    """Guarda un mensaje en el historial"""
    db.chat_history.insert_one({
        "document_id": document_id,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    })

def get_history(document_id, limit=5):
    """Obtiene el historial reciente"""
    history = list(
        db.chat_history.find(
            {"document_id": document_id},
            {"_id": 0, "role": 1, "content": 1}
        ).sort("timestamp", -1).limit(limit)
    )
    return history[::-1]

@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...), x_admin_key: str = Header(...)):
    """
    Sube un PDF y lo almacena en MongoDB
    
    Requiere header: `x-admin-key` con la clave de admin
    """
    
    # Validar autenticación
    if x_admin_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Clave de admin inválida"
        )
    
    try:
        inicio = time.time()
        
        # Leer y procesar PDF
        stream = file.file.read()
        pdf_doc = fitz.open(stream=stream, filetype="pdf")
        text = "".join(page.get_text() for page in pdf_doc)
        
        # Generar ID
        document_id = str(uuid4())
        file_name = unquote(file.filename)
        
        # Guardar documento
        db.documents.insert_one({
            "document_id": document_id,
            "file_name": file_name,
            "content": text,
            "uploaded_at": datetime.utcnow()
        })
        
        # Guardar saludo inicial
        save_message(document_id, "assistant", SALUDO_INICIAL)
        
        tiempo = round(time.time() - inicio, 2)
        
        return {
            "document_id": document_id,
            "file_name": file_name,
            "mensaje": "Documento cargado exitosamente"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el PDF: {str(e)}"
        )

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Envía un mensaje - busca la respuesta en TODOS los PDFs cargados
    """
    
    try:
        inicio = time.time()
        
        # ✅ Busca TODOS los documentos
        all_docs = list(db.documents.find({}, {"content": 1}))
        
        if not all_docs:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay documentos cargados"
            )
        
        # ✅ Concatena todo el contenido de todos los PDFs
        context_text = "\n\n---NUEVO DOCUMENTO---\n\n".join([d["content"] for d in all_docs])
        
        # Historial con ID genérico para chat global
        history = get_history("global_chat")
        formatted_history = "\n".join(f"{m['role']}: {m['content']}" for m in history)

        prompt = f"""
{PROMPT_INICIAL}

INFORMACION DE REFERENCIA DISPONIBLE:
{context_text}

HISTORIAL DE CONVERSACION:
{formatted_history}

PREGUNTA/COMENTARIO DEL USUARIO:
{req.message}

Responde de forma natural, empática y conversacional. Usa la información disponible para ayudar, pero no menciones que viene de "documentos".
"""
        
        # Generar respuesta
        model = genai.GenerativeModel(settings.GOOGLE_MODEL)
        response = model.generate_content(prompt)
        answer = limpiar_respuesta(response.text)
        
        # Guardar en historial global
        save_message("global_chat", "user", req.message)
        save_message("global_chat", "assistant", answer)
        
        tiempo = round(time.time() - inicio, 2)
        
        return {"respuesta": answer}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en el chat: {str(e)}"
        )