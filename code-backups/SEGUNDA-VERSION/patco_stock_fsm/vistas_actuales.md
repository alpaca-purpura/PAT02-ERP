# Vistas Actuales - PATCO Stock FSM

**Versión:** 18.0.1.0.0  
**Fecha de análisis:** Enero 2025  

## 1. Estructura de Menús

### 1.1 Menú Principal
- **ID:** `menu_patco_stock_fsm_root`
- **Nombre:** "PATCO Stock FSM"
- **Icono:** `patco_stock_fsm,static/src/img/PATCO-Logo.png`
- **Secuencia:** 50
- **Descripción:** Menú raíz del módulo de gestión de stock para servicios de campo

### 1.2 Submenús Principales

#### 1.2.1 Gestión de Stock
- **ID:** `menu_patco_stock_management`
- **Nombre:** "Gestión de Stock"
- **Padre:** `menu_patco_stock_fsm_root`
- **Secuencia:** 10

#### 1.2.2 Transferencias
- **ID:** `menu_patco_stock_transfers`
- **Nombre:** "Transferencias"
- **Padre:** `menu_patco_stock_fsm_root`
- **Secuencia:** 20

## 2. Opciones de Menú y Acciones

### 2.1 Ubicaciones de Vehículos

#### 2.1.1 Vista Lista/Formulario
- **ID del Menú:** `menu_stock_location_vehicles`
- **Acción:** `action_stock_location_vehicle`
- **Descripción:** Gestión de ubicaciones de vehículos con vista lista y formulario
- **Modelo:** `stock.location`
- **Modos de Vista:** `list,form`
- **Dominio:** `[('is_vehicle_location', '=', True)]`

**Vistas Implementadas:**

| ID de Vista | Tipo | Propósito | Vista Heredada |
|-------------|------|-----------|----------------|
| `view_stock_location_vehicle_form` | form | Formulario para configurar vehículos | `stock.view_location_form` |
| `view_stock_location_vehicle_list` | list | Lista de ubicaciones de vehículos | `stock.view_location_tree2` |
| `view_stock_location_vehicle_search` | search | Filtros y búsqueda para vehículos | `stock.view_location_search` |

#### 2.1.2 Vista Kanban
- **ID del Menú:** `menu_stock_location_vehicles_kanban`
- **Acción:** `action_stock_location_vehicle_kanban`
- **Descripción:** Vista kanban especializada para vehículos con indicadores visuales
- **Modelo:** `stock.location`
- **Modos de Vista:** `kanban,list,form`

**Vistas Implementadas:**

| ID de Vista | Tipo | Propósito | Vista Heredada |
|-------------|------|-----------|----------------|
| `view_stock_location_vehicle_kanban` | kanban | Tarjetas visuales con indicadores de capacidad | Nueva vista |

### 2.2 Solicitudes de Transferencia

- **ID del Menú:** `menu_stock_transfer_requests`
- **Acción:** `action_stock_transfer_request`
- **Descripción:** Gestión completa del workflow de solicitudes de transferencia
- **Modelo:** `stock.transfer.request`
- **Modos de Vista:** `list,kanban,form`

**Vistas Implementadas:**

| ID de Vista | Tipo | Propósito | Vista Heredada |
|-------------|------|-----------|----------------|
| `view_stock_transfer_request_form` | form | Formulario de solicitud con workflow | Nueva vista |
| `view_stock_transfer_request_list` | list | Lista de solicitudes con estados | Nueva vista |
| `view_stock_transfer_request_kanban` | kanban | Organización por estados del workflow | Nueva vista |
| `view_stock_transfer_request_search` | search | Filtros por estado, técnico y fecha | Nueva vista |
| `view_stock_transfer_request_line_form` | form | Formulario para líneas de transferencia | Nueva vista |

## 3. Campos Implementados por Modelo

### 3.1 stock.location (Extensión)

