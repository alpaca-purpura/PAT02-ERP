## Estructura Detallada del Menú

### Menú Principal: "Gestión de Habilidades"
- **ID del menú**: `menu_skills_management`
- **Acción**: Ninguna (menú padre)
- **Descripción**: Menú principal para el sistema de gestión de habilidades técnicas

### Submenús y Opciones

#### 1. Configuración (`menu_skills_config`)
Submenú para la configuración básica del sistema de habilidades.

##### 1.1 Tipos de Habilidades
- **ID del menú**: `menu_hr_skill_type`
- **Acción**: `action_hr_skill_type`
- **Modelo**: `hr.skill.type`
- **Descripción**: Gestión de categorías de habilidades (COC, REF, LAV, ELEC, FONT)

**Vistas implementadas:**
- **Vista Lista** (`view_hr_skill_type_list`):
  - **Propósito**: Visualización tabular de tipos de habilidades
  - **Campos mostrados**:
    - `name` (Nombre) - *Origen: Odoo Core hr_skills*
    - `code` (Código) - *Origen: patco_skills_mgmt*
    - `skill_count` (Cantidad de Habilidades) - *Origen: patco_skills_mgmt*
    - `active` (Activo) - *Origen: patco_skills_mgmt*

- **Vista Formulario** (`view_hr_skill_type_form`):
  - **Propósito**: Creación y edición de tipos de habilidades
  - **Campos mostrados**:
    - `name` (Nombre) - *Origen: Odoo Core hr_skills*
    - `code` (Código) - *Origen: patco_skills_mgmt*
    - `description` (Descripción) - *Origen: patco_skills_mgmt*
    - `active` (Activo) - *Origen: patco_skills_mgmt*

##### 1.2 Niveles de Habilidades
- **ID del menú**: `menu_hr_skill_level`
- **Acción**: `action_hr_skill_level`
- **Modelo**: `hr.skill.level`
- **Descripción**: Definición de niveles de competencia (N1-Básico, N2-Intermedio, N3-Avanzado)

**Vistas implementadas:**
- **Vista Lista** (`view_hr_skill_level_list`):
  - **Propósito**: Visualización de niveles de habilidades
  - **Campos mostrados**:
    - `name` (Nombre) - *Origen: Odoo Core hr_skills*
    - `level_progress` (Progreso del Nivel) - *Origen: Odoo Core hr_skills*
    - `active` (Activo) - *Origen: patco_skills_mgmt*

- **Vista Formulario** (`view_hr_skill_level_form`):
  - **Propósito**: Configuración de niveles de competencia
  - **Campos mostrados**:
    - `name` (Nombre) - *Origen: Odoo Core hr_skills*
    - `level_progress` (Progreso del Nivel) - *Origen: Odoo Core hr_skills*
    - `description` (Descripción) - *Origen: patco_skills_mgmt*
    - `active` (Activo) - *Origen: patco_skills_mgmt*

##### 1.3 Habilidades
- **ID del menú**: `menu_hr_skill`
- **Acción**: `action_hr_skill`
- **Modelo**: `hr.skill`
- **Descripción**: Catálogo completo de habilidades técnicas específicas

**Vistas implementadas:**
- **Vista Lista** (`view_hr_skill_list`):
  - **Propósito**: Listado de habilidades disponibles
  - **Campos mostrados**:
    - `name` (Nombre) - *Origen: Odoo Core hr_skills*
    - `code` (Código) - *Origen: patco_skills_mgmt*
    - `skill_type_id` (Tipo de Habilidad) - *Origen: Odoo Core hr_skills*
    - `employee_count` (Cantidad de Empleados) - *Origen: patco_skills_mgmt*
    - `active` (Activo) - *Origen: patco_skills_mgmt*

- **Vista Formulario** (`view_hr_skill_form`):
  - **Propósito**: Creación y edición de habilidades
  - **Campos mostrados**:
    - `name` (Nombre) - *Origen: Odoo Core hr_skills*
    - `code` (Código) - *Origen: patco_skills_mgmt*
    - `skill_type_id` (Tipo de Habilidad) - *Origen: Odoo Core hr_skills*
    - `description` (Descripción) - *Origen: patco_skills_mgmt*
    - `active` (Activo) - *Origen: patco_skills_mgmt*

- **Vista Búsqueda** (`view_hr_skill_search`):
  - **Propósito**: Filtrado y búsqueda de habilidades
  - **Filtros disponibles**: Activas, Inactivas, Agrupación por tipo

