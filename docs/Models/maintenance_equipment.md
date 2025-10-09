# Modelo maintenance.equipment - Documentación Técnica

## Información General

**Modelo:** `maintenance.equipment`  
**Descripción:** Gestión de equipos y activos para mantenimiento  
**Módulo Base:** `maintenance` (Odoo Core)  
**Herencia:** `mail.thread`, `mail.activity.mixin`, `maintenance.mixin`  
**Tabla:** `maintenance_equipment`  

## Campos del Core de Odoo 18

### Campos Generales
- **name** (`Char`): Nombre del equipo
  - Requerido: Sí
  - Tracking: Sí
  - Ayuda: Nombre identificativo del equipo

- **active** (`Boolean`): Activo
  - Default: True
  - Ayuda: Si está desmarcado, el equipo no será visible

- **owner_user_id** (`Many2one` → `res.users`): Propietario
  - Ayuda: Usuario responsable del equipo

- **category_id** (`Many2one` → `maintenance.equipment.category`): Categoría de Equipo
  - Requerido: Sí
  - Ondelete: restrict
  - Ayuda: Categoría del equipo para clasificación

- **partner_id** (`Many2one` → `res.partner`): Proveedor
  - Check_company: True
  - Ayuda: Proveedor del equipo

- **partner_ref** (`Char`): Referencia del Proveedor
  - Ayuda: Referencia del proveedor para el equipo

- **company_id** (`Many2one` → `res.company`): Empresa
  - Default: self.env.company
  - Ayuda: Empresa propietaria del equipo (heredado de maintenance.mixin)

- **model** (`Char`): Modelo
  - Ayuda: Modelo del equipo

- **serial_no** (`Char`): Número de Serie
  - Copy: False
  - Ayuda: Número de serie único del equipo

- **assign_date** (`Date`): Fecha de Asignación
  - Ayuda: Fecha cuando el equipo fue asignado

- **effective_date** (`Date`): Fecha Efectiva
  - Default: fields.Date.context_today
  - Required: True
  - Ayuda: Fecha desde cuando el equipo está efectivo (heredado de maintenance.mixin)

- **maintenance_team_id** (`Many2one` → `maintenance.team`): Equipo de Mantenimiento
  - Compute: `_compute_maintenance_team_id`
  - Store: True
  - Readonly: False
  - Check_company: True
  - Ayuda: Equipo responsable del mantenimiento (heredado de maintenance.mixin)

- **technician_user_id** (`Many2one` → `res.users`): Técnico
  - Tracking: True
  - Ayuda: Técnico asignado al equipo (heredado de maintenance.mixin)

- **expected_mtbf** (`Integer`): MTBF Esperado
  - Ayuda: Tiempo medio entre fallas esperado (heredado de maintenance.mixin)

- **cost** (`Float`): Costo
  - Ayuda: Costo del equipo

- **note** (`Html`): Nota
  - Ayuda: Información adicional sobre el equipo

- **warranty_date** (`Date`): Fecha de Vencimiento de Garantía
  - Ayuda: Fecha de vencimiento de la garantía

- **equipment_properties** (`Properties`): Propiedades
  - Definition: `category_id.equipment_properties_definition`
  - Copy: True
  - Ayuda: Propiedades específicas del equipo según su categoría

- **color** (`Integer`): Color
  - Ayuda: Color para identificación visual

### Campos Computados del Core
- **maintenance_count** (`Integer`): Número de Mantenimientos
  - Compute: `_compute_maintenance_count`
  - Store: True
  - Ayuda: Cantidad de solicitudes de mantenimiento (heredado de maintenance.mixin)

- **maintenance_open_count** (`Integer`): Mantenimientos Abiertos
  - Compute: `_compute_maintenance_count`
  - Store: True
  - Ayuda: Cantidad de mantenimientos pendientes (heredado de maintenance.mixin)

