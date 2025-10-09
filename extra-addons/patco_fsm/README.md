# PATCO FSM - Gestión Avanzada de Servicios de Campo

**Versión:** 18.0.1.0.0  
**Autor:** PATCO  
**Categoría:** Field Service  

## Descripción

Módulo de extensión para Field Service Management (FSM) que integra funcionalidades específicas de PATCO para la gestión completa de órdenes de servicio técnico. Incluye hojas de trabajo digitales con firmas electrónicas, consumo inteligente de repuestos, control de tiempo con timer integrado, facturación automatizada y sistema de habilidades técnicas.

## Funcionalidades Principales

### 1. Extensiones a Órdenes de Servicio (fsm.order)

#### Sistema de Clasificación PATCO
- **Naturaleza del Servicio** (`x_service_nature_id`): Categorización por tipo de trabajo
- **Área de Trabajo** (`x_service_area_id`): Clasificación por especialidad técnica  
- **Complejidad** (`x_service_complexity_id`): Niveles de dificultad del servicio
- **Código de Clasificación** (`x_classification_code`): Generación automática formato "NAT-ARE-COM"

#### Gestión Inteligente de Habilidades Técnicas
- **Habilidades Requeridas** (`x_required_skill_ids`): Competencias necesarias para el servicio
- **Filtrado Automático**: Solo técnicos con habilidades compatibles aparecen en selección
- **Advertencias de Compatibilidad** (`x_skill_warning`): Alertas cuando técnico no tiene todas las habilidades
- **Sugerencias Inteligentes** (`x_suggested_person_ids`): Técnicos recomendados por habilidades y ubicación
- **Técnicos Disponibles** (`x_available_technicians_count`): Contador de técnicos aptos

#### Control de Tiempo Avanzado
- **Timer Integrado** (`x_timer_start`, `x_timer_pause`): Control de tiempo en tiempo real
- **Estado del Timer** (`x_timer_status`): Detenido/Corriendo/Pausado
- **Tiempo Total** (`x_total_timesheet_time`): Suma automática de registros de tiempo
- **Conteo de Timesheets** (`x_timesheet_count`): Número de registros de tiempo
- **Integración Completa**: Sincronización automática con `hr.timesheet`

#### Sistema de Checklists Dinámicos
- **Checklist de Entrada** (`x_checklist_entry`): Verificaciones HTML previas al trabajo
- **Checklist de Salida** (`x_checklist_exit`): Validaciones HTML al finalizar
- **Contenido Dinámico**: Basado en categoría del equipo asociado
- **Base de Conocimientos**: Integración con artículos de conocimiento del equipo

### 2. Hojas de Trabajo Digitales (fsm.worksheet)

#### Características Principales
- **Plantillas Configurables** (`template_id`): Basadas en categoría de equipo y naturaleza de servicio
- **Datos Dinámicos JSON** (`worksheet_data`): Estructura flexible para cualquier tipo de información
- **Estados de Workflow**: `draft` → `in_progress` → `completed` → `approved`/`rejected`
- **Firmas Digitales**: Captura de firmas de técnico (`technician_signature`) y cliente (`customer_signature`)
- **Generación PDF**: Reportes automáticos con firmas integradas
- **Nomenclatura Automática**: Formato "WS-{orden}-{secuencia}" generado automáticamente
- **Duración Calculada**: Campo computado `duration` basado en fechas de inicio y fin

#### Campos de Información Completos
- **Identificación**: `name`, `fsm_order_id`, `template_id`, `state`
- **Personal**: `technician_id`, `customer_id` (computados desde la orden)
- **Temporales**: `start_date`, `end_date`, `duration` (calculada automáticamente)
- **Contenido**: `worksheet_data` (JSON), `comments`, `attachments`
- **Firmas**: `technician_signature`, `customer_signature`, `customer_name`, `customer_document`
- **Reportes**: `report_pdf` (generado automáticamente)

