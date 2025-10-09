# PATCO Suite - Solución Completa de Mantenimiento HORECA

## Descripción

PATCO Suite es el módulo orquestador que instala automáticamente toda la suite PATCO para gestión de mantenimiento en el sector HORECA (Hoteles, Restaurantes y Cafeterías). Este meta-módulo actúa como punto de entrada único, instalando automáticamente todos los módulos PATCO junto con sus dependencias OCA en el orden correcto, simplificando el proceso de implementación mediante un sistema de dependencias declarativas.

## Funcionalidad Principal

### Orquestación Automática por Dependencias
- **Instalación Unificada**: Un solo módulo instala automáticamente los 6 módulos PATCO
- **Gestión de Dependencias OCA**: Instalación automática de 7 módulos OCA requeridos
- **Orden Correcto**: Odoo maneja la secuencia de instalación (Core → OCA → PATCO)
- **Configuración Persistente**: Parámetros almacenados en `ir.config_parameter`

### Hook Post-Instalación Inteligente
- **Validación de Módulos**: Verifica instalación correcta de los 6 módulos PATCO consolidados
- **Verificación de Schema**: Confirma existencia del campo `fsm_order_id` en `account.analytic.line`
- **Logging con Símbolos**: Usa ✓ para éxito y ⚠ para advertencias en logs
- **Manejo de Errores**: Try-catch con logging detallado de excepciones

## Estructura Técnica

### Archivos del Módulo
```
patco_suite/
├── __manifest__.py      # Definición del módulo y dependencias (74 líneas)
├── __init__.py          # Importación del hook (12 líneas)
├── hooks.py             # Hook post-instalación (50+ líneas)
├── data/
│   └── suite_configuration.xml  # Configuración de parámetros (23 líneas)
├── models/              # (Vacío - solo orquestación)
├── views/               # (Vacío - solo orquestación)
└── README.md            # Documentación completa
```

### Hook Post-Instalación (`hooks.py`)
- **Función**: `post_init_hook(cr, registry)`
- **Validaciones**:
  - Módulos PATCO: `patco_base`, `patco_equipment`, `patco_fsm`, `patco_stock_fsm`, `patco_skills_mgmt`, `patco_timesheet`
  - Campo crítico: `fsm_order_id` en `account_analytic_line`
- **Logging**: Mensajes con símbolos ✓ y ⚠ para estado visual
- **Manejo de Errores**: Try-catch con logging detallado

```python
def post_init_hook(cr, registry):
    """Hook ejecutado después de la instalación del módulo"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Verificar instalación de módulos PATCO
    patco_modules = ['patco_base', 'patco_skills_mgmt', 'patco_equipment', 
                     'patco_fsm', 'patco_stock_fsm', 'patco_timesheet']
    
    # Verificar campo fsm_order_id en account.analytic.line
    if env['account.analytic.line']._fields.get('fsm_order_id'):
        _logger.info("Campo fsm_order_id encontrado en account.analytic.line")
    else:
        _logger.warning("Campo fsm_order_id no encontrado")
```

### Configuración de la Suite (`data/suite_configuration.xml`)
```xml
<!-- Parámetros de configuración almacenados en ir.config_parameter -->
<record id="patco_suite_version" model="ir.config_parameter">
    <field name="key">patco.suite.version</field>
    <field name="value">2.0.0</field>
</record>
```

## Características Técnicas del Orquestador

### 🎯 Instalación Automática Inteligente
- **Dependencias Declarativas**: Instalación automática vía `depends` en `__manifest__.py`
- **Orden de Instalación**: Secuencia optimizada (Core → OCA → PATCO)
- **Hook Post-Instalación**: Función `post_init_hook()` en `hooks.py` con validación completa
- **Configuración Persistente**: Parámetros en `ir.config_parameter` con `noupdate="1"`

### 📋 Sistema de Validación Avanzado
- **Verificación de Módulos**: Consulta directa a `ir.module.module` por estado `installed`
- **Validación de Schema**: Query SQL a `information_schema.columns` para campo `fsm_order_id`
- **Logging Estructurado**: Símbolos ✓ (éxito) y ⚠ (advertencia) con `_logger.info/warning`
- **Manejo de Errores**: Try-catch con logging detallado de excepciones

## Módulos PATCO Integrados (Instalación Automática)

### Instalación Automática por Dependencias
```python
# Dependencias PATCO declaradas en __manifest__.py
'patco_base',          # Núcleo arquitectónico
'patco_equipment',     # Activos HORECA
'patco_fsm',          # Órdenes de trabajo
'patco_stock_fsm',    # Logística de campo
'patco_skills_mgmt',   # Competencias técnicas
'patco_timesheet',    # Control temporal
```

### 1. **patco_base** - Núcleo Arquitectónico
- **Propósito**: Funcionalidades base y configuración central de la suite
- **Modelos Base**: `patco.base.mixin`, configuraciones centrales
- **Extensiones Core**: `res.partner`, `res.company` con campos PATCO
- **Configuración Global**: Parámetros de sistema y datos maestros
- **Dependencias**: `base`, `contacts`, `mail`

### 2. **patco_equipment** - Activos HORECA
- **Propósito**: Gestión integral de equipos y mantenimiento HORECA
- **Modelo Central**: `maintenance.equipment` extendido
- **Características**: Inventario de equipos, códigos PATCO, QR, mantenimiento preventivo/correctivo
- **Trazabilidad**: Historial completo de intervenciones
- **Contratos**: Gestión de garantías y SLAs
- **Dependencias**: `maintenance`, `fieldservice` (OCA), `patco_base`

### 3. **patco_fsm** - Órdenes de Trabajo
- **Propósito**: Integración con Field Service Management
- **Workflow FSM**: Estados personalizados con validaciones
- **Hojas Digitales**: JSON `worksheet_data` con firmas Base64
- **Características**: Órdenes de servicio, planificación de técnicos, integración con equipos
- **Wizards**: Consumo repuestos, aprobación cliente
- **Dependencias**: `fieldservice` (OCA), `patco_equipment`