##### 1.4 Habilidades de Empleados
- **ID del menú**: `menu_hr_employee_skill`
- **Acción**: `action_hr_employee_skill`
- **Modelo**: `hr.employee.skill`
- **Descripción**: Gestión de competencias asignadas a empleados

**Vistas implementadas:**
- **Vista Lista** (`view_hr_employee_skill_list`):
  - **Propósito**: Visualización de habilidades por empleado
  - **Campos mostrados**:
    - `employee_id` (Empleado) - *Origen: Odoo Core hr_skills*
    - `skill_id` (Habilidad) - *Origen: Odoo Core hr_skills*
    - `skill_type_id` (Tipo de Habilidad) - *Origen: Odoo Core hr_skills*
    - `skill_level_id` (Nivel de Habilidad) - *Origen: Odoo Core hr_skills*
    - `level_progress` (Progreso del Nivel) - *Origen: Odoo Core hr_skills*
    - `is_certified` (Certificado) - *Origen: patco_skills_mgmt*
    - `certification_date` (Fecha de Certificación) - *Origen: patco_skills_mgmt*
    - `date_start` (Fecha de Inicio) - *Origen: patco_skills_mgmt*
    - `date_end` (Fecha de Fin) - *Origen: patco_skills_mgmt*

- **Vista Formulario** (`view_hr_employee_skill_form`):
  - **Propósito**: Registro detallado de habilidades de empleados
  - **Campos mostrados**:
    - `employee_id` (Empleado) - *Origen: Odoo Core hr_skills*
    - `skill_id` (Habilidad) - *Origen: Odoo Core hr_skills*
    - `skill_type_id` (Tipo de Habilidad) - *Origen: Odoo Core hr_skills*
    - `skill_level_id` (Nivel de Habilidad) - *Origen: Odoo Core hr_skills*
    - `level_progress` (Progreso del Nivel) - *Origen: Odoo Core hr_skills*
    - `is_certified` (Certificado) - *Origen: patco_skills_mgmt*
    - `certification_date` (Fecha de Certificación) - *Origen: patco_skills_mgmt*
    - `certification_body` (Entidad Certificadora) - *Origen: patco_skills_mgmt*
    - `date_start` (Fecha de Inicio) - *Origen: patco_skills_mgmt*
    - `date_end` (Fecha de Fin) - *Origen: patco_skills_mgmt*
    - `notes` (Notas) - *Origen: patco_skills_mgmt*

- **Vista Búsqueda** (`view_hr_employee_skill_search`):
  - **Propósito**: Filtrado de habilidades de empleados
  - **Filtros disponibles**: Certificadas, No certificadas, Activas, Vencidas

##### 1.5 Historial de Habilidades
- **ID del menú**: `menu_hr_employee_skill_log`
- **Acción**: `action_hr_employee_skill_log`
- **Modelo**: `hr.employee.skill.log`
- **Descripción**: Seguimiento de cambios en habilidades de empleados

**Vistas implementadas:**
- **Vista Lista** (`view_hr_employee_skill_log_list`):
  - **Propósito**: Historial de cambios en habilidades
  - **Campos mostrados**:
    - `date` (Fecha) - *Origen: patco_skills_mgmt*
    - `employee_id` (Empleado) - *Origen: patco_skills_mgmt*
    - `department_id` (Departamento) - *Origen: patco_skills_mgmt*
    - `skill_id` (Habilidad) - *Origen: patco_skills_mgmt*
    - `skill_type_id` (Tipo de Habilidad) - *Origen: patco_skills_mgmt*
    - `old_level_progress` (Nivel Anterior) - *Origen: patco_skills_mgmt*
    - `new_level_progress` (Nivel Nuevo) - *Origen: patco_skills_mgmt*
    - `change_type` (Tipo de Cambio) - *Origen: patco_skills_mgmt*

- **Vista Formulario** (`view_hr_employee_skill_log_form`):
  - **Propósito**: Detalle de cambios registrados
  - **Campos mostrados**: Todos los campos del modelo más `notes` (Notas)

#### 2. Empleados (`menu_skills_employees`)
Submenú para la gestión de empleados y técnicos.

##### 2.1 Técnicos de Campo
- **ID del menú**: `menu_field_technicians`
- **Acción**: `action_field_technicians`
- **Modelo**: `hr.employee`
- **Descripción**: Gestión específica de técnicos de campo

**Vistas heredadas:**

