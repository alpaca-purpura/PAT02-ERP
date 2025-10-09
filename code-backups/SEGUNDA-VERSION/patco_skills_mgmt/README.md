# PATCO Skills Management

## Descripción

El módulo **PATCO Skills Management** es una extensión integral del sistema de gestión de habilidades de Odoo 18 Community, diseñado específicamente para empresas del sector HORECA (Hoteles, Restaurantes y Catering). Este módulo permite gestionar las competencias técnicas de los empleados y su integración con las órdenes de servicio de campo (Field Service Management).

## Funcionalidades Principales

### 🎯 Gestión de Habilidades Técnicas
- **Catálogo de habilidades HORECA**: Habilidades específicas para cocina, refrigeración, lavandería, sistemas eléctricos y fontanería
- **Niveles de competencia**: Sistema de 3 niveles (N1-Básico, N2-Intermedio, N3-Avanzado)
- **Certificaciones**: Registro de certificaciones con entidad certificadora y fechas
- **Historial de habilidades**: Seguimiento completo de la evolución de competencias

### 👥 Gestión de Empleados
- **Técnicos de campo**: Identificación y gestión de personal técnico
- **Matriz de habilidades**: Vista consolidada de competencias por empleado
- **Integración FSM**: Sincronización con el módulo Field Service Management
- **Reportes de competencias**: Estadísticas y análisis de habilidades

### 🔧 Integración con Field Service Management
- **Asignación inteligente**: Sugerencia de técnicos basada en habilidades requeridas
- **Validación de competencias**: Verificación de habilidades antes de asignación
- **Órdenes con habilidades**: Definición de requisitos técnicos por orden
- **Compatibilidad de habilidades**: Cálculo automático de porcentaje de compatibilidad

## Modelos Principales

### Extensiones de Habilidades (HR Skills)

#### `hr.skill.type` (Tipos de Habilidades)
- **Campos añadidos**: `code`, `description`, `skill_count`
- **Funcionalidad**: Categorización de habilidades con códigos únicos

#### `hr.skill.level` (Niveles de Habilidades)
- **Campos añadidos**: `description`, `active`
- **Funcionalidad**: Definición de niveles de competencia

#### `hr.skill` (Habilidades)
- **Campos añadidos**: `code`, `description`, `employee_count`, `active`
- **Funcionalidad**: Catálogo de habilidades técnicas específicas

#### `hr.employee.skill` (Habilidades de Empleados)
- **Campos añadidos**: `is_certified`, `certification_date`, `certification_body`, `date_start`, `date_end`, `date_acquired`, `notes`
- **Funcionalidad**: Registro detallado de competencias por empleado

#### `hr.employee.skill.log` (Historial de Habilidades)
- **Modelo nuevo**: Seguimiento de cambios en habilidades
- **Campos**: `employee_id`, `skill_id`, `skill_level_id`, `change_type`, `old_level_progress`, `new_level_progress`, `date`, `notes`

### Extensiones de Empleados

#### `hr.employee` (Empleados)
- **Campos añadidos**: `employee_skill_ids`, `main_skills`, `is_field_technician`, `fsm_order_ids`, `fsm_order_count`
- **Funcionalidad**: Gestión de técnicos de campo y sus competencias

### Extensiones FSM (Field Service Management)

#### `fsm.order` (Órdenes de Servicio)
- **Campos añadidos**: `required_skill_ids`, `required_skill_types`, `min_skill_level`, `technician_skill_match`, `missing_skills`, `suggested_technician_ids`
- **Funcionalidad**: Asignación inteligente basada en habilidades

#### `fsm.location` (Ubicaciones FSM)
- **Campos añadidos**: `default_skill_ids`, `skill_notes`
- **Funcionalidad**: Habilidades por defecto por ubicación

#### `fsm.equipment` (Equipos FSM)
- **Campos añadidos**: `required_skill_ids`, `skill_notes`
- **Funcionalidad**: Habilidades requeridas por tipo de equipo

## Datos Iniciales

### Tipos de Habilidades HORECA
| Código | Nombre | Descripción |
|--------|--------|-------------|
| COC | Cocina y Equipos de Cocción | Habilidades para equipos de cocina comercial |
| REF | Refrigeración y Conservación | Competencias en sistemas de refrigeración |
| LAV | Lavandería y Secado | Habilidades en equipos de lavandería comercial |
| ELEC | Sistemas Eléctricos | Competencias eléctricas y generadores |
| FONT | Fontanería y Plomería | Habilidades en sistemas de agua y gas |

### Niveles de Competencia
- **N1 - Básico**: Conocimientos fundamentales
- **N2 - Intermedio**: Competencia operativa
- **N3 - Avanzado**: Expertise y especialización

### Habilidades Específicas
- **Cocina**: COC-CAL (Calentadores), COC-PRE (Presión), COC-LAV (Lavavajillas)
- **Refrigeración**: REF-COM (Comercial), REF-AC (Aire Acondicionado)
- **Lavandería**: LAV-LAV (Lavadoras), LAV-SEC (Secadoras), LAV-PLA (Planchadoras)
- **Eléctrico**: ELEC-BT (Baja Tensión), ELEC-GEN (Generadores)
- **Fontanería**: FONT-AGUA (Sistemas de Agua), FONT-GAS (Sistemas de Gas)

### Estructura Organizacional
- **Departamentos**: Dirección, Administración, Operaciones, Servicio Técnico, Ventas
- **Puestos de trabajo**: Técnico Senior, Técnico Junior, Supervisor, Coordinador

## Configuración de Seguridad

### Permisos por Grupo
| Modelo | Grupo HR User | Grupo HR Manager |
|--------|---------------|------------------|
| hr.skill.type | Lectura/Escritura/Creación | Todos los permisos |
| hr.skill.level | Lectura/Escritura/Creación | Todos los permisos |
| hr.skill | Lectura/Escritura/Creación | Todos los permisos |
| hr.employee.skill | Lectura/Escritura/Creación | Todos los permisos |
| hr.employee.skill.log | Solo lectura | Todos los permisos |

## Dependencias

### Módulos Odoo Core
- `base`: Funcionalidades básicas de Odoo
- `hr`: Gestión de recursos humanos
- `hr_skills`: Sistema base de habilidades (Odoo 18)

### Módulos OCA
- `fieldservice`: Field Service Management
- `patco_base`: Módulo base de PATCO

## Estructura de Archivos

```
patco_skills_mgmt/
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── hr_skill.py              # Extensiones de habilidades
│   ├── hr_employee.py           # Extensiones de empleados
│   ├── fieldservice_integration.py  # Integración FSM básica
│   ├── fsm_order.py            # Extensiones de órdenes FSM
│   ├── fsm_location.py         # Extensiones de ubicaciones
│   └── fsm_equipment.py        # Extensiones de equipos
├── views/
│   ├── hr_skill_views.xml      # Vistas de habilidades
│   ├── hr_employee_views.xml   # Vistas de empleados
│   ├── fieldservice_views.xml  # Vistas FSM principales
│   ├── fsm_order_views.xml     # Vistas de órdenes FSM
│   ├── actions.xml             # Acciones del sistema
│   └── menu_views.xml          # Estructura de menús
├── data/
│   ├── hr_skill_type_data.xml  # Tipos de habilidades
│   ├── hr_skill_level_data.xml # Niveles de competencia
│   ├── hr_skill_data.xml       # Habilidades específicas
│   ├── hr_job_data.xml         # Puestos y departamentos
│   └── skill_types_data.xml    # Datos adicionales
├── demo/
│   └── demo_data.xml           # Datos de demostración
└── security/
    └── ir.model.access.csv     # Permisos de acceso
```

## Instalación y Configuración

### Requisitos Previos
1. Odoo 18 Community Edition
2. Módulos OCA: `fieldservice`
3. Módulo base: `patco_base`

### Instalación
```bash
# Actualizar módulo completo PATCO
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -u patco_suite --stop-after-init

# Instalación limpia (si es necesario)
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_suite --stop-after-init
```

### Configuración Inicial
1. **Acceder al menú**: Gestión de Habilidades
2. **Configurar tipos**: Revisar y ajustar tipos de habilidades
3. **Definir habilidades**: Personalizar catálogo según necesidades
4. **Asignar competencias**: Registrar habilidades de empleados
5. **Configurar FSM**: Definir habilidades requeridas por equipo/ubicación

## Navegación del Sistema

### Menú Principal: "Gestión de Habilidades"

#### Configuración
- **Tipos de Habilidades**: Gestión de categorías (COC, REF, LAV, etc.)
- **Niveles de Habilidades**: Definición de competencias (N1, N2, N3)
- **Habilidades**: Catálogo completo de habilidades técnicas

#### Empleados
- **Matriz de Habilidades**: Vista consolidada de competencias
- **Técnicos de Campo**: Gestión de personal técnico
- **Historial de Habilidades**: Seguimiento de evolución

#### Field Service
- **Órdenes con Habilidades**: Órdenes que requieren competencias específicas
- **Asignación por Habilidades**: Herramientas de asignación inteligente

#### Reportes
- **Estadísticas de Habilidades**: Análisis de competencias
- **Reportes de Certificaciones**: Seguimiento de certificaciones

## Integración con Otros Módulos

### Con `patco_base`
- Utiliza tipos de servicio y áreas de servicio
- Integra con la estructura organizacional base

### Con `fieldservice` (OCA)
- Extiende órdenes de servicio con habilidades requeridas
- Mejora la asignación de técnicos
- Integra con equipos y ubicaciones

### Con `hr` (Core Odoo)
- Extiende el modelo de empleados
- Utiliza la estructura de departamentos y puestos
- Integra con el sistema base de habilidades

## Casos de Uso Prácticos

### 1. Asignación de Técnico para Reparación de Horno
- **Orden**: Reparación de horno comercial
- **Habilidades requeridas**: COC-CAL (N2 mínimo)
- **Sistema**: Sugiere técnicos con competencia en calentadores
- **Resultado**: Asignación automática del técnico más calificado

### 2. Certificación de Empleado
- **Empleado**: Obtiene certificación en refrigeración
- **Registro**: Fecha, entidad certificadora, nivel
- **Historial**: Se registra automáticamente el cambio
- **Disponibilidad**: Empleado disponible para órdenes REF

### 3. Análisis de Competencias
- **Reporte**: Habilidades por departamento
- **Identificación**: Gaps de competencias
- **Planificación**: Necesidades de capacitación
- **Decisión**: Plan de desarrollo de habilidades

## Notas Técnicas

### Compatibilidad
- **Odoo 18 Community**: Totalmente compatible
- **Módulos Enterprise**: No requiere funcionalidades Enterprise
- **OCA**: Integración completa con módulos OCA

### Rendimiento
- **Campos computados**: Optimizados con `store=True`
- **Índices**: Configurados para consultas frecuentes
- **Caché**: Utiliza caché de Odoo para mejorar rendimiento

### Personalización
- **Extensible**: Fácil adición de nuevos tipos de habilidades
- **Configurable**: Niveles y competencias personalizables
- **Integrable**: API para integración con sistemas externos

### Mantenimiento
- **Logs automáticos**: Seguimiento de cambios en habilidades
- **Limpieza de datos**: Función de limpieza de logs antiguos
- **Validaciones**: Controles de integridad de datos