#### Proceso de Aprobación Avanzado
- **Inicio de Trabajo**: Botón "Iniciar Trabajo" cambia estado a `in_progress`
- **Completar Trabajo**: Botón "Completar Trabajo" requiere firma del técnico
- **Aprobación Cliente**: Wizard especializado para captura de datos y firma del cliente
- **Estados Finales**: `approved` (cliente conforme) o `rejected` (cliente no conforme)
- **Trazabilidad**: Registro completo de fechas y responsables en cada etapa

### 3. Gestión Inteligente de Repuestos (fsm.order.consumed.part)

#### Control de Inventario Avanzado
- **Registro Detallado** (`sequence`, `part_id`, `quantity`): Control secuencial de repuestos consumidos
- **Ubicación de Origen** (`source_location_id`): Integración con ubicaciones de vehículos técnicos
- **Validación de Stock**: Verificación automática de disponibilidad antes del consumo
- **Movimientos Automáticos** (`stock_move_id`): Generación automática de movimientos de inventario
- **Estados de Control** (`state`): `draft` → `confirmed` → `cancelled` con trazabilidad completa
- **Métodos Principales**: `_compute_cost()`, `confirm_consumption()`, `cancel_consumption()`, `_create_stock_move()`

#### Costos y Facturación Automatizada
- **Costo Unitario** (`unit_cost`): Calculado automáticamente desde el producto
- **Costo Total** (`total_cost`): Computado como `quantity * unit_cost`
- **Costo Total de Orden** (`x_total_consumed_parts_cost`): Suma de todos los repuestos consumidos
- **Integración Facturación**: Automática al cambiar etapas de la orden de servicio
- **Trazabilidad Completa**: Registro de todos los movimientos y costos
- **Notas Técnicas** (`notes`): Observaciones del técnico sobre el consumo

### 4. Plantillas de Hojas de Trabajo (fsm.worksheet.template)

#### Configuración Flexible y Reutilizable
- **Asociación Múltiple** (`equipment_category_ids`): Vinculación a categorías específicas de equipos
- **Naturalezas de Servicio** (`service_nature_ids`): Configuración por tipo de trabajo
- **Campos Dinámicos** (`field_configuration`): Estructura JSON para definir campos personalizados
- **Reutilización Inteligente**: Una plantilla puede usarse en múltiples órdenes y equipos
- **Descripción Detallada** (`description`): Documentación completa del propósito de la plantilla

#### Estructura de Datos JSON
- **Configuración de Campos**: Definición de tipos, validaciones y valores por defecto
- **Metadatos**: Información adicional para renderizado dinámico
- **Validaciones Personalizadas**: Reglas de negocio específicas por plantilla
- **Ayudas Contextuales**: Textos de ayuda y ejemplos para el técnico

### 5. Integración con Contactos (res.partner)

#### Pestaña de Ubicaciones FSM
- **Vista Integrada**: Nueva pestaña "Ubicaciones FSM" en el formulario de contactos
- **Gestión Centralizada**: Visualización y gestión de todas las ubicaciones FSM asociadas a un cliente
- **Campos de Control**:
  - `fsm_location` (Boolean): Indica si el contacto es una ubicación FSM
  - `service_location_id` (Many2one): Ubicación principal de servicio
  - `owned_location_ids` (One2many): Lista de todas las ubicaciones propiedad del contacto

#### Funcionalidades de la Pestaña
- **Lista Completa**: Visualización de todas las ubicaciones FSM del cliente
- **Creación Directa**: Posibilidad de crear nuevas ubicaciones desde el contacto
- **Edición Integrada**: Modificación de ubicaciones existentes sin salir del formulario
- **Campos Visibles**:
  - Nombre de la ubicación
  - Dirección completa (calle, ciudad, estado, país)
  - Teléfono y email de contacto
  - Persona de contacto en la ubicación
  - Propietario de la ubicación
  - Estado activo/inactivo

