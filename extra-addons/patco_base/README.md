# PATCO Base Module

## 📋 **Descripción**

**PATCO Base** es el módulo fundamental del sistema de gestión de activos PATCO. Proporciona las funcionalidades base, modelos maestros, clasificaciones de servicio y el **sistema de permisos jerárquico** que utilizan todos los demás módulos PATCO.

## 🎯 **Funcionalidades Principales**

### **Clasificaciones de Servicio**
- **Naturaleza del Servicio** (`patco.service.nature`): M1-Correctivo, M2-Preventivo, M3-Instalación, M4-Inspección
- **Área del Servicio** (`patco.service.area`): COC-CAL, COC-PRE, REF-COM, AC, LAV, ELEC, FONT
- **Complejidad del Servicio** (`patco.service.complexity`): N1-Básico, N2-Intermedio, N3-Avanzado, N4-Crítico

### **Sistema de Permisos**
- **4 Roles Jerárquicos**: Técnico → Jefe de Operaciones → Administrativo → Gerente General
- **Restricciones de Datos**: Técnicos solo ven sus órdenes asignadas
- **Integración OCA**: Mapeo automático con grupos de Field Service, Helpdesk, Maintenance
- **Seguridad Granular**: Permisos CRUD específicos por modelo y rol

## 🏗️ **Modelos Principales**

### **Clasificaciones Base**
```python
# Naturaleza del Servicio
class PatcoServiceNature(models.Model):
    _name = 'patco.service.nature'
    code = fields.Char(required=True)  # M1, M2, M3, M4
    name = fields.Char(required=True)  # Correctivo, Preventivo, etc.

# Área del Servicio  
class PatcoServiceArea(models.Model):
    _name = 'patco.service.area'
    code = fields.Char(required=True)  # COC-CAL, REF-COM, etc.
    name = fields.Char(required=True)  # Cocina-Calor, Refrigeración, etc.

# Complejidad del Servicio
class PatcoServiceComplexity(models.Model):
    _name = 'patco.service.complexity'
    code = fields.Char(required=True)  # N1, N2, N3, N4
    name = fields.Char(required=True)  # Básico, Intermedio, etc.
```

## 🔐 **Sistema de Permisos**

### **Roles Principales**
1. **🔧 PATCO Técnico** (`group_patco_technician`)
   - Acceso limitado a órdenes asignadas
   - Puede crear activos y consumir repuestos de su furgoneta
   - Solo lectura de acuerdos relacionados

2. **👨‍💼 PATCO Jefe de Operaciones** (`group_patco_operations_manager`)
   - Control operativo completo (órdenes, tickets, activos)
   - Sin acceso a facturación
   - Puede crear usuarios técnicos

3. **📊 PATCO Administrativo** (`group_patco_administrative`)
   - Acceso completo incluyendo facturación
   - Puede crear todos los usuarios excepto administradores

4. **👑 PATCO Gerente General** (`group_patco_administrator`)
   - Superusuario sin restricciones
   - Acceso total al sistema

### **Archivos de Seguridad**
- `security/patco_security_groups.xml` - Definición de grupos
- `security/patco_record_rules.xml` - Reglas de restricción de datos
- `security/ir.model.access.csv` - Permisos CRUD por modelo
- **📖 [SECURITY.md](SECURITY.md)** - Documentación completa de permisos

## 📦 **Dependencias**

### **Odoo Core**
- `base`, `mail`, `contacts`, `stock`, `sale`, `account`, `hr`, `maintenance`

### **OCA Modules**
- `fieldservice` - Gestión de servicios de campo
- `fieldservice_stock` - Integración con inventario
- `hr_timesheet` - Registro de tiempos
- `partner_firstname` - Nombres estructurados
- `agreement` - Gestión de contratos
- `mail_debrand` - Eliminación de marca Odoo

## 🗂️ **Estructura de Archivos**

```
patco_base/
├── data/                          # Datos maestros
│   ├── patco_service_area_data.xml
│   ├── patco_service_complexity_data.xml
│   └── patco_service_nature_data.xml
├── models/                        # Modelos Python
│   ├── patco_service_area.py
│   ├── patco_service_complexity.py
│   └── patco_service_nature.py
├── security/                      # Configuración de seguridad
│   ├── patco_security_groups.xml  # Grupos de usuarios
│   ├── patco_record_rules.xml     # Reglas de datos
│   └── ir.model.access.csv        # Permisos de modelos
├── views/                         # Vistas XML
│   ├── patco_menus.xml
│   └── patco_*_views.xml
├── SECURITY.md                    # Documentación de permisos
└── README.md                      # Este archivo
```