- **Vista Formulario Heredada** (`view_employee_form_skills`):
  - **Vista origen**: `hr.view_employee_form` (Odoo Core HR)
  - **Propósito**: Añadir gestión de habilidades técnicas a empleados
  - **Campos añadidos**:
    - `is_field_technician` (Es Técnico de Campo) - *Origen: patco_skills_mgmt*
    - `main_skills` (Habilidades Principales) - *Origen: patco_skills_mgmt*
    - `employee_skill_ids` (Habilidades del Empleado) - *Origen: Odoo Core hr_skills extendido*
    - `fsm_person_id` (Persona FSM) - *Origen: patco_skills_mgmt*
    - `fsm_sync_date` (Fecha de Sincronización FSM) - *Origen: patco_skills_mgmt*
    - `fsm_sync_status` (Estado de Sincronización FSM) - *Origen: patco_skills_mgmt*
  - **Funcionalidades añadidas**:
    - Botones de sincronización con FSM
    - Pestaña "Habilidades Técnicas"
    - Matriz de competencias técnicas

- **Vista Lista Heredada** (`view_hr_employee_list_skills_and_fsm_integration`):
  - **Vista origen**: `hr.view_employee_tree` (Odoo Core HR)
  - **Propósito**: Mostrar información de habilidades en la lista de empleados
  - **Campos añadidos**:
    - `is_field_technician` (Técnico) - *Origen: patco_skills_mgmt*
    - `main_skills` (Habilidades Principales) - *Origen: patco_skills_mgmt*
    - `fsm_sync_status` (Estado FSM) - *Origen: patco_skills_mgmt*
    - `fsm_person_id` (Persona FSM) - *Origen: patco_skills_mgmt*

- **Vista Búsqueda Heredada** (`view_employee_filter_skills`):
  - **Vista origen**: `hr.view_employee_filter` (Odoo Core HR)
  - **Propósito**: Filtros específicos para técnicos de campo
  - **Filtros añadidos**:
    - "Técnicos de Campo" - Filtra empleados marcados como técnicos

#### 3. Órdenes de Servicio (`menu_skills_fsm`)
Submenú para la integración con Field Service Management.

##### 3.1 Órdenes con Habilidades
- **ID del menú**: `menu_fsm_orders_with_skills`
- **Acción**: `action_fsm_orders_with_skills`
- **Modelo**: `fsm.order`
- **Descripción**: Órdenes de servicio que requieren habilidades específicas

**Vistas heredadas:**

- **Vista Formulario Heredada** (`view_fsm_order_form_skills_text`):
  - **Vista origen**: `fieldservice.fsm_order_form` (OCA Field Service)
  - **Propósito**: Añadir campo de habilidades requeridas a órdenes FSM
  - **Campos añadidos**:
    - `required_skills` (Habilidades Requeridas) - *Origen: patco_skills_mgmt*

##### 3.2 Órdenes Mal Emparejadas
- **ID del menú**: `menu_fsm_orders_mismatched`
- **Acción**: `action_fsm_orders_mismatched`
- **Modelo**: `fsm.order`
- **Descripción**: Órdenes donde el técnico asignado no tiene las habilidades requeridas

#### 4. Reportes (`menu_skills_reports`)
Submenú para reportes y análisis (actualmente vacío, preparado para futuras extensiones).

### Integración con Menús Externos

#### Menú HR (Recursos Humanos)
- **Técnicos de Campo** (`menu_field_technicians`): Acceso directo desde el menú principal de HR
- **Habilidades de Empleados** (`menu_employee_skills`): Gestión de habilidades desde HR

### Campos Computados y Funcionalidades Especiales

#### Campos Computados en `hr.employee`:
- `main_skills`: Calcula automáticamente las habilidades principales del empleado
- `fsm_sync_status`: Estado de sincronización con el sistema FSM

#### Campos Computados en `fsm.order`:
- `technician_skill_match`: Verifica si el técnico tiene las habilidades requeridas
- `missing_skills`: Lista de habilidades faltantes del técnico asignado

#### Métodos de Sincronización:
- `action_sync_to_fsm_person()`: Sincroniza empleado con persona FSM
- `action_sync_skills_to_fsm()`: Sincroniza habilidades del empleado con FSM

### Acciones de Servidor Configuradas

1. **Sincronización Masiva FSM**: `action_sync_all_field_technicians_server`
2. **Sincronización Empleados Seleccionados**: `action_sync_selected_employees_server`
3. **Sincronización Individual FSM**: `action_sync_to_fsm_person_server`
4. **Sincronización de Habilidades**: `action_sync_skills_to_fsm_server`

---

**Versión**: 18.0.1.0.0  
**Autor**: PATCO  
**Licencia**: LGPL-3  
**Categoría**: Human Resources / Field Service