| Campo | Tipo | Descripción | Origen |
|-------|------|-------------|--------|
| `name` | Char | Nombre de la ubicación | **Odoo Core** |
| `usage` | Selection | Tipo de ubicación (internal, customer, etc.) | **Odoo Core** |
| `active` | Boolean | Estado activo/inactivo | **Odoo Core** |
| `company_id` | Many2one | Compañía propietaria | **Odoo Core** |
| `location_id` | Many2one | Ubicación padre | **Odoo Core** |
| `child_ids` | One2many | Ubicaciones hijas | **Odoo Core** |
| `quant_ids` | One2many | Cantidades en stock | **Odoo Core** |
| `is_vehicle_location` | Boolean | Marca como ubicación de vehículo | **PATCO** |
| `technician_id` | Many2one | Técnico asignado al vehículo | **PATCO** |
| `vehicle_code` | Char | Código único del vehículo | **PATCO** |
| `max_capacity` | Float | Capacidad máxima en kg | **PATCO** |
| `current_weight` | Float | Peso actual calculado | **PATCO** (Computado) |
| `capacity_percentage` | Float | Porcentaje de capacidad utilizada | **PATCO** (Computado) |

### 3.2 stock.transfer.request (Nuevo Modelo)

| Campo | Tipo | Descripción | Origen |
|-------|------|-------------|--------|
| `name` | Char | Número de secuencia automática | **PATCO** |
| `date` | Datetime | Fecha de solicitud | **PATCO** |
| `technician_id` | Many2one | Técnico solicitante | **PATCO** |
| `vehicle_location_id` | Many2one | Vehículo destino | **PATCO** |
| `source_location_id` | Many2one | Ubicación origen | **PATCO** |
| `state` | Selection | Estado del workflow | **PATCO** |
| `line_ids` | One2many | Líneas de productos solicitados | **PATCO** |
| `picking_ids` | One2many | Transferencias generadas | **PATCO** |
| `picking_count` | Integer | Contador de transferencias | **PATCO** (Computado) |
| `notes` | Text | Notas adicionales | **PATCO** |
| `company_id` | Many2one | Compañía | **PATCO** |
| `create_uid` | Many2one | Usuario creador | **Odoo Core** (Heredado) |
| `write_uid` | Many2one | Usuario modificador | **Odoo Core** (Heredado) |
| `create_date` | Datetime | Fecha de creación | **Odoo Core** (Heredado) |
| `write_date` | Datetime | Fecha de modificación | **Odoo Core** (Heredado) |

### 3.3 stock.transfer.request.line (Nuevo Modelo)

| Campo | Tipo | Descripción | Origen |
|-------|------|-------------|--------|
| `sequence` | Integer | Orden de las líneas | **PATCO** |
| `request_id` | Many2one | Solicitud padre | **PATCO** |
| `product_id` | Many2one | Producto solicitado | **PATCO** |
| `product_uom_id` | Many2one | Unidad de medida | **PATCO** (Related) |
| `quantity_requested` | Float | Cantidad solicitada | **PATCO** |
| `quantity_available` | Float | Cantidad disponible en origen | **PATCO** (Computado) |
| `quantity_to_transfer` | Float | Cantidad a transferir | **PATCO** |
| `notes` | Char | Notas de la línea | **PATCO** |

### 3.4 stock.picking (Extensión)

| Campo | Tipo | Descripción | Origen |
|-------|------|-------------|--------|
| `name` | Char | Número de transferencia | **Odoo Core** |
| `origin` | Char | Documento origen | **Odoo Core** |
| `state` | Selection | Estado de la transferencia | **Odoo Core** |
| `picking_type_id` | Many2one | Tipo de operación | **Odoo Core** |
| `location_id` | Many2one | Ubicación origen | **Odoo Core** |
| `location_dest_id` | Many2one | Ubicación destino | **Odoo Core** |
| `move_ids` | One2many | Movimientos de stock | **Odoo Core** |
| `x_transfer_request_id` | Many2one | Solicitud de transferencia relacionada | **PATCO** |
| `fsm_order_id` | Many2one | Orden FSM relacionada | **PATCO** |

## 4. Herencia de Vistas

### 4.1 Vista de Formulario de Ubicaciones
- **Vista Heredada:** `stock.view_location_form`
- **Vista PATCO:** `view_stock_location_vehicle_form`
- **Modificaciones:**
  - Agrega campos específicos de vehículos después del campo `usage`
  - Agrega campos de peso y capacidad antes del campo `usage`
  - Campos condicionales basados en `is_vehicle_location`

