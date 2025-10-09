
## Estructura Detallada del Menú

### 📋 Menú Principal: Gestión de Activos y Manuales

**ID del Menú:** `menu_patco_asset`  
**Nombre:** "Gestión de Activos y Manuales"  
**Icono:** PATCO Logo (`patco_equipment,static/src/img/PATCO-Logo.png`)  
**Secuencia:** 10  
**Descripción:** Menú principal que agrupa todas las funcionalidades de gestión de activos de clientes, categorías, checklists y documentación técnica.

---

### 🔧 Opción 1: Activos de Clientes

**ID del Menú:** `menu_patco_asset_management`  
**Acción:** `action_maintenance_equipment_patco`  
**Modelo:** `maintenance.equipment`  
**Secuencia:** 20  
**Funcionalidad:** Gestión completa de equipos de clientes con códigos PATCO, QR, trazabilidad de servicios y métricas avanzadas.

#### Vistas Llamadas por la Acción

##### 1. Vista Lista - `view_maintenance_equipment_list_patco`
**Propósito:** Visualización tabular de todos los activos de clientes con filtros y métricas  
**Tipo:** Vista nueva (no heredada)  
**Campos Implementados:**

| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `name` | maintenance.equipment | Odoo Core | Nombre del activo |
| `x_patco_code` | maintenance.equipment | PATCO | Código único PATCO generado automáticamente |
| `category_id` | maintenance.equipment | Odoo Core | Categoría del equipo |
| `x_customer_id` | maintenance.equipment | PATCO | Cliente propietario del activo |
| `x_service_location_id` | maintenance.equipment | PATCO | Ubicación específica de servicio |
| `x_maintenance_state` | maintenance.equipment | PATCO | Estado operacional (draft/active/maintenance/retired) |
| `x_last_service_date` | maintenance.equipment | PATCO | Fecha del último servicio (computed) |
| `x_service_count` | maintenance.equipment | PATCO | Contador de servicios FSM (computed) |
| `x_ticket_count` | maintenance.equipment | PATCO | Contador de tickets de soporte (computed) |
| `x_fsm_order_count` | maintenance.equipment | PATCO | Contador de órdenes FSM (computed) |
| `x_assigned_technician_count` | maintenance.equipment | PATCO | Técnicos únicos asignados (computed) |
| `x_multi_asset_order_count` | maintenance.equipment | PATCO | Órdenes multi-activo (computed) |
| `company_id` | maintenance.equipment | Odoo Core | Compañía (oculto para filtros) |
| `create_date` | maintenance.equipment | Odoo Core | Fecha de creación (oculto para filtros) |

##### 2. Vista Formulario - `view_maintenance_equipment_form_patco`
**Propósito:** Formulario completo para creación y edición de activos con todas las funcionalidades PATCO  
**Tipo:** Vista nueva (no heredada)  
**Campos Implementados:**

**Grupo: Cliente y Ubicación**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `x_customer_id` | maintenance.equipment | PATCO | Cliente propietario con dominio de clientes |
| `x_service_location_id` | maintenance.equipment | PATCO | Ubicación de servicio con dominio por cliente |
| `x_installation_date` | maintenance.equipment | PATCO | Fecha de instalación del activo |

**Grupo: Datos Técnicos**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `category_id` | maintenance.equipment | Odoo Core | Categoría que determina checklists |
| `partner_id` | maintenance.equipment | Odoo Core | Fabricante/proveedor |
| `model` | maintenance.equipment | Odoo Core | Modelo específico del fabricante |
| `serial_no` | maintenance.equipment | Odoo Core | Número de serie único |
| `x_warranty_expiry` | maintenance.equipment | PATCO | Fecha de vencimiento de garantía |

**Grupo: Estado y Métricas**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `x_last_service_date` | maintenance.equipment | PATCO | Último servicio realizado (computed, readonly) |
| `x_service_count` | maintenance.equipment | PATCO | Total de servicios (computed, readonly) |
| `x_ticket_count` | maintenance.equipment | PATCO | Tickets activos (computed, readonly) |
| `x_fsm_order_count` | maintenance.equipment | PATCO | Órdenes FSM relacionadas (computed, readonly) |
| `x_assigned_technician_count` | maintenance.equipment | PATCO | Técnicos asignados (computed, readonly) |
| `x_multi_asset_order_count` | maintenance.equipment | PATCO | Órdenes multi-activo (computed, readonly) |

