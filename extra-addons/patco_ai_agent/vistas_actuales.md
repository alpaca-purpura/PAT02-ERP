# Vistas Actuales - Módulo PATCO AI Agent

**Versión:** 18.0.1.0.0  
**Fecha:** Enero 2025  
**Módulo:** patco_ai_agent  

## 📋 Estructura de Menús Implementados

### Menú Principal: Asistente IA

| ID del Menú | Acción | Descripción de Funcionalidad |
|-------------|--------|-------------------------------|
| `menu_ai_agent_main` | - | Menú principal del asistente IA con acceso a todas las funcionalidades |
| `menu_ai_conversations` | - | Submenú para gestión de conversaciones IA |
| `menu_ai_conversation_all` | `action_ai_conversation` | Acceso a todas las conversaciones IA del sistema |
| `menu_knowledge_base` | - | Submenú para gestión de base de conocimiento RAG |
| `menu_knowledge_base_rag` | `action_knowledge_base_rag` | Gestión de documentos indexados para RAG |
| `menu_pending_indexing` | `action_pending_indexing` | Documentos pendientes de indexación RAG |
| `menu_fsm_ai` | - | Submenú para órdenes FSM con IA |
| `menu_fsm_orders_ai_active` | `action_fsm_orders_with_ai` | Órdenes FSM con asistente IA activo |
| `menu_ai_config` | - | Submenú de configuración del sistema IA |
| `menu_ai_statistics` | `action_view_ai_statistics` | Estadísticas de uso del asistente IA |
| `menu_rag_statistics` | `action_view_rag_statistics` | Estadísticas de la base de conocimiento RAG |
| `menu_fsm_ai_conversations` | `action_ai_conversation` | Acceso directo a conversaciones IA desde configuración |

## 🎯 Acciones Definidas

### Acciones de Ventana (Window Actions)

| ID de Acción | Modelo | Vistas | Descripción |
|--------------|--------|--------|-------------|
| `action_ai_conversation` | `ai.conversation` | kanban, list, form | Gestión completa de conversaciones IA |
| `action_knowledge_base_rag` | `ir.attachment` | list, form | Base de conocimiento con documentos RAG |
| `action_pending_indexing` | `ir.attachment` | list, form | Documentos pendientes de indexación |
| `action_fsm_orders_with_ai` | `fsm.order` | kanban, list, form | Órdenes FSM con IA habilitada |
| `action_ai_channels` | `discuss.channel` | list, form | Canales de conversación IA |

### Acciones de Servidor (Server Actions)

| ID de Acción | Modelo | Método | Descripción |
|--------------|--------|--------|-------------|
| `action_view_ai_statistics` | `fsm.order` | `action_view_ai_statistics()` | Estadísticas de uso IA |
| `action_view_rag_statistics` | `ir.attachment` | `action_view_rag_stats()` | Estadísticas RAG |

## 📊 Vistas Implementadas por Modelo

### 1. Modelo: `ai.conversation` (PATCO)

#### Vistas Propias (No Heredadas)

| ID de Vista | Tipo | Propósito |
|-------------|------|-----------|
| `view_ai_conversation_form` | form | Formulario detallado de conversación IA |
| `view_ai_conversation_tree` | list | Lista tabular de conversaciones |
| `view_ai_conversation_kanban` | kanban | Vista de tarjetas agrupadas por estado |
| `view_ai_conversation_search` | search | Filtros y búsquedas avanzadas |

#### Campos Implementados

| Campo | Tipo | Origen | Descripción Funcional |
|-------|------|--------|----------------------|
| `name` | Char | PATCO | Nombre descriptivo de la conversación |
| `fsm_order_id` | Many2one | PATCO | Orden FSM asociada a la conversación |
| `technician_id` | Many2one | PATCO | Técnico asignado a la conversación |
| `channel_id` | Many2one | PATCO | Canal discuss asociado |
| `state` | Selection | PATCO | Estado actual de la conversación |
| `current_equipment_id` | Many2one | PATCO | Equipo actualmente en trabajo |
| `start_time` | Datetime | PATCO | Fecha y hora de inicio |
| `end_time` | Datetime | PATCO | Fecha y hora de finalización |
| `duration` | Float | PATCO | Duración total en horas (computado) |
| `message_count` | Integer | PATCO | Número de mensajes (computado) |
| `context_data` | Text | PATCO | Contexto JSON para el agente IA |
| `conversation_summary` | Text | PATCO | Resumen de la conversación |
| `report_generation_status` | Selection | PATCO | Estado de generación de reporte |
| `report_generated` | Boolean | PATCO | Indica si se generó reporte (computado) |

