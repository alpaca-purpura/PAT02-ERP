# Documentación del Modelo fsm.order - Odoo 18

## Tabla de Contenidos
1. [Información General](#información-general)
2. [Campos del Core OCA (fieldservice)](#campos-del-core-oca-fieldservice)
3. [Campos Computados](#campos-computados)
4. [Métodos Principales](#métodos-principales)
5. [Lógica de Negocio](#lógica-de-negocio)
6. [Campos Agregados por Módulos OCA](#campos-agregados-por-módulos-oca)
7. [Campos Agregados por Módulos PATCO](#campos-agregados-por-módulos-patco)

---

## Información General

El modelo `fsm.order` es el modelo central del sistema de Field Service Management (FSM) en Odoo, representando órdenes de servicio de campo. Este modelo es proporcionado por la OCA (Odoo Community Association) y es extendido por múltiples módulos para proporcionar funcionalidades avanzadas.

**Herencias:**
- `mail.thread`: Seguimiento de mensajes y actividades
- `mail.activity.mixin`: Gestión de actividades

**Archivo principal:** `extra-addons/OCA/field-service/fieldservice/models/fsm_order.py`

---

## Campos del Core OCA (fieldservice)

### Campos de Identificación y Estado
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | Char | Nombre/número de la orden de servicio |
| `stage_id` | Many2one | Etapa actual de la orden (fsm.stage) |
| `is_closed` | Boolean (related) | Indica si la orden está cerrada |
| `priority` | Selection | Prioridad: '0' (Lowest), '1' (Low), '2' (Normal), '3' (High) |
| `color` | Integer | Índice de color para vista kanban |
| `custom_color` | Char (related) | Color personalizado de la etapa |

### Campos de Clasificación
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `tag_ids` | Many2many | Etiquetas para clasificar órdenes (fsm.tag) |
| `team_id` | Many2one | Equipo de servicio responsable (fsm.team) |
| `type` | Many2one | Tipo de orden (fsm.order.type) |
| `internal_type` | Selection (related) | Tipo interno: 'fsm', 'repair' |
| `category_ids` | Many2many | Categorías de servicio (fsm.category) |

### Campos de Ubicación y Cliente
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `location_id` | Many2one | Ubicación del servicio (fsm.location) |
| `location_directions` | Char (computed) | Direcciones de la ubicación |
| `street` | Char (related) | Calle de la ubicación |
| `street2` | Char (related) | Calle 2 de la ubicación |
| `zip` | Char (related) | Código postal |
| `city` | Char (related) | Ciudad |
| `state_name` | Char (related) | Estado/provincia |
| `country_name` | Char (related) | País |
| `phone` | Char (related) | Teléfono de la ubicación |
| `mobile` | Char (related) | Móvil de la ubicación |

### Campos de Territorio y Organización
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `territory_id` | Many2one (related) | Territorio (res.territory) |
| `branch_id` | Many2one (related) | Sucursal (res.branch) |
| `district_id` | Many2one (related) | Distrito (res.district) |
| `region_id` | Many2one (related) | Región (res.region) |
| `company_id` | Many2one | Empresa responsable |

### Campos de Fechas y Programación
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `request_early` | Datetime | Fecha más temprana solicitada |
| `request_late` | Datetime | Fecha más tardía solicitada |
| `scheduled_date_start` | Datetime | Inicio programado (ETA) |
| `scheduled_date_end` | Datetime | Fin programado |
| `scheduled_duration` | Float | Duración programada en horas |
| `date_start` | Datetime | Inicio real |
| `date_end` | Datetime | Fin real |
| `duration` | Float (computed) | Duración real en horas |
| `current_date` | Datetime | Fecha actual (para referencia) |

### Campos de Asignación de Personal
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `person_id` | Many2one | Técnico asignado (fsm.person) |
| `person_ids` | Many2many | Trabajadores de servicio de campo |
| `person_phone` | Char (related) | Teléfono del técnico |

### Campos de Equipos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `equipment_id` | Many2one | Equipo principal (fsm.equipment) |
| `equipment_ids` | Many2many (computed) | Múltiples equipos |

### Campos de Trabajo y Resolución
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `description` | Text (computed) | Descripción del trabajo |
| `todo` | Text (computed) | Instrucciones de trabajo |
| `resolution` | Text | Resolución del problema |
| `sequence` | Integer | Secuencia para ordenamiento |

### Campos de Plantilla
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `template_id` | Many2one | Plantilla de servicio (fsm.template) |

### Campos Técnicos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `display_name` | Char (related) | Nombre para mostrar |
| `stage_name` | Char (related) | Nombre de la etapa |
| `is_button` | Boolean | Control interno para botones |

---

## Campos Computados

### Principales Campos Computados
- **`duration`**: Calcula la duración real basada en `date_start` y `date_end`
- **`location_directions`**: Obtiene las direcciones completas de la ubicación
- **`description`**: Genera descripción basada en equipos y notas
- **`todo`**: Obtiene instrucciones de la plantilla seleccionada
- **`equipment_ids`**: Auto-popula equipos basado en la ubicación y empresa
- **`custom_color`**: Color de la etapa para vista kanban

---

## Métodos Principales

### Métodos de Creación y Escritura
- **`create(vals_list)`**: Creación con generación automática de nombre y cálculo de fechas
- **`write(vals)`**: Escritura con validaciones de etapa y cálculo de fechas
- **`unlink()`**: Eliminación con validaciones de estado

### Métodos de Cálculo de Fechas
- **`_calc_scheduled_dates(vals)`**: Calcula fechas programadas y duración
- **`_calc_request_late(vals)`**: Calcula fecha límite basada en prioridad

### Métodos de Acciones
- **`action_complete()`**: Marca la orden como completada
- **`action_cancel()`**: Cancela la orden

### Métodos OnChange
- **`onchange_scheduled_date_end()`**: Actualiza fecha de inicio al cambiar fin
- **`onchange_scheduled_duration()`**: Actualiza fecha de fin al cambiar duración
- **`_onchange_template_id()`**: Aplica configuración de plantilla

### Métodos de Validación
- **`can_unlink()`**: Verifica si la orden puede ser eliminada
- **`check_day()`**: Valida que las fechas no caigan en días festivos

### Métodos Utilitarios
- **`_read_group_stage_ids()`**: Agrupa etapas para vista kanban
- **`_track_subtype()`**: Define subtipos de seguimiento para mail.thread

---

## Lógica de Negocio

### Generación Automática de Nombres
Las órdenes se crean con nombre "New" y se asigna automáticamente un número de secuencia usando `ir.sequence` con código `fsm.order`.

### Cálculo de Fechas Programadas
El sistema calcula automáticamente:
- Si se proporciona inicio y fin: calcula duración
- Si se proporciona fin y duración: calcula inicio
- Si se proporciona inicio y duración: calcula fin

### Gestión de Prioridades
Las prioridades afectan el cálculo de `request_late`:
- Lowest (0): +horas configuradas en empresa
- Low (1): +horas configuradas en empresa
- Normal (2): +horas configuradas en empresa
- High (3): +horas configuradas en empresa

### Auto-población de Equipos
Si está habilitado en la empresa (`auto_populate_equipments_on_order`), se auto-populan los equipos de la ubicación.

### Validaciones de Etapa
- No se puede mover a "Completado" desde vista kanban
- Solo se pueden eliminar órdenes en etapa inicial

---

## Campos Agregados por Módulos OCA

### Módulo: fieldservice_account
**Archivo:** `fieldservice_account/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `account_analytic_line_ids` | One2many | Líneas analíticas de cuenta |
| `invoice_ids` | One2many | Facturas relacionadas |
| `invoice_count` | Integer (computed) | Contador de facturas |

### Módulo: fieldservice_agreement
**Archivo:** `fieldservice_agreement/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `agreement_id` | Many2one | Acuerdo de servicio |
| `serviceprofile_id` | Many2one | Perfil de servicio |

### Módulo: fieldservice_calendar
**Archivo:** `fieldservice_calendar/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `calendar_event_id` | Many2one | Evento de calendario |

### Módulo: fieldservice_crm
**Archivo:** `fieldservice_crm/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `opportunity_id` | Many2one | Oportunidad CRM |

### Módulo: fieldservice_project
**Archivo:** `fieldservice_project/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `project_id` | Many2one | Proyecto relacionado |
| `project_task_id` | Many2one | Tarea del proyecto |

### Módulo: fieldservice_recurring
**Archivo:** `fieldservice_recurring/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `fsm_recurring_id` | Many2one | Orden recurrente padre |
| `is_recurring` | Boolean | Es orden recurrente |

### Módulo: fieldservice_repair
**Archivo:** `fieldservice_repair/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `repair_id` | Many2one | Orden de reparación |

### Módulo: fieldservice_route
**Archivo:** `fieldservice_route/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `fsm_route_id` | Many2one | Ruta de servicio |
| `dayroute_id` | Many2one | Ruta del día |

### Módulo: fieldservice_sale
**Archivo:** `fieldservice_sale/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `sale_order_id` | Many2one | Orden de venta |
| `sale_line_id` | Many2one | Línea de venta |

### Módulo: fieldservice_size
**Archivo:** `fieldservice_size/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `size_id` | Many2one | Tamaño del servicio |
| `size_value` | Float | Valor del tamaño |

### Módulo: fieldservice_skill
**Archivo:** `fieldservice_skill/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `skill_ids` | Many2many | Habilidades requeridas |

### Módulo: fieldservice_stock
**Archivo:** `fieldservice_stock/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `request_id` | Many2one | Solicitud de stock |
| `picking_ids` | One2many | Albaranes relacionados |

### Módulo: fieldservice_vehicle
**Archivo:** `fieldservice_vehicle/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `vehicle_id` | Many2one | Vehículo asignado |

### Módulo: helpdesk_mgmt_fieldservice
**Archivo:** `helpdesk_mgmt_fieldservice/models/fsm_order.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `helpdesk_ticket_id` | Many2one | Ticket de helpdesk |

---

## Campos Agregados por Módulos PATCO

### Módulo: patco_fsm
**Archivo:** `patco_fsm/models/fsm_order.py`

#### Campos de Clasificación y Naturaleza
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `x_nature_id` | Many2one | Naturaleza del servicio (patco.service.nature) |
| `x_area_id` | Many2one | Área de servicio (patco.service.area) |
| `x_complexity_id` | Many2one | Complejidad del servicio |
| `x_classification_code` | Char (computed) | Código automático de clasificación |

#### Campos de Habilidades y Recursos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `x_required_skill_types` | Many2many | Tipos de habilidades requeridas |
| `x_min_skill_level` | Many2one | Nivel mínimo de habilidad requerido |
| `x_available_technicians` | Many2many (computed) | Técnicos que cumplen requisitos |
| `x_skill_match_warning` | Text (computed) | Advertencias de compatibilidad |

#### Campos de Herramientas y Equipos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `x_required_tools_ids` | Many2many | Herramientas requeridas |
| `x_special_equipment_ids` | Many2many | Equipos especiales requeridos |
| `x_multiple_assets_ids` | Many2many | Múltiples activos involucrados |

#### Campos de Repuestos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `x_consumed_parts_ids` | One2many | Repuestos consumidos |
| `x_total_parts_cost` | Float (computed) | Costo total de repuestos |
| `consumed_parts_count` | Integer (computed) | Contador de repuestos |

#### Campos de Hojas de Trabajo
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `worksheet_ids` | One2many | Hojas de trabajo |
| `worksheet_count` | Integer (computed) | Contador de hojas |
| `has_signed_worksheet` | Boolean (computed) | Tiene hoja firmada |
| `worksheet_completion_rate` | Float (computed) | % de completitud |

#### Campos de Checklists
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `x_entry_checklist` | Html | Checklist de entrada |
| `x_exit_checklist` | Html | Checklist de salida |

#### Campos de Tiempo y Facturación
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `timesheet_ids` | One2many | Registros de tiempo |
| `timesheet_count` | Integer (computed) | Contador de registros |
| `total_timesheet_time` | Float (computed) | Tiempo total en horas |
| `is_timer_running` | Boolean (computed) | Timer activo |
| `current_timesheet_id` | Many2one (computed) | Timesheet actual |
| `invoice_policy` | Selection | Política de facturación |
| `service_product_id` | Many2one | Producto de servicio |
| `auto_invoice_time` | Boolean | Facturar tiempo automáticamente |
| `auto_invoice_materials` | Boolean | Facturar materiales automáticamente |

#### Campos de Equipo de Trabajo
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `x_asset_technician_ids` | One2many | Activos y técnicos asignados |
| `x_lead_technician_id` | Many2one | Técnico líder |
| `x_team_technician_ids` | Many2many | Equipo de técnicos |
| `x_total_assigned_technicians` | Integer (computed) | Total técnicos asignados |
| `x_total_assigned_assets` | Integer (computed) | Total activos asignados |

#### Campos de Información de Equipos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `x_equipment_category_name` | Char (computed) | Categoría del equipo |
| `x_equipment_location_name` | Char (computed) | Ubicación del equipo |
| `x_equipment_brand_model` | Char (computed) | Marca y modelo |

#### Campos de Base de Conocimiento
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `x_knowledge_base_count` | Integer (computed) | Artículos de base de conocimiento |

### Módulo: patco_ai_agent
**Archivo:** `patco_ai_agent/models/fsm_order.py`

#### Campos de Integración con IA
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `x_ai_channel_id` | Many2one | Canal de conversación IA |
| `x_ai_enabled` | Boolean | IA habilitada |
| `x_ai_status` | Selection | Estado IA: 'not_started', 'active', 'completed', 'error' |
| `x_ai_auto_start` | Boolean | Inicio automático de IA |
| `x_ai_conversation_id` | Many2one | Conversación IA (legacy) |
| `x_ai_channel_name` | Char (related) | Nombre del canal IA |
| `x_ai_message_count` | Integer (computed) | Contador de mensajes IA |
| `x_ai_duration` | Float (computed) | Duración de conversación IA |

---

## Métodos Principales por Módulo

### Métodos del Core (fieldservice)
- **Gestión de fechas**: `_calc_scheduled_dates()`, `_calc_request_late()`
- **Acciones de estado**: `action_complete()`, `action_cancel()`
- **Validaciones**: `can_unlink()`, `check_day()`

### Métodos de patco_fsm
- **Gestión de técnicos**: `action_suggest_technician()`, `action_suggest_technicians()`
- **Gestión de tiempo**: `action_start_timer()`, `action_stop_timer()`
- **Gestión de hojas**: `action_create_worksheet()`, `action_view_worksheets()`
- **Facturación**: `action_create_invoice()`, `_auto_invoice_on_stage_change()`
- **Repuestos**: `action_consume_parts()`, `action_view_consumed_parts()`
- **Asignaciones**: `action_assign_technicians_to_assets()`

### Métodos de patco_ai_agent
- **Gestión de IA**: `_create_ai_channel()`, `action_open_ai_channel()`
- **Control de IA**: `action_enable_ai()`, `action_disable_ai()`
- **Estadísticas**: `get_ai_statistics()`, `action_view_ai_statistics()`

---

## Consideraciones de Rendimiento

### Campos Computados Costosos
- `x_available_technicians`: Busca técnicos con habilidades específicas
- `worksheet_completion_rate`: Calcula porcentaje de hojas completadas
- `x_ai_message_count`: Cuenta mensajes en canal IA

### Optimizaciones Implementadas
- Uso de `store=True` en campos computados frecuentemente accedidos
- Índices en campos de búsqueda frecuente (`stage_id`, `person_id`, `location_id`)
- Cálculos lazy en campos relacionados

### Recomendaciones
- Usar filtros en vistas para reducir registros cargados
- Implementar paginación en vistas con muchos registros
- Considerar archivado de órdenes antiguas

---

## Flujos de Trabajo Típicos

### Creación de Orden
1. Se crea con nombre "New"
2. Se asigna número de secuencia automáticamente
3. Se calculan fechas límite basadas en prioridad
4. Se auto-populan equipos si está configurado

### Asignación de Técnico
1. Se evalúan habilidades requeridas vs disponibles
2. Se muestran advertencias de incompatibilidad
3. Se puede iniciar conversación IA automáticamente
4. Se actualiza información de contacto

### Ejecución del Servicio
1. Se inicia timer de trabajo
2. Se registran repuestos consumidos
3. Se completan hojas de trabajo
4. Se registra resolución

### Cierre de Orden
1. Se valida completitud de documentación
2. Se genera facturación automática si está configurada
3. Se actualiza estado a completado
4. Se archivan conversaciones IA

---

*Documentación generada para Odoo 18 Community Edition con módulos OCA y PATCO*
*Última actualización: Enero 2025*