#### Beneficios Operativos
- **Vista Unificada**: Toda la información de ubicaciones del cliente en un solo lugar
- **Navegación Eficiente**: Acceso rápido a ubicaciones sin cambiar de vista
- **Gestión Simplificada**: Creación y edición de ubicaciones desde el contexto del cliente
- **Trazabilidad Completa**: Relación clara entre clientes y sus ubicaciones de servicio

## Wizards y Asistentes Especializados

### 1. Wizard de Consumo de Repuestos (fsm.consume.parts.wizard)
- **Selección Inteligente**: Repuestos disponibles desde ubicación del vehículo técnico
- **Validación de Stock**: Verificación automática de cantidades disponibles
- **Generación Automática**: Creación de movimientos de stock y registros de consumo
- **Integración Completa**: Actualización automática de costos en la orden de servicio

### 2. Wizard de Aprobación del Cliente (fsm.worksheet.customer.approval.wizard)
- **Captura de Datos**: Nombre, documento y cargo del cliente firmante
- **Firma Digital**: Captura táctil o con mouse de la firma del cliente
- **Proceso de Decisión**: Botones de aprobación/rechazo con comentarios obligatorios
- **Observaciones**: Campo de texto libre para comentarios del cliente

### 3. Wizard de Firmas Digitales (fsm.worksheet.signature.wizard)
- **Tipos de Firma**: Técnico (`technician`) o Cliente (`customer`)
- **Captura Segura**: Almacenamiento en formato base64 de las firmas
- **Validación de Datos**: Verificación de campos requeridos según el tipo de firma
- **Integración Workflow**: Actualización automática del estado de la hoja de trabajo

### 4. Wizard de Datos Dinámicos (fsm.worksheet.data.wizard)
- **Carga de Plantilla**: Obtención automática de la configuración de campos
- **Datos Dinámicos**: Interfaz generada automáticamente según la plantilla
- **Almacenamiento JSON**: Guardado estructurado de la información capturada
- **Validación**: Verificación de campos obligatorios y formatos

## Arquitectura de Modelos de Datos

### Modelos Principales
- **`fsm.order`** - Extensión de órdenes de servicio con clasificación PATCO, habilidades, timer y facturación
  - Métodos clave: `_generate_classification_code()`, `_compute_consumed_parts_cost()`, `_onchange_person_id()`, `_suggest_technicians_by_skills()`
- **`fsm.worksheet`** - Hojas de trabajo digitales con workflow, firmas y datos JSON dinámicos
  - Métodos clave: `_compute_duration()`, `action_start_work()`, `action_complete_work()`, `action_approve()`, `action_reject()`
- **`fsm.worksheet.template`** - Plantillas configurables por categoría de equipo y naturaleza de servicio
- **`fsm.order.consumed.part`** - Gestión de repuestos consumidos con control de stock y costos
  - Métodos clave: `_compute_cost()`, `confirm_consumption()`, `cancel_consumption()`, `_create_stock_move()`

### Modelos Transitorios (Wizards)
- **`fsm.consume.parts.wizard`** - Asistente para consumo inteligente de repuestos
  - Métodos clave: `action_consume_parts()`, `_create_consumed_part()`, `_create_stock_move()`, `_validate_quantities()`
- **`fsm.worksheet.customer.approval.wizard`** - Proceso de aprobación del cliente con firma
- **`fsm.worksheet.signature.wizard`** - Captura de firmas digitales de técnico y cliente
- **`fsm.worksheet.data.wizard`** - Manejo de datos dinámicos basados en plantillas JSON

## Dependencias del Módulo

### Módulos Odoo Core Requeridos
- **`base`** - Funcionalidades básicas del framework
- **`maintenance`** - Gestión de equipos y mantenimiento
- **`hr_timesheet`** - Sistema de registro de tiempo y timesheets
- **`helpdesk_mgmt`** - Gestión de tickets y soporte técnico