### 2. Modelo: `fsm.order` (Extensión)

#### Vistas Heredadas

| ID de Vista | Vista Base | Tipo | Propósito |
|-------------|------------|------|-----------|
| `view_fsm_order_form_ai` | `fieldservice.fsm_order_form` | form | Formulario con integración IA |
| `view_fsm_order_tree_ai` | `fieldservice.fsm_order_list_view` | list | Lista con campos IA |
| `view_fsm_order_search_ai` | `fieldservice.fsm_order_search_view` | search | Búsqueda con filtros IA |

#### Campos Agregados por PATCO

| Campo | Tipo | Origen | Descripción Funcional |
|-------|------|--------|----------------------|
| `x_ai_enabled` | Boolean | PATCO | Habilita asistente IA para esta orden |
| `x_ai_channel_id` | Many2one | PATCO | Canal discuss de IA asociado |
| `x_ai_channel_name` | Char | PATCO | Nombre del canal IA (computado) |
| `x_ai_status` | Selection | PATCO | Estado del asistente IA |
| `x_ai_auto_start` | Boolean | PATCO | Inicio automático al asignar técnico |
| `x_ai_conversation_id` | Many2one | PATCO | Conversación IA asociada (legacy) |
| `x_ai_message_count` | Integer | PATCO | Número de mensajes IA (computado) |
| `x_ai_duration` | Float | PATCO | Duración de conversación IA (computado) |

#### Campos Heredados de `fieldservice.fsm_order_form`

| Campo | Tipo | Origen | Descripción |
|-------|------|--------|-------------|
| `name` | Char | fieldservice | Número de orden de servicio |
| `stage_id` | Many2one | fieldservice | Etapa actual de la orden |
| `person_id` | Many2one | fieldservice | Técnico asignado |
| `location_id` | Many2one | fieldservice | Ubicación del servicio |
| `equipment_id` | Many2one | fieldservice | Equipo principal a atender |
| `request_early` | Datetime | fieldservice | Fecha/hora más temprana solicitada |
| `date_start` | Datetime | fieldservice | Fecha/hora de inicio real |
| `date_end` | Datetime | fieldservice | Fecha/hora de finalización |
| `description` | Text | fieldservice | Descripción del trabajo |

### 3. Modelo: `ir.attachment` (Extensión RAG)

#### Vistas Heredadas

| ID de Vista | Vista Base | Tipo | Propósito |
|-------------|------------|------|-----------|
| `view_ir_attachment_form_rag` | `base.view_attachment_form` | form | Formulario con campos RAG |
| `view_ir_attachment_tree_rag` | `base.view_attachment_tree` | list | Lista con información RAG |
| `view_ir_attachment_search_rag` | `base.view_attachment_search` | search | Búsqueda con filtros RAG |

#### Campos Agregados por PATCO (RAG)

| Campo | Tipo | Origen | Descripción Funcional |
|-------|------|--------|----------------------|
| `x_document_type` | Selection | PATCO | Tipo de documento (manual, procedimiento, etc.) |
| `x_language` | Selection | PATCO | Idioma del documento |
| `x_technical_level` | Selection | PATCO | Nivel técnico del contenido |
| `x_keywords` | Char | PATCO | Palabras clave para búsqueda |
| `x_is_indexed` | Boolean | PATCO | Estado de indexación RAG |
| `x_indexed_date` | Datetime | PATCO | Fecha de indexación |
| `x_indexing_priority` | Selection | PATCO | Prioridad de indexación |
| `x_embedding` | Binary | PATCO | Vector embedding del contenido |
| `x_embedding_model` | Char | PATCO | Modelo usado para embedding |
| `x_content_hash` | Char | PATCO | Hash SHA256 del contenido |
| `x_equipment_category_ids` | Many2many | PATCO | Categorías de equipos relacionadas |
| `x_service_nature_ids` | Many2many | PATCO | Naturalezas de servicio relacionadas |
| `x_parent_document_id` | Many2one | PATCO | Documento padre si es fragmento |
| `x_chunk_index` | Integer | PATCO | Índice del fragmento |
| `x_indexing_error` | Text | PATCO | Error de indexación si existe |

#### Campos Heredados de `base.view_attachment_form`

