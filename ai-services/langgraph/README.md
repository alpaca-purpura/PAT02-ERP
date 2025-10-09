# 🤖 LangGraph Service - PATCO IA

Servicio de orquestación de conversaciones IA usando LangGraph para el sistema PATCO.

## 📋 Descripción

Este servicio implementa la lógica de conversación del asistente IA PATCO utilizando LangGraph para orquestar el flujo de interacciones entre técnicos de campo y el sistema de IA durante servicios técnicos.

## 🏗️ Arquitectura

### Componentes Principales

- **LangGraph Workflow**: Orquestador principal de conversaciones
- **Nodos Especializados**: Cada fase del servicio técnico
- **Integración RAG**: Búsqueda inteligente en base de conocimiento
- **Generación de Reportes**: Creación automática de documentos técnicos

### Nodos del Grafo

1. **conversation_dispatcher**: Despacho inteligente de conversaciones
2. **equipment_selector**: Selección de equipos para servicio
3. **checklist_manager**: Gestión de listas de verificación
4. **knowledge_retriever**: Búsqueda RAG en manuales técnicos
5. **report_generator**: Generación automática de reportes con OnlyOffice

## 🔧 Funcionalidades

### Fase 8: Generación de Reportes con OnlyOffice

#### Características
- **Extracción Inteligente**: Análisis automático de conversaciones con Gemini
- **Plantillas Dinámicas**: Diferentes tipos según naturaleza del servicio
- **OnlyOffice Integration**: Generación de documentos DOCX profesionales
- **Almacenamiento en Odoo**: Integración completa con sistema ERP
- **Sistema de Fallback**: Generación de reportes de texto en caso de error

#### Tipos de Plantillas Disponibles
- `servicio_general`: Reporte estándar de servicio
- `mantenimiento_preventivo`: Reporte de mantenimiento preventivo
- `mantenimiento_correctivo`: Reporte de mantenimiento correctivo
- `instalacion_equipo`: Reporte de instalación de equipos
- `calibracion_tecnica`: Reporte de calibración técnica
- `inspeccion_tecnica`: Reporte de inspección técnica

#### Flujo de Generación
```
Conversación Completada
    ↓
Extracción de Información Estructurada (Gemini)
    ↓
Selección de Plantilla según Tipo de Servicio
    ↓
Generación de Script OnlyOffice Document Builder
    ↓
Llamada a API OnlyOffice Document Server
    ↓
Almacenamiento en Odoo (ir.attachment)
    ↓
Actualización de Orden FSM
    ↓
Notificación al Usuario
```

## 🚀 Instalación y Configuración

### Variables de Entorno

```bash
# Configuración de Gemini
GEMINI_API_KEY=your_gemini_api_key

# Configuración de OnlyOffice
ONLYOFFICE_SERVER_URL=http://onlyoffice-documentserver:80
ONLYOFFICE_JWT_SECRET=patco-onlyoffice-jwt-secret-2025

# Configuración de MCP
MCP_SERVER_URL=http://mcp-server:8080

# Configuración de LangGraph
LANGGRAPH_SERVER_PORT=8001
```

### Dependencias

```bash
pip install -r requirements.txt
```

#### requirements.txt
```
langgraph>=0.0.40
langchain>=0.1.0
google-generativeai>=0.3.0
requests>=2.31.0
pyjwt>=2.8.0
fastapi>=0.104.0
uvicorn>=0.24.0
python-multipart>=0.0.6
```

### Ejecución

```bash
# Desarrollo
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Producción con Docker
docker compose up langgraph-server
```

## 📁 Estructura del Proyecto