### Módulos OCA (Odoo Community Association)
- **`fieldservice`** - Base del sistema de gestión de servicios de campo
- **`fieldservice_skill`** - Integración de habilidades técnicas con FSM

### Módulos PATCO Internos
- **`patco_base`** - Configuraciones base y datos maestros PATCO
- **`patco_timesheet`** - Extensiones de timesheet con integración FSM específica
- **`patco_equipment`** - Gestión de equipos con códigos PATCO y QR

### Estructura de Archivos del Módulo
```
patco_fsm/
├── __init__.py
├── __manifest__.py
├── README.md
├── data/
│   └── fsm_worksheet_template_data.xml          # Plantillas predefinidas
├── migrations/
│   └── 18.0.1.0.0/
│       └── pre-init.sql                        # Migración inicial
├── models/
│   ├── __init__.py
│   ├── fsm_order.py                            # Extensión órdenes FSM (400+ líneas)
│   ├── fsm_order_consumed_part.py              # Gestión repuestos (140 líneas)
│   └── fsm_worksheet.py                        # Hojas de trabajo (200+ líneas)
├── security/
│   └── ir.model.access.csv                     # Permisos de acceso
├── views/
│   ├── fsm_consumed_parts_views.xml            # Vistas repuestos consumidos
│   ├── fsm_order_checklist_views.xml           # Vistas checklists
│   ├── fsm_order_views.xml                     # Vistas órdenes FSM
│   ├── fsm_worksheet_customer_approval_wizard_views.xml  # Wizard aprobación
│   └── fsm_worksheet_signature_wizard_views.xml # Wizard firmas
└── wizards/
    ├── __init__.py
    ├── fsm_consume_parts_wizard.py             # Wizard consumo repuestos (184 líneas)
    ├── fsm_worksheet_customer_approval_wizard.py
    └── fsm_worksheet_signature_wizard.py
```

## Instalación y Configuración

### Requisitos Previos del Sistema
1. **Módulos OCA**: `fieldservice`, `fieldservice_skill` instalados y configurados
2. **Módulos PATCO**: `patco_base`, `patco_timesheet` como dependencias internas
3. **Configuración de Inventario**: Ubicaciones de vehículos técnicos definidas
4. **Gestión de Habilidades**: Habilidades técnicas configuradas en HR
5. **Equipos de Cliente**: Categorías de equipos y equipos registrados

### Proceso de Instalación Recomendado
1. **Instalación Automática**: Usar `patco_suite` que instala automáticamente este módulo
2. **Configuración de Plantillas**: Crear plantillas de hojas de trabajo por categoría de equipo
3. **Datos Maestros**: Definir naturalezas de servicio, áreas de trabajo y niveles de complejidad
4. **Políticas de Facturación**: Configurar facturación automática por etapas
5. **Capacitación**: Entrenar técnicos en el uso de dispositivos móviles y tablets

### Configuración Post-Instalación
- **Plantillas de Worksheet**: Configurar campos JSON dinámicos por tipo de servicio
- **Ubicaciones de Stock**: Asignar ubicaciones de inventario a vehículos técnicos
- **Habilidades Técnicas**: Mapear habilidades requeridas por categoría de equipo
- **Flujos de Aprobación**: Definir procesos de firma y aprobación del cliente

## Casos de Uso Técnicos Detallados

### Flujo de Servicio Preventivo Completo
1. **Creación de Orden**: Clasificación automática con `service_nature_id`, `service_area_id`, `service_complexity_id`
2. **Asignación Inteligente**: Sistema sugiere técnicos basado en `required_skill_ids` y `suggested_person_ids`
3. **Validación de Habilidades**: Verificación automática con alertas en `skill_warning`
4. **Generación de Worksheet**: Creación automática desde `template_id` con datos JSON dinámicos
5. **Checklist de Entrada**: Ejecución de `checklist_entry` HTML personalizado
6. **Control de Tiempo**: Activación de timer con `timer_start` y seguimiento en `timer_status`
7. **Consumo de Repuestos**: Uso del wizard `fsm.consume.parts.wizard` con validación de stock
8. **Completar Trabajo**: Cambio de estado a `completed` con firma del técnico
9. **Aprobación Cliente**: Wizard `fsm.worksheet.customer.approval.wizard` con firma digital
10. **Facturación Automática**: Generación basada en `billing_policy` al cambiar etapa