### 4. **patco_stock_fsm** - Logística de Campo
- **Propósito**: Integración entre inventario y servicios de campo
- **Integración Stock**: `stock.move` automático desde FSM
- **Inventario Técnico**: Asignación de stock por empleado
- **Características**: Gestión de repuestos, consumos en órdenes de servicio
- **Consumo Inteligente**: Wizard con validaciones de disponibilidad
- **Dependencias**: `stock`, `patco_fsm`

### 5. **patco_skills_mgmt** - Competencias Técnicas
- **Propósito**: Gestión avanzada de habilidades técnicas
- **Modelos Principales**: `hr.skill.patco`, `hr.employee.skill.patco`
- **Certificaciones**: Sistema de niveles y validaciones temporales
- **Características**: Certificaciones, competencias, evaluaciones de técnicos
- **Asignación Inteligente**: Matching automático técnico-competencia
- **Dependencias**: `hr_skills` (OCA), `patco_base`

### 6. **patco_timesheet** - Control Temporal
- **Propósito**: Gestión avanzada de hojas de tiempo
- **Timesheet Extendido**: Campo `fsm_order_id` en `account.analytic.line`
- **Timer Integrado**: Inicio/pausa automático desde FSM
- **Características**: Registro de tiempo por proyecto/tarea, reportes, integración FSM
- **Reportes**: Productividad y análisis de tiempos
- **Dependencias**: `hr_timesheet`, `project`, `patco_fsm`

## Dependencias Automáticas

### Módulos Odoo Core (8 módulos)
```python
# Módulos base de Odoo
'base',               # Framework base de Odoo
'mail',               # Sistema de mensajería
'contacts',           # Gestión de contactos
'hr',                 # Recursos humanos
'maintenance',        # Mantenimiento de equipos
'stock',              # Gestión de inventario
'project',            # Gestión de proyectos
'account',            # Contabilidad
```

### Módulos OCA (4 módulos)
```python
# Módulos OCA instalados automáticamente
'fieldservice',       # OCA/field-service - FSM core
'hr_timesheet',       # OCA/hr - Gestión de tiempo
'partner_firstname',  # OCA/partner-contact - Nombres
'hr_skills',          # OCA/hr - Competencias
```

### Arquitectura de Dependencias
1. **Core Odoo** (8 módulos): Base del sistema
2. **OCA Specialized** (4 módulos): Funcionalidades avanzadas
3. **PATCO Suite** (6 módulos): Lógica de negocio HORECA

### Módulos OCA Detallados
- `fieldservice`: Gestión de servicios de campo
- `hr_timesheet`: Gestión de hojas de tiempo
- `partner_firstname`: Nombres y apellidos separados
- `hr_skills`: Sistema de competencias técnicas

### Módulos PATCO Consolidados
- `patco_base`: Modelos fundamentales y clasificaciones base
- `patco_skills_mgmt`: Gestión avanzada de habilidades técnicas
- `patco_equipment`: Gestión integral de equipos con códigos QR
- `patco_fsm`: Extensiones para Field Service Management
- `patco_stock_fsm`: Gestión de stock para servicios de campo
- `patco_timesheet`: Extensiones de timesheet para FSM

## Estructura Técnica de Archivos

```
patco_suite/
├── __init__.py                    # Import hook: from .hooks import post_init_hook
├── __manifest__.py                # Meta-módulo: 18 dependencias declarativas
├── hooks.py                       # Validación post-instalación (50 líneas)
├── data/
│   └── suite_configuration.xml    # ir.config_parameter: versión, fecha, descripción
├── models/                        # Vacío (orquestador puro)
├── views/                         # Vacío (sin interfaz propia)
└── README.md                      # Documentación técnica (732 líneas)
```

### Archivos Críticos del Orquestador

#### `__manifest__.py` - Declaración de Dependencias (74 líneas)
```python
{
    'name': 'PATCO Suite - Solución Completa HORECA',
    'version': '18.0.1.0.0',
    'category': 'Services/Field Service',
    'summary': 'Suite completa PATCO para mantenimiento HORECA - Instalación automática',
    'description': '''Suite completa PATCO que instala automáticamente todos los módulos...
    
    Módulos PATCO integrados:
    • patco_base: Funcionalidades base y configuración
    • patco_equipment: Gestión de equipos y mantenimiento
    • patco_fsm: Field Service Management
    • patco_stock_fsm: Integración stock-FSM
    • patco_skills_mgmt: Gestión de habilidades técnicas
    • patco_timesheet: Gestión de hojas de tiempo
    
    Dependencias OCA incluidas:
    • maintenance, fieldservice, hr_skills, helpdesk
    • partner_contact, account_payment, project
    ''',
    'depends': [
        # Core Odoo
        'base', 'mail', 'web',
        # OCA Dependencies  
        'maintenance', 'fieldservice', 'hr_skills', 'helpdesk',
        'partner_contact', 'account_payment', 'project',
        # PATCO Modules
        'patco_base', 'patco_equipment', 'patco_fsm',
        'patco_stock_fsm', 'patco_skills_mgmt', 'patco_timesheet'
    ],
    'data': ['data/suite_configuration.xml'],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'author': 'PATCO Development Team',
}
```

#### `hooks.py` - Sistema de Validación (50+ líneas)
```python
def post_init_hook(cr, registry):
    """Hook ejecutado después de la instalación de PATCO Suite"""
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        try:
            _logger.info("🚀 Iniciando validación post-instalación PATCO Suite...")
            
            # Validar módulos PATCO consolidados
            patco_modules = [
                'patco_base', 'patco_equipment', 'patco_fsm',
                'patco_stock_fsm', 'patco_skills_mgmt', 'patco_timesheet'
            ]
            
            for module in patco_modules:
                if env['ir.module.module'].search([('name', '=', module), ('state', '=', 'installed')]):
                    _logger.info(f"✓ Módulo {module} instalado correctamente")
                else:
                    _logger.warning(f"⚠ Módulo {module} no encontrado o no instalado")
            
            # Verificar campo crítico fsm_order_id en account.analytic.line
            if hasattr(env['account.analytic.line'], '_fields') and 'fsm_order_id' in env['account.analytic.line']._fields:
                _logger.info("✓ Campo fsm_order_id disponible en account.analytic.line")
            else:
                _logger.warning("⚠ Campo fsm_order_id no encontrado en account.analytic.line")
                
            _logger.info("✅ PATCO Suite instalado correctamente")
            
        except Exception as e:
            _logger.error(f"❌ Error en hook post-instalación: {e}")
```