**Grupo: Acceso Móvil**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `x_qr_code` | maintenance.equipment | PATCO | Código QR binario generado automáticamente |
| `x_qr_url` | maintenance.equipment | PATCO | URL de acceso directo (computed, readonly) |

**Campos Adicionales en Notebook:**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `x_technical_specs` | maintenance.equipment | PATCO | Especificaciones técnicas detalladas |
| `x_operating_conditions` | maintenance.equipment | PATCO | Condiciones ambientales y operativas |
| `description` | maintenance.equipment | PATCO | Descripción general del equipo |

##### 3. Vista Búsqueda - `view_maintenance_equipment_search_patco`
**Propósito:** Filtros y agrupaciones específicas para activos PATCO  
**Tipo:** Vista heredada de `maintenance.hr_equipment_view_search`  
**Vista Origen:** `maintenance.hr_equipment_view_search` (Odoo Core)

**Campos de Búsqueda Agregados:**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `x_patco_code` | maintenance.equipment | PATCO | Búsqueda por código PATCO |
| `x_customer_id` | maintenance.equipment | PATCO | Búsqueda por cliente |

**Filtros Agregados:**
- `active_equipment`: Activos en estado activo
- `maintenance_equipment`: Activos en mantenimiento  
- `retired_equipment`: Activos retirados

**Agrupaciones Agregadas:**
- `group_customer`: Agrupar por cliente
- `group_maintenance_state`: Agrupar por estado PATCO

---

### 📂 Opción 2: Categorías, Checklists y Manuales

**ID del Menú:** `menu_patco_equipment_categories`  
**Acción:** `action_maintenance_equipment_category_patco`  
**Modelo:** `maintenance.equipment.category`  
**Secuencia:** 30  
**Funcionalidad:** Gestión de categorías de equipos con sistema de herencia inteligente, checklists HTML personalizables y base de conocimiento.

#### Vistas Llamadas por la Acción

##### 1. Vista Lista - `view_list_maintenance_equipment_category_inherit`
**Propósito:** Lista de categorías con información de herencia y documentación  
**Tipo:** Vista heredada de `maintenance.hr_equipment_category_view_tree`  
**Vista Origen:** `maintenance.hr_equipment_category_view_tree` (Odoo Core)

**Campos Heredados Mostrados:**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `name` | maintenance.equipment.category | Odoo Core | Nombre de la categoría |
| `color` | maintenance.equipment.category | Odoo Core | Color identificativo |

**Campos Agregados por PATCO:**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `x_knowledge_base_count` | maintenance.equipment.category | PATCO | Documentos propios de la categoría (computed) |
| `x_inherited_knowledge_count` | maintenance.equipment.category | PATCO | Documentos heredados de categorías padre (computed) |
| `x_inherit_checklists` | maintenance.equipment.category | PATCO | Indica si hereda checklists del padre |
| `x_inherit_knowledge_base` | maintenance.equipment.category | PATCO | Indica si hereda documentación del padre |

##### 2. Vista Formulario - `view_form_maintenance_equipment_category_new`
**Propósito:** Formulario completo para gestión de categorías con herencia y checklists  
**Tipo:** Vista nueva (no heredada)  
**Campos Implementados:**

**Grupo: Información General**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `name` | maintenance.equipment.category | Odoo Core | Nombre de la categoría |
| `parent_id` | maintenance.equipment.category | OCA (hierarchy) | Categoría padre para herencia |
| `complete_name` | maintenance.equipment.category | OCA (hierarchy) | Nombre completo jerárquico (computed) |
| `color` | maintenance.equipment.category | Odoo Core | Color identificativo |

**Grupo: Configuración de Herencia**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `x_inherit_checklists` | maintenance.equipment.category | PATCO | Heredar plantillas de checklist del padre |
| `x_inherit_knowledge_base` | maintenance.equipment.category | PATCO | Heredar documentación del padre |

