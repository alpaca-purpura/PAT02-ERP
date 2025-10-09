# PATCO AI Agent with RAG

**Versión:** 18.0.1.0.0  
**Categoría:** Artificial Intelligence  
**Autor:** PATCO  
**Licencia:** LGPL-3  

## 📋 Descripción

Módulo de **Asistente IA conversacional** integrado con capacidades **RAG (Retrieval-Augmented Generation)** para guiar técnicos de campo durante servicios, con generación automática de reportes técnicos.

### Características Principales

- 🤖 **Conversaciones IA** integradas nativamente con órdenes FSM
- 📚 **Base de conocimiento vectorial** con búsqueda semántica
- 📄 **Generación automática** de reportes técnicos
- 💬 **Integración nativa** con discuss.channel de Odoo
- 🔍 **Soporte múltiples tipos** de documentos técnicos
- 🎯 **Filtrado contextual** por equipos y servicios

## 🏗️ Arquitectura

### Modelos Principales

#### `ai.conversation`
Gestiona conversaciones entre técnicos y el asistente IA.

**Campos principales:**
- `fsm_order_id`: Orden FSM asociada
- `technician_id`: Técnico asignado
- `channel_id`: Canal de conversación en discuss
- `state`: Estado de la conversación (iniciado, en progreso, completado)
- `context_data`: Contexto JSON para el agente IA
- `report_generated`: Indica si se generó reporte automático

**Estados de conversación:**
1. `initiated` - Conversación iniciada
2. `equipment_selected` - Equipo seleccionado
3. `checklist_entry` - Checklist de entrada
4. `work_in_progress` - Trabajo en progreso
5. `checklist_exit` - Checklist de salida
6. `report_generated` - Reporte generado
7. `completed` - Completado
8. `archived` - Archivado

#### Extensión `ir.attachment` (RAG)
Extiende adjuntos con capacidades de búsqueda semántica.

**Campos RAG:**
- `x_document_type`: Tipo de documento (manual, procedimiento, checklist, etc.)
- `x_is_indexed`: Indica si está indexado para RAG
- `x_embedding`: Vector embedding del contenido
- `x_equipment_category_ids`: Categorías de equipos relacionadas
- `x_service_nature_ids`: Naturalezas de servicio relacionadas
- `x_keywords`: Palabras clave para búsqueda

#### Extensión `fsm.order` (IA)
Integra órdenes FSM con el asistente IA.

**Campos IA:**
- `x_ai_enabled`: IA habilitada para esta orden
- `x_ai_conversation_id`: Conversación IA asociada
- `x_ai_status`: Estado del asistente IA
- `x_ai_auto_start`: Inicio automático al asignar técnico

## 🚀 Funcionalidades

### Para Técnicos de Campo
- **Guía conversacional** durante todo el servicio
- **Acceso instantáneo** a manuales y procedimientos
- **Checklists dinámicos** según tipo de equipo
- **Generación automática** de reportes técnicos

### Para Administradores
- **Gestión de base de conocimiento** con indexación automática
- **Estadísticas de uso** del asistente IA
- **Configuración de tipos** de documentos
- **Control de permisos** granular

### Tipos de Documentos Soportados
- 📖 **Manuales Técnicos**: Documentación detallada de equipos
- 📝 **Procedimientos**: Pasos para tareas específicas
- ✅ **Listas de Verificación**: Checklists para servicios
- 📊 **Especificaciones**: Datos técnicos y especificaciones
- 🔧 **Diagramas**: Esquemas y diagramas técnicos
- 📷 **Imágenes Técnicas**: Fotos de referencia
- 🎥 **Videos Instructivos**: Contenido multimedia

## 📦 Instalación

### Dependencias
- `base` - Módulo base de Odoo
- `mail` - Sistema de mensajería
- `discuss` - Chat y conversaciones
- `patco_suite` - Suite completa PATCO

### Dependencias Python
```txt
requests
numpy
psycopg2-binary
```

### Pasos de Instalación

1. **Copiar módulo** a `extra-addons/patco_ai_agent/`
2. **Actualizar lista** de módulos en Odoo
3. **Instalar** el módulo desde Apps
4. **Configurar permisos** de usuario según roles

## ⚙️ Configuración

### Parámetros del Sistema

Acceder a **Configuración > Técnico > Parámetros > Parámetros del Sistema**:

- `patco_ai_agent.ai_enabled`: Habilitar IA globalmente
- `patco_ai_agent.ai_auto_start_default`: Inicio automático por defecto
- `patco_ai_agent.indexing_batch_size`: Tamaño de lote para indexación
- `patco_ai_agent.similarity_threshold`: Umbral de similitud RAG (0.7)
- `patco_ai_agent.max_search_results`: Máximo resultados de búsqueda

### Grupos de Seguridad

#### Usuario IA (`group_ai_user`)
- Usar conversaciones IA
- Acceder a base de conocimiento
- Ver documentos indexados

#### Administrador IA (`group_ai_manager`)
- Gestionar todas las conversaciones
- Configurar sistema IA
- Ver estadísticas completas

#### Administrador Base de Conocimiento (`group_knowledge_manager`)
- Gestionar documentos RAG
- Configurar indexación
- Administrar tipos de documentos

## 🎯 Uso

### Crear Conversación IA

1. **Automático**: Al asignar técnico a orden FSM
2. **Manual**: Botón "Iniciar IA" en orden FSM
3. **Programático**: Método `create_service_conversation()`

