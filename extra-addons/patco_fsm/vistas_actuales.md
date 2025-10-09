# 📋 Vistas Actuales - Módulo PATCO FSM

**Versión:** 18.0.1.0.0  
**Módulo:** patco_fsm  
**Fecha de Análisis:** Enero 2025  

---

## 🎯 Estructura del Menú Principal

### 📂 Menú Raíz: Servicios Externos
- **ID del Menú:** `menu_fsm_root`
- **Nombre:** "Servicios Externos"
- **Secuencia:** 10
- **Icono:** PATCO Logo (`patco_fsm,static/src/img/PATCO-Logo.png`)
- **Descripción:** Menú principal para la gestión de servicios de campo con funcionalidades específicas de PATCO

---

## 📋 Opciones del Menú y Vistas Implementadas

### 1. 🔧 Órdenes de Servicio (`menu_fsm_orders`)

#### 1.1 📝 Todas las Órdenes (`menu_fsm_order_all`)
- **ID del Menú:** `menu_fsm_order_all`
- **Acción:** `action_fsm_order_patco`
- **Secuencia:** 10
- **Funcionalidad:** Gestión completa de órdenes de servicio con clasificación PATCO, control de tiempo, consumo de repuestos y hojas de trabajo digitales

**Vistas Llamadas por la Acción:**

| Vista | ID | Tipo | Propósito |
|-------|----|----- |-----------|
| Lista | `fsm_order_list_view_patco` | list | Visualización tabular de órdenes con campos PATCO |
| Formulario | `fsm_order_form_view_patco` | form | Formulario completo con pestañas especializadas |

#### 1.2 👤 Mis Órdenes (`menu_fsm_order_my`)
- **ID del Menú:** `menu_fsm_order_my`
- **Acción:** `action_fsm_order_patco` (misma acción con filtro)
- **Secuencia:** 20
- **Funcionalidad:** Vista filtrada de órdenes asignadas al usuario actual

---

### 2. 📄 Hojas de Trabajo (`menu_fsm_worksheets`)

#### 2.1 📋 Todas las Hojas (`menu_fsm_worksheet_all`)
- **ID del Menú:** `menu_fsm_worksheet_all`
- **Acción:** `action_fsm_worksheet_patco`
- **Secuencia:** 10
- **Funcionalidad:** Gestión de hojas de trabajo digitales con firmas electrónicas y datos JSON dinámicos

**Vistas Llamadas por la Acción:**

| Vista | Tipo | Propósito |
|-------|------|-----------|
| Lista | list | Listado de hojas de trabajo con filtros |
| Formulario | form | Formulario de hoja de trabajo con workflow |

---

### 3. 🔩 Repuestos (`menu_fsm_parts`)

#### 3.1 📦 Repuestos Consumidos (`menu_fsm_consumed_parts`)
- **ID del Menú:** `menu_fsm_consumed_parts`
- **Acción:** `action_fsm_order_consumed_part`
- **Secuencia:** 10
- **Funcionalidad:** Control de inventario y costos de repuestos utilizados en órdenes de servicio

**Vistas Llamadas por la Acción:**

| Vista | ID | Tipo | Propósito |
|-------|----|----- |-----------|
| Lista | `view_fsm_order_consumed_part_list` | list | Listado de repuestos consumidos |
| Formulario | `view_fsm_order_consumed_part_form` | form | Detalle de repuesto consumido |
| Búsqueda | `view_fsm_order_consumed_part_search` | search | Filtros y agrupaciones |

---

### 4. ⚙️ Configuración (`menu_fsm_configuration`)

#### 4.1 📝 Plantillas de Hojas de Trabajo (`menu_fsm_worksheet_templates`)
- **ID del Menú:** `menu_fsm_worksheet_templates`
- **Acción:** `action_fsm_worksheet_template`
- **Secuencia:** 10
- **Funcionalidad:** Configuración de plantillas reutilizables para hojas de trabajo por categoría de equipo

**Vistas Llamadas por la Acción:**

| Vista | Tipo | Propósito |
|-------|------|-----------|
| Lista | list | Listado de plantillas disponibles |
| Formulario | form | Configuración de plantilla con campos JSON |

---

## 🔄 Herencia de Vistas y Campos Implementados

### 📋 Modelo: fsm.order

#### Vista Principal: `fsm_order_form_view_patco`
- **Tipo:** Formulario primario (mode="primary")
- **Prioridad:** 999
- **Origen:** Nueva vista PATCO (no hereda)

**Campos Implementados:**

| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `stage_id` | fsm.order | OCA Fieldservice | Estado de la orden con statusbar |
| `consumed_parts_count` | fsm.order | PATCO | Contador de repuestos utilizados |
| `worksheet_count` | fsm.order | PATCO | Contador de hojas de trabajo |
| `timesheet_count` | fsm.order | PATCO | Contador de registros de tiempo |
| `x_nature_id` | fsm.order | PATCO | Naturaleza del servicio |
| `x_area_id` | fsm.order | PATCO | Área de servicio |
| `x_complexity_id` | fsm.order | PATCO | Complejidad del trabajo |
| `x_classification_code` | fsm.order | PATCO | Código automático de clasificación |
| `x_multiple_assets_ids` | fsm.order | PATCO | Múltiples activos asignados |
| `x_total_assigned_assets` | fsm.order | PATCO | Contador de activos |
| `x_required_skill_types` | fsm.order | PATCO | Habilidades requeridas |
| `x_min_skill_level` | fsm.order | PATCO | Nivel mínimo de habilidad |
| `x_available_technicians` | fsm.order | PATCO | Técnicos disponibles |
| `x_skill_match_warning` | fsm.order | PATCO | Advertencia de compatibilidad |
| `person_id` | fsm.order | OCA Fieldservice | Técnico asignado (filtrado) |
| `x_team_technician_ids` | fsm.order | PATCO | Equipo de técnicos |
| `x_total_assigned_technicians` | fsm.order | PATCO | Total técnicos asignados |
| `has_signed_worksheet` | fsm.order | PATCO | Estado de firmas |
| `worksheet_completion_rate` | fsm.order | PATCO | Porcentaje de completitud |
| `total_timesheet_time` | fsm.order | PATCO | Tiempo total trabajado |
| `is_timer_running` | fsm.order | PATCO | Estado del cronómetro |
| `current_timesheet_id` | fsm.order | PATCO | Timesheet activo |
| `x_consumed_parts_ids` | fsm.order | PATCO | Lista de repuestos consumidos |
| `invoice_policy` | fsm.order | PATCO | Política de facturación |
| `service_product_id` | fsm.order | PATCO | Producto de servicio |
| `auto_invoice_time` | fsm.order | PATCO | Facturación automática de tiempo |
| `auto_invoice_materials` | fsm.order | PATCO | Facturación automática de materiales |
| `x_total_parts_cost` | fsm.order | PATCO | Costo total de repuestos |
| `timesheet_ids` | fsm.order | PATCO | Registros de tiempo detallados |

#### Vistas Heredadas:

**1. Vista de Filtro de Persona:** `view_fsm_order_form_person_filter`
- **Hereda de:** `fieldservice.fsm_order_form`
- **Modificaciones:** Filtro automático del campo `person_id` por habilidades disponibles
- **Campos Agregados:** Advertencia de compatibilidad de habilidades

**2. Vista de Lista:** `fsm_order_list_view_patco`
- **Hereda de:** `fieldservice.fsm_order_list_view`
- **Campos Agregados:** `x_nature_id`, `x_area_id`, `x_complexity_id`

**3. Vista Kanban:** `fsm_order_kanban_view_patco`
- **Hereda de:** `fieldservice.fsm_order_kanban_view`
- **Campos Agregados:** Tags de clasificación, código, tiempo, contadores

---

### 📄 Modelo: fsm.worksheet

#### Campos Principales:

| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `name` | fsm.worksheet | PATCO | Nombre de la hoja de trabajo |
| `order_id` | fsm.worksheet | PATCO | Orden de servicio asociada |
| `template_id` | fsm.worksheet | PATCO | Plantilla utilizada |
| `state` | fsm.worksheet | PATCO | Estado del workflow |
| `technician_id` | fsm.worksheet | PATCO | Técnico (relacionado) |
| `customer_id` | fsm.worksheet | PATCO | Cliente (relacionado) |
| `start_date` | fsm.worksheet | PATCO | Fecha de inicio |
| `end_date` | fsm.worksheet | PATCO | Fecha de finalización |
| `duration` | fsm.worksheet | PATCO | Duración calculada |
| `worksheet_data` | fsm.worksheet | PATCO | Datos JSON dinámicos |
| `technician_signature` | fsm.worksheet | PATCO | Firma digital del técnico |
| `customer_signature` | fsm.worksheet | PATCO | Firma digital del cliente |
| `customer_name` | fsm.worksheet | PATCO | Nombre del firmante |
| `customer_document` | fsm.worksheet | PATCO | Documento del firmante |
| `comments` | fsm.worksheet | PATCO | Comentarios adicionales |
| `report_pdf` | fsm.worksheet | PATCO | Reporte PDF generado |

---

### 📦 Modelo: fsm.order.consumed.part

#### Campos Principales:

| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `sequence` | fsm.order.consumed.part | PATCO | Orden secuencial |
| `order_id` | fsm.order.consumed.part | PATCO | Orden de servicio |
| `asset_technician_id` | fsm.order.consumed.part | PATCO | Asignación específica |
| `product_id` | fsm.order.consumed.part | PATCO | Producto/repuesto |
| `product_uom_id` | fsm.order.consumed.part | PATCO | Unidad de medida |
| `quantity` | fsm.order.consumed.part | PATCO | Cantidad consumida |
| `unit_cost` | fsm.order.consumed.part | PATCO | Costo unitario |
| `total_cost` | fsm.order.consumed.part | PATCO | Costo total |
| `location_id` | fsm.order.consumed.part | PATCO | Ubicación de origen |
| `state` | fsm.order.consumed.part | PATCO | Estado del consumo |
| `stock_move_id` | fsm.order.consumed.part | PATCO | Movimiento de inventario |
| `notes` | fsm.order.consumed.part | PATCO | Observaciones técnicas |

