# PATCO Core - Field Service Management Extensions

Módulo especializado de PATCO que proporciona extensiones específicas para Field Service Management (FSM), enfocado en la gestión avanzada de órdenes de servicio, hojas de trabajo digitales y stock en vehículos.

## Características Principales

### Extensiones de Órdenes de Servicio FSM
- Extensiones al modelo `fsm.order` con campos personalizados
- Integración con checklists y bases de conocimiento
- Gestión de stock en vehículos de técnicos
- Cálculo automático de costos y tiempos
- Integración con habilidades técnicas

### Hojas de Trabajo Digitales
- Modelo `fsm.worksheet` para documentación de trabajos
- Firmas digitales de técnicos y clientes
- Adjuntos y fotografías
- Estados de workflow (borrador, en progreso, completado, aprobado)
- Integración completa con órdenes de servicio

### Gestión de Stock en Vehículos
- Ubicaciones específicas para vehículos de técnicos
- Modelo `fsm.order.consumed.part` para consumo de repuestos
- Transferencias automáticas de stock
- Validaciones de disponibilidad en campo

### Análisis de Tiempos FSM
- Extensiones a `account.analytic.line` para timesheets FSM
- Reportes de análisis de tiempos específicos de campo
- Métricas de productividad por técnico

### Categorías de Equipos con Checklists
- Extensiones a `maintenance.equipment.category`
- Checklists específicos por tipo de equipo
- Integración con bases de conocimiento

## Modelos FSM Específicos

### Modelos Principales
- `fsm.order` - Extensiones avanzadas para órdenes de servicio
- `fsm.worksheet` - Hojas de trabajo digitales
- `fsm.order.consumed.part` - Consumo de repuestos en campo
- `stock.location` - Ubicaciones de vehículos y técnicos
- `account.analytic.line` - Registro de tiempos FSM
- `maintenance.equipment.category` - Categorías con checklists

## Dependencias

- `patco_base` - Módulo base con clasificaciones y configuraciones
- `base` - Funcionalidades base de Odoo
- `sale_management` - Gestión de ventas
- `maintenance` - Mantenimiento de equipos
- `fieldservice` - Servicios de campo (OCA)
- `helpdesk_mgmt` - Gestión de helpdesk (OCA)
- `hr_timesheet` - Hojas de tiempo
- `stock` - Gestión de inventario
- `account` - Contabilidad

## Instalación

1. Asegúrate de tener instalado `patco_base` primero
2. Instala todos los módulos de dependencia OCA
3. Instala el módulo desde Apps > PATCO Core
4. Las ubicaciones de stock para vehículos se crean automáticamente

## Configuración FSM

### Ubicaciones de Stock para Vehículos
El módulo crea automáticamente:
- Vehículos de servicio (ubicación padre)
- Vehículos específicos por técnico (001, 002, 003)
- Ubicación de consumo en campo

### Grupos de Seguridad FSM
- **PATCO Técnico**: Acceso a órdenes asignadas y hojas de trabajo
- **PATCO Líder Técnico**: Supervisión y aprobación de trabajos
- **PATCO Administrador**: Gestión completa del sistema FSM

### Datos Específicos de FSM
El módulo incluye:
- Ubicaciones de stock para vehículos
- Productos de repuestos básicos
- Plantillas de hojas de trabajo
- Reglas de stock para vehículos
- Configuraciones de seguridad FSM

## Uso del Sistema FSM

### Para Técnicos de Campo
1. Accede a "Mis Órdenes de Servicio"
2. Selecciona una orden asignada
3. Inicia la hoja de trabajo digital
4. Registra el consumo de repuestos del vehículo
5. Completa checklists según el tipo de equipo
6. Obtén la firma digital del cliente
7. Finaliza la orden

### Para Líderes Técnicos
1. Supervisa hojas de trabajo completadas
2. Aprueba o rechaza trabajos realizados
3. Gestiona stock en vehículos del equipo
4. Analiza tiempos y productividad

### Para Administradores FSM
1. Configura ubicaciones de vehículos
2. Gestiona permisos de técnicos
3. Supervisa métricas de campo
4. Configura checklists por categoría de equipo