####### `suite_configuration.xml` - Parámetros Persistentes (23 líneas)
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <!-- Configuración de la Suite PATCO -->
        <record id="patco_suite_version" model="ir.config_parameter">
            <field name="key">patco_suite.version</field>
            <field name="value">1.0.0</field>
        </record>
        
        <record id="patco_suite_install_date" model="ir.config_parameter">
            <field name="key">patco_suite.install_date</field>
            <field name="value" eval="datetime.now().strftime('%Y-%m-%d %H:%M:%S')"/>
        </record>
        
        <record id="patco_suite_description" model="ir.config_parameter">
            <field name="key">patco_suite.description</field>
            <field name="value">Suite completa PATCO con módulos: patco_base, patco_equipment, patco_fsm, patco_stock_fsm, patco_skills_mgmt, patco_timesheet. Dependencias OCA: maintenance, fieldservice, hr_skills, helpdesk, partner_contact, account_payment, project.</field>
        </record>
    </data>
</odoo>
```

## Configuración Post-Instalación Automática

El hook `post_init_hook()` ejecuta automáticamente:

### ✅ Validación de Módulos PATCO (6 verificaciones)
```python
patco_modules = [
    'patco_base', 'patco_skills_mgmt', 'patco_equipment',
    'patco_fsm', 'patco_stock_fsm', 'patco_timesheet'
]
# Query: SELECT name FROM ir_module_module WHERE name IN %s AND state = 'installed'
```

### 🔍 Validación de Schema Crítico
```sql
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'account_analytic_line' 
AND column_name = 'fsm_order_id'
```

### 📊 Parámetros de Sistema Configurados
```xml
<!-- Automáticamente creados en ir.config_parameter -->
patco.suite.version = "18.0.1.0.0"
patco.suite.install_date = "2024-01-15 10:30:00"
patco.suite.description = "Módulo orquestador PATCO con 6 módulos integrados"
```

### 🔍 Logging Estructurado de Validación
```python
_logger.info("✓ PATCO Suite: Módulo %s instalado correctamente", module)
_logger.warning("⚠ PATCO Suite: Módulo %s no encontrado", module)
_logger.info("✓ Campo fsm_order_id encontrado en account.analytic.line")
```

### Hook de Verificación (`hooks.py`)
El módulo incluye un `post_init_hook` que:

1. **Verifica instalación** de los 6 módulos PATCO consolidados
2. **Valida el campo `fsm_order_id`** en la tabla `account_analytic_line`
3. **Genera logs con símbolos** (✓ para éxito, ⚠ para advertencias)
4. **Manejo de errores** con logging detallado

### Parámetros de Configuración (`suite_configuration.xml`)
Se crean automáticamente con `noupdate="1"`:

- `patco_suite.version`: "18.0.1.0.0"
- `patco_suite.install_date`: Fecha y hora actual de instalación
- `patco_suite.description`: Descripción completa del módulo orquestador

## Instalación y Uso

### Instalación Única (Recomendada)
```bash
# Instalar SOLO patco_suite - instala automáticamente los 6 módulos PATCO + 7 OCA
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_suite --stop-after-init
```

**⚠️ IMPORTANTE**: Nunca instalar módulos PATCO individuales. Solo usar `patco_suite`.

### Flujo de Instalación Automática
1. **Odoo Core**: `base`, `mail`, `web` (ya instalados)
2. **Módulos OCA**: `maintenance`, `fieldservice`, `hr_skills`, `helpdesk`, `partner_contact`, `account_payment`, `project`
3. **Módulos PATCO**: `patco_base` → `patco_equipment` → `patco_fsm` → `patco_stock_fsm` → `patco_skills_mgmt` → `patco_timesheet`
4. **Hook Post-Instalación**: Validación automática con logging
5. **Configuración**: Parámetros en `ir.config_parameter`

### Instalación Completa con Docker
```bash
# 1. Clonar repositorio
git clone <repository-url>
cd patco-erp

# 2. Construir e iniciar contenedores
docker compose up --build -d

# 3. Instalar suite completa (UN SOLO COMANDO)
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_suite --stop-after-init

# 4. Iniciar Odoo
docker compose up
```

### Actualización
```bash
# Actualizar toda la suite (propaga a todos los módulos)
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -u patco_suite --stop-after-init
```

### Verificación Post-Instalación
1. **Revisar logs**: `docker logs odoo-patco-app | grep "✓\|⚠\|❌"`
2. **Verificar módulos**: Apps → Buscar "PATCO" → 6 módulos instalados
3. **Hook validation**: Buscar mensajes con símbolos ✓ (éxito) y ⚠ (advertencia)
4. **Campo crítico**: Verificar que `fsm_order_id` existe en timesheet
5. **Parámetros**: Settings → Technical → Parameters → Buscar "patco_suite"

### Validación Post-Instalación
```bash
# 1. Verificar logs de instalación
tail -f logs/odoo.log | grep "PATCO Suite"

# 2. Consultar módulos instalados
psql -d odoo_patco -c "SELECT name, state FROM ir_module_module WHERE name LIKE 'patco_%';"

# 3. Verificar campo crítico
psql -d odoo_patco -c "\d account_analytic_line" | grep fsm_order_id
```

### Actualización Avanzada
```bash
# Actualizar orquestador (actualiza todos los PATCO)
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin \
  -c /etc/odoo/odoo.conf -d odoo_patco \
  -u patco_suite --stop-after-init
```

### Troubleshooting de Instalación
```bash
# Verificar dependencias OCA
psql -d odoo_patco -c "SELECT name, state FROM ir_module_module WHERE name IN ('fieldservice', 'hr_timesheet', 'partner_firstname', 'hr_skills');"

# Reinstalación completa (si es necesario)
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin \
  -c /etc/odoo/odoo.conf -d odoo_patco \
  -i patco_suite --init=patco_suite --stop-after-init
