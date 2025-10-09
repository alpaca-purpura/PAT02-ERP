# PATCO Timesheet

**Versión:** 18.0.1.0.0  
**Autor:** PATCO  
**Categoría:** Services/Timesheets  
**Licencia:** LGPL-3  

## Descripción General

Módulo especializado que proporciona extensiones avanzadas para el registro de tiempo en el contexto de Field Service Management (FSM) de PATCO. Integra un sistema de timer inteligente con seguimiento automático de órdenes de servicio, ubicaciones y clientes, optimizando el registro de tiempo para técnicos de campo.

## Funcionalidades Principales

### ⏱️ Sistema de Timer Integrado
- **Timer en tiempo real**: Inicio y parada automática con cálculo preciso de duración
- **Estado visual**: Indicador de timer activo/inactivo en interfaces
- **Validaciones inteligentes**: Prevención de timers duplicados y estados inconsistentes
- **Notificaciones**: Feedback inmediato al usuario sobre acciones de timer

### 🔗 Integración FSM Completa
- **Vinculación automática**: Asociación directa con órdenes de servicio FSM
- **Datos contextuales**: Información automática de ubicación y cliente
- **Proyecto por defecto**: Creación automática de proyecto "Servicios de Campo"
- **Filtros especializados**: Búsquedas optimizadas para registros FSM

### 📊 Reportes y Análisis Extendidos
- **Análisis FSM**: Extensión de reportes de timesheet con datos de campo
- **Métricas especializadas**: Tiempo por orden, ubicación y cliente
- **Agrupaciones avanzadas**: Organización por orden FSM y cliente
- **Vistas optimizadas**: Interfaces adaptadas para técnicos de campo

### 🛠️ Gestión de Proyectos FSM
- **Proyecto automático**: Creación de "Servicios de Campo" si no existe
- **Configuración inteligente**: Habilitación automática de timesheets en proyectos FSM
- **Secuencias personalizadas**: Numeración específica para registros FSM

## Modelos Implementados

### `account.analytic.line` (Extensión)
- **Campos añadidos:**
  - `fsm_order_id` (Many2one): Orden de servicio FSM asociada
  - `date_time` (Datetime): Hora de inicio del timer (vacío cuando está detenido)
  - `fsm_location` (Char): Ubicación del servicio (campo relacionado)
  - `fsm_customer` (Char): Cliente FSM (campo relacionado)
  - `is_timer_running` (Boolean): Estado del timer (campo computado)

- **Métodos principales:**
  - `_compute_timer_running()`: Determina si el timer está activo
  - `action_start_timer()`: Inicia el timer con validaciones
  - `action_stop_timer()`: Detiene el timer y calcula duración
  - `_get_or_create_fsm_project()`: Obtiene o crea proyecto FSM por defecto
  - `create()`: Override con lógica de asignación automática de proyectos

### `timesheets.analysis.report` (Extensión)
- **Campos añadidos:**
  - `fsm_order_id` (Many2one): Orden FSM para análisis
  - `fsm_location` (Char): Ubicación para reportes
  - `fsm_customer` (Char): Cliente para análisis

- **Métodos principales:**
  - `_select()`: Extensión de consulta SELECT con campos FSM
  - `_from()`: Joins con tablas FSM (fsm_order, fsm_location, res_partner)
  - `_group_by()`: Agrupación por campos FSM

### 2. Integración con Field Service Management

#### Extensión del Modelo account.analytic.line
El módulo extiende directamente el modelo `account.analytic.line` con campos FSM:

**Archivo**: `models/account_analytic_line.py`

```python
class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    # Campos FSM integrados
    fsm_order_id = fields.Many2one('fsm.order', 'Orden FSM')
    fsm_location = fields.Char('Ubicación FSM')
    fsm_customer = fields.Char('Cliente FSM')
    is_timer_running = fields.Boolean('Timer Activo')
    date_time = fields.Datetime('Fecha y Hora de Inicio')
    
    # Métodos de control de timer
    def action_start_timer(self)
    def action_stop_timer(self)
    def _compute_timer_running(self)
```

### 3. Vistas Extendidas

#### Vista de Lista de Timesheet
- Campos FSM agregados: orden, ubicación, cliente
- Filtros por órdenes de servicio
- Agrupación por ubicación y cliente FSM

#### Vista de Formulario
- Campos FSM integrados en el formulario
- Información contextual de la orden de servicio
- Timer integrado para control de tiempo

#### Vista de Búsqueda
- Filtros específicos FSM:
  - Por orden de servicio
  - Por ubicación de trabajo
  - Por cliente FSM
  - Por estado de timer

### 4. Reportes de Análisis Avanzado

#### Vista Gráfica
- Análisis de tiempo por ubicación
- Distribución por cliente FSM
- Tendencias de tiempo por tipo de servicio

#### Vista Pivot
- Análisis multidimensional:
  - Tiempo por técnico y ubicación
  - Horas por cliente y período
  - Eficiencia por tipo de orden

### 5. Menús y Navegación

#### Estructura de Menús
```
Fieldservice
├── Registro de Tiempo
│   ├── Mis Registros de Tiempo
│   ├── Todos los Registros
│   └── Análisis de Tiempo
└── Análisis
    └── Análisis de Timesheet FSM
```

## Modelos Técnicos

### TimesheetsAnalysisReport

**Archivo**: `models/timesheets_analysis_report.py`

