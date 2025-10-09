# Vistas Actuales - PATCO Timesheet

**Versión:** 18.0.1.0.0  
**Fecha de análisis:** Enero 2025  

## 1. Estructura de Menús

### 1.1 Menús Activos

#### 1.1.1 Control de Tiempo FSM (Principal)
- **ID:** `menu_patco_timesheet_fsm`
- **Acción:** `action_hr_timesheet_fsm`
- **Ubicación:** `fieldservice.menu_fieldservice_root`
- **Secuencia:** 30
- **Descripción:** Menú principal para el registro de tiempo FSM integrado en el módulo Field Service

#### 1.1.2 Tiempo FSM (Alternativo)
- **ID:** `menu_patco_timesheet_project`
- **Acción:** `action_hr_timesheet_fsm`
- **Ubicación:** `project.menu_project_management`
- **Secuencia:** 15
- **Descripción:** Acceso alternativo desde el menú de Proyectos para registros de tiempo FSM

### 1.2 Menús Deshabilitados (Comentados)

#### 1.2.1 Registro de Tiempo FSM (Raíz)
- **ID:** `menu_timesheet_fsm_root`
- **Ubicación:** `hr_timesheet.timesheet_menu_root`
- **Secuencia:** 30
- **Estado:** Comentado en `menu_views.xml`

#### 1.2.2 Submenús Deshabilitados
- **Mis Registros:** `menu_timesheet_fsm_entries` → `action_hr_timesheet_fsm`
- **Análisis de Tiempo:** `menu_timesheet_fsm_analysis` → `action_timesheets_analysis_report_fsm`
- **Tiempo FSM:** `menu_hr_timesheet_fsm` → `action_hr_timesheet_fsm`

## 2. Acciones Implementadas

### 2.1 Acción Principal: Registro de Tiempo FSM

- **ID:** `action_hr_timesheet_fsm`
- **Modelo:** `account.analytic.line`
- **Modos de Vista:** `list,form`
- **Dominio:** `[('project_id', '!=', False)]`
- **Contexto:** 
  ```python
  {
      'search_default_fsm_timesheets': 1,
      'default_project_id': ref('patco_timesheet.project_fsm_default'),
  }
  ```
- **Descripción:** Gestión de registros de tiempo con integración FSM y sistema de timer

### 2.2 Acción de Análisis (Deshabilitada)

- **ID:** `action_timesheets_analysis_report_fsm`
- **Modelo:** `timesheets.analysis.report`
- **Modos de Vista:** `graph,pivot,list`
- **Contexto:**
  ```python
  {
      'search_default_fsm_only': 1,
      'search_default_group_fsm_customer': 1,
  }
  ```
- **Estado:** Definida en archivo `.disabled`

## 3. Vistas Implementadas

### 3.1 Vista de Lista: Timesheet FSM

- **ID:** `hr_timesheet_line_list_fsm`
- **Modelo:** `account.analytic.line`
- **Vista Heredada:** `hr_timesheet.hr_timesheet_line_tree`
- **Propósito:** Lista extendida de registros de tiempo con campos FSM

**Campos Agregados:**

| Campo | Tipo | Descripción | Origen |
|-------|------|-------------|--------|
| `fsm_order_id` | Many2one | Orden de servicio FSM asociada | **PATCO** |
| `fsm_location` | Char | Ubicación del servicio (campo relacionado) | **PATCO** |
| `fsm_customer` | Char | Cliente FSM (campo relacionado) | **PATCO** |
| `is_timer_running` | Boolean | Estado del timer (campo computado) | **PATCO** |

**Campos Heredados de la Vista Base:**

| Campo | Tipo | Descripción | Origen |
|-------|------|-------------|--------|
| `date` | Date | Fecha del registro de tiempo | **Odoo Core** |
| `name` | Char | Descripción del trabajo realizado | **Odoo Core** |
| `project_id` | Many2one | Proyecto asociado | **Odoo Core** |
| `task_id` | Many2one | Tarea específica del proyecto | **Odoo Core** |
| `unit_amount` | Float | Horas trabajadas | **Odoo Core** |
| `employee_id` | Many2one | Empleado que registra el tiempo | **Odoo Core** |
| `user_id` | Many2one | Usuario responsable | **Odoo Core** |
| `company_id` | Many2one | Compañía | **Odoo Core** |

### 3.2 Vista de Formulario: Timesheet FSM

- **ID:** `hr_timesheet_line_form_fsm`
- **Modelo:** `account.analytic.line`
- **Vista Heredada:** `hr_timesheet.hr_timesheet_line_form`
- **Propósito:** Formulario extendido con campos FSM y funcionalidades de timer