```

### Logs de Instalación
Monitorear en logs de Odoo:
```
✓ Módulo patco_base instalado correctamente
✓ Módulo patco_skills_mgmt instalado correctamente
✓ Módulo patco_equipment instalado correctamente
✓ Campo fsm_order_id encontrado en account.analytic.line
```

## Ventajas Técnicas del Meta-Módulo

### 🚀 Orquestación Inteligente
- **Dependencias Declarativas**: 18 módulos instalados automáticamente vía `depends`
- **Orden de Instalación**: Core → OCA → PATCO (sin conflictos de dependencias)
- **Hook Automático**: Validación post-instalación sin intervención manual
- **Atomicidad**: Instalación completa o rollback automático

### 🔧 Gestión Centralizada de Ciclo de Vida
- **Single Point of Truth**: Un solo `__manifest__.py` controla 18 módulos
- **Versionado Semántico**: `18.0.1.0.0` para toda la suite
- **Actualizaciones Coordinadas**: `-u patco_suite` actualiza todos los PATCO
- **Logging Unificado**: Todos los eventos en un solo namespace

### 📊 Sistema de Validación Robusto
```python
# Verificación de integridad automática
def post_init_hook(cr, registry):
    # 1. Validación de módulos instalados
    # 2. Verificación de schema de BD
    # 3. Logging estructurado con símbolos
    # 4. Parámetros de configuración persistentes
```

### 🏗️ Arquitectura Sin Estado
- **Orquestador Puro**: Sin modelos, vistas o datos propios
- **Separación de Responsabilidades**: Solo coordinación, no funcionalidad
- **Extensibilidad**: Fácil adición de nuevos módulos PATCO
- **Mantenibilidad**: Lógica de orquestación aislada

## Troubleshooting Técnico

### Error: Dependencias OCA No Encontradas
```bash
# Síntoma: ModuleNotFoundError durante instalación
# Causa: Módulos OCA no están en addons_path

# 1. Verificar configuración
grep addons_path /etc/odoo/odoo.conf

# 2. Verificar estructura de carpetas
ls -la /mnt/extra-addons/OCA/

# 3. Reinstalar dependencias OCA faltantes
# Ejemplo para fieldservice:
git clone https://github.com/OCA/field-service.git /mnt/extra-addons/OCA/field-service
```

### Error: Falla del Hook Post-Instalación
```python
# Síntoma en logs:
# "⚠ PATCO Suite: Módulo patco_xxx no está instalado o no es funcional"

# Causa: Módulo PATCO individual falló durante instalación
# Solución: Reinstalar suite completa
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_suite --stop-after-init

# Verificar logs específicos:
docker logs odoo-patco-app | grep "PATCO Suite"
```

### Error: Campo `fsm_order_id` Ausente
```python
# Síntoma en logs:
# "❌ PATCO Suite: Campo crítico fsm_order_id no encontrado en account.analytic.line"

# Causa: Integración FSM-Timesheet no completada
# Solución 1: Actualizar módulos FSM
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -u patco_fsm,patco_timesheet --stop-after-init

# Solución 2: Verificar dependencias OCA
# Asegurar que 'fieldservice' esté instalado antes que patco_fsm
```

### Error: Hook No Se Ejecuta
```python
# Síntoma: No aparecen mensajes "✓ PATCO Suite" en logs
# Causa: Hook post_init_hook no configurado correctamente

# Verificar __manifest__.py:
grep -n "post_init_hook" /mnt/extra-addons/patco_suite/__manifest__.py

# Debe mostrar:
# 'post_init_hook': 'post_init_hook',
```

### Diagnóstico Completo del Sistema
```bash
# Script de diagnóstico completo
echo "=== PATCO Suite Diagnostic ==="
psql -d odoo_patco -c "SELECT name, state FROM ir_module_module WHERE name LIKE 'patco_%' ORDER BY name;"
psql -d odoo_patco -c "SELECT key, value FROM ir_config_parameter WHERE key LIKE 'patco.suite.%';"
grep -c "✓\|⚠" logs/odoo.log | tail -10
```

## Información Técnica del Orquestador

### Arquitectura de Meta-Módulo
```
patco_suite (Meta-Módulo)
├── Core Odoo (8 módulos)
│   ├── base, mail, contacts, hr
│   ├── maintenance, stock, project, account
├── OCA Specialized (4 módulos)
│   ├── fieldservice (FSM core)
│   ├── hr_timesheet (Timesheet avanzado)
│   ├── partner_firstname (Separación nombres)
│   └── hr_skills (Gestión competencias)
└── PATCO Suite (6 módulos)
    ├── patco_base (Núcleo arquitectónico)
    ├── patco_skills_mgmt (Competencias técnicas)
    ├── patco_equipment (Activos HORECA)
    ├── patco_fsm (Órdenes de trabajo)
    ├── patco_stock_fsm (Logística de campo)
    └── patco_timesheet (Control temporal)
```

### Flujo de Instalación Técnico
```python
# 1. Resolución de dependencias (18 módulos)
Odoo.resolve_dependencies(patco_suite.depends)

# 2. Instalación secuencial automática
for module in dependency_order:
    install_module(module)

# 3. Ejecución del hook de validación
post_init_hook(cr, registry)

# 4. Configuración de parámetros persistentes
ir_config_parameter.create(suite_params)
```

### Principios de Diseño
- **Single Responsibility**: Solo orquestación, sin lógica de negocio
- **Dependency Injection**: Dependencias declarativas en `__manifest__.py`
- **Fail Fast**: Validación inmediata post-instalación
- **Observability**: Logging estructurado para debugging
- **Idempotency**: Instalación repetible sin efectos secundarios

### Verificación Manual
```python
# Verificar estado de módulos PATCO
self.env['ir.module.module'].search([('name', 'like', 'patco_%')])

