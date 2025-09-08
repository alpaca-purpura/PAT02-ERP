# PATCO Core - Motor Central del Sistema

## Descripción

`patco_core` es el núcleo del sistema PATCO, proporcionando las funcionalidades base y modelos centrales para la gestión integral de mantenimiento HORECA. Este módulo contiene las extensiones fundamentales de Odoo, los datos maestros necesarios y todas las funcionalidades avanzadas para el ecosistema PATCO.

## Funcionalidades Principales

### 1. Sistema de Clasificación PATCO

#### Naturalezas de Servicio (`patco.service.nature`)
- **Propósito**: Clasificación estándar de tipos de servicio según matriz PATCO
- **Datos maestros incluidos**:
  - **M1-Correctivo**: Reparación de fallas y averías
  - **M2-Preventivo**: Mantenimiento programado y rutinario
  - **M3-Instalación**: Instalación de nuevos equipos
  - **M4-Inspección**: Revisiones técnicas y auditorías

#### Áreas de Servicio (`patco.service.area`)
- **Propósito**: Clasificación por área técnica especializada
- **Datos maestros incluidos**:
  - **COC-CAL**: Cocina - Calor (hornos, freidoras, planchas)
  - **COC-PRE**: Cocina - Preparación
  - **COC-LAV**: Cocina - Lavado
  - **REF-COM**: Refrigeración Comercial
  - **AC**: Aire Acondicionado
  - **LAV**: Lavandería Industrial

#### Complejidad de Servicio (`patco.service.complexity`)
- **Propósito**: Clasificación por nivel de dificultad técnica
- **Datos maestros incluidos**:
  - **N1-Básico**: Tareas rutinarias y mantenimiento simple
  - **N2-Intermedio**: Requiere conocimiento técnico especializado
  - **N3-Avanzado**: Requiere alta especialización técnica
  - **N4-Crítico**: Requiere experto certificado y experiencia avanzada

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
│   ├── patco_service_area.py            # Modelo de áreas de servicio
│   ├── patco_service_complexity.py      # Modelo de complejidad de servicio
│   ├── patco_service_nature.py          # Modelo de naturalezas de servicio
│   └── stock_transfer_request.py        # Modelo de solicitudes de transferencia
├── wizards/
│   ├── __init__.py
│   ├── fsm_consume_parts_wizard.py       # Wizard para consumir repuestos
│   └── fsm_worksheet_customer_approval_wizard.py # Wizard de aprobación del cliente
├── views/
│   ├── account_analytic_line_views.xml  # Vistas de líneas analíticas
│   ├── fsm_order_views.xml              # Vistas de órdenes FSM
│   ├── fsm_worksheet_views.xml          # Vistas de hojas de trabajo
│   ├── patco_service_area_views.xml     # Vistas de áreas de servicio
│   ├── patco_service_complexity_views.xml # Vistas de complejidad
│   ├── patco_service_nature_views.xml   # Vistas de naturalezas de servicio
│   └── stock_transfer_request_views.xml # Vistas de transferencias
├── data/
│   ├── patco_actions.xml                # Acciones y menús del sistema
│   ├── patco_service_area_data.xml      # Datos maestros de áreas
│   ├── patco_service_complexity_data.xml # Datos maestros de complejidad
│   └── patco_service_nature_data.xml    # Datos maestros de naturalezas
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
- **data/**: Datos maestros, acciones y configuraciones iniciales
- **security/**: Grupos de seguridad y permisos de acceso
- **static/**: Recursos estáticos (iconos, descripciones)

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
5. **Configurar Productos**: Establecer productos/servicios para facturación automática

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

### Consideraciones de Rendimiento
- Los cálculos de clasificación son automáticos y eficientes
- Las consultas de stock están optimizadas
- Los timers utilizan campos computados para mejor rendimiento

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