## 🚀 **Instalación y Configuración**

### **Instalación**
```bash
# Instalar a través de patco_suite (recomendado)
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_suite --stop-after-init
```

### **Configuración Inicial**
1. **Datos Maestros**: Se cargan automáticamente las clasificaciones base
2. **Grupos de Usuario**: Asignar usuarios a los grupos PATCO apropiados
3. **Permisos**: Se aplican automáticamente según el rol asignado

### **Verificación**
- Acceder a **Configuración > PATCO > Clasificaciones**
- Verificar que aparezcan las áreas, naturalezas y complejidades
- Probar accesos con usuarios de diferentes roles

## 🔧 **Uso y Ejemplos**

### **Asignación de Roles**
```python
# Crear usuario técnico
user = self.env['res.users'].create({
    'name': 'Juan Pérez',
    'login': 'juan.perez',
    'groups_id': [(4, self.env.ref('patco_base.group_patco_technician').id)]
})

# El usuario automáticamente hereda todos los permisos de técnico
```

### **Uso en Otros Módulos**
```python
# En patco_fsm - Clasificar orden de servicio
fsm_order = self.env['fsm.order'].create({
    'name': 'Reparación Freidora',
    'x_service_nature_id': self.env.ref('patco_base.service_nature_m1').id,
    'x_service_area_id': self.env.ref('patco_base.service_area_coc_cal').id,
    'x_service_complexity_id': self.env.ref('patco_base.service_complexity_n2').id,
})
```

## 🔄 **Integración con Otros Módulos**

### **Módulos PATCO que Dependen**
- `patco_fsm` - Servicios de campo
- `patco_equipment` - Gestión de equipos
- `patco_ai_agent` - Agente de IA
- `patco_stock_fsm` - Stock para servicios
- `patco_timesheet` - Registro de tiempos

### **Extensiones Futuras**
- Nuevas clasificaciones de servicio
- Roles adicionales según necesidades del negocio
- Integraciones con módulos OCA adicionales

## 📊 **Reportes y Análisis**

### **Datos Disponibles**
- Distribución de servicios por naturaleza
- Análisis de complejidad por área
- Métricas de uso por clasificación

### **Integración con BI**
- Campos disponibles para reportes personalizados
- Compatibilidad con herramientas de análisis externas

## 🛠️ **Mantenimiento**

### **Actualización de Clasificaciones**
1. Editar archivos en `data/`
2. Actualizar módulo: `-u patco_base`
3. Verificar integridad de datos

### **Modificación de Permisos**
1. Consultar **[SECURITY.md](SECURITY.md)** para procedimientos
2. Probar en entorno de desarrollo
3. Documentar cambios realizados

## 📞 **Soporte**

### **Documentación Adicional**
- **[SECURITY.md](SECURITY.md)** - Sistema completo de permisos
- Documentación de módulos dependientes
- Guías de integración OCA

### **Resolución de Problemas**
1. Verificar dependencias instaladas
2. Revisar logs de Odoo para errores
3. Validar permisos de usuario
4. Consultar documentación de seguridad

---

**Versión**: 18.0.1.0.0  
**Compatibilidad**: Odoo 18 Community  
**Licencia**: LGPL-3  
**Autor**: PATCO Development Team

## Descripción

**PATCO Base** es el módulo fundamental del sistema PATCO que proporciona las funcionalidades base y modelos maestros para la gestión de servicios técnicos especializados. Este módulo establece la base sobre la cual se construyen todos los demás módulos del ecosistema PATCO.

## Funcionalidades Principales

### 🎯 Clasificación Operativa
- **Áreas de Especialización**: Clasificación de servicios por área técnica (Cocina-Lavandería, Refrigeración, A/C, Electromecánica)
- **Niveles de Complejidad**: Categorización de servicios por dificultad técnica (Básico, Intermedio, Avanzado, Crítico)
- **Naturaleza de Servicio**: Tipos de intervención técnica (Mantenimiento, Instalación, Reparación, Diagnóstico, Consultoría)