# Verificar parámetros de configuración
self.env['ir.config_parameter'].get_param('patco_suite.version')
```

---

**PATCO Suite v18.0.1.0.0** - Meta-Módulo Orquestador  
*18 Dependencias • 6 Módulos PATCO • Validación Automática • Logging Estructurado*

## Información Técnica

- **Versión Odoo:** 18.0
- **Categoría:** Field Service Management
- **Licencia:** LGPL-3
- **Autor:** PATCO Development Team
- **Dependencias:** Automáticas vía manifest

---

> **Nota:** Este es un módulo orquestador puro. No define modelos ni vistas propias, sino que coordina la instalación y configuración de toda la suite PATCO para proporcionar una experiencia de despliegue unificada.

`patco_suite` es el módulo orquestador principal del ecosistema PATCO, diseñado para simplificar la instalación y gestión de la solución completa de mantenimiento HORECA. Actúa como un meta-módulo que coordina la instalación de todos los componentes necesarios, incluyendo dependencias OCA y módulos PATCO consolidados, garantizando una implementación coherente y optimizada.

### Nueva Estructura Modular Consolidada (v2.0)
A partir de la versión 2.0, PATCO Suite utiliza una arquitectura modular consolidada que mejora la mantenibilidad, reduce duplicaciones y optimiza el rendimiento del sistema.

## Función como Orquestador

### 1. Instalación Unificada
- **Punto de Entrada Único**: Una sola instalación para toda la solución PATCO
- **Gestión de Dependencias**: Instalación automática de módulos OCA requeridos
- **Orden de Instalación**: Secuencia correcta de instalación de componentes
- **Validación de Integridad**: Verificación de que todos los módulos se instalen correctamente

### 2. Coordinación de Módulos
- **Integración Seamless**: Asegura la correcta integración entre módulos
- **Configuración Centralizada**: Parámetros de configuración unificados
- **Sincronización de Datos**: Coordinación de datos maestros entre módulos
- **Gestión de Versiones**: Compatibilidad entre versiones de módulos

### 3. Simplificación para el Usuario
- **Experiencia Unificada**: Interface única para toda la solución
- **Configuración Guiada**: Asistentes de configuración inicial
- **Documentación Centralizada**: Acceso a toda la documentación desde un punto
- **Soporte Técnico**: Canal único de soporte para toda la suite

## Arquitectura de Dependencias

### Módulos PATCO Consolidados:
```python
'depends': [
    # Odoo Core
    'base', 'mail', 'contacts', 'stock', 'sale', 'purchase',
    'account', 'hr', 'project', 'maintenance',
    
    # OCA Dependencies
    'fieldservice',                 # Gestión de servicios de campo
    'hr_timesheet',                # Gestión de hojas de tiempo
    'partner_firstname',           # Nombres de contactos
    'base_location',               # Gestión de ubicaciones
    'base_location_geonames_import', # Importación de ubicaciones
    'web_widget_x2many_2d_matrix', # Widget de matriz 2D
    
    # PATCO Modules - Nueva estructura consolidada
    'patco_base',                  # Funcionalidades base y clasificaciones
    'patco_skills_mgmt',           # Gestión de habilidades técnicas
    'patco_equipment',             # Gestión consolidada de equipos
    'patco_fsm',                   # Field Service Management consolidado
    'patco_stock_fsm',             # Integración Stock-FSM
    'patco_timesheet',             # Integración Timesheet-FSM
]
```

### Migración desde Estructura Anterior:
- `patco_core` → **Consolidado** en `patco_base`, `patco_fsm`, `patco_stock_fsm`
- `patco_customer_equipment` → **Consolidado** en `patco_equipment`
- Funcionalidades FSM dispersas → **Consolidado** en `patco_fsm`
- Integraciones específicas → **Separadas** en `patco_stock_fsm` y `patco_timesheet`

## Dependencias OCA

El orquestador gestiona automáticamente las dependencias OCA requeridas:

### Módulos OCA Declarados
```python
# Dependencias OCA en __manifest__.py
'fieldservice',                    # Gestión de servicios de campo
'hr_timesheet',                   # Gestión de hojas de tiempo
'partner_firstname',              # Nombres de contactos
'base_location',                  # Gestión de ubicaciones
'base_location_geonames_import',  # Importación de ubicaciones
'web_widget_x2many_2d_matrix',   # Widget de matriz 2D
```

### Dependencias Opcionales
```python
# Módulos opcionales (si están disponibles)
'agreement',          # Gestión de contratos
'helpdesk',          # Sistema de tickets
'fieldservice_skill', # Habilidades para servicios
'fieldservice_stock', # Stock en servicios de campo
```

### Gestión Automática
- **Instalación Declarativa**: Odoo maneja automáticamente la instalación de dependencias
- **Orden de Instalación**: El sistema respeta las dependencias entre módulos
- **Validación Automática**: Odoo verifica la disponibilidad de módulos requeridos
- **Configuración Base**: Los módulos OCA proporcionan la funcionalidad base extendida por PATCO

### Dependencias Externas Gestionadas:
- **OCA Field Service**: Suite completa de servicios de campo
- **OCA Helpdesk**: Sistema de gestión de tickets
- **OCA Agreement**: Gestión de contratos
- **OCA HR Skills**: Extensiones de recursos humanos
- **Odoo Core**: Módulos base del sistema

## Estructura de Archivos

```
patco_suite/
├── __init__.py
├── __manifest__.py              # Definición de dependencias y metadatos
├── security/
│   └── ir.model.access.csv      # Permisos de acceso unificados
├── data/
│   ├── patco_suite_data.xml     # Datos iniciales de configuración
│   └── menu_structure.xml       # Estructura de menús unificada
├── views/
│   ├── patco_dashboard.xml      # Dashboard principal PATCO
│   └── configuration_wizard.xml # Asistente de configuración inicial
├── wizard/
│   └── patco_setup_wizard.py    # Lógica del asistente de configuración
├── static/
│   ├── description/
│   │   ├── icon.png             # Icono de la suite
│   │   └── index.html           # Página de descripción
│   └── src/
│       ├── css/
│       │   └── patco_style.css  # Estilos personalizados
│       └── js/
│           └── patco_dashboard.js # JavaScript del dashboard
└── README.md
```

## Funcionalidades Principales

### 1. Dashboard Unificado PATCO
- **Vista Consolidada**: Métricas y KPIs de toda la operación
- **Accesos Rápidos**: Enlaces directos a funcionalidades principales
- **Alertas Centralizadas**: Notificaciones de todos los módulos
- **Reportes Ejecutivos**: Resúmenes de alto nivel

#### Métricas del Dashboard:
```python
dashboard_metrics = {
    'tickets_abiertos': 'Tickets de soporte pendientes',
    'ordenes_fsm_activas': 'Órdenes de servicio en progreso',
    'tecnicos_disponibles': 'Técnicos disponibles para asignación',
    'equipos_mantenimiento': 'Equipos próximos a mantenimiento',
    'contratos_vigentes': 'Contratos activos de servicio',
    'satisfaccion_cliente': 'Promedio de satisfacción del cliente',
    'tiempo_respuesta': 'Tiempo promedio de respuesta',
    'eficiencia_tecnica': 'Eficiencia operacional de técnicos'
}
```

### 2. Asistente de Configuración Inicial
- **Configuración Guiada**: Paso a paso para configuración inicial
- **Datos Maestros**: Creación de catálogos básicos
- **Integración de Módulos**: Configuración de conexiones entre módulos
- **Validación de Setup**: Verificación de configuración correcta

#### Pasos del Asistente:
1. **Información de la Empresa**: Datos básicos de la organización
2. **Configuración de Usuarios**: Creación de roles y permisos
3. **Catálogo de Servicios**: Definición de naturalezas de servicio
4. **Matriz de Habilidades**: Configuración de competencias técnicas
5. **Tipos de Equipos**: Definición de categorías de equipos HORECA
6. **Plantillas de Contratos**: Configuración de acuerdos tipo
7. **Configuración de Notificaciones**: Alertas y comunicaciones
8. **Validación Final**: Verificación de configuración completa

### 3. Gestión Centralizada de Configuración
- **Parámetros Globales**: Configuración que afecta a todos los módulos
- **Sincronización de Datos**: Mantenimiento de consistencia entre módulos
- **Backup de Configuración**: Respaldo de configuraciones críticas
- **Migración de Datos**: Herramientas para actualización de versiones

### 4. Monitoreo y Salud del Sistema
- **Health Check**: Verificación del estado de todos los módulos
- **Performance Monitoring**: Seguimiento de rendimiento del sistema
- **Error Tracking**: Registro y seguimiento de errores
- **Usage Analytics**: Análisis de uso de funcionalidades

## Casos de Uso Principales

### 1. Instalación Nueva de PATCO
```python
# Instalación completa con un solo comando
def install_patco_suite():
    # El sistema instala automáticamente:
    # 1. Todos los módulos OCA requeridos
    # 2. Todos los módulos PATCO en orden correcto
    # 3. Datos iniciales y configuración base
    # 4. Estructura de menús y permisos
    
    modules_to_install = [
        'fieldservice', 'fieldservice_skill', 'fieldservice_stock',
        'helpdesk_mgmt', 'agreement',
        'patco_base', 'patco_equipment', 'patco_skills_mgmt'
    ]
    
    for module in modules_to_install:
        install_module(module)
        validate_installation(module)
    
    run_configuration_wizard()
    create_initial_data()
    
    return "PATCO Suite instalado exitosamente"