## Integración con Otros Módulos PATCO

- **patco_base**: Utiliza clasificaciones de servicio y configuraciones base
- **patco_equipment**: Integración con gestión de equipos de clientes
- **patco_skills_mgmt**: Asignación basada en habilidades técnicas

## Personalización FSM

Puedes extender:
- Campos personalizados en hojas de trabajo
- Checklists específicos por industria
- Validaciones de consumo de repuestos
- Métricas personalizadas de campo

## Soporte

Para soporte técnico especializado en FSM, contacta al equipo de desarrollo de PATCO.

## Licencia

LGPL-3

**Nota**: Los modelos de clasificación PATCO (naturalezas, áreas y complejidad de servicio) ahora se encuentran en el módulo `patco_base`. Este módulo se enfoca únicamente en las extensiones específicas de Field Service Management (FSM).

### 2. Gestión Avanzada de Órdenes FSM

#### Extensiones del Modelo `fsm.order`
- **Clasificación Automática**: Código generado automáticamente (ej. "M1-COC-CAL-N2")
- **Gestión de Habilidades**: Asignación de técnicos basada en competencias requeridas
- **Control de Stock en Vehículos**: Gestión de repuestos en ubicaciones móviles
- **Checklists Dinámicos**: Listas de verificación de entrada y salida
- **Timer Integrado**: Control de tiempo de trabajo en tiempo real
- **Facturación Automática**: Políticas configurables de facturación

#### Campos Principales Añadidos:
- `x_nature_id`, `x_area_id`, `x_complexity_id`: Clasificación PATCO
- `x_classification_code`: Código automático generado
- `x_entry_checklist`, `x_exit_checklist`: Checklists dinámicos
- `x_vehicle_location_id`: Ubicación del vehículo del técnico
- `x_consumed_parts_ids`: Repuestos consumidos
- `x_required_skill_types`: Habilidades requeridas
- `worksheet_ids`: Hojas de trabajo digitales
- `timesheet_ids`: Registros de tiempo integrados

### 3. Sistema de Hojas de Trabajo Digitales

#### Modelo `fsm.worksheet`
- **Plantillas Configurables**: Sistema de plantillas con campos dinámicos
- **Firmas Digitales**: Captura de firmas de técnico y cliente
- **Estados de Flujo**: Borrador → En Progreso → Completada → Firmada
- **Aprobación del Cliente**: Proceso de conformidad con firma digital
- **Generación de PDF**: Documentos firmados automáticamente
- **Adjuntos**: Soporte para fotos y documentos adicionales

#### Funcionalidades Avanzadas:
- Control de tiempo automático (inicio/fin)
- Validaciones de secuencia temporal
- Integración con órdenes FSM
- Sistema de aprobación/rechazo del cliente
- Generación automática de PDFs firmados

### 4. Gestión de Repuestos y Stock

#### Repuestos Consumidos (`fsm.order.consumed.part`)
- **Trazabilidad Completa**: Seguimiento de cada repuesto utilizado
- **Cálculo Automático de Costos**: Costos unitarios y totales
- **Integración con Stock**: Movimientos automáticos de inventario
- **Estados de Flujo**: Borrador → Confirmado → Realizado

#### Solicitudes de Transferencia (`stock.transfer.request`)
- **Transferencias a Vehículos**: Gestión de stock móvil para técnicos
- **Validación de Disponibilidad**: Verificación automática de stock
- **Generación de Pickings**: Creación automática de transferencias
- **Seguimiento Completo**: Estados y trazabilidad de movimientos

### 5. Extensiones de Líneas Analíticas

#### Modelo extendido `account.analytic.line`
- **Timer de Trabajo**: Control de tiempo en tiempo real
- **Integración FSM**: Vinculación directa con órdenes de servicio
- **Gestión de Proyectos**: Asignación automática de proyectos
- **Análisis de Tiempos**: Reportes y análisis de productividad

#### Campos y Métodos Añadidos:
- `fsm_order_id`: Relación con orden de servicio
- `date_time`: Fecha y hora para timer
- `is_timer_running`: Estado del timer
- `action_timer_start()`: Inicia el timer