- **mtbf** (`Integer`): MTBF
  - Compute: `_compute_maintenance_request`
  - Ayuda: Tiempo medio entre fallas actual (heredado de maintenance.mixin)

- **mttr** (`Integer`): MTTR
  - Compute: `_compute_maintenance_request`
  - Ayuda: Tiempo medio de reparación (heredado de maintenance.mixin)

- **estimated_next_failure** (`Date`): Próxima Falla Estimada
  - Compute: `_compute_maintenance_request`
  - Ayuda: Fecha estimada de la próxima falla (heredado de maintenance.mixin)

- **latest_failure_date** (`Date`): Última Fecha de Falla
  - Compute: `_compute_maintenance_request`
  - Ayuda: Fecha de la última falla registrada (heredado de maintenance.mixin)

- **display_name** (`Char`): Nombre a Mostrar
  - Compute: `_compute_display_name`
  - Depends: `serial_no`
  - Ayuda: Nombre del equipo con número de serie si existe

- **match_serial** (`Boolean`): Serie Coincidente
  - Compute: `_compute_match_serial`
  - Depends: `serial_no`
  - Ayuda: Indica si el número de serie coincide con lotes de stock

### Campos de Seguimiento
- **fold** (`Boolean`): Plegado
  - Ayuda: Campo técnico para vistas kanban

- **maintenance_ids** (`One2many` → `maintenance.request`): Solicitudes de Mantenimiento
  - Inverse: equipment_id
  - Ayuda: Todas las solicitudes de mantenimiento del equipo (heredado de maintenance.mixin)

- **scrap_date** (`Date`): Fecha de Desecho
  - Ayuda: Fecha cuando el equipo fue desechado

## Campos Agregados por Módulos Nativos de Odoo

### Módulo: hr_maintenance
**Archivo:** `addons/hr_maintenance/models/equipment.py`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `employee_id` | Many2one → `hr.employee` | Empleado Asignado |
| `department_id` | Many2one → `hr.department` | Departamento Asignado |
| `equipment_assign_to` | Selection | Usado Por |
| `owner_user_id` | Many2one (computed) | Usuario Propietario |
| `assign_date` | Date (computed) | Fecha de Asignación |

**Campos Computados:**
- **`owner_user_id`**: Se calcula basado en el tipo de asignación:
  - Si está asignado a empleado: usuario del empleado
  - Si está asignado a departamento: usuario del manager del departamento
  - Compute: `_compute_owner`
  - Store: True

- **`assign_date`**: Fecha de asignación calculada automáticamente
  - Compute: `_compute_equipment_assign`
  - Store: True
  - Readonly: False
  - Copy: True

**Opciones del Campo `equipment_assign_to`:**
- `department`: Departamento
- `employee`: Empleado  
- `other`: Otro

**Métodos Principales:**
- **`_compute_owner()`**: Calcula el usuario propietario según el tipo de asignación
- **`_compute_equipment_assign()`**: Gestiona la lógica de asignación y limpia campos según el tipo
- **`create(vals_list)`**: Suscribe automáticamente al empleado o manager del departamento
- **`write(vals)`**: Actualiza suscripciones cuando cambia la asignación
- **`_track_subtype(init_values)`**: Seguimiento de cambios de asignación

**Lógica de Negocio:**
- **Asignación Exclusiva**: Cuando se asigna a empleado, se limpia el departamento y viceversa
- **Suscripción Automática**: El sistema suscribe automáticamente a los usuarios relevantes para recibir notificaciones
- **Seguimiento de Cambios**: Los cambios de asignación se registran en el chatter
- **Fecha Automática**: La fecha de asignación se actualiza automáticamente al cambiar el tipo de asignación

## Campos Agregados por Módulos OCA

### maintenance_product
- **product_id** (`Many2one` → `product.product`): Producto
  - Ayuda: Producto asociado al equipo