**Campos Agregados:**

| Campo | Tipo | Descripción | Origen | Ubicación |
|-------|------|-------------|--------|-----------|
| `fsm_order_id` | Many2one | Orden de servicio FSM | **PATCO** | Después de `project_id` |
| `fsm_location` | Char | Ubicación FSM (solo lectura) | **PATCO** | Después de `name` |
| `fsm_customer` | Char | Cliente FSM (solo lectura) | **PATCO** | Después de `name` |
| `date_time` | Datetime | Hora de inicio del timer (solo lectura) | **PATCO** | Después de `unit_amount` |
| `is_timer_running` | Boolean | Estado del timer (invisible) | **PATCO** | Después de `unit_amount` |

**Campos Heredados de la Vista Base:**

| Campo | Tipo | Descripción | Origen |
|-------|------|-------------|--------|
| `date` | Date | Fecha del registro | **Odoo Core** |
| `name` | Char | Descripción del trabajo | **Odoo Core** |
| `project_id` | Many2one | Proyecto | **Odoo Core** |
| `task_id` | Many2one | Tarea | **Odoo Core** |
| `unit_amount` | Float | Cantidad de horas | **Odoo Core** |
| `employee_id` | Many2one | Empleado | **Odoo Core** |
| `user_id` | Many2one | Usuario | **Odoo Core** |
| `company_id` | Many2one | Compañía | **Odoo Core** |

### 3.3 Vista de Búsqueda: Timesheet FSM

- **ID:** `hr_timesheet_line_search_fsm`
- **Modelo:** `account.analytic.line`
- **Vista Heredada:** `hr_timesheet.hr_timesheet_line_search`
- **Propósito:** Búsqueda extendida con filtros y agrupaciones FSM

**Campos de Búsqueda Agregados:**

| Campo | Descripción | Origen |
|-------|-------------|--------|
| `fsm_order_id` | Búsqueda por orden FSM | **PATCO** |
| `fsm_location` | Búsqueda por ubicación | **PATCO** |
| `fsm_customer` | Búsqueda por cliente FSM | **PATCO** |

**Filtros Agregados:**

| Filtro | ID | Dominio | Descripción |
|--------|----|---------| ------------|
| Con Orden FSM | `fsm_timesheets` | `[('fsm_order_id', '!=', False)]` | Solo registros con orden FSM |
| Timer Activo | `timer_active` | `[('date_time', '!=', False), ('unit_amount', '=', 0)]` | Registros con timer corriendo |

**Agrupaciones Agregadas:**

| Agrupación | ID | Campo | Descripción |
|------------|----| ------|-------------|
| Orden FSM | `groupby_fsm_order` | `fsm_order_id` | Agrupa por orden de servicio |
| Cliente FSM | `groupby_fsm_customer` | `fsm_customer` | Agrupa por cliente |

**Filtros y Agrupaciones Heredados:**

| Elemento | Descripción | Origen |
|----------|-------------|--------|
| Filtro por fecha | Filtros de período | **Odoo Core** |
| Filtro por proyecto | Filtros por proyecto | **Odoo Core** |
| Filtro por empleado | Filtros por empleado | **Odoo Core** |
| Agrupación por proyecto | `groupby_project` | **Odoo Core** |
| Agrupación por empleado | `groupby_employee` | **Odoo Core** |
| Agrupación por fecha | `groupby_date` | **Odoo Core** |

### 3.4 Vistas de Análisis (Deshabilitadas)

#### 3.4.1 Vista de Lista de Análisis
- **ID:** `view_timesheets_analysis_report_list_fsm`
- **Modelo:** `timesheets.analysis.report`
- **Vista Heredada:** `hr_timesheet.view_timesheets_analysis_report_list`
- **Estado:** Archivo `.disabled`

#### 3.4.2 Vista de Búsqueda de Análisis
- **ID:** `view_timesheets_analysis_report_search_fsm`
- **Modelo:** `timesheets.analysis.report`
- **Vista Heredada:** `hr_timesheet.view_timesheets_analysis_report_search`
- **Estado:** Archivo `.disabled`

#### 3.4.3 Vista de Gráfico de Análisis
- **ID:** `view_timesheets_analysis_report_graph_fsm`
- **Modelo:** `timesheets.analysis.report`
- **Vista Heredada:** `hr_timesheet.view_timesheets_analysis_report_graph`
- **Estado:** Archivo `.disabled`