### 🔐 Sistema de Seguridad
- **Grupos de Usuario**: Estructura jerárquica de permisos (Técnico, Líder Técnico, Administrador)
- **Control de Acceso**: Permisos granulares por modelo y operación
- **Categoría de Módulo**: Organización específica para módulos PATCO

### 🎨 Interfaz de Usuario
- **Menú Principal**: "Configuración Operativa" con estructura organizada
- **Vistas Optimizadas**: Formularios, listas y búsquedas para cada modelo
- **Navegación Intuitiva**: Menús jerárquicos con secuenciación lógica

## Modelos de Datos

### 1. Área de Especialización (`patco.service.area`)
**Propósito**: Clasificar servicios por especialización técnica

**Campos principales**:
- `name`: Nombre del área (ej: "Cocina-Lavandería")
- `code`: Código corto (ej: "COC-LAV")
- `sequence`: Orden de visualización
- `description`: Descripción detallada
- `active`: Estado activo/inactivo

**Características**:
- Códigos y nombres únicos
- Visualización personalizada con formato `[CÓDIGO] Nombre`
- Ordenamiento por secuencia y nombre

### 2. Complejidad de Servicio (`patco.service.complexity`)
**Propósito**: Categorizar servicios por nivel de dificultad técnica

**Campos principales**:
- `name`: Nivel de complejidad (ej: "Básico")
- `code`: Código de nivel (ej: "N1")
- `sequence`: Orden de visualización
- `description`: Descripción del nivel
- `active`: Estado activo/inactivo

**Características**:
- Códigos y nombres únicos
- Visualización personalizada con formato `[CÓDIGO] Nombre`
- Ordenamiento por secuencia y nombre

### 3. Naturaleza de Servicio (`patco.service.nature`)
**Propósito**: Definir tipos de intervención técnica

**Campos principales**:
- `name`: Tipo de servicio (ej: "Mantenimiento")
- `code`: Código de tipo (ej: "M1")
- `sequence`: Orden de visualización
- `description`: Descripción del tipo
- `active`: Estado activo/inactivo

**Características**:
- Códigos y nombres únicos
- Visualización personalizada con formato `[CÓDIGO] Nombre`
- Ordenamiento por secuencia y nombre

## Datos Iniciales

### Áreas de Especialización Predefinidas
- **COC-LAV**: Cocina-Lavandería
- **REF**: Refrigeración
- **A/C**: Aire Acondicionado
- **ELEC**: Electromecánica
- **GAS**: Sistemas de Gas

### Niveles de Complejidad Predefinidos
- **N1**: Básico - Servicios rutinarios
- **N2**: Intermedio - Requiere experiencia
- **N3**: Avanzado - Alta especialización
- **N4**: Crítico - Máxima complejidad

### Naturalezas de Servicio Predefinidas
- **M1**: Mantenimiento - Preventivo y correctivo
- **I1**: Instalación - Equipos nuevos
- **R1**: Reparación - Equipos averiados
- **D1**: Diagnóstico - Evaluación técnica
- **C1**: Consultoría - Asesoramiento especializado

## Grupos de Seguridad

### Jerarquía de Permisos
1. **PATCO Technician**: Acceso básico de solo lectura
2. **PATCO Technical Leader**: Permisos de creación y edición (sin eliminación)
3. **PATCO Administrator**: Acceso completo (CRUD)

### Matriz de Permisos
| Grupo | Lectura | Escritura | Creación | Eliminación |
|-------|---------|-----------|----------|-------------|
| Técnico | ✅ | ❌ | ❌ | ❌ |
| Líder Técnico | ✅ | ✅ | ✅ | ❌ |
| Administrador | ✅ | ✅ | ✅ | ✅ |

## Dependencias

### Módulos Core de Odoo
- `base`: Funcionalidades básicas
- `product`: Gestión de productos
- `maintenance`: Mantenimiento de equipos

### Módulos OCA Integrados
- **partner-contact**: `partner_contact_access_link`
- **reporting-engine**: `report_xlsx`
- **web**: `web_responsive`, `web_favicon`, `web_company_color`, `web_quick_start_screen`, `web_dialog_size`, `web_refresher`, `web_search_with_and`
- **mail**: `mail_debrand`
- **server-brand**: `disable_odoo_online`
- **server-tool**: `base_name_search_improved`