```python
class TimesheetsAnalysisReport(models.Model):
    _inherit = 'timesheets.analysis.report'
    
    # Campos FSM
    fsm_order_id = fields.Many2one('fsm.order', 'Orden FSM', readonly=True)
    fsm_location = fields.Char('Ubicación FSM', readonly=True)
    fsm_customer = fields.Char('Cliente FSM', readonly=True)
```

#### Métodos Extendidos

- **_select()**: Agrega campos FSM al SELECT
- **_from()**: Incluye JOIN con fsm.order
- **_group_by()**: Agrupa por campos FSM

## Configuración y Datos

### Datos Iniciales

**Archivo**: `data/timesheet_data.xml`

- **Proyecto FSM por Defecto**: Proyecto para registros de tiempo FSM
- **Secuencia de Timesheet**: Numeración automática para registros

### Seguridad

**Archivo**: `security/ir.model.access.csv`

| Modelo | Usuario | Manager | Permisos |
|--------|---------|---------|----------|
| account.analytic.line | ✓ | ✓ | read,write,create,unlink |
| timesheets.analysis.report | ✓ | ✓ | read |

## Migración de Base de Datos

### Pre-inicialización

**Archivo**: `migrations/18.0.1.0.0/pre-init-add-fsm-field.sql`

```sql
-- Agrega campo fsm_order_id si no existe
ALTER TABLE account_analytic_line 
ADD COLUMN IF NOT EXISTS fsm_order_id INTEGER;

-- Crea índice para rendimiento
CREATE INDEX IF NOT EXISTS idx_account_analytic_line_fsm_order_id 
ON account_analytic_line(fsm_order_id);
```

## Dependencias

### Módulos Requeridos
- `patco_base`: Funcionalidades base de PATCO
- `hr_timesheet`: Sistema de timesheet de Odoo
- `fieldservice`: Gestión de servicios de campo

### Integración con Otros Módulos
- **patco_fsm**: Integración con órdenes de servicio de campo
- **patco_base**: Clasificaciones y configuraciones base

## Correcciones Implementadas

### Solución al Error KeyError 'fsm_order_id'
**Fecha**: 2024-01-XX
**Problema**: Error `KeyError: 'fsm_order_id'` durante instalación de patco_suite
**Solución**: 
- Se agregó el archivo `models/account_analytic_line.py` con la extensión completa del modelo
- Se definieron todos los campos FSM necesarios directamente en este módulo
- Se corrigieron las dependencias en `__manifest__.py` para incluir `hr_timesheet`

**Archivos modificados**:
- `models/__init__.py`: Agregada importación de `account_analytic_line`
- `models/account_analytic_line.py`: Nuevo archivo con extensión del modelo
- `__manifest__.py`: Dependencias actualizadas

## Casos de Uso

### 1. Registro de Tiempo en Órdenes FSM

```python
# Crear registro de tiempo para orden FSM
timesheet = env['account.analytic.line'].create({
    'name': 'Mantenimiento preventivo',
    'fsm_order_id': order.id,
    'project_id': project.id,
    'task_id': task.id,
    'unit_amount': 2.5,  # 2.5 horas
    'date': fields.Date.today(),
})
```

### 2. Análisis de Tiempo por Ubicación

```python
# Buscar tiempo trabajado por ubicación
analysis = env['timesheets.analysis.report'].search([
    ('fsm_location', '=', 'Planta Industrial Norte'),
    ('date', '>=', '2024-01-01'),
])

total_hours = sum(analysis.mapped('unit_amount'))
```

### 3. Reporte de Eficiencia por Cliente

```python
# Análisis de tiempo por cliente FSM
client_analysis = env['timesheets.analysis.report'].read_group(
    [('fsm_customer', '!=', False)],
    ['fsm_customer', 'unit_amount'],
    ['fsm_customer']
)
```

## Características Técnicas

### Rendimiento
- Índices optimizados para consultas FSM
- Vistas materializadas para análisis rápido
- Consultas eficientes con JOINs optimizados

### Escalabilidad
- Soporte para miles de registros de tiempo
- Análisis en tiempo real
- Reportes paginados para grandes volúmenes

### Integración
- API compatible con módulos externos
- Webhooks para sincronización
- Exportación a formatos estándar (CSV, Excel)

## Instalación y Configuración

### Requisitos Previos
1. Odoo 18.0 Community
2. Módulos patco_base y fieldservice instalados
3. PostgreSQL 12+

### Pasos de Instalación
1. Copiar módulo a `extra-addons/patco_timesheet`
2. Actualizar lista de módulos
3. Instalar módulo desde Apps
4. Configurar permisos de usuario

### Configuración Post-Instalación
1. Verificar proyecto FSM por defecto
2. Configurar secuencias si es necesario
3. Asignar permisos a usuarios
4. Probar integración con órdenes FSM

## Mantenimiento

### Logs y Monitoreo
- Logs de creación de timesheet
- Monitoreo de rendimiento de consultas
- Alertas de inconsistencias de datos

### Respaldos
- Respaldo diario de registros de tiempo
- Exportación periódica de análisis
- Versionado de configuraciones

## Soporte y Documentación

### Recursos Adicionales
- Documentación técnica en `/docs`
- Ejemplos de uso en `/examples`
- Tests unitarios en `/tests`

### Contacto
- Desarrollador: Equipo PATCO
- Versión: 18.0.1.0.0
- Licencia: LGPL-3

---

**Nota**: Este módulo es parte del ecosistema PATCO y está diseñado para trabajar en conjunto con otros módulos PATCO para proporcionar una solución completa de gestión de servicios de campo.