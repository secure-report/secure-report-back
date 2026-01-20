# Documentación de Endpoints - Media (Subida de Archivos)

## 1. Subir un Archivo (Imagen o Video)

### Postman
```
POST http://localhost:5000/api/media/upload
```

**Headers:**
- (No agregar Content-Type, Postman lo configura automáticamente)

**Body:**
- Tipo: `form-data`
- Key: `file`
- Type: `File`
- Value: Seleccionar archivo (imagen o video)

**Tipos de archivo permitidos:**
- Imágenes: jpg, jpeg, png, gif, webp
- Videos: mp4, mov, avi, wmv

---

### cURL (Git Bash / Terminal)

**Subir imagen:**
```bash
curl -X POST http://localhost:5000/api/media/upload \
  -F "file=@/c/Users/TuUsuario/Pictures/imagen.jpg"
```

**Subir video:**
```bash
curl -X POST http://localhost:5000/api/media/upload \
  -F "file=@/c/Users/TuUsuario/Videos/video.mp4"
```

**Ruta relativa (desde directorio actual):**
```bash
curl -X POST http://localhost:5000/api/media/upload \
  -F "file=@./mi-imagen.jpg"
```

---

### Respuesta Exitosa
```json
{
  "success": true,
  "type": "image",
  "url": "https://res.cloudinary.com/dupo3axec/image/upload/v1234567/secure-report/filename.jpg",
  "public_id": "secure-report/filename",
  "format": "jpg",
  "size": 123456
}
```

---

## 2. Subir Múltiples Archivos

### Postman
```
POST http://localhost:5000/api/media/upload/multiple
```

**Body:**
- Tipo: `form-data`
- Key: `files` (repetir para cada archivo)
- Type: `File`
- Value: Seleccionar archivo 1
- Key: `files`
- Type: `File`
- Value: Seleccionar archivo 2
- ... (hasta 10 archivos)

---

### cURL (Git Bash / Terminal)

```bash
curl -X POST http://localhost:5000/api/media/upload/multiple \
  -F "files=@/c/Users/TuUsuario/Pictures/imagen1.jpg" \
  -F "files=@/c/Users/TuUsuario/Pictures/imagen2.png" \
  -F "files=@/c/Users/TuUsuario/Videos/video.mp4"
```

---

### Respuesta Exitosa
```json
{
  "success": true,
  "uploaded": 3,
  "failed": 0,
  "results": [
    {
      "filename": "imagen1.jpg",
      "type": "image",
      "url": "https://res.cloudinary.com/dupo3axec/image/upload/v123/secure-report/imagen1.jpg"
    },
    {
      "filename": "imagen2.png",
      "type": "image",
      "url": "https://res.cloudinary.com/dupo3axec/image/upload/v124/secure-report/imagen2.png"
    },
    {
      "filename": "video.mp4",
      "type": "video",
      "url": "https://res.cloudinary.com/dupo3axec/video/upload/v125/secure-report/video.mp4"
    }
  ],
  "errors": null
}
```

---

## Notas Importantes

- **Tamaño máximo:** Depende de la configuración de Cloudinary
- **Máximo de archivos:** 10 archivos por request en el endpoint múltiple
- **URL resultante:** Usar la URL de la respuesta en el campo `media` al crear reportes
- **Carpeta en Cloudinary:** Todos los archivos se guardan en `secure-report/`