## Estructura de Archivos

```
patco_base/
├── __manifest__.py          # Configuración del módulo
├── README.md               # Documentación (este archivo)
├── data/                   # Datos iniciales
│   ├── patco_general_data.xml
│   ├── patco_service_area_data.xml
│   ├── patco_service_complexity_data.xml
│   └── patco_service_nature_data.xml
├── models/                 # Modelos de datos
│   ├── __init__.py
│   ├── patco_service_area.py
│   ├── patco_service_complexity.py
│   └── patco_service_nature.py
├── security/              # Configuración de seguridad
│   ├── ir.model.access.csv
│   └── patco_security_groups.xml
├── static/src/img/        # Recursos estáticos
└── views/                 # Vistas de interfaz
    ├── patco_menus.xml
    ├── patco_service_area_views.xml
    ├── patco_service_complexity_views.xml
    └── patco_service_nature_views.xml
```

## Instalación y Configuración

### Requisitos Previos
- Odoo Community 18.0
- Módulos OCA especificados en dependencias

### Instalación
```bash
# Actualizar módulo
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -u patco_suite --stop-after-init

# Instalación completa del suite
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_suite --stop-after-init
```

### Configuración Post-Instalación
1. **Asignar Grupos de Usuario**: Configurar usuarios en los grupos PATCO apropiados
2. **Revisar Datos Maestros**: Verificar y ajustar áreas, complejidades y naturalezas según necesidades
3. **Personalizar Secuencias**: Ajustar el orden de visualización según preferencias

## Navegación en la Interfaz

### Acceso Principal
**Menú**: Configuración Operativa → Configuración → Clasificación Operativa

### Submenús Disponibles
- **Naturaleza de Servicio**: Gestión de tipos de intervención
- **Área de Especialización**: Gestión de áreas técnicas
- **Complejidad de Servicio**: Gestión de niveles de dificultad

## Integración con Otros Módulos

Este módulo base es utilizado por:
- **patco_equipment**: Gestión de equipos y activos
- **patco_fsm**: Integración con Field Service Management
- **patco_skills_mgmt**: Gestión de habilidades técnicas
- **patco_hr_fsm_integration**: Integración HR con FSM

## Notas Técnicas

### Convenciones de Código
- Nombres de campos en `snake_case`
- Códigos únicos por modelo
- Visualización personalizada con método `name_get()`
- Restricciones SQL para integridad de datos

### Consideraciones de Rendimiento
- Índices automáticos en campos `code` y `name`
- Ordenamiento optimizado por `sequence`
- Consultas eficientes con ORM de Odoo

### Mantenimiento
- Datos con `noupdate="1"` para preservar personalizaciones
- Estructura modular para fácil extensión
- Documentación actualizada con cada cambio

---

**Versión**: 18.0.1.0.0  
**Autor**: PATCO  
**Licencia**: LGPL-3  
**Sitio Web**: https://www.patco.pe

## 📋 **Documentación Detallada del Menú Implementado**

### 🎯 **1. Estructura del Menú Principal**

#### **Menú Raíz: Configuración Operativa**
- **ID del Menú**: `menu_patco_main`
- **Nombre**: "Configuración Operativa"
- **Icono**: `patco_base,static/src/img/PATCO-Logo.png`
- **Secuencia**: 10
- **Descripción**: Menú principal que agrupa todas las funcionalidades operativas del sistema PATCO

#### **Jerarquía de Menús**
```
Configuración Operativa (menu_patco_main)
├── Configuración (menu_patco_configuration) - Secuencia: 90
│   └── Clasificación Operativa (menu_patco_operational_classification) - Secuencia: 10
│       ├── Naturaleza de Servicio (menu_patco_service_nature) - Secuencia: 10
│       ├── Área de Especialización (menu_patco_service_area) - Secuencia: 20
│       └── Complejidad de Servicio (menu_patco_service_complexity) - Secuencia: 30
└── Registro de Tiempo (menu_patco_time_registration) - Secuencia: 20
```

---

### 🔧 **2. Opciones del Menú y sus Acciones**

#### **2.1 Naturaleza de Servicio**

##### **Información del Menú**
- **ID del Menú**: `menu_patco_service_nature`
- **ID de la Acción**: `action_patco_service_nature`
- **Modelo**: `patco.service.nature`
- **Modos de Vista**: `list,form`
- **Descripción**: Gestión de tipos de intervención técnica (Mantenimiento, Instalación, Reparación, etc.)