```
ai-services/langgraph/
├── main.py                     # Servidor FastAPI principal
├── workflow/
│   ├── __init__.py
│   ├── conversation_graph.py   # Definición del grafo LangGraph
│   └── state.py               # Estados de conversación
├── nodes/
│   ├── __init__.py
│   ├── conversation_dispatcher.py
│   ├── equipment_selector.py
│   ├── checklist_manager.py
│   ├── knowledge_retriever.py
│   └── report_generator.py    # 🆕 Generación de reportes
├── templates/
│   ├── __init__.py
│   └── report_templates.js    # 🆕 Plantillas OnlyOffice
├── utils/
│   ├── __init__.py
│   ├── gemini_client.py
│   ├── mcp_client.py
│   └── onlyoffice_client.py   # 🆕 Cliente OnlyOffice
├── config/
│   ├── __init__.py
│   └── settings.py
├── tests/
│   ├── __init__.py
│   ├── test_nodes.py
│   └── test_report_generation.py  # 🆕 Tests de reportes
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## 🔄 API Endpoints

### Conversaciones
- `POST /conversation/start` - Iniciar nueva conversación
- `POST /conversation/{id}/message` - Enviar mensaje
- `GET /conversation/{id}/status` - Estado de conversación
- `POST /conversation/{id}/generate_report` - 🆕 Generar reporte

### Reportes
- `POST /reports/generate` - 🆕 Generar reporte desde conversación
- `GET /reports/{id}/status` - 🆕 Estado de generación de reporte
- `GET /reports/templates` - 🆕 Listar plantillas disponibles

### Salud del Sistema
- `GET /health` - Estado del servicio
- `GET /health/onlyoffice` - 🆕 Estado del servidor OnlyOffice

## 📊 Monitoreo y Logs

### Estructura de Logs
```json
{
  "timestamp": "2025-01-27T10:30:00Z",
  "level": "INFO",
  "service": "langgraph",
  "node": "report_generator",
  "conversation_id": "conv_123",
  "message": "Reporte generado exitosamente",
  "metadata": {
    "template_type": "mantenimiento_preventivo",
    "filename": "Reporte_Servicio_FSM001_20250127_1030.docx",
    "attachment_id": 456
  }
}
```

### Métricas Clave
- Tiempo de generación de reportes
- Tasa de éxito de OnlyOffice API
- Uso de plantillas por tipo de servicio
- Errores de extracción de información

## 🧪 Testing

### Ejecutar Tests
```bash
# Tests unitarios
python -m pytest tests/ -v

# Tests específicos de reportes
python -m pytest tests/test_report_generation.py -v

# Tests de integración con OnlyOffice
python -m pytest tests/test_onlyoffice_integration.py -v
```

### Tests de Reportes
```python
# Ejemplo de test
def test_report_generation():
    conversation_data = {
        "messages": [...],
        "context": {...}
    }
    
    result = await generate_report(conversation_data)
    
    assert result["report_generated"] == True
    assert result["report_attachment_id"] is not None
    assert result["report_filename"].endswith(".docx")
```

## 🔧 Configuración de OnlyOffice

### Docker Compose Integration
El servicio se integra con OnlyOffice Document Server configurado en el `docker-compose.yml` principal:

```yaml
services:
  onlyoffice-documentserver:
    image: onlyoffice/documentserver:latest
    ports:
      - "8081:80"
    environment:
      - JWT_ENABLED=true
      - JWT_SECRET=patco-onlyoffice-jwt-secret-2025
```

### Document Builder API
El servicio utiliza la API de OnlyOffice Document Builder para generar documentos programáticamente:

```javascript
// Ejemplo de script generado
builder.CreateFile("docx");
var oDocument = Api.GetDocument();
// ... lógica de generación de documento
builder.SaveFile("docx", "reporte.docx");
builder.CloseFile();
```

## 🚨 Troubleshooting

### Problemas Comunes

#### Error de Conexión con OnlyOffice
```bash
# Verificar estado del servidor
curl http://localhost:8081/healthcheck

# Revisar logs del contenedor
docker logs onlyoffice-documentserver
```

#### Error de JWT en OnlyOffice
```python
# Verificar configuración de JWT
import jwt
token = jwt.encode(payload, "patco-onlyoffice-jwt-secret-2025", algorithm="HS256")
```

#### Error de Extracción con Gemini
```python
# Verificar API key
import google.generativeai as genai
genai.configure(api_key="your_api_key")
```

## 📈 Roadmap

### Próximas Funcionalidades
- [ ] Plantillas personalizables por cliente
- [ ] Generación de reportes en múltiples formatos (PDF, HTML)
- [ ] Integración con firma digital
- [ ] Reportes con imágenes y diagramas
- [ ] Analytics de reportes generados
- [ ] Plantillas con campos dinámicos avanzados

### Mejoras Técnicas
- [ ] Cache de plantillas compiladas
- [ ] Pool de conexiones OnlyOffice
- [ ] Retry automático con backoff exponencial
- [ ] Compresión de documentos generados
- [ ] Validación de esquemas de datos extraídos

## 🤝 Contribución

### Agregar Nueva Plantilla
1. Definir plantilla en `templates/report_templates.js`
2. Implementar secciones específicas
3. Agregar tests correspondientes
4. Actualizar documentación

### Ejemplo de Nueva Plantilla
```javascript
const nueva_plantilla = {
    name: "Reporte de Nueva Funcionalidad",
    sections: ["header", "custom_section", "footer"],
    styles: {
        title_color: [255, 0, 0],
        title_size: 18,
        section_size: 14,
        body_size: 11
    }
};
```

## 📞 Soporte

Para soporte técnico o consultas sobre la generación de reportes:
- 📧 Email: soporte@patco.pe
- 📱 WhatsApp: +51 999 999 999
- 🐛 Issues: GitHub Issues del proyecto

---

**PATCO IA - Transformando el servicio técnico con inteligencia artificial** 🚀