### Indexar Documentos para RAG

1. **Subir documento** en Adjuntos
2. **Clasificar tipo** de documento
3. **Asociar con categorías** de equipos
4. **Hacer clic** en "Indexar para RAG"

### Flujo de Conversación

```
Orden FSM creada
    ↓
Técnico asignado
    ↓
Conversación IA iniciada automáticamente
    ↓
Canal discuss creado
    ↓
Mensaje inicial del asistente
    ↓
Conversación guiada con acceso RAG
    ↓
Generación automática de reporte
    ↓
Conversación completada
```

## 🔌 API Endpoints

### Webhooks para Integración IA

- `POST /ai/webhook/message` - Recibir mensajes del agente IA
- `POST /ai/webhook/user_message` - Enviar mensajes del usuario
- `GET /ai/conversation/<id>/status` - Estado de conversación
- `POST /ai/conversation/get_active` - Obtener conversación activa
- `POST /ai/conversation/create` - Crear nueva conversación
- `POST /ai/conversation/history` - Historial de mensajes
- `GET /ai/health` - Estado de salud del módulo

### Ejemplo de Uso

```python
# Crear conversación para orden FSM
conversation = env['ai.conversation'].create_service_conversation(fsm_order)

# Iniciar conversación
conversation.action_start_conversation()

# Buscar documentos similares
results = env['ir.attachment'].search_similar(
    query="calibración termostato",
    context={'equipment_category_ids': [1, 2]},
    limit=5
)
```

## 📊 Vistas y Menús

### Menús Principales
- **Asistente IA** > **Conversaciones** > Todas las Conversaciones
- **Asistente IA** > **Base de Conocimiento** > Documentos RAG
- **Asistente IA** > **Órdenes FSM** > Con IA Activa
- **Asistente IA** > **Configuración** > Estadísticas

### Vistas Disponibles
- **Kanban**: Vista de tarjetas por estado
- **Lista**: Vista tabular con filtros
- **Formulario**: Vista detallada de conversación
- **Búsqueda**: Filtros avanzados y agrupaciones

## 🔄 Integración con PATCO Suite

### Módulos Relacionados
- **patco_fsm**: Órdenes de servicio de campo
- **patco_equipment**: Gestión de equipos y categorías
- **patco_base**: Naturalezas y áreas de servicio

### Flujo de Datos
```
patco_fsm.order → ai.conversation → discuss.channel
     ↓                    ↓              ↓
patco_equipment    ir.attachment    mail.message
```

## 🚧 Fase de Desarrollo

**Estado Actual:** Fase 1 - Módulo Base Completado

### ✅ Implementado
- Modelo `ai.conversation` con estados completos
- Extensión `ir.attachment` para capacidades RAG
- Extensión `fsm.order` para integración IA
- Vistas completas (kanban, lista, formulario)
- Sistema de permisos y seguridad
- Webhooks básicos para integración
- Datos iniciales y configuración

### 🔄 Próximas Fases
- **Fase 2**: Extensión PostgreSQL + PGVector
- **Fase 3**: Indexador de documentos con Gemini
- **Fase 4**: Servidor MCP para conectividad
- **Fase 5**: LangGraph para orquestación conversacional

## 🐛 Solución de Problemas

### Problemas Comunes

**Error: Conversación no se crea automáticamente**
- Verificar que `x_ai_enabled = True` en la orden FSM
- Verificar que `x_ai_auto_start = True`
- Verificar que el técnico tiene usuario asignado

**Error: Documentos no se indexan**
- Verificar tipo MIME soportado
- Verificar que el documento tiene contenido
- Revisar logs de indexación en `x_indexing_error`

**Error: Incorrect padding en base64**
- Verificar que el contenido del adjunto es válido
- El sistema ahora maneja automáticamente contenido no base64
- Revisar logs para advertencias de contenido no válido
- Usar método `_compute_content_hash` mejorado con validación

**Error: Permisos insuficientes**
- Verificar grupos de seguridad asignados
- Revisar reglas de registro (`ir.rule`)
- Verificar permisos en `ir.model.access.csv`

### Logs y Debugging

Los logs del módulo se registran con el prefijo `patco_ai_agent`:

```python
import logging
_logger = logging.getLogger(__name__)
_logger.info("Mensaje informativo")
_logger.error("Mensaje de error")
```

## 📞 Soporte

Para soporte técnico y consultas:
- **Email**: soporte@patco.com.pe
- **Documentación**: Menú Asistente IA > Configuración
- **Logs**: Configuración > Técnico > Logging

## 🔄 Changelog

### v18.0.1.0.1 (Septiembre 2025)
- 🐛 **Corrección crítica**: Manejo robusto de errores base64 en `_compute_content_hash`
- 🛡️ **Mejora de estabilidad**: Validación de contenido base64 antes de decodificación
- 📝 **Logging mejorado**: Advertencias detalladas para contenido no válido
- ✅ **Compatibilidad**: Fallback para contenido que no es base64 válido

### v18.0.1.0.0 (Enero 2025)
- ✨ Implementación inicial del módulo base
- 🤖 Modelo `ai.conversation` con estados completos
- 📚 Extensión RAG para `ir.attachment`
- 🔧 Integración con órdenes FSM
- 🎨 Vistas completas (kanban, lista, formulario)
- 🔒 Sistema de permisos y seguridad
- 🌐 Webhooks para integración con servicios IA
- 📊 Datos iniciales y configuración base