##### **Vistas Implementadas**

###### **Vista Lista (`view_patco_service_nature_list`)**
- **ID**: `view_patco_service_nature_list`
- **Propósito**: Mostrar listado de naturalezas de servicio con capacidad de ordenamiento
- **Ordenamiento**: Por `sequence` y `name`

**Campos Mostrados**:
| Campo | Modelo | Origen | Tipo | Características |
|-------|--------|--------|------|-----------------|
| `sequence` | `patco.service.nature` | Implementado en este módulo | Integer | Widget handle para reordenamiento |
| `code` | `patco.service.nature` | Implementado en este módulo | Char | Código único, requerido |
| `name` | `patco.service.nature` | Implementado en este módulo | Char | Nombre único, requerido, traducible |
| `description` | `patco.service.nature` | Implementado en este módulo | Text | Descripción detallada, traducible |
| `active` | `patco.service.nature` | Implementado en este módulo | Boolean | Estado activo/inactivo |

###### **Vista Formulario (`view_patco_service_nature_form`)**
- **ID**: `view_patco_service_nature_form`
- **Propósito**: Crear y editar naturalezas de servicio
- **Características**: Botón de archivo/desarchivar, campos agrupados

**Campos del Formulario**:
| Campo | Modelo | Origen | Tipo | Características |
|-------|--------|--------|------|-----------------|
| `active` | `patco.service.nature` | Implementado en este módulo | Boolean | Widget boolean_button con terminología "archive" |
| `name` | `patco.service.nature` | Implementado en este módulo | Char | Placeholder: "Nombre de la naturaleza del servicio" |
| `code` | `patco.service.nature` | Implementado en este módulo | Char | Placeholder: "Código corto" |
| `sequence` | `patco.service.nature` | Implementado en este módulo | Integer | Control de orden |
| `description` | `patco.service.nature` | Implementado en este módulo | Text | Placeholder: "Descripción detallada de la naturaleza del servicio" |

###### **Vista Búsqueda (`view_patco_service_nature_search`)**
- **ID**: `view_patco_service_nature_search`
- **Propósito**: Filtrar y buscar naturalezas de servicio
- **Características**: Búsqueda por nombre/código, filtros por estado, agrupación

**Campos de Búsqueda**:
| Campo | Modelo | Origen | Funcionalidad |
|-------|--------|--------|---------------|
| `name` | `patco.service.nature` | Implementado en este módulo | Búsqueda en nombre y código |
| `code` | `patco.service.nature` | Implementado en este módulo | Búsqueda específica por código |
| `description` | `patco.service.nature` | Implementado en este módulo | Búsqueda en descripción |

---

#### **2.2 Área de Especialización**

##### **Información del Menú**
- **ID del Menú**: `menu_patco_service_area`
- **ID de la Acción**: `action_patco_service_area`
- **Modelo**: `patco.service.area`
- **Modos de Vista**: `list,form`
- **Descripción**: Gestión de áreas técnicas especializadas (Cocina-Lavandería, Refrigeración, A/C, etc.)

##### **Vistas Implementadas**

###### **Vista Lista (`view_patco_service_area_list`)**
- **ID**: `view_patco_service_area_list`
- **Propósito**: Mostrar listado de áreas de servicio con capacidad de ordenamiento
- **Ordenamiento**: Por `sequence` y `name`

**Campos Mostrados**:
| Campo | Modelo | Origen | Tipo | Características |
|-------|--------|--------|------|-----------------|
| `sequence` | `patco.service.area` | Implementado en este módulo | Integer | Widget handle para reordenamiento |
| `code` | `patco.service.area` | Implementado en este módulo | Char | Código único, requerido |
| `name` | `patco.service.area` | Implementado en este módulo | Char | Nombre único, requerido, traducible |
| `description` | `patco.service.area` | Implementado en este módulo | Text | Descripción detallada, traducible |
| `active` | `patco.service.area` | Implementado en este módulo | Boolean | Estado activo/inactivo |

###### **Vista Formulario (`view_patco_service_area_form`)**
- **ID**: `view_patco_service_area_form`
- **Propósito**: Crear y editar áreas de servicio
- **Características**: Botón de archivo/desarchivar, campos agrupados