```

### 2. Configuración Inicial Guiada
```python
# Asistente de configuración paso a paso
def run_setup_wizard():
    wizard_steps = [
        ('company_info', 'Configurar información de empresa'),
        ('user_roles', 'Crear roles y usuarios'),
        ('service_catalog', 'Definir catálogo de servicios'),
        ('skill_matrix', 'Configurar matriz de habilidades'),
        ('equipment_types', 'Definir tipos de equipos'),
        ('contract_templates', 'Crear plantillas de contratos'),
        ('notifications', 'Configurar notificaciones'),
        ('validation', 'Validar configuración completa')
    ]
    
    for step_id, step_name in wizard_steps:
        execute_wizard_step(step_id)
        validate_step_completion(step_id)
    
    return "Configuración inicial completada"
```

### 3. Monitoreo de Salud del Sistema
```python
# Verificación del estado de todos los módulos consolidados
def system_health_check():
    health_status = {
        # Módulos PATCO consolidados
        'patco_base': check_module_health('patco_base'),
        'patco_skills_mgmt': check_module_health('patco_skills_mgmt'),
        'patco_equipment': check_module_health('patco_equipment'),
        'patco_fsm': check_module_health('patco_fsm'),
        'patco_stock_fsm': check_module_health('patco_stock_fsm'),
        'patco_timesheet': check_module_health('patco_timesheet'),
        
        # Dependencias OCA
        'fieldservice': check_module_health('fieldservice'),
        'hr_timesheet': check_module_health('hr_timesheet'),
        'agreement': check_module_health('agreement')
    }
    
    overall_health = all(status['healthy'] for status in health_status.values())
    
    return {
        'overall_healthy': overall_health,
        'module_status': health_status,
        'recommendations': generate_health_recommendations(health_status)
    }
