# Documentación de Endpoints - Reports (Reportes)

## 1. Crear un Reporte

### Postman
```
POST http://localhost:5000/api/reports/
```

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "anonymousUserId": "anon_7f93a2c1",
  "category": "precios_abusivos",
  "description": "El local cobra valores diferentes a los exhibidos en la percha.",
  "location": {
    "type": "Point",
    "coordinates": [-78.4678, -0.1807]
  },
  "addressReference": "Sector La Mariscal, Quito",
  "media": [
    {
      "type": "image",
      "url": "https://res.cloudinary.com/dupo3axec/image/upload/v123/secure-report/img1.jpg"
    },
    {
      "type": "video",
      "url": "https://res.cloudinary.com/dupo3axec/video/upload/v124/secure-report/video1.mp4"
    }
  ]
}
```

---

### cURL (Git Bash / Terminal)

**Con media:**
```bash
curl -X POST http://localhost:5000/api/reports/ \
  -H "Content-Type: application/json" \
  -d '{
    "anonymousUserId": "anon_7f93a2c1",
    "category": "precios_abusivos",
    "description": "El local cobra valores diferentes a los exhibidos en la percha.",
    "location": {
      "type": "Point",
      "coordinates": [-78.4678, -0.1807]
    },
    "addressReference": "Sector La Mariscal, Quito",
    "media": [
      {
        "type": "image",
        "url": "https://res.cloudinary.com/dupo3axec/image/upload/v123/secure-report/img1.jpg"
      }
    ]
  }'
```

**Sin media (ejemplo mínimo):**
```bash
curl -X POST http://localhost:5000/api/reports/ \
  -H "Content-Type: application/json" \
  -d '{
    "anonymousUserId": "anon_123456",
    "category": "mala_atencion",
    "description": "El personal fue muy descortés y grosero con los clientes en el establecimiento.",
    "location": {
      "type": "Point",
      "coordinates": [-78.5, -0.2]
    },
    "addressReference": "Centro Comercial El Recreo, Quito",
    "media": []
  }'
```

---

### Respuesta Exitosa
```json
{
  "_id": "rep_98a21f",
  "anonymousUserId": "anon_7f93a2c1",
  "category": "precios_abusivos",
  "description": "El local cobra valores diferentes a los exhibidos en la percha.",
  "location": {
    "type": "Point",
    "coordinates": [-78.4678, -0.1807]
  },
  "addressReference": "Sector La Mariscal, Quito",
  "media": [
    {
      "type": "image",
      "url": "https://res.cloudinary.com/dupo3axec/image/upload/v123/secure-report/img1.jpg"
    }
  ],
  "status": "pending",
  "createdAt": "2026-01-20T01:45:00.000Z",
  "updatedAt": "2026-01-20T01:45:00.000Z"
}
```

---

## 2. Listar Reportes de un Usuario Anónimo

### Postman
```
GET http://localhost:5000/api/reports/user/anon_7f93a2c1
```

**Headers:**
- No requiere headers especiales

**Path Parameters:**
- `anonymous_user_id`: ID del usuario anónimo (ej: `anon_7f93a2c1`)

---

### cURL (Git Bash / Terminal)

```bash
curl -X GET http://localhost:5000/api/reports/user/anon_7f93a2c1
```

**Otro usuario:**
```bash
curl -X GET http://localhost:5000/api/reports/user/anon_123456
```

---

### Respuesta Exitosa
```json
[
  {
    "_id": "rep_98a21f",
    "anonymousUserId": "anon_7f93a2c1",
    "category": "precios_abusivos",
    "description": "El local cobra valores diferentes a los exhibidos en la percha.",
    "location": {
      "type": "Point",
      "coordinates": [-78.4678, -0.1807]
    },
    "addressReference": "Sector La Mariscal, Quito",
    "media": [
      {
        "type": "image",
        "url": "https://res.cloudinary.com/dupo3axec/image/upload/v123/secure-report/img1.jpg"
      }
    ],
    "status": "pending",
    "createdAt": "2026-01-20T01:45:00.000Z",
    "updatedAt": "2026-01-20T01:45:00.000Z"
  },
  {
    "_id": "rep_a1b2c3",
    "anonymousUserId": "anon_7f93a2c1",
    "category": "mala_atencion",
    "description": "Personal descortés.",
    "location": {
      "type": "Point",
      "coordinates": [-78.5, -0.2]
    },
    "addressReference": "Centro Comercial",
    "media": [],
    "status": "pending",
    "createdAt": "2026-01-19T18:30:00.000Z",
    "updatedAt": "2026-01-19T18:30:00.000Z"
  }
]
```

**Respuesta sin reportes:**
```json
[]
```

---

## Categorías Válidas

- `precios_abusivos` - Precios abusivos
- `mala_atencion` - Mala atención
- `productos_defectuosos` - Productos defectuosos
- `publicidad_enganosa` - Publicidad engañosa
- `falta_higiene` - Falta de higiene
- `otros` - Otros

---

## Estados de Reporte

- `pending` - Pendiente (por defecto al crear)
- `in_review` - En revisión
- `approved` - Aprobado
- `rejected` - Rechazado
- `resolved` - Resuelto

---

## Validaciones

### Description
- Mínimo: 10 caracteres
- Máximo: 1000 caracteres

### AddressReference
- Mínimo: 5 caracteres
- Máximo: 200 caracteres

### Location
- Tipo: Debe ser "Point"
- Coordinates: Array de 2 números [longitud, latitud]
  - Longitud: -180 a 180
  - Latitud: -90 a 90

### Media
- Opcional (puede ser array vacío)
- Cada item debe tener:
  - `type`: "image" o "video"
  - `url`: URL válida (generalmente de Cloudinary)

---

## Flujo Completo

1. **Subir archivos multimedia** (si hay fotos/videos):
   ```bash
   POST /api/media/upload
   ```
   Guardar las URLs retornadas

2. **Crear reporte** con las URLs obtenidas:
   ```bash
   POST /api/reports/
   ```

3. **Consultar reportes** del usuario:
   ```bash
   GET /api/reports/user/{anonymousUserId}
   ```
