# SecureReport - Backend

Sistema de reportes anónimos con chat inteligente. Permite a usuarios denunciar situaciones de acoso, abusos y otros problemas de forma segura y privada.

## Descripción

API REST construida con FastAPI que permite:
- Crear reportes anónimos con ubicación y multimedia
- Subir fotos y videos a la nube
- Chat con inteligencia artificial para orientación
- Gestión de usuarios administradores
- Seguimiento de estado de reportes

## Tecnologías

- Python 3.11
- FastAPI (API REST)
- MongoDB (Base de datos)
- Cloudinary (Almacenamiento de imágenes/videos)
- OpenAI (Chat inteligente)
- Docker (Contenedores)
- JWT (Autenticación)

## Instalación Local

### Requisitos previos
- Python 3.11 o superior
- MongoDB (local o Atlas)
- Cuenta en Cloudinary
- Cuenta en OpenAI

### Pasos

1. Clonar el repositorio
```bash
git clone https://github.com/secure-report/secure-report-back.git
cd secure-report-back
```

2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias
```bash
pip install -r app/requirements.txt
```

4. Crear archivo .env
```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-muy-larga
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=securereport
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
OPENAI_API_KEY=sk-tu-api-key
OPENAI_MODEL=gpt-4-turbo
ADMIN_API_KEY=clave-para-subir-pdfs
```

5. Ejecutar servidor
```bash
uvicorn main:app --reload --port 5000
```

La API estará disponible en: http://localhost:5000

## Endpoints Principales

### Autenticación
- POST /api/auth/register - Registrar administrador
- POST /api/auth/login - Iniciar sesión

### Reportes
- POST /api/reports/ - Crear reporte
- GET /api/reports/ - Listar todos los reportes
- GET /api/reports/user/{id} - Reportes de un usuario
- GET /api/reports/{id} - Ver reporte específico
- PATCH /api/reports/{id}/status - Cambiar estado

### Multimedia
- POST /api/media/upload - Subir archivo
- POST /api/media/upload/multiple - Subir varios archivos

### Chat
- POST /api/chat/upload - Subir PDF de información (requiere admin key)
- POST /api/chat/chat - Enviar mensaje al chat

### Utilidad
- GET /api/health - Estado del servidor
- GET / - Información básica

## Documentación Interactiva

Una vez ejecutando el servidor, visita:
- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

## Estructura del Proyecto
```
secure-report-back/
├── app/
│   ├── core/           # Configuración
│   ├── db/             # Conexión MongoDB
│   ├── models/         # Modelos de datos
│   └── routers/        # Endpoints
├── docs/               # Documentación de uso
├── main.py             # Entrada de la aplicación
├── Dockerfile          # Imagen Docker
└── docker-compose.yml  # Orquestación
```

## Deployment con Docker

### Opción 1: Docker Compose
```bash
docker-compose up -d --build
```

### Opción 2: Docker manual
```bash
docker build -t secure-report-back .
docker run -p 5000:5000 --env-file .env secure-report-back
```

## Deployment en AWS EC2

El proyecto incluye GitHub Actions para despliegue automático:
1. Configurar secrets en GitHub (EC2_HOST, EC2_USER, EC2_PRIVATE_KEY, etc.)
2. Push a la rama feat/login
3. El workflow construye y despliega automáticamente

## Categorías de Reportes

- acoso - Acoso, violencia, amenazas
- precios_abusivos - Precios excesivos
- mala_atencion - Mal servicio
- productos_defectuosos - Productos dañados
- publicidad_enganosa - Publicidad falsa
- falta_higiene - Problemas de limpieza
- otros - Otras situaciones

## Estados de Reportes

- pending - Recién creado
- in_review - En revisión
- approved - Aprobado
- rejected - Rechazado
- resolved - Resuelto

## Seguridad

- Contraseñas hasheadas con bcrypt
- Autenticación con JWT
- CORS configurado
- Variables de entorno para credenciales
- IDs anónimos para proteger identidad

## Notas Importantes

- El chat usa OpenAI GPT-4 Turbo por defecto
- Los archivos multimedia se almacenan en Cloudinary (carpeta secure-report)
- MongoDB debe tener índices creados automáticamente
- El sistema permite reportes completamente anónimos