---

### 📝 Modelo: fsm.worksheet.template

#### Campos Principales:

| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `name` | fsm.worksheet.template | PATCO | Nombre de la plantilla |
| `description` | fsm.worksheet.template | PATCO | Descripción detallada |
| `sequence` | fsm.worksheet.template | PATCO | Orden de visualización |
| `active` | fsm.worksheet.template | PATCO | Estado activo/inactivo |
| `field_config` | fsm.worksheet.template | PATCO | Configuración JSON de campos |
| `equipment_category_ids` | fsm.worksheet.template | PATCO | Categorías de equipos aplicables |
| `service_nature_ids` | fsm.worksheet.template | PATCO | Naturalezas de servicio aplicables |

---

### 👥 Modelo: res.partner (Extensión)

#### Vista Heredada: `view_partner_form_fsm_locations`
- **Hereda de:** `base.view_partner_form`
- **Modificación:** Agrega pestaña "Ubicaciones FSM"

**Campos Agregados:**

| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `fsm_location` | res.partner | PATCO | Indica si es ubicación FSM |
| `service_location_id` | res.partner | PATCO | Ubicación principal de servicio |
| `owned_location_ids` | res.partner | PATCO | Ubicaciones propiedad del contacto |

---

### 🔧 Modelo: fsm.order.asset.technician

#### Campos Principales:

| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `order_id` | fsm.order.asset.technician | PATCO | Orden de servicio |
| `asset_id` | fsm.order.asset.technician | PATCO | Activo asignado |
| `technician_id` | fsm.order.asset.technician | PATCO | Técnico asignado |
| `sequence` | fsm.order.asset.technician | PATCO | Orden de prioridad |
| `is_lead` | fsm.order.asset.technician | PATCO | Indica si es líder técnico |
| `status` | fsm.order.asset.technician | PATCO | Estado del trabajo |
| `estimated_hours` | fsm.order.asset.technician | PATCO | Horas estimadas |
| `actual_hours` | fsm.order.asset.technician | PATCO | Horas reales |
| `parts_cost` | fsm.order.asset.technician | PATCO | Costo de repuestos |
| `estimated_cost` | fsm.order.asset.technician | PATCO | Costo estimado |
| `actual_cost` | fsm.order.asset.technician | PATCO | Costo real |
| `date_start` | fsm.order.asset.technician | PATCO | Fecha de inicio |
| `date_end` | fsm.order.asset.technician | PATCO | Fecha de finalización |
| `notes` | fsm.order.asset.technician | PATCO | Observaciones |
| `consumed_parts_ids` | fsm.order.asset.technician | PATCO | Repuestos consumidos |

---

## 🎯 Características Especiales de las Vistas

### ✨ Funcionalidades Avanzadas

1. **🎛️ Botones Estadísticos (Smart Buttons):**
   - Repuestos Utilizados
   - Hojas de Trabajo
   - Registros de Tiempo
   - Sugerir Técnicos

2. **⏱️ Control de Tiempo Integrado:**
   - Timer en tiempo real
   - Registro automático de timesheet
   - Cálculo de tiempo total

3. **🔧 Gestión de Habilidades:**
   - Filtrado automático de técnicos
   - Advertencias de compatibilidad
   - Sugerencias inteligentes

4. **📋 Workflow de Hojas de Trabajo:**
   - Estados: draft → in_progress → completed → signed
   - Firmas digitales integradas
   - Generación automática de PDF

5. **💰 Control Financiero:**
   - Cálculo automático de costos
   - Facturación configurable
   - Trazabilidad de repuestos

### 🔒 Seguridad y Permisos

- **Campos de Solo Lectura:** Campos calculados y relacionados
- **Dominios Dinámicos:** Filtrado por habilidades y disponibilidad
- **Validaciones:** Estados de workflow y consumo de repuestos
- **Trazabilidad:** Seguimiento completo con mail.thread

---

## 📊 Resumen de Implementación

| Modelo | Vistas Nuevas | Vistas Heredadas | Campos PATCO | Funcionalidades |
|--------|---------------|------------------|--------------|-----------------|
| fsm.order | 1 Form Principal | 3 (Form, List, Kanban) | 25+ | Timer, Habilidades, Repuestos |
| fsm.worksheet | 0 | 0 | 15+ | Workflow, Firmas, JSON |
| fsm.order.consumed.part | 3 (Form, List, Search) | 0 | 12+ | Control Stock, Costos |
| fsm.worksheet.template | 0 | 0 | 7+ | Configuración JSON |
| res.partner | 0 | 1 (Form) | 3+ | Ubicaciones FSM |
| fsm.order.asset.technician | 4 (List, Form, Search, Kanban) | 0 | 20+ | Asignaciones Múltiples |

**Total:** 8 vistas nuevas, 4 vistas heredadas, 80+ campos PATCO implementados

---

*📅 Documento generado automáticamente - Enero 2025*  
*🏢 PATCO - Gestión Avanzada de Servicios de Campo*