- **product_category_id** (`Many2one` → `product.category`): Categoría de Producto
  - Related: `product_id.categ_id`
  - Readonly: True
  - Ayuda: Categoría del producto asociado

### maintenance_project
- **project_id** (`Many2one` → `project.project`): Proyecto
  - Ayuda: Proyecto asociado al equipo

- **preventive_default_task_id** (`Many2one` → `project.task`): Tarea Preventiva por Defecto
  - Ayuda: Tarea por defecto para mantenimiento preventivo

### maintenance_equipment_usage
- **usage_ids** (`One2many` → `maintenance.equipment.usage`): Usos del Equipo
  - Inverse: equipment_id
  - Ayuda: Registros de uso del equipo

- **usage_count** (`Integer`): Contador de Usos
  - Compute: `_compute_usage_count`
  - Ayuda: Número total de registros de uso

- **in_use** (`Boolean`): En Uso
  - Compute: `_compute_in_use`
  - Ayuda: Indica si el equipo está actualmente en uso

## Campos Agregados por PATCO

### Campos de Identificación PATCO
- **x_patco_code** (`Char`): Código PATCO
  - Copy: False
  - Readonly: True
  - Default: 'Nuevo'
  - Tracking: True
  - Ayuda: Código único PATCO del equipo

- **x_customer_id** (`Many2one` → `res.partner`): Cliente
  - Domain: `[('customer_rank', '>', 0)]`
  - Tracking: True
  - Ayuda: Cliente propietario del equipo

- **x_service_location_id** (`Many2one` → `res.partner`): Ubicación de Servicio
  - Domain: `[('parent_id', '=', x_customer_id)]`
  - Tracking: True
  - Ayuda: Ubicación donde se encuentra el equipo para servicios

### Campos de Código QR
- **x_qr_code** (`Binary`): Código QR
  - Readonly: True
  - Ayuda: Código QR generado automáticamente para el equipo

- **x_qr_url** (`Char`): URL del QR
  - Readonly: True
  - Ayuda: URL contenida en el código QR

### Campos de Relaciones de Servicio
- **x_service_order_ids** (`One2many` → `fsm.order`): Órdenes de Servicio
  - Inverse: x_equipment_id
  - Ayuda: Órdenes de servicio relacionadas con este equipo

- **x_helpdesk_ticket_ids** (`One2many` → `helpdesk.ticket`): Tickets de Soporte
  - Inverse: x_equipment_id
  - Ayuda: Tickets de soporte relacionados con este equipo

### Campos de Estado PATCO
- **maintenance_state** (`Selection`): Estado PATCO
  - Opciones: 
    - `draft`: Borrador
    - `active`: Activo
    - `maintenance`: En Mantenimiento
    - `retired`: Retirado
  - Default: 'draft'
  - Tracking: True
  - Ayuda: Estado específico PATCO del equipo

### Campos Computados PATCO
- **x_service_count** (`Integer`): Servicios
  - Compute: `_compute_service_count`
  - Store: True
  - Ayuda: Número total de servicios realizados

- **x_ticket_count** (`Integer`): Tickets
  - Compute: `_compute_ticket_count`
  - Store: True
  - Ayuda: Número total de tickets de soporte

- **x_fsm_order_count** (`Integer`): Órdenes FSM
  - Compute: `_compute_fsm_order_count`
  - Store: True
  - Ayuda: Número total de órdenes FSM relacionadas

- **x_assigned_technician_count** (`Integer`): Técnicos Asignados
  - Compute: `_compute_assigned_technician_count`
  - Store: True
  - Ayuda: Número de técnicos únicos asignados a este activo

- **x_multi_asset_order_count** (`Integer`): Órdenes Multi-Activo
  - Compute: `_compute_multi_asset_order_count`
  - Store: True
  - Ayuda: Número de órdenes que involucran múltiples activos

- **x_last_service_date** (`Datetime`): Último Servicio
  - Compute: `_compute_last_service_date`
  - Ayuda: Fecha del último servicio realizado