### Flujo de Servicio Correctivo de Emergencia
1. **Orden de Alta Prioridad**: Creación con clasificación correctiva y prioridad alta
2. **Asignación por Proximidad**: Algoritmo de `suggested_person_ids` considera ubicación
3. **Timer Automático**: Inicio inmediato con `timer_start` al asignar técnico
4. **Documentación de Falla**: Captura en `worksheet_data` JSON con campos específicos
5. **Consumo de Emergencia**: Repuestos desde ubicación del vehículo con `source_location_id`
6. **Registro de Solución**: Actualización de `worksheet_data` con solución implementada
7. **Conformidad Rápida**: Proceso de aprobación simplificado del cliente
8. **Facturación T&M**: Tiempo (`total_timesheet_time`) y materiales (`total_consumed_parts_cost`)

## Funcionalidades Técnicas Avanzadas

### Sistema de Timer Integrado
- **Estados**: `stopped`, `running`, `paused` en `timer_status`
- **Control**: Métodos `action_start_timer()`, `action_stop_timer()`, `action_pause_timer()`
- **Sincronización**: Automática con registros de `hr.timesheet`
- **Cálculos**: Tiempo total en `total_timesheet_time`

### Gestión de Firmas Digitales
- **Captura**: Base64 en `technician_signature` y `customer_signature`
- **Validación**: Datos obligatorios según tipo de firma
- **Almacenamiento**: Seguro con trazabilidad completa
- **PDF**: Generación automática con firmas integradas

### Sistema de Facturación Inteligente
- **Políticas**: `time_material`, `fixed_price`, `no_billing`
- **Automática**: Trigger en cambio de etapa con `_auto_create_invoice()`
- **Componentes**: Tiempo de técnicos + costo de repuestos
- **Trazabilidad**: Completa desde orden hasta factura

## Integración con Ecosistema PATCO

### Conexión con patco_base
- Datos maestros de clasificación (naturaleza, área, complejidad)
- Configuraciones globales del sistema
- Secuencias y numeración automática

### Integración con patco_timesheet
- Campo `fsm_order_id` en `account.analytic.line`
- Sincronización bidireccional de tiempos
- Reportes unificados de productividad

### Compatibilidad con patco_equipment
- Información automática del equipo en `equipment_info`
- Checklists dinámicos por categoría de equipo
- Base de conocimientos integrada

### Funcionalidades Móviles y Técnicas
- **Responsive Design**: Interfaz adaptada automáticamente para dispositivos móviles
- **Firmas Digitales**: Captura táctil con almacenamiento Base64 seguro
- **Formularios Dinámicos**: Renderizado de `worksheet_data` JSON en dispositivos móviles
- **Timer Móvil**: Control de tiempo desde cualquier dispositivo
- **Consumo de Repuestos**: Wizard optimizado para uso en campo

### Arquitectura Técnica
- **Modelos Principales**: `fsm.order` (extendido), `fsm.worksheet`, `fsm.worksheet.template`
- **Modelos Transitorios**: Wizards para consumo, firmas y aprobaciones
- **Integración OCA**: Compatible con `fieldservice` y módulos relacionados
- **Extensibilidad**: Hooks y métodos para personalización empresarial
- **Seguridad**: RLS y permisos granulares por rol de usuario

### Configuración Post-Instalación
1. **Plantillas de Hojas de Trabajo**: Crear templates con `field_config` JSON
2. **Datos Maestros**: Configurar naturalezas, áreas y complejidades de servicio
3. **Políticas de Facturación**: Definir `billing_policy` por tipo de servicio
4. **Flujos de Aprobación**: Configurar procesos de firma según empresa
5. **Integración Timesheet**: Verificar campo `fsm_order_id` en líneas analíticas