### 6. Gestión de Clientes

#### Submenú de Clientes
- **Acceso Directo**: Submenú "Clientes" bajo el menú principal de Contactos
- **Filtrado Automático**: Vista filtrada que muestra solo empresas con rango de cliente
- **Creación Simplificada**: Contexto predefinido para crear nuevos clientes
- **Integración Nativa**: Utiliza el modelo estándar `res.partner` de Odoo

#### Características:
- Dominio: `[('is_company', '=', True), ('customer_rank', '>', 0)]`
- Contexto por defecto: `{'default_is_company': True, 'default_customer_rank': 1}`
- Vista: Lista y formulario estándar de partners
- Secuencia: 10 (aparece al inicio del menú Contactos)
- `action_timer_stop()`: Detiene el timer y calcula duración

### 6. Wizards y Asistentes

#### Wizard de Consumo de Repuestos (`fsm.consume.parts.wizard`)
- **Selección Inteligente**: Lista de repuestos disponibles en vehículo
- **Validación de Stock**: Verificación automática de disponibilidad
- **Procesamiento Automático**: Generación de movimientos de stock
- **Integración Completa**: Actualización automática de la orden FSM

#### Wizard de Aprobación del Cliente (`fsm.worksheet.customer.approval.wizard`)
- **Captura de Datos**: Información completa del cliente que aprueba
- **Firma Digital**: Captura de firma electrónica
- **Comentarios**: Observaciones del cliente sobre el servicio
- **Flujo de Aprobación**: Aprobación o rechazo con justificación

### 7. Sistema de Seguridad y Permisos

#### Grupos de Seguridad PATCO:
- **PATCO Administrador**: Acceso completo al sistema
- **PATCO Gerente**: Gestión de proyectos, clientes y facturación
- **PATCO Técnico Líder**: Supervisión de técnicos y aprobaciones
- **PATCO Técnico**: Acceso a proyectos asignados y mantenimientos

#### Permisos Integrados:
- Permisos de proyecto por rol
- Permisos de mantenimiento especializados
- Permisos de facturación según nivel
- Reglas de acceso a datos por grupo

## Estructura de Archivos

```
patco_core/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── account_analytic_line.py          # Extensión de líneas analíticas con timer
│   ├── fsm_order.py                      # Extensión de órdenes FSM con clasificación PATCO
│   ├── fsm_order_consumed_part.py        # Modelo de repuestos consumidos
│   ├── fsm_worksheet.py                  # Sistema de hojas de trabajo digitales
│   ├── maintenance_equipment_category.py # Extensión de categorías de equipos
│   ├── stock_location.py                # Extensión de ubicaciones (vehículos)
│   ├── stock_transfer_request.py        # Modelo de solicitudes de transferencia
│   └── timesheets_analysis_report.py    # Reportes de análisis de tiempo
├── wizards/
│   ├── __init__.py
│   ├── fsm_consume_parts_wizard.py       # Wizard para consumir repuestos
│   └── fsm_worksheet_customer_approval_wizard.py # Wizard de aprobación del cliente
├── views/
│   ├── account_analytic_line_views.xml  # Vistas de líneas analíticas
│   ├── fsm_order_views.xml              # Vistas de órdenes FSM
│   ├── fsm_worksheet_views.xml          # Vistas de hojas de trabajo
│   └── stock_transfer_request_views.xml # Vistas de transferencias
├── data/
│   ├── agreement_type_data.xml          # Tipos de acuerdos y contratos
│   ├── fsm_worksheet_template_data.xml  # Plantillas de hojas de trabajo
│   ├── maintenance_equipment_category_data.xml # Categorías de equipos
│   ├── patco_actions.xml                # Acciones y menús del sistema
│   ├── patco_core_data.xml              # Datos centrales del sistema
│   ├── patco_menu_visibility.xml        # Configuración de visibilidad de menús
│   ├── patco_module_restrictions.xml    # Restricciones de módulos
│   ├── patco_security_groups.xml        # Grupos de seguridad


│   ├── stock_initial_data.xml           # Datos iniciales de inventario
│   ├── stock_locations_data.xml         # Ubicaciones de almacén
│   ├── stock_rules_data.xml             # Reglas de inventario
│   └── stock_vehicle_data.xml           # Datos de vehículos y ubicaciones móviles
├── security/
│   ├── ir.model.access.csv              # Permisos de acceso a modelos
│   └── patco_security.xml               # Grupos de seguridad PATCO
├── static/
│   └── description/
│       ├── icon.png                     # Icono del módulo
│       └── index.html                   # Descripción HTML del módulo
└── README.md                            # Documentación completa
```