**Campos Heredados de la Vista Base:**
- `name`: Nombre de la ubicación
- `complete_name`: Nombre completo con jerarquía
- `usage`: Tipo de ubicación (internal, customer, vendor, etc.)
- `location_id`: Ubicación padre
- `company_id`: Compañía
- `active`: Estado activo
- `comment`: Información adicional
- `barcode`: Código de barras
- `removal_strategy_id`: Estrategia de remoción

### 4.2 Vista de Lista de Ubicaciones
- **Vista Heredada:** `stock.view_location_tree2`
- **Vista PATCO:** `view_stock_location_vehicle_list`
- **Modificaciones:**
  - Agrega columnas específicas de vehículos después del campo `usage`
  - Campos opcionales para mostrar/ocultar información de vehículos

**Campos Heredados de la Vista Base:**
- `name`: Nombre de la ubicación
- `complete_name`: Ruta completa
- `usage`: Tipo de ubicación
- `company_id`: Compañía
- `active`: Estado

### 4.3 Vista de Búsqueda de Ubicaciones
- **Vista Heredada:** `stock.view_location_search`
- **Vista PATCO:** `view_stock_location_vehicle_search`
- **Modificaciones:**
  - Agrega filtros específicos para ubicaciones de vehículos
  - Agrega agrupaciones por técnico y tipo de ubicación

**Filtros Heredados de la Vista Base:**
- Filtro por ubicaciones internas
- Filtro por compañía
- Búsqueda por nombre
- Agrupación por ubicación padre
- Agrupación por tipo de uso

### 4.4 Vista de Formulario de Picking
- **Vista Heredada:** `stock.view_picking_form`
- **Vista PATCO:** `view_picking_form_transfer_request`
- **Modificaciones:**
  - Agrega campo de solicitud de transferencia después del campo `origin`
  - Campo visible solo cuando existe una solicitud relacionada

## 5. Integraciones con Otros Módulos

### 5.1 Integración con Inventario (stock)
- **Menú:** `menu_inventory_vehicle_locations` → `action_stock_location_vehicle`
- **Menú:** `menu_inventory_transfer_requests` → `action_stock_transfer_request`
- **Ubicación:** Bajo `stock.menu_stock_warehouse_mgmt`

### 5.2 Integración con Field Service (fieldservice)
- **Menú:** `menu_fsm_vehicle_stock` → `action_stock_location_vehicle_kanban`
- **Menú:** `menu_fsm_transfer_requests` → `action_stock_transfer_request`
- **Ubicación:** Bajo `fieldservice.root`
- **Restricción:** Solo para usuarios con `fieldservice.group_fsm_user`

## 6. Funcionalidades Especiales

### 6.1 Workflow de Estados
**stock.transfer.request** implementa un workflow con 4 estados:
- `draft`: Borrador (estado inicial)
- `confirmed`: Confirmado (validación de stock)
- `done`: Completado (transferencia creada)
- `cancelled`: Cancelado

### 6.2 Validaciones Automáticas
- **Código único de vehículo:** Previene duplicados
- **Técnico único por vehículo:** Un técnico solo puede estar asignado a un vehículo activo
- **Validación de stock:** Verifica disponibilidad antes de confirmar transferencias

### 6.3 Cálculos Automáticos
- **Peso actual:** Calculado en tiempo real basado en productos almacenados
- **Porcentaje de capacidad:** Calculado automáticamente
- **Cantidad disponible:** Calculada por ubicación de origen

### 6.4 Secuencias Automáticas
- **Solicitudes de transferencia:** Formato `STR/YYYY/NNNN`
- **Generación automática:** Al crear nuevas solicitudes

## 7. Dependencias y Relaciones

### 7.1 Módulos Requeridos
- `base`: Funcionalidades básicas de Odoo
- `stock`: Gestión de inventario y transferencias
- `fieldservice`: Gestión de servicios de campo (opcional)
- `fieldservice_stock`: Integración stock con FSM (opcional)
- `patco_base`: Modelos base del ecosistema PATCO

### 7.2 Modelos Relacionados
- `res.partner`: Para técnicos
- `product.product`: Para productos a transferir
- `stock.quant`: Para cantidades en stock
- `stock.move`: Para movimientos de inventario
- `fsm.order`: Para órdenes de servicio (opcional)