| Campo | Tipo | Origen | Descripción |
|-------|------|--------|-------------|
| `name` | Char | base | Nombre del archivo |
| `datas` | Binary | base | Contenido del archivo |
| `mimetype` | Char | base | Tipo MIME del archivo |
| `file_size` | Integer | base | Tamaño del archivo en bytes |
| `checksum` | Char | base | Checksum del archivo |
| `res_model` | Char | base | Modelo al que está adjunto |
| `res_id` | Integer | base | ID del registro asociado |
| `create_date` | Datetime | base | Fecha de creación |
| `create_uid` | Many2one | base | Usuario que creó el adjunto |

### 4. Modelo: `discuss.channel` (Extensión)

#### Vistas Heredadas

| ID de Vista | Vista Base | Tipo | Propósito |
|-------------|------------|------|-----------|
| `view_mail_channel_ai_form` | `mail.discuss_channel_view_form` | form | Formulario con información FSM |

#### Campos Agregados por PATCO

| Campo | Tipo | Origen | Descripción Funcional |
|-------|------|--------|----------------------|
| `fsm_order_id` | Many2one | PATCO | Orden FSM asociada (computado) |
| `technician_id` | Many2one | PATCO | Técnico del canal (computado) |
| `client_name` | Char | PATCO | Nombre del cliente (computado) |

#### Campos Heredados de `mail.discuss_channel_view_form`

| Campo | Tipo | Origen | Descripción |
|-------|------|--------|-------------|
| `name` | Char | mail | Nombre del canal |
| `description` | Text | mail | Descripción del canal |
| `channel_type` | Selection | mail | Tipo de canal |
| `channel_partner_ids` | Many2many | mail | Participantes del canal |
| `is_member` | Boolean | mail | Usuario es miembro |
| `message_ids` | One2many | mail | Mensajes del canal |

## 🔧 Funcionalidades Especiales

### Integración con discuss.channel
- **Canales IA automáticos**: Creación automática de canales para conversaciones IA
- **Participantes controlados**: Solo técnico y bot IA como participantes
- **Mensajes contextuales**: Mensajes con contexto FSM y equipos

### Sistema RAG (Retrieval-Augmented Generation)
- **Indexación automática**: Procesamiento de documentos para búsqueda semántica
- **Búsqueda híbrida**: Combinación de búsqueda semántica y por palabras clave
- **Filtrado contextual**: Resultados filtrados por categorías de equipos y servicios
- **Múltiples formatos**: Soporte para PDF, texto, imágenes, Word, etc.

### Estados de Conversación
1. **initiated** - Conversación iniciada
2. **equipment_selected** - Equipo seleccionado para trabajo
3. **checklist_entry** - Checklist de entrada completado
4. **work_in_progress** - Trabajo en progreso
5. **checklist_exit** - Checklist de salida completado
6. **report_generated** - Reporte técnico generado
7. **completed** - Conversación completada
8. **archived** - Conversación archivada

### Webhooks y API Endpoints
- **POST** `/ai/webhook/message` - Recibir mensajes del agente IA
- **POST** `/ai/webhook/user_message` - Enviar mensajes del usuario
- **GET** `/ai/conversation/<id>/status` - Estado de conversación
- **POST** `/ai/conversation/get_active` - Obtener conversación activa
- **POST** `/ai/conversation/create` - Crear nueva conversación
- **POST** `/ai/conversation/history` - Historial de mensajes
- **GET** `/ai/health` - Estado de salud del módulo

### Generación Automática de Reportes
- **Contexto completo**: Incluye información de orden, cliente, equipos y conversación
- **Plantillas dinámicas**: Adaptadas según tipo de servicio y equipos
- **Estados controlados**: Seguimiento del proceso de generación
- **Integración FSM**: Reportes vinculados automáticamente a la orden FSM

## 📈 Estadísticas y Métricas

### Estadísticas IA
- Total de conversaciones por técnico
- Duración promedio de conversaciones
- Mensajes por conversación
- Reportes generados automáticamente
- Órdenes con IA habilitada

### Estadísticas RAG
- Total de documentos en base de conocimiento
- Documentos indexados vs pendientes
- Documentos con errores de indexación
- Distribución por tipo de documento
- Porcentaje de indexación completado

## 🔒 Seguridad y Permisos

### Grupos de Seguridad
- **group_ai_user**: Usuario básico de IA
- **group_ai_manager**: Administrador de IA
- **group_knowledge_manager**: Gestor de base de conocimiento

### Reglas de Acceso
- Técnicos solo ven sus propias conversaciones
- Administradores ven todas las conversaciones
- Documentos RAG según permisos de adjuntos base
- Canales IA restringidos a participantes

---

**Nota**: Este documento refleja el estado actual del módulo patco_ai_agent v18.0.1.0.0. Para actualizaciones y cambios futuros, consultar el changelog en el README.md principal.