#### 3.4.4 Vista de Pivot de Análisis
- **ID:** `view_timesheets_analysis_report_pivot_fsm`
- **Modelo:** `timesheets.analysis.report`
- **Vista Heredada:** `hr_timesheet.view_timesheets_analysis_report_pivot`
- **Estado:** Archivo `.disabled`

## 4. Modelos y Campos Implementados

### 4.1 account.analytic.line (Extensión)

| Campo | Tipo | Descripción | Origen | Funcionalidad |
|-------|------|-------------|--------|---------------|
| `date` | Date | Fecha del registro | **Odoo Core** | Campo base heredado |
| `name` | Char | Descripción del trabajo | **Odoo Core** | Campo base heredado |
| `project_id` | Many2one | Proyecto asociado | **Odoo Core** | Campo base heredado |
| `task_id` | Many2one | Tarea del proyecto | **Odoo Core** | Campo base heredado |
| `unit_amount` | Float | Horas trabajadas | **Odoo Core** | Campo base heredado |
| `employee_id` | Many2one | Empleado | **Odoo Core** | Campo base heredado |
| `user_id` | Many2one | Usuario | **Odoo Core** | Campo base heredado |
| `company_id` | Many2one | Compañía | **Odoo Core** | Campo base heredado |
| `fsm_order_id` | Many2one | Orden de servicio FSM | **PATCO** | Vinculación con FSM |
| `date_time` | Datetime | Hora de inicio del timer | **PATCO** | Control de timer |
| `fsm_location` | Char | Ubicación del servicio | **PATCO** | Campo relacionado (computed) |
| `fsm_customer` | Char | Cliente FSM | **PATCO** | Campo relacionado (computed) |
| `is_timer_running` | Boolean | Estado del timer | **PATCO** | Campo computado |

### 4.2 timesheets.analysis.report (Extensión)

| Campo | Tipo | Descripción | Origen | Funcionalidad |
|-------|------|-------------|--------|---------------|
| `date` | Date | Fecha del análisis | **Odoo Core** | Campo base heredado |
| `project_id` | Many2one | Proyecto | **Odoo Core** | Campo base heredado |
| `task_id` | Many2one | Tarea | **Odoo Core** | Campo base heredado |
| `unit_amount` | Float | Horas totales | **Odoo Core** | Campo base heredado |
| `employee_id` | Many2one | Empleado | **Odoo Core** | Campo base heredado |
| `user_id` | Many2one | Usuario | **Odoo Core** | Campo base heredado |
| `company_id` | Many2one | Compañía | **Odoo Core** | Campo base heredado |
| `fsm_order_id` | Many2one | Orden FSM | **PATCO** | Análisis por orden FSM |
| `fsm_location` | Char | Ubicación FSM | **PATCO** | Análisis por ubicación |
| `fsm_customer` | Char | Cliente FSM | **PATCO** | Análisis por cliente |

## 5. Funcionalidades Especiales

### 5.1 Sistema de Timer Integrado

**Métodos Implementados:**
- `action_start_timer()`: Inicia el timer con validaciones
- `action_stop_timer()`: Detiene el timer y calcula duración
- `_compute_timer_running()`: Determina estado del timer

**Características:**
- Timer en tiempo real con cálculo automático de duración
- Validaciones para prevenir timers duplicados
- Notificaciones de feedback al usuario
- Estado visual del timer en interfaces

### 5.2 Integración FSM Automática

**Funcionalidades:**
- Vinculación automática con órdenes de servicio FSM
- Información contextual de ubicación y cliente
- Creación automática de proyecto "Servicios de Campo"
- Asignación inteligente de proyectos FSM

### 5.3 Validaciones y Controles

**Validaciones Implementadas:**
- Prevención de timers duplicados activos
- Validación de estados de timer
- Control de acceso por permisos de usuario
- Verificación de integridad de datos FSM

## 6. Dependencias y Relaciones

### 6.1 Módulos Requeridos
- `patco_base`: Funcionalidades base de PATCO
- `hr_timesheet`: Sistema de timesheet de Odoo
- `fieldservice`: Gestión de servicios de campo

### 6.2 Integraciones
- **patco_fsm**: Órdenes de servicio de campo
- **project**: Gestión de proyectos
- **hr**: Gestión de empleados
- **base**: Funcionalidades básicas de Odoo

### 6.3 Modelos Relacionados
- `fsm.order`: Órdenes de servicio de campo
- `fsm.location`: Ubicaciones de servicio
- `res.partner`: Clientes y contactos
- `project.project`: Proyectos
- `project.task`: Tareas de proyecto
- `hr.employee`: Empleados