## Seguridad y Permisos

### Grupos de Seguridad (ir.model.access.csv)
- **FSM User**: Acceso básico a órdenes de servicio asignadas
- **FSM Manager**: Gestión completa de órdenes y hojas de trabajo
- **FSM Admin**: Configuración de plantillas y datos maestros
- **Portal User**: Acceso limitado para aprobaciones de cliente

### Reglas de Registro (ir.rule)
- **Órdenes por Técnico**: Filtro automático `[('person_id', '=', user.employee_id.id)]`
- **Hojas de Trabajo**: Acceso basado en asignación de orden
- **Repuestos Consumidos**: Visibilidad según orden asociada
- **Plantillas**: Acceso según grupo de usuario

### Campos Sensibles Protegidos
- **Firmas Digitales**: Almacenamiento seguro Base64
- **Datos de Cliente**: Encriptación en `customer_data` JSON
- **Costos**: Acceso restringido a `unit_cost` y `total_cost`
- **Configuraciones**: Solo administradores pueden modificar `field_config`

### Auditoría y Trazabilidad
- **Tracking**: Automático en campos críticos (`state`, `stage_id`, `person_id`)
- **Logs**: Registro completo de cambios en hojas de trabajo
- **Firmas**: Trazabilidad completa con timestamp y usuario
- **Aprobaciones**: Historial completo del proceso de aprobación

## Mantenimiento y Soporte Técnico

### Estructura de Archivos del Módulo
```
patco_fsm/
├── __manifest__.py          # Definición del módulo y dependencias
├── models/                  # Modelos de datos principales
│   ├── fsm_order.py        # Extensión del modelo fsm.order
│   ├── fsm_worksheet.py    # Hojas de trabajo digitales
│   └── fsm_consumed_parts.py # Gestión de repuestos
├── views/                   # Definiciones de vistas XML
│   ├── fsm_order_views.xml # Vistas extendidas de órdenes
│   ├── fsm_consumed_parts_views.xml # Vistas de repuestos
│   └── fsm_order_checklist_views.xml # Checklists
├── wizards/                 # Asistentes transitorios
│   ├── fsm_worksheet_signature_wizard.py # Firmas
│   ├── fsm_worksheet_customer_approval_wizard.py # Aprobaciones
│   └── fsm_consume_parts_wizard.py # Consumo de repuestos
├── security/               # Permisos y seguridad
│   ├── ir.model.access.csv # Permisos de modelos
│   └── security.xml        # Grupos y reglas
└── data/                   # Datos iniciales
    └── fsm_data.xml        # Configuraciones base
```

### Comandos de Mantenimiento
```bash
# Instalación completa (recomendado)
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_suite --stop-after-init

# Actualización del módulo
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -u patco_fsm --stop-after-init

# Verificación de logs
tail -f c:\Trabajo\PAT02-ERP\logs\odoo.log
```

### Personalización y Extensión
- **Plantillas Personalizadas**: Modificar `field_config` JSON en templates
- **Nuevos Estados**: Extender `selection` en campos de estado
- **Campos Adicionales**: Heredar modelos y agregar campos específicos
- **Wizards Personalizados**: Crear nuevos asistentes para procesos específicos
- **Reportes Customizados**: Integrar con `reporting-engine` de OCA

### Troubleshooting Común
- **Error de Permisos**: Verificar `ir.model.access.csv` y grupos de usuario
- **Firmas No Guardan**: Validar formato Base64 y campos obligatorios
- **Timer No Funciona**: Verificar integración con `patco_timesheet`
- **Facturación Falla**: Revisar `billing_policy` y configuración de etapas

---

**Versión**: 18.0.1.0.0  
**Autor**: PATCO  
**Licencia**: LGPL-3  
**Soporte**: soporte@patco.pe