### Campos de Fechas PATCO
- **x_installation_date** (`Date`): Fecha de Instalación
  - Tracking: True
  - Ayuda: Fecha de instalación del equipo

- **x_warranty_expiry** (`Date`): Vencimiento de Garantía
  - Tracking: True
  - Ayuda: Fecha de vencimiento de la garantía

### Campos Técnicos PATCO
- **x_technical_specs** (`Text`): Especificaciones Técnicas
  - Ayuda: Especificaciones técnicas detalladas del equipo

- **x_operating_conditions** (`Text`): Condiciones de Operación
  - Ayuda: Condiciones ambientales y operativas del equipo

- **description** (`Text`): Descripción
  - Ayuda: Descripción detallada del equipo

## Métodos Principales

### Métodos del Core
- **create(vals)**: Creación de equipos con validaciones
- **write(vals)**: Actualización con seguimiento de cambios
- **_compute_maintenance_count()**: Cálculo de estadísticas de mantenimiento
- **_track_subtype(init_values)**: Seguimiento de cambios para mail.thread
- **_compute_display_name()**: Cálculo del nombre a mostrar
- **_compute_match_serial()**: Verificación de números de serie duplicados
- **_onchange_category_id()**: Cambio automático al seleccionar categoría
- **_read_group_category_ids()**: Agrupación por categorías
- **action_open_matched_serial()**: Acción para abrir equipos con serie duplicada

### Métodos OCA
- **_onchange_product_id()** (maintenance_product): Actualización automática al cambiar producto
- **_prepare_project_values()** (maintenance_project): Preparación de valores para crear proyecto
- **_compute_usage_count()** (maintenance_equipment_usage): Cálculo de contador de usos
- **_compute_in_use()** (maintenance_equipment_usage): Verificación si está en uso
- **_prepare_project_from_equipment_values()** (maintenance_timesheet): Configuración de timesheet en proyectos

### Métodos PATCO
- **create(vals)**: Generación automática de código PATCO y QR
- **write(vals)**: Regeneración de QR al cambiar datos relevantes
- **_generate_qr_code()**: Generación de código QR con URL del equipo
- **_compute_service_count()**: Cálculo del número de servicios
- **_compute_ticket_count()**: Cálculo del número de tickets
- **_compute_fsm_order_count()**: Cálculo de órdenes FSM
- **_compute_assigned_technician_count()**: Cálculo de técnicos asignados
- **_compute_multi_asset_order_count()**: Cálculo de órdenes multi-activo
- **_compute_last_service_date()**: Cálculo de fecha del último servicio
- **_check_unique_serial_per_customer()**: Validación de serie única por cliente

### Métodos de Acción PATCO
- **action_activate()**: Activar equipo
- **action_maintenance()**: Poner en mantenimiento
- **action_retire()**: Retirar equipo
- **action_view_service_orders()**: Ver órdenes de servicio
- **action_view_helpdesk_tickets()**: Ver tickets de soporte
- **action_view_fsm_orders()**: Ver órdenes FSM
- **action_view_assigned_technicians()**: Ver técnicos asignados
- **action_view_multi_asset_orders()**: Ver órdenes multi-activo
- **regenerate_qr_code()**: Regenerar código QR manualmente

### Métodos de Checklist PATCO
- **get_entry_checklist_template()**: Obtener plantilla de checklist de entrada
- **get_exit_checklist_template()**: Obtener plantilla de checklist de salida
- **has_entry_checklist()**: Verificar si tiene checklist de entrada
- **has_exit_checklist()**: Verificar si tiene checklist de salida
- **action_view_category_knowledge_base()**: Ver base de conocimiento de categoría
- **get_category_hierarchy_info()**: Obtener información de jerarquía de categorías

## Lógica de Negocio