### Descripción de Directorios

- **models/**: Modelos Python del núcleo del sistema PATCO
- **wizards/**: Asistentes para procesos específicos (consumo de repuestos, aprobaciones)
- **views/**: Definiciones de vistas XML para todos los modelos
- **data/**: Datos maestros específicos de FSM, acciones y configuraciones iniciales
- **security/**: Grupos de seguridad y permisos de acceso
- **static/**: Recursos estáticos (iconos, descripciones)
- **migrations/**: Scripts de migración para actualizaciones de versión
- **i18n/**: Archivos de traducción (español peruano)

## Dependencias

### Módulos Base Requeridos
- `base`: Módulo base de Odoo
- `project`: Gestión de proyectos y tareas
- `industry_fsm`: Field Service Management (Gestión de Servicios de Campo)
- `maintenance`: Gestión de equipos y mantenimiento
- `hr_timesheet`: Hojas de tiempo y seguimiento de horas
- `stock`: Gestión de inventario y almacenes
- `account`: Contabilidad y facturación

### Módulos Opcionales
- `hr_skills`: Gestión de habilidades de empleados (para asignación automática)
- `website`: Para funcionalidades web (si se requiere portal de cliente)

## Instalación

### Pasos de Instalación
1. **Copiar Módulo**: Colocar la carpeta `patco_core` en el directorio `addons` de Odoo
2. **Actualizar Lista**: Ejecutar "Actualizar Lista de Aplicaciones" en Odoo
3. **Instalar Dependencias**: Asegurar que todos los módulos dependientes estén instalados
4. **Instalar PATCO Core**: Instalar el módulo `patco_core`
5. **Verificar Datos**: Confirmar que los datos maestros se cargaron correctamente

### Verificación Post-Instalación
- Verificar que los grupos de seguridad PATCO estén creados
- Confirmar que las naturalezas, áreas y complejidades estén disponibles
- Probar la creación de una orden FSM con clasificación PATCO

## Configuración

### Datos Maestros Incluidos

#### Naturalezas de Servicio (Automáticas)
- **M1-Correctivo**: Reparación de fallas y averías
- **M2-Preventivo**: Mantenimiento programado y rutinario  
- **M3-Instalación**: Instalación de nuevos equipos
- **M4-Inspección**: Revisiones técnicas y auditorías

#### Áreas de Servicio (Automáticas)
- **COC-CAL**: Cocina - Equipos de Calor
- **COC-PRE**: Cocina - Equipos de Preparación
- **COC-LAV**: Cocina - Equipos de Lavado
- **REF-COM**: Refrigeración Comercial
- **AC**: Aire Acondicionado
- **LAV**: Lavandería Industrial

#### Niveles de Complejidad (Automáticos)
- **N1-Básico**: Mantenimiento rutinario
- **N2-Intermedio**: Requiere conocimiento técnico
- **N3-Avanzado**: Alta especialización técnica
- **N4-Crítico**: Experto certificado requerido

### Configuración Inicial Recomendada

1. **Asignar Usuarios a Grupos**: Configurar usuarios en los grupos PATCO apropiados
2. **Configurar Ubicaciones de Vehículos**: Crear ubicaciones de stock para vehículos de técnicos
3. **Configurar Proyectos FSM**: Establecer proyectos por defecto para órdenes de servicio
4. **Configurar Plantillas de Worksheet**: Crear plantillas de hojas de trabajo según necesidades
5. **Verificar Categorías de Productos**: Las categorías consolidadas se cargan automáticamente desde patco_base
6. **Configurar Productos**: Establecer productos/servicios para facturación automática usando las categorías predefinidas

## Uso del Sistema

### Flujo Típico de Orden de Servicio

1. **Creación**: Crear orden FSM con clasificación PATCO automática
2. **Asignación**: Asignar técnico basado en habilidades requeridas
3. **Preparación**: Transferir repuestos al vehículo del técnico
4. **Ejecución**: Usar timer, checklists y hojas de trabajo
5. **Consumo**: Registrar repuestos consumidos durante el servicio
6. **Finalización**: Obtener aprobación del cliente con firma digital
7. **Facturación**: Generar factura automática según políticas configuradas

### Funcionalidades Clave

#### Timer de Trabajo
```python
# Iniciar timer automáticamente al comenzar trabajo
analytic_line.action_timer_start()

# Detener timer al finalizar
analytic_line.action_timer_stop()
```

#### Consumo de Repuestos
- Usar wizard de consumo desde la orden FSM
- Validación automática de stock disponible en vehículo
- Generación automática de movimientos de inventario

#### Hojas de Trabajo Digitales
- Crear desde plantillas configurables
- Capturar firmas digitales de técnico y cliente
- Generar PDFs automáticamente al completar













## Estructura de Categorías de Productos

### Categorías Consolidadas
El sistema incluye categorías consolidadas de productos definidas en el módulo `patco_base` que eliminan duplicaciones y proporcionan una estructura jerárquica coherente:

#### Servicios de Mantenimiento
- **Servicios de Mantenimiento** (categoría principal)
  - Mantenimiento Preventivo
  - Mantenimiento Correctivo
  - Servicios de Instalación

#### Repuestos y Consumibles
- **Repuestos y Consumibles** (categoría principal)
  - **Repuestos de Cocina**
    - Equipos de Cocción
    - Equipos de Preparación
    - Equipos de Lavado de Vajilla
    - Sistemas de Ventilación
  - **Repuestos de Refrigeración**
    - Refrigeración Comercial
    - Climatización (HVAC)
  - **Repuestos de Lavandería**
    - Equipos de Lavado
    - Equipos de Secado
    - Equipos de Planchado
  - **Repuestos de Bar y Cafetería**
  - **Componentes Eléctricos**
  - **Componentes de Fontanería**
  - **Filtros**
  - **Aceites y Lubricantes**
  - **Consumibles Generales**

### Beneficios de la Consolidación
- Eliminación de categorías duplicadas entre archivos
- Estructura jerárquica alineada con el documento funcional PATCO
- Categorización específica para el sector HORECA
- Facilita la organización y búsqueda de productos
- Mejora la consistencia en la clasificación de repuestos

## Notas Técnicas

### Compatibilidad
- **Versión Odoo**: 18.0 Community Edition
- **Python**: 3.11+
- **Base de Datos**: PostgreSQL 15+

### Características Técnicas
- Utiliza la nueva API de Odoo 18
- Implementa patrones de diseño recomendados
- Código optimizado para rendimiento
- Preparado para extensiones futuras
- Cumple con estándares de seguridad de Odoo
- Sistema consolidado de categorías de productos

### Consideraciones de Rendimiento
- Los cálculos de clasificación son automáticos y eficientes
- Las consultas de stock están optimizadas
- Los timers utilizan campos computados para mejor rendimiento
- Carga única de categorías consolidadas mejora el rendimiento

## Extensibilidad

El módulo está diseñado para ser extendido fácilmente:

- **Nuevas Clasificaciones**: Agregar más naturalezas, áreas o complejidades
- **Campos Personalizados**: Extender modelos con campos específicos del cliente
- **Workflows Adicionales**: Implementar flujos de trabajo personalizados
- **Integraciones**: Conectar con sistemas externos vía API

## Soporte y Mantenimiento

Para soporte técnico, consultas o reportes de errores:
- Revisar la documentación técnica en cada archivo Python
- Consultar los comentarios en archivos XML de vistas
- Contactar al equipo de desarrollo PATCO para soporte especializado

---

**Nota**: Este módulo es el núcleo del ecosistema PATCO y debe instalarse antes que cualquier otro módulo PATCO especializado.

---

**PATCO Core** - La base sólida para la digitalización del mantenimiento HORECA