```

## Integración con Macro-procesos PATCO

### Macro-proceso 1: Comercial y Onboarding
- **Configuración de Clientes**: Asistente para onboarding de nuevos clientes
- **Creación de Contratos**: Plantillas y flujos de creación de acuerdos
- **Registro de Activos**: Proceso guiado de registro de equipos
- **Configuración de Servicios**: Definición de servicios específicos del cliente

### Macro-proceso 2: Operaciones de Servicio
- **Dashboard Operacional**: Vista unificada de operaciones en curso
- **Asignación Inteligente**: Coordinación entre tickets, FSM y habilidades
- **Gestión de Stock**: Integración con inventario y logística
- **Seguimiento en Tiempo Real**: Monitoreo de servicios activos

### Macro-proceso 3: Ejecución en Campo
- **Interface Móvil**: Acceso unificado para técnicos en campo
- **Sincronización de Datos**: Coordinación entre aplicaciones móviles y sistema
- **Reportes de Campo**: Consolidación de información de servicios
- **Validación de Calidad**: Procesos de verificación y aprobación

### Macro-proceso 4: Cierre y Facturación
- **Consolidación de Servicios**: Agrupación de servicios para facturación
- **Generación de Reportes**: Reportes ejecutivos y operacionales
- **Análisis de Performance**: Métricas y KPIs consolidados
- **Facturación Automática**: Integración con sistemas de facturación

## Beneficios del Módulo Orquestador

### Para Administradores:
1. **Instalación Simplificada**: Un solo punto de instalación
2. **Gestión Centralizada**: Control unificado de toda la suite
3. **Configuración Guiada**: Proceso estructurado de setup inicial
4. **Monitoreo Integral**: Visibilidad completa del sistema

### Para Usuarios Finales:
1. **Experiencia Unificada**: Interface consistente en todos los módulos
2. **Acceso Centralizado**: Dashboard único con toda la información
3. **Navegación Intuitiva**: Estructura de menús lógica y organizada
4. **Soporte Integrado**: Ayuda y documentación centralizadas

### Para el Negocio:
1. **Reducción de Complejidad**: Simplificación de la gestión técnica
2. **Menor Tiempo de Implementación**: Setup más rápido y eficiente
3. **Consistencia Operacional**: Procesos estandarizados en toda la organización
4. **Escalabilidad**: Fácil adición de nuevos módulos y funcionalidades

## Configuración y Personalización

### Configuración Inicial Requerida:
1. **Información de la Empresa**:
   - Datos básicos de la organización
   - Configuración de moneda y localización
   - Estructura organizacional

2. **Usuarios y Permisos**:
   - Creación de roles PATCO
   - Asignación de permisos por módulo
   - Configuración de grupos de acceso

3. **Datos Maestros**:
   - Catálogo de naturalezas de servicio
   - Matriz de habilidades técnicas
   - Tipos y categorías de equipos
   - Plantillas de contratos

4. **Configuración de Integración**:
   - Conexiones entre módulos
   - Flujos de datos automatizados
   - Reglas de negocio específicas

### Personalización Avanzada:
- **Dashboard Customizado**: Métricas específicas del negocio
- **Flujos de Trabajo**: Procesos adaptados a la organización
- **Reportes Personalizados**: Análisis según necesidades específicas
- **Integraciones Externas**: Conexiones con sistemas de terceros

## Estructura de Menús Unificada

```
PATCO Suite/
├── Dashboard Principal
├── Configuración/
│   ├── Asistente de Setup
│   ├── Parámetros Globales
│   ├── Gestión de Usuarios
│   └── Monitoreo del Sistema
├── Operaciones/
│   ├── Tickets de Soporte (Helpdesk)
│   ├── Órdenes de Servicio (FSM)
│   ├── Gestión de Equipos
│   └── Asignación de Técnicos
├── Recursos Humanos/
│   ├── Gestión de Técnicos
│   ├── Matriz de Habilidades
│   ├── Evaluaciones
│   └── Capacitaciones
├── Contratos y Acuerdos/
│   ├── Gestión de Contratos
│   ├── Plantillas
│   ├── Renovaciones
│   └── Facturación
├── Reportes y Análisis/
│   ├── Dashboard Ejecutivo
│   ├── Reportes Operacionales
│   ├── Análisis de Performance
│   └── KPIs y Métricas
└── Soporte y Ayuda/
    ├── Documentación
    ├── Tutoriales
    ├── Soporte Técnico
    └── Actualizaciones