**Campos del Formulario**:
| Campo | Modelo | Origen | Tipo | Características |
|-------|--------|--------|------|-----------------|
| `active` | `patco.service.area` | Implementado en este módulo | Boolean | Widget boolean_button con terminología "archive" |
| `name` | `patco.service.area` | Implementado en este módulo | Char | Placeholder: "Nombre del área de servicio" |
| `code` | `patco.service.area` | Implementado en este módulo | Char | Placeholder: "Código corto" |
| `sequence` | `patco.service.area` | Implementado en este módulo | Integer | Control de orden |
| `description` | `patco.service.area` | Implementado en este módulo | Text | Placeholder: "Descripción detallada del área de especialización" |

###### **Vista Búsqueda (`view_patco_service_area_search`)**
- **ID**: `view_patco_service_area_search`
- **Propósito**: Filtrar y buscar áreas de servicio
- **Características**: Búsqueda por nombre/código, filtros por estado, agrupación

**Campos de Búsqueda**:
| Campo | Modelo | Origen | Funcionalidad |
|-------|--------|--------|---------------|
| `name` | `patco.service.area` | Implementado en este módulo | Búsqueda en nombre y código |
| `code` | `patco.service.area` | Implementado en este módulo | Búsqueda específica por código |
| `description` | `patco.service.area` | Implementado en este módulo | Búsqueda en descripción |

---

#### **2.3 Complejidad de Servicio**

##### **Información del Menú**
- **ID del Menú**: `menu_patco_service_complexity`
- **ID de la Acción**: `action_patco_service_complexity`
- **Modelo**: `patco.service.complexity`
- **Modos de Vista**: `list,form`
- **Descripción**: Gestión de niveles de complejidad técnica (Básico, Intermedio, Avanzado, Crítico)

##### **Vistas Implementadas**

###### **Vista Lista (`view_patco_service_complexity_list`)**
- **ID**: `view_patco_service_complexity_list`
- **Propósito**: Mostrar listado de niveles de complejidad con capacidad de ordenamiento
- **Ordenamiento**: Por `sequence` y `name`

**Campos Mostrados**:
| Campo | Modelo | Origen | Tipo | Características |
|-------|--------|--------|------|-----------------|
| `sequence` | `patco.service.complexity` | Implementado en este módulo | Integer | Widget handle para reordenamiento |
| `code` | `patco.service.complexity` | Implementado en este módulo | Char | Código único, requerido |
| `name` | `patco.service.complexity` | Implementado en este módulo | Char | Nombre único, requerido, traducible |
| `description` | `patco.service.complexity` | Implementado en este módulo | Text | Descripción detallada, traducible |
| `active` | `patco.service.complexity` | Implementado en este módulo | Boolean | Estado activo/inactivo |

###### **Vista Formulario (`view_patco_service_complexity_form`)**
- **ID**: `view_patco_service_complexity_form`
- **Propósito**: Crear y editar niveles de complejidad
- **Características**: Botón de archivo/desarchivar, campos agrupados

**Campos del Formulario**:
| Campo | Modelo | Origen | Tipo | Características |
|-------|--------|--------|------|-----------------|
| `active` | `patco.service.complexity` | Implementado en este módulo | Boolean | Widget boolean_button con terminología "archive" |
| `name` | `patco.service.complexity` | Implementado en este módulo | Char | Placeholder: "Nombre del nivel de complejidad" |
| `code` | `patco.service.complexity` | Implementado en este módulo | Char | Placeholder: "Código corto" |
| `sequence` | `patco.service.complexity` | Implementado en este módulo | Integer | Control de orden |
| `description` | `patco.service.complexity` | Implementado en este módulo | Text | Placeholder: "Descripción detallada del nivel de complejidad" |

###### **Vista Búsqueda (`view_patco_service_complexity_search`)**
- **ID**: `view_patco_service_complexity_search`
- **Propósito**: Filtrar y buscar niveles de complejidad
- **Características**: Búsqueda por nombre/código, filtros por estado, agrupación

**Campos de Búsqueda**:
| Campo | Modelo | Origen | Funcionalidad |
|-------|--------|--------|---------------|
| `name` | `patco.service.complexity` | Implementado en este módulo | Búsqueda en nombre y código |
| `code` | `patco.service.complexity` | Implementado en este módulo | Búsqueda específica por código |
| `description` | `patco.service.complexity` | Implementado en este módulo | Búsqueda en descripción |