**Página: Plantillas de Checklist**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `x_entry_checklist_template` | maintenance.equipment.category | PATCO | Plantilla HTML para checklist de entrada |
| `x_exit_checklist_template` | maintenance.equipment.category | PATCO | Plantilla HTML para checklist de salida |
| `x_effective_entry_checklist` | maintenance.equipment.category | PATCO | Plantilla efectiva de entrada (computed, readonly) |
| `x_effective_exit_checklist` | maintenance.equipment.category | PATCO | Plantilla efectiva de salida (computed, readonly) |

**Página: Base de Conocimiento**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `x_attachment_ids` | maintenance.equipment.category | PATCO | Documentos técnicos adjuntos |

**Botones Estadísticos:**
| Botón | Acción | Descripción |
|-------|--------|-------------|
| `action_view_knowledge_base` | Ver documentos | Acceso a documentación completa (propia + heredada) |
| `action_export_knowledge_base` | Exportar docs | Descarga masiva de documentación |

##### 3. Vista Kanban - `maintenance_equipment_category_view_kanban_inherit`
**Propósito:** Vista de tarjetas con información visual de herencia y documentación  
**Tipo:** Vista heredada de `maintenance.view_maintenance_equipment_category_kanban`  
**Vista Origen:** `maintenance.view_maintenance_equipment_category_kanban` (Odoo Core)

**Campos Heredados Mostrados:**
| Campo | Modelo | Origen | Descripción |
|-------|--------|--------|-------------|
| `name` | maintenance.equipment.category | Odoo Core | Nombre de la categoría |
| `color` | maintenance.equipment.category | Odoo Core | Color de fondo de la tarjeta |

**Elementos Agregados por PATCO:**
- **Badge "Propios"**: Muestra `x_knowledge_base_count` con icono de libro
- **Badge "Heredados"**: Muestra `x_inherited_knowledge_count` con icono de nivel
- **Badge "Hereda CL"**: Indica si `x_inherit_checklists` está activo
- **Botón "Ver Base"**: Acceso rápido a `action_view_knowledge_base`
- **Botón "Ver Heredados"**: Acceso a `action_view_inherited_knowledge_base`

---

### 🔗 Integraciones del Menú

#### Integración con FSM (Field Service Management)
- **Modelo Extendido:** `fsm.order`
- **Campos Agregados:** `x_equipment_id`, `x_equipment_ids`, `x_equipment_code`
- **Funcionalidad:** Vinculación directa entre activos y órdenes de servicio

#### Integración con Helpdesk
- **Modelo Extendido:** `helpdesk.ticket`  
- **Campos Agregados:** `x_equipment_id`, `x_equipment_code`, `x_fsm_order_id`
- **Funcionalidad:** Creación de tickets de soporte desde activos

#### Reportes Disponibles desde el Menú
1. **Etiquetas de Equipos** (`equipment_label_report`)
2. **Etiquetas QR** (`equipment_qr_labels`)
3. **Etiquetas QR Compactas** (`equipment_qr_labels_compact`)

---

### 📊 Características Especiales del Menú

#### Campos Computados en Tiempo Real
- **Contadores de Servicios**: Se actualizan automáticamente con cada nueva orden FSM
- **Métricas de Técnicos**: Calculan técnicos únicos asignados por activo
- **Fechas de Último Servicio**: Combinan datos de FSM y Helpdesk
- **Herencia Inteligente**: Las plantillas efectivas se calculan considerando la jerarquía

#### Automatizaciones Integradas
- **Generación de Códigos PATCO**: Secuencia automática al crear activos
- **Códigos QR**: Generación automática con URL de acceso directo
- **Validaciones**: Unicidad de número de serie por cliente
- **Sincronización**: Actualización automática de campos relacionados

#### Seguridad y Permisos
- **Grupo "Gestor de Activos"**: Acceso completo a todas las funcionalidades
- **Reglas por Cliente**: Los usuarios solo ven activos de sus clientes
- **Acceso Portal**: Clientes pueden ver sus propios activos (solo lectura)

Esta estructura de menú proporciona una gestión completa y profesional de activos de clientes, con funcionalidades avanzadas de trazabilidad, documentación y herencia inteligente, optimizada para empresas de servicios técnicos.