```

## Métricas y KPIs del Dashboard

### Métricas Operacionales:
- **Tickets Activos**: Número de tickets de soporte abiertos
- **Órdenes FSM**: Servicios de campo en progreso
- **Técnicos Disponibles**: Recursos humanos disponibles
- **Equipos en Mantenimiento**: Activos en proceso de servicio
- **Tiempo de Respuesta**: Promedio de respuesta a tickets
- **Eficiencia de Asignación**: Porcentaje de asignaciones exitosas

### Métricas de Calidad:
- **Satisfacción del Cliente**: Rating promedio de servicios
- **Primera Resolución**: Porcentaje de tickets resueltos en primera visita
- **Cumplimiento de SLA**: Porcentaje de servicios dentro de SLA
- **Calidad de Servicio**: Evaluación de calidad técnica

### Métricas Financieras:
- **Contratos Activos**: Valor de contratos vigentes
- **Facturación Mensual**: Ingresos por servicios
- **Costos Operacionales**: Gastos de operación
- **Rentabilidad por Cliente**: Margen por cliente

### Métricas de Recursos Humanos:
- **Utilización de Técnicos**: Porcentaje de tiempo productivo
- **Desarrollo de Habilidades**: Progreso en competencias
- **Rotación de Personal**: Indicadores de retención
- **Productividad**: Servicios completados por técnico

## Flujos de Trabajo Principales

### 1. Instalación y Setup Inicial
1. **Instalación del Módulo**: `patco_suite` instala todas las dependencias
2. **Ejecución del Asistente**: Configuración guiada paso a paso
3. **Creación de Datos Maestros**: Catálogos y configuraciones base
4. **Configuración de Usuarios**: Roles y permisos específicos
5. **Validación del Setup**: Verificación de configuración correcta
6. **Capacitación de Usuarios**: Introducción al sistema

### 2. Operación Diaria
1. **Acceso al Dashboard**: Vista consolidada de operaciones
2. **Revisión de Alertas**: Notificaciones y tareas pendientes
3. **Gestión de Tickets**: Procesamiento de solicitudes de soporte
4. **Asignación de Servicios**: Coordinación de recursos y servicios
5. **Monitoreo de Progreso**: Seguimiento de servicios activos
6. **Generación de Reportes**: Análisis de performance y resultados

### 3. Mantenimiento del Sistema
1. **Health Check Regular**: Verificación del estado del sistema
2. **Actualización de Configuraciones**: Ajustes según necesidades
3. **Backup de Datos**: Respaldo de configuraciones críticas
4. **Monitoreo de Performance**: Seguimiento de rendimiento
5. **Actualizaciones de Módulos**: Gestión de versiones
6. **Soporte Técnico**: Resolución de incidencias

## Estado Actual del Módulo

### Implementación Actual:
- **Estructura Base**: Manifiesto con dependencias completas definidas
- **Dependencias OCA**: Integración con módulos de Field Service, Helpdesk y Agreement
- **Módulos PATCO**: Coordinación de todos los módulos específicos
- **Configuración**: Archivos de datos y vistas básicas implementados

### Funcionalidades Implementadas:
- **Gestión de Dependencias**: Instalación automática de módulos requeridos
- **Estructura de Menús**: Organización lógica de funcionalidades
- **Permisos de Acceso**: Control de acceso unificado
- **Datos Iniciales**: Configuración base del sistema

### Desarrollo Futuro:
1. **Dashboard Avanzado**: Métricas en tiempo real y visualizaciones
2. **Asistente de Configuración**: Wizard interactivo de setup
3. **Monitoreo de Salud**: Sistema de health check automatizado
4. **Reportes Ejecutivos**: Análisis avanzados y KPIs
5. **Integración Mobile**: Soporte para aplicaciones móviles
6. **API de Integración**: Conectores para sistemas externos

## Compatibilidad y Requisitos

### Versión de Odoo:
- **Compatible con**: Odoo 18 Community Edition
- **Arquitectura**: Modular y escalable
- **Base de Datos**: PostgreSQL recomendado

### Módulos OCA Requeridos:
- `fieldservice`: Gestión de servicios de campo
- `fieldservice_skill`: Habilidades para servicios
- `fieldservice_stock`: Gestión de stock en servicios
- `helpdesk_mgmt`: Sistema de tickets de soporte
- `agreement`: Gestión de contratos y acuerdos

### Recursos del Sistema:
- **RAM**: Mínimo 4GB, recomendado 8GB+
- **Almacenamiento**: 10GB+ para datos y logs
- **CPU**: Procesador multi-core recomendado
- **Red**: Conexión estable para sincronización

## Nueva Estructura Modular Consolidada (v2.0)

### Beneficios de la Consolidación

#### 1. Eliminación de Duplicaciones
- **Modelos Unificados**: Clasificaciones de servicios consolidadas en `patco_base`
- **Funcionalidades FSM**: Todas las extensiones FSM en un solo módulo `patco_fsm`
- **Gestión de Equipos**: Consolidación completa en `patco_equipment`
- **Integraciones Específicas**: Separación clara en `patco_stock_fsm` y `patco_timesheet`

#### 2. Mejor Mantenibilidad
- **Responsabilidades Claras**: Cada módulo tiene un propósito específico y bien definido
- **Dependencias Simplificadas**: Reducción de interdependencias complejas
- **Testing Mejorado**: Pruebas más focalizadas por módulo
- **Documentación Centralizada**: Cada módulo con su documentación específica

#### 3. Performance Optimizado
- **Carga Selectiva**: Instalación solo de módulos necesarios
- **Menos Overhead**: Reducción de código duplicado y consultas redundantes
- **Cache Eficiente**: Mejor utilización de cache por separación de responsabilidades
- **Startup Más Rápido**: Inicialización optimizada del sistema

### Módulos Consolidados Detallados

#### `patco_base` - Fundamentos del Sistema
- **Clasificaciones de Servicios**: Naturaleza, área, complejidad
- **Configuraciones Base**: Parámetros globales del sistema
- **Utilidades Comunes**: Funciones compartidas entre módulos
- **Datos Maestros**: Catálogos base del sistema

#### `patco_equipment` - Gestión Integral de Equipos
- **Equipos de Cliente**: Gestión completa de equipos HORECA
- **Categorías y Jerarquías**: Organización de tipos de equipos
- **Historial de Mantenimiento**: Trazabilidad completa
- **Base de Conocimiento**: Documentación técnica por equipo

#### `patco_fsm` - Field Service Management
- **Órdenes de Servicio Extendidas**: Campos y funcionalidades adicionales
- **Hojas de Trabajo Digitales**: Formularios personalizables
- **Gestión de Repuestos**: Consumo y seguimiento de partes
- **Checklists**: Listas de verificación de entrada y salida

#### `patco_stock_fsm` - Integración Stock-FSM
- **Consumo de Repuestos**: Integración directa con inventario
- **Movimientos de Stock**: Trazabilidad de movimientos por orden
- **Ubicaciones de Vehículos**: Gestión de stock móvil
- **Reportes de Consumo**: Análisis de uso de repuestos

#### `patco_timesheet` - Integración Timesheet-FSM
- **Registro de Tiempo**: Integración con hojas de tiempo
- **Costos de Servicio**: Cálculo automático de costos
- **Análisis de Productividad**: Métricas de eficiencia técnica
- **Facturación de Servicios**: Base para facturación de tiempo

### Migración y Compatibilidad

Para instalaciones existentes, consulte el [Plan de Migración](MIGRATION_PLAN.md) que incluye:
- **Estrategias de Migración**: Opciones para diferentes escenarios
- **Scripts de Migración**: Herramientas automáticas de migración
- **Verificación Post-Migración**: Checklists de validación
- **Rollback Procedures**: Procedimientos de reversión

## Soporte y Mantenimiento

### Logs y Debugging
- **Logs Centralizados**: Todos los módulos PATCO escriben logs con prefijo `[PATCO]`
- **Niveles de Log**: DEBUG, INFO, WARNING, ERROR según configuración
- **Rotación de Logs**: Configuración automática de rotación de archivos
- **Alertas Automáticas**: Notificaciones en caso de errores críticos

### Actualizaciones
- **Versionado Semántico**: Seguimiento de versiones MAJOR.MINOR.PATCH
- **Migración de Datos**: Scripts automáticos para actualización de versiones
- **Rollback**: Procedimientos de reversión en caso de problemas
- **Testing**: Suite de pruebas automatizadas antes de cada release

### Documentación
- **Wiki Interna**: Documentación técnica detallada
- **Guías de Usuario**: Manuales paso a paso para usuarios finales
- **API Documentation**: Documentación de APIs y métodos públicos
- **Troubleshooting**: Guía de resolución de problemas comunes

### Canales de Soporte:
- **Documentación**: README completo de cada módulo
- **Tutoriales**: Guías paso a paso de configuración
- **Soporte Técnico**: Canal dedicado para resolución de incidencias
- **Comunidad**: Foro de usuarios y desarrolladores

### Mantenimiento Preventivo:
- **Actualizaciones Regulares**: Nuevas versiones y parches
- **Backup Automático**: Respaldo de configuraciones críticas
- **Monitoreo Proactivo**: Detección temprana de problemas
- **Optimización de Performance**: Ajustes de rendimiento

### Ciclo de Vida:
- **Desarrollo Continuo**: Nuevas funcionalidades basadas en feedback
- **Compatibilidad**: Soporte para nuevas versiones de Odoo
- **Migración**: Herramientas para actualización de versiones
- **Deprecación**: Comunicación clara de cambios importantes

---

**Versión**: 2.0.0 (Estructura Consolidada)  
**Compatibilidad**: Odoo 18.0 Community  
**Licencia**: LGPL-3  
**Autor**: PATCO Development Team  
**Fecha**: 2024

---

**PATCO Suite** - La solución completa para mantenimiento HORECA en una sola instalación

*Simplificando la complejidad, maximizando la eficiencia*