### Flujo de Creación
1. **Generación Automática**: Al crear un equipo, se genera automáticamente:
   - Código PATCO único usando secuencia `maintenance.equipment.patco`
   - Código QR con URL del equipo
   - Estado inicial 'draft'

2. **Validaciones**: 
   - Número de serie único por cliente
   - Campos requeridos según configuración

### Flujo de Estados PATCO
- **draft** → **active**: Equipo listo para uso
- **active** → **maintenance**: Equipo en mantenimiento
- **maintenance** → **active**: Equipo disponible nuevamente
- **active/maintenance** → **retired**: Equipo fuera de servicio

### Integración con FSM y Helpdesk
- Relación automática con órdenes de servicio FSM
- Vinculación con tickets de helpdesk
- Cálculo automático de estadísticas de servicio
- Seguimiento de técnicos asignados

### Gestión de QR
- Generación automática al crear/modificar
- Regeneración cuando cambian datos relevantes:
  - Nombre del equipo
  - Código PATCO
  - Cliente
  - Ubicación de servicio

## Ejemplos Prácticos

### Crear Equipo con Cliente
```python
# Crear equipo con cliente y ubicación
equipment = self.env['maintenance.equipment'].create({
    'name': 'Compresor Industrial XYZ',
    'category_id': category_id,
    'x_customer_id': customer_id,
    'x_service_location_id': location_id,
    'serial_no': 'CI-2024-001',
    'x_installation_date': '2024-01-15',
    'x_warranty_expiry': '2026-01-15',
})
# Resultado: Código PATCO y QR generados automáticamente
```

### Buscar Equipos por Cliente
```python
# Equipos de un cliente específico
customer_equipment = self.env['maintenance.equipment'].search([
    ('x_customer_id', '=', customer_id),
    ('maintenance_state', 'in', ['active', 'maintenance'])
])
```

### Cambiar Estado del Equipo
```python
# Poner equipo en mantenimiento
equipment.action_maintenance()

# Activar equipo después de mantenimiento
equipment.action_activate()

# Retirar equipo
equipment.action_retire()
```

### Obtener Estadísticas de Servicio
```python
# Información completa de servicios
equipment_stats = {
    'total_services': equipment.x_service_count,
    'total_tickets': equipment.x_ticket_count,
    'fsm_orders': equipment.x_fsm_order_count,
    'assigned_technicians': equipment.x_assigned_technician_count,
    'last_service': equipment.x_last_service_date,
}
```

### Regenerar Código QR
```python
# Regenerar QR manualmente
equipment.regenerate_qr_code()

# Regeneración automática al cambiar datos
equipment.write({
    'name': 'Nuevo Nombre del Equipo',
    'x_customer_id': new_customer_id,
})
# QR se regenera automáticamente
```

## Instalación y Dependencias

### Módulos Requeridos
- `maintenance` (Odoo Core)
- `mail` (Odoo Core)
- `fieldservice` (OCA - para FSM)
- `helpdesk` (OCA - para tickets)
- `patco_core` (PATCO - configuraciones base)

### Dependencias Python
- `qrcode`: Generación de códigos QR
- `Pillow`: Procesamiento de imágenes

### Secuencias Requeridas
- `maintenance.equipment.patco`: Para códigos PATCO únicos

### Configuración
1. Instalar módulo `patco_equipment`
2. Configurar secuencia para códigos PATCO
3. Configurar categorías de equipos
4. Establecer parámetro `web.base.url` para QR correctos

## Notas Técnicas

### Rendimiento
- Campos computados con `store=True` para mejor rendimiento
- Índices automáticos en campos Many2one
- Cálculos optimizados para estadísticas

### Seguridad
- Validación de números de serie únicos por cliente
- Control de acceso mediante `ir.model.access.csv`
- Seguimiento de cambios con `tracking=True`

### Extensibilidad
- Herencia múltiple preparada para extensiones
- Métodos modulares para fácil sobrescritura
- Campos técnicos para integraciones futuras