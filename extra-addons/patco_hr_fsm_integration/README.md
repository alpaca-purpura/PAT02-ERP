# PATCO HR FSM Integration

## Descripción

Módulo de integración que sincroniza automáticamente empleados de Recursos Humanos (HR) con trabajadores de Field Service Management (FSM). Este módulo implementa el principio de "Alta cohesión y bajo acoplamiento", evitando duplicar funcionalidades existentes en otros módulos PATCO.

## Funcionalidades Principales

### Sincronización Automática
- **Creación automática de FSM Person**: Al marcar `is_field_technician=True` en un empleado, se crea automáticamente el registro correspondiente en `fsm.person`
- **Sincronización bidireccional**: Los cambios en datos de contacto (nombre, teléfono, email) se sincronizan automáticamente entre ambos modelos
- **Vinculación inteligente**: El sistema busca automáticamente empleados existentes al crear personas FSM

### Sincronización Periódica
- **Cron Jobs**: Tareas programadas que se ejecutan cada 6 horas para mantener la sincronización
- **Migración de datos**: Método para migrar técnicos existentes que no tengan persona FSM asociada

## Estructura del Módulo

```
patco_hr_fsm_integration/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── hr_employee.py      # Extensión de hr.employee
│   └── fsm_person.py       # Extensión de fsm.person
├── data/
│   └── ir_cron_data.xml    # Tareas programadas
├── security/
│   └── ir.model.access.csv # Permisos de acceso
└── README.md
```

## Dependencias

- `hr`: Módulo base de Recursos Humanos
- `fieldservice`: Módulo base de Field Service Management
- `patco_hr_skills`: Módulo PATCO que define `is_field_technician`

## Instalación

1. Asegúrate de que los módulos dependientes estén instalados
2. Instala el módulo desde Apps o línea de comandos:
   ```bash
   odoo -i patco_hr_fsm_integration
   ```
3. Ejecuta la migración de datos existentes (opcional):
   ```python
   # Desde el shell de Odoo
   env['hr.employee'].migrate_existing_technicians()
   ```

## Uso

### Creación Automática
1. Ve a **Empleados** > **Empleados**
2. Selecciona un empleado o crea uno nuevo
3. Marca la casilla **Es Técnico de Campo** (`is_field_technician`)
4. El sistema creará automáticamente el registro en **Field Service** > **Workers**

### Sincronización Manual
- **Desde Empleado**: Usa el botón "Crear Persona FSM" si no se creó automáticamente
- **Desde Persona FSM**: Usa el botón "Vincular Empleado" para buscar empleado asociado

### Métodos Disponibles

#### En hr.employee
- `_create_fsm_person()`: Crea persona FSM para el empleado
- `_sync_to_fsm_person()`: Sincroniza datos hacia FSM
- `sync_all_field_technicians()`: Sincroniza todos los técnicos (cron)
- `migrate_existing_technicians()`: Migra técnicos existentes

#### En fsm.person
- `_find_and_link_employee()`: Busca y vincula empleado asociado
- `_sync_to_employee()`: Sincroniza datos hacia HR
- `sync_all_with_employees()`: Sincroniza todas las personas FSM (cron)

## Configuración

### Tareas Programadas
Las tareas programadas se ejecutan cada 6 horas por defecto. Puedes modificar la frecuencia en:
**Configuración** > **Técnico** > **Automatización** > **Acciones Programadas**

- `Sincronización HR-FSM: Técnicos de Campo`
- `Sincronización FSM-HR: Personas de Campo`

### Permisos
El módulo respeta los permisos existentes de HR y Field Service:
- **Usuarios básicos**: Solo lectura
- **Usuarios HR/FSM**: Lectura, escritura y creación
- **Managers HR/FSM**: Todos los permisos

## Principios de Diseño

### Alta Cohesión
- Cada clase tiene una responsabilidad específica y bien definida
- Los métodos están relacionados con la funcionalidad principal del modelo
- La lógica de sincronización está encapsulada en métodos específicos

### Bajo Acoplamiento
- No duplica funcionalidades existentes en `patco_hr_skills` o `patco_core`
- Usa las extensiones existentes (`is_field_technician`) sin modificarlas
- Implementa solo la sincronización que faltaba entre los módulos

## Logging

El módulo registra todas las operaciones importantes:
- Creación de personas FSM
- Sincronización de datos
- Errores y excepciones
- Resultados de cron jobs

Los logs se pueden revisar en **Configuración** > **Técnico** > **Logging**

## Troubleshooting

### Problemas Comunes

1. **No se crea persona FSM automáticamente**
   - Verifica que `is_field_technician=True`
   - Revisa los logs para errores
   - Ejecuta manualmente `_create_fsm_person()`

2. **Datos no sincronizados**
   - Verifica que ambos registros estén vinculados
   - Ejecuta los cron jobs manualmente
   - Revisa permisos de usuario

3. **Duplicados o conflictos**
   - El sistema busca por email, teléfono y nombre
   - Asegúrate de que los datos de contacto sean únicos
   - Usa los métodos de migración para limpiar datos

### Comandos Útiles

```python
# Migrar todos los técnicos existentes
env['hr.employee'].migrate_existing_technicians()

# Sincronizar todos los técnicos
env['hr.employee'].sync_all_field_technicians()

# Sincronizar todas las personas FSM
env['fsm.person'].sync_all_with_employees()

# Buscar empleados sin persona FSM
employees_without_fsm = env['hr.employee'].search([
    ('is_field_technician', '=', True),
    ('fsm_person_id', '=', False)
])

# Buscar personas FSM sin empleado
fsm_without_employee = env['fsm.person'].search([
    ('employee_id', '=', False)
])
```

## Contribución

Este módulo sigue las convenciones de desarrollo de PATCO:
- Código limpio y documentado
- Principios SOLID
- Logging apropiado
- Manejo de errores
- Tests unitarios (cuando aplique)

## Licencia

LGPL-3

## Autor

PATCO - Desarrollo de Software ERP