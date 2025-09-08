# PATCO Core - Motor Central del Sistema

## Descripción

`patco_core` es el núcleo del sistema PATCO, proporcionando las funcionalidades base y modelos centrales para la gestión de mantenimiento HORECA. Este módulo contiene las extensiones fundamentales de Odoo y los datos maestros necesarios para el funcionamiento del ecosistema PATCO.

## Funcionalidades Principales

### 1. Gestión de Naturalezas de Servicio
- **Modelo**: `patco.service.nature`
- **Propósito**: Clasificación estándar de tipos de servicio según matriz PATCO
- **Campos principales**:
  - `name`: Nombre descriptivo (ej. "Correctivo", "Preventivo")
  - `code`: Código único (ej. "M1", "M2")
  - `sequence`: Orden de visualización
  - `active`: Estado del registro

### 2. Extensiones de Líneas Analíticas
- **Modelo extendido**: `account.analytic.line`
- **Funcionalidades añadidas**:
  - **Timer de Trabajo**: Control de tiempo en tiempo real
  - **Integración FSM**: Vinculación con órdenes de servicio de campo
  - **Gestión de Proyectos**: Asignación automática de proyectos por defecto

#### Campos Añadidos:
- `fsm_order_id`: Relación con orden de servicio (`fsm.order`)
- `date_time`: Fecha y hora para funcionalidad de timer
- `is_timer_running`: Estado del timer (activo/inactivo)

#### Métodos Principales:
- `action_timer_start()`: Inicia el timer de trabajo
- `action_timer_stop()`: Detiene el timer y calcula duración
- `_get_default_project()`: Asigna proyecto por defecto para FSM

### 3. Extensiones de Categorías de Equipos
- **Modelo extendido**: `maintenance.equipment.category`
- **Propósito**: Categorización especializada para equipos HORECA
- **Integración**: Preparado para checklists y procedimientos específicos

## Estructura de Archivos

```
patco_core/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── patco_service_nature.py      # Naturalezas de servicio
│   ├── account_analytic_line.py     # Extensión de timesheets
│   └── maintenance_equipment_category.py  # Extensión de categorías
├── data/
│   └── patco_service_nature_data.xml    # Datos iniciales
├── views/
│   ├── patco_service_nature_views.xml   # Vistas de naturalezas
│   └── account_analytic_line_views.xml  # Vistas de timesheets
├── security/
│   └── ir.model.access.csv              # Permisos de acceso
└── README.md
```

## Datos Iniciales

El módulo incluye datos maestros preconfigurados:

### Naturalezas de Servicio (`patco.service.nature`)
- **M1-Correctivo**: Reparación de fallas y averías
- **M2-Preventivo**: Mantenimiento programado y rutinario
- **M3-Instalación**: Instalación de nuevos equipos
- **M4-Inspección**: Revisiones técnicas y auditorías

## Dependencias

### Módulos Odoo Core:
- `base`: Funcionalidades básicas
- `hr_timesheet`: Gestión de hojas de tiempo
- `maintenance`: Gestión de equipos
- `analytic`: Contabilidad analítica

### Módulos OCA:
- `fieldservice`: Gestión de órdenes de servicio de campo

## Funcionalidades Técnicas

### 1. Timer de Trabajo en Tiempo Real
```python
# Iniciar timer
analytic_line.action_timer_start()

# Detener timer (calcula automáticamente la duración)
analytic_line.action_timer_stop()
```

### 2. Integración con FSM
- Creación automática de líneas analíticas desde órdenes FSM
- Asignación de proyecto por defecto basado en la orden
- Validaciones de integridad de datos

### 3. Gestión de Naturalezas
```python
# Búsqueda por código
nature = env['patco.service.nature'].search([('code', '=', 'M1')])

# Visualización personalizada
print(nature.display_name)  # "M1 - Correctivo"
```

## Validaciones y Restricciones

### Naturalezas de Servicio:
- **Código único**: No se permiten códigos duplicados
- **Nombre único**: No se permiten nombres duplicados
- **Formato de código**: Validación de estructura

### Líneas Analíticas:
- **Timer único**: Solo un timer activo por empleado
- **Validación FSM**: Verificación de coherencia con órdenes
- **Proyecto obligatorio**: Asignación automática si no se especifica

## Vistas y Interfaz

### Naturalezas de Servicio:
- **Vista Lista**: Gestión de naturalezas con filtros por estado
- **Vista Formulario**: Edición completa de naturalezas
- **Búsqueda**: Filtros por código, nombre y estado

### Líneas Analíticas Extendidas:
- **Campos FSM**: Integración en vistas existentes
- **Timer Controls**: Botones de inicio/parada de timer
- **Filtros FSM**: Búsqueda por orden de servicio

## Seguridad

### Permisos de Acceso:
- **Naturalezas de Servicio**: Lectura para usuarios, escritura para administradores
- **Líneas Analíticas**: Permisos heredados de `hr_timesheet`
- **Categorías de Equipos**: Permisos heredados de `maintenance`

## Integración con Otros Módulos PATCO

### Con `patco_customer_equipment`:
- Naturalezas de servicio disponibles para clasificación
- Integración con órdenes FSM generadas

### Con `patco_hr_skills`:
- Líneas analíticas vinculadas a competencias técnicas
- Seguimiento de tiempo por tipo de habilidad

### Con `patco_suite`:
- Instalación automática como dependencia
- Configuración inicial coordinada

## Casos de Uso

### 1. Registro de Tiempo de Servicio
```python
# El técnico inicia el timer al comenzar el trabajo
self.env['account.analytic.line'].create({
    'name': 'Reparación freidora',
    'project_id': fsm_order.project_id.id,
    'task_id': fsm_order.task_id.id,
    'employee_id': self.env.user.employee_id.id,
    'fsm_order_id': fsm_order.id,
})
```

### 2. Clasificación de Servicios
```python
# Asignación de naturaleza a ticket/orden
ticket.service_nature_id = env.ref('patco_core.service_nature_corrective')
```

### 3. Análisis de Tiempos FSM
```python
# Consulta de tiempos por naturaleza de servicio
lines = env['account.analytic.line'].search([
    ('fsm_order_id', '!=', False),
    ('fsm_order_id.service_nature_id.code', '=', 'M1')
])
```

## Configuración

### Instalación:
1. El módulo se instala automáticamente con `patco_suite`
2. Los datos iniciales se cargan automáticamente
3. Las vistas se integran con las existentes

### Configuración Post-Instalación:
1. **Verificar Naturalezas**: Revisar datos maestros cargados
2. **Configurar Proyectos**: Asegurar proyectos por defecto para FSM
3. **Permisos**: Ajustar permisos según roles de usuario

## Mantenimiento

### Actualización de Datos Maestros:
- Las naturalezas de servicio pueden editarse desde la interfaz
- Nuevas naturalezas pueden añadirse según necesidades del negocio
- Los códigos deben seguir el estándar PATCO (M1, M2, etc.)

### Monitoreo:
- Revisar logs de timer para detectar inconsistencias
- Validar integridad de datos FSM periódicamente
- Monitorear rendimiento de consultas analíticas

---

**PATCO Core** - La base sólida para la digitalización del mantenimiento HORECA