---

### 🔄 **3. Herencia de Vistas**

#### **Vistas Base (Sin Herencia)**
Todas las vistas implementadas en este módulo son **vistas base** que no heredan de otras vistas existentes. Cada modelo (`patco.service.nature`, `patco.service.area`, `patco.service.complexity`) define sus propias vistas desde cero:

- **Vistas Lista**: Implementación completa con ordenamiento personalizado
- **Vistas Formulario**: Diseño específico con agrupación de campos y botones de acción
- **Vistas Búsqueda**: Filtros y agrupaciones específicas para cada modelo

#### **Patrón de Diseño Consistente**
Todas las vistas siguen el mismo patrón de diseño:
1. **Vista Lista**: Campos principales con handle de secuencia
2. **Vista Formulario**: Botón de archivo, campos agrupados, placeholders descriptivos
3. **Vista Búsqueda**: Filtros por estado activo/inactivo, agrupación por estado

---

### 📊 **4. Documentación Detallada de Campos**

#### **Campos Comunes a Todos los Modelos**

##### **Campo `name` (Char)**
- **Propósito**: Nombre descriptivo del elemento
- **Características**: Requerido, traducible, único
- **Ayuda**: Texto descriptivo específico por modelo
- **Restricción SQL**: `name_unique`

##### **Campo `code` (Char)**
- **Propósito**: Código corto para identificación rápida
- **Características**: Requerido, único
- **Ayuda**: Código alfanumérico para clasificación
- **Restricción SQL**: `code_unique`

##### **Campo `active` (Boolean)**
- **Propósito**: Control de estado activo/inactivo
- **Características**: Valor por defecto True
- **Ayuda**: "Si está desactivado, no aparecerá en las selecciones"
- **Widget**: `boolean_button` con terminología "archive"

##### **Campo `sequence` (Integer)**
- **Propósito**: Control de orden de visualización
- **Características**: Valor por defecto 10
- **Ayuda**: "Orden de aparición en las listas"
- **Widget**: `handle` en vistas lista para reordenamiento

##### **Campo `description` (Text)**
- **Propósito**: Descripción detallada del elemento
- **Características**: Traducible, opcional
- **Ayuda**: Texto específico por modelo para descripción detallada

#### **Método Personalizado `name_get()`**
Todos los modelos implementan un método personalizado `name_get()` que:
- **Formato de Visualización**: `[CÓDIGO] Nombre`
- **Propósito**: Mostrar código y nombre juntos en selecciones
- **Ejemplo**: `[M1] Mantenimiento`, `[COC-LAV] Cocina-Lavandería`

#### **Restricciones SQL**
Cada modelo implementa restricciones de unicidad:
```sql
('code_unique', 'UNIQUE(code)', 'El código debe ser único.')
('name_unique', 'UNIQUE(name)', 'El nombre debe ser único.')
```

#### **Configuración de Ordenamiento**
- **Orden por defecto**: `sequence, name`
- **Permite reordenamiento**: Sí, mediante widget handle en campo sequence
- **Optimización**: Índices automáticos en campos code y name

---

### 🎨 **5. Características de Interfaz de Usuario**

#### **Mensajes de Ayuda Contextuales**
Cada acción incluye mensajes de ayuda cuando no hay registros:
- **Icono**: Cara sonriente (`o_view_nocontent_smiling_face`)
- **Texto motivacional**: "¡Crea tu primer/primera [elemento]!"
- **Descripción funcional**: Explicación del propósito del modelo

#### **Filtros y Agrupaciones Estándar**
Todas las vistas de búsqueda incluyen:
- **Filtros por Estado**: Activos/Inactivos
- **Agrupación**: Por campo `active`
- **Búsqueda Inteligente**: Por nombre o código simultáneamente

#### **Navegación Optimizada**
- **Secuenciación Lógica**: Menús ordenados por importancia operativa
- **Iconografía Consistente**: Logo PATCO en menú principal
- **Jerarquía Clara**: Estructura de 3 niveles máximo

---

**Documentación actualizada**: Enero 2025  
**Versión del módulo**: 18.0.1.0.0  
**Compatibilidad**: Odoo Community 18.0