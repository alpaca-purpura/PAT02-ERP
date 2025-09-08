# PATCO Customer Equipment - Gestión Avanzada de Equipos

## Descripción

`patco_customer_equipment` es el módulo especializado en la gestión integral de equipos de clientes dentro del ecosistema PATCO. Proporciona funcionalidades avanzadas para el registro, seguimiento y mantenimiento de activos HORECA, incluyendo generación automática de códigos QR, historial de servicios y integración completa con órdenes de trabajo.

## Funcionalidades Principales

### 1. Extensión de Equipos de Mantenimiento
- **Modelo extendido**: `maintenance.equipment`
- **Propósito**: Gestión especializada de equipos HORECA con trazabilidad completa
- **Integración**: Conexión directa con FSM, Helpdesk y servicios de campo

#### Campos Añadidos:
- `x_patco_code`: Código único PATCO para identificación rápida
- `x_customer_id`: Relación con cliente propietario del equipo
- `x_qr_code`: Código QR generado automáticamente
- `x_service_count`: Contador de servicios realizados
- `x_last_service_date`: Fecha del último servicio
- `x_next_service_date`: Fecha programada del próximo servicio
- `x_warranty_expiry`: Fecha de vencimiento de garantía
- `x_installation_date`: Fecha de instalación del equipo
- `x_brand`: Marca del equipo
- `x_model_number`: Número de modelo específico
- `x_serial_number`: Número de serie del fabricante
- `x_location_details`: Ubicación detallada dentro del establecimiento

### 2. Generación Automática de Códigos QR
- **Funcionalidad**: Creación automática de códigos QR únicos
- **Contenido del QR**: URL con información del equipo para acceso móvil
- **Actualización**: Regeneración automática cuando cambian datos clave
- **Formato**: Compatible con lectores QR estándar

### 3. Gestión de Servicios y Historial
- **Contador de Servicios**: Seguimiento automático de intervenciones
- **Historial Completo**: Registro de todos los servicios realizados
- **Fechas Clave**: Control de último servicio y próximo programado
- **Análisis de Tendencias**: Datos para optimización de mantenimiento

### 4. Integración con Helpdesk
- **Modelo extendido**: `helpdesk.ticket`
- **Funcionalidad**: Vinculación directa de tickets con equipos
- **Automatización**: Creación de órdenes FSM desde tickets
- **Trazabilidad**: Seguimiento completo desde incidencia hasta resolución

### 5. Integración con FSM (Field Service Management)
- **Modelo extendido**: `fsm.order`
- **Funcionalidad**: Órdenes de servicio vinculadas a equipos específicos
- **Automatización**: Actualización automática de contadores y fechas
- **Optimización**: Datos para planificación de rutas y recursos

## Estructura de Archivos

```
patco_customer_equipment/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── patco_customer_equipment.py    # Extensión de equipos
│   ├── helpdesk_ticket.py             # Integración con tickets
│   └── fsm_order.py                   # Integración con FSM
├── views/
│   ├── patco_customer_equipment_views.xml  # Vistas de equipos
│   ├── helpdesk_ticket_views.xml           # Vistas de tickets
│   └── fsm_order_views.xml                 # Vistas de órdenes FSM
├── security/
│   └── ir.model.access.csv                 # Permisos de acceso
├── static/
│   └── description/
│       └── icon.png                        # Icono del módulo
└── README.md
```

## Dependencias

### Módulos Odoo Core:
- `base`: Funcionalidades básicas
- `maintenance`: Gestión de equipos base
- `helpdesk`: Sistema de tickets de soporte

### Módulos OCA:
- `fieldservice`: Gestión de órdenes de servicio de campo
- `fieldservice_maintenance`: Integración FSM-Mantenimiento

### Módulos PATCO:
- `patco_core`: Funcionalidades centrales y naturalezas de servicio

## Funcionalidades Técnicas

### 1. Generación de Códigos QR
```python
# Generación automática al crear/modificar equipo
def _compute_qr_code(self):
    for equipment in self:
        if equipment.x_patco_code:
            # URL con información del equipo
            qr_url = f"{base_url}/equipment/{equipment.x_patco_code}"
            equipment.x_qr_code = self._generate_qr_code(qr_url)
```

### 2. Cálculo de Contadores de Servicio
```python
# Actualización automática de estadísticas
def _compute_service_stats(self):
    for equipment in self:
        # Contar servicios FSM completados
        fsm_orders = self.env['fsm.order'].search([
            ('equipment_id', '=', equipment.id),
            ('stage_id.is_closed', '=', True)
        ])
        equipment.x_service_count = len(fsm_orders)
        
        # Última fecha de servicio
        if fsm_orders:
            equipment.x_last_service_date = max(fsm_orders.mapped('date_end'))
```

### 3. Validaciones de Integridad
```python
# Validaciones de datos
@api.constrains('x_patco_code')
def _check_patco_code_unique(self):
    if self.x_patco_code:
        existing = self.search([
            ('x_patco_code', '=', self.x_patco_code),
            ('id', '!=', self.id)
        ])
        if existing:
            raise ValidationError("El código PATCO debe ser único")
```

## Casos de Uso Principales

### 1. Registro de Nuevo Equipo
```python
# Creación de equipo con datos PATCO
equipment = self.env['maintenance.equipment'].create({
    'name': 'Freidora Industrial FI-001',
    'x_patco_code': 'EQ-REST-001-FI',
    'x_customer_id': customer.id,
    'x_brand': 'Rational',
    'x_model_number': 'SCC-101',
    'x_serial_number': 'RAT2024001',
    'x_installation_date': fields.Date.today(),
    'x_location_details': 'Cocina - Zona de fritura',
    'category_id': fryer_category.id,
})
# El código QR se genera automáticamente
```

### 2. Creación de Ticket desde Equipo
```python
# Ticket vinculado a equipo específico
ticket = self.env['helpdesk.ticket'].create({
    'name': 'Falla en freidora - No calienta',
    'equipment_id': equipment.id,
    'partner_id': equipment.x_customer_id.id,
    'description': 'El equipo no alcanza la temperatura requerida',
})
# Se puede generar orden FSM automáticamente
```

### 3. Orden de Servicio desde Ticket
```python
# Conversión automática de ticket a orden FSM
fsm_order = ticket.action_create_fsm_order()
fsm_order.update({
    'equipment_id': ticket.equipment_id.id,
    'location_id': ticket.equipment_id.x_customer_id.id,
    'description': ticket.description,
})
```

## Vistas y Interfaz de Usuario

### Vista de Equipos Extendida:
- **Información PATCO**: Campos específicos en pestañas organizadas
- **Código QR**: Visualización y descarga del código generado
- **Historial de Servicios**: Lista de todas las intervenciones
- **Botones de Acción**: Crear ticket, orden FSM, ver historial

### Vista de Tickets Integrada:
- **Selección de Equipo**: Campo de relación con búsqueda avanzada
- **Información Contextual**: Datos del equipo en el ticket
- **Acciones Rápidas**: Crear orden FSM, ver equipo

### Vista de Órdenes FSM:
- **Datos del Equipo**: Información completa en la orden
- **Historial**: Servicios previos del mismo equipo
- **Ubicación**: Detalles de localización del equipo

## Seguridad y Permisos

### Grupos de Acceso:
- **PATCO User**: Lectura de equipos y creación de tickets
- **PATCO Technician**: Acceso completo a órdenes FSM
- **PATCO Manager**: Gestión completa de equipos y configuración

### Reglas de Seguridad:
- **Equipos por Cliente**: Los usuarios solo ven equipos de sus clientes asignados
- **Tickets Propios**: Acceso limitado a tickets del usuario o su equipo
- **Órdenes Asignadas**: Técnicos solo ven órdenes asignadas a ellos

## Integración con Otros Módulos PATCO

### Con `patco_core`:
- **Naturalezas de Servicio**: Clasificación de servicios por equipo
- **Líneas Analíticas**: Registro de tiempo por equipo específico
- **Datos Maestros**: Uso de configuraciones centrales

### Con `patco_hr_skills`:
- **Asignación por Competencia**: Técnicos asignados según habilidades requeridas
- **Especialización**: Servicios específicos por tipo de equipo
- **Capacitación**: Identificación de necesidades de entrenamiento

### Con `patco_suite`:
- **Instalación Coordinada**: Configuración automática de dependencias
- **Datos Iniciales**: Carga de categorías y configuraciones base
- **Flujo Completo**: Integración con todo el ecosistema

## Flujos de Trabajo

### 1. Onboarding de Equipos
1. **Registro Inicial**: Creación del equipo con datos básicos
2. **Asignación de Código**: Generación automática de código PATCO
3. **Generación QR**: Creación automática del código QR
4. **Configuración**: Asignación de categoría y responsables
5. **Validación**: Verificación de datos y activación

### 2. Gestión de Incidencias
1. **Detección**: Cliente reporta problema o detección automática
2. **Ticket**: Creación de ticket vinculado al equipo
3. **Clasificación**: Asignación de prioridad y naturaleza
4. **Orden FSM**: Conversión a orden de servicio de campo
5. **Ejecución**: Técnico realiza el servicio
6. **Cierre**: Actualización automática de contadores y fechas

### 3. Mantenimiento Preventivo
1. **Programación**: Definición de fechas de mantenimiento
2. **Alertas**: Notificaciones automáticas de vencimientos
3. **Planificación**: Creación de órdenes preventivas
4. **Ejecución**: Realización del mantenimiento programado
5. **Reprogramación**: Cálculo de próxima fecha de servicio

## Reportes y Análisis

### Métricas por Equipo:
- **Frecuencia de Servicios**: Análisis de intervenciones por período
- **Tiempo de Respuesta**: Desde ticket hasta resolución
- **Costos de Mantenimiento**: Seguimiento de gastos por equipo
- **Disponibilidad**: Tiempo operativo vs. tiempo de mantenimiento

### Análisis de Flota:
- **Equipos Críticos**: Identificación de activos problemáticos
- **Tendencias de Fallas**: Patrones de averías por tipo/marca
- **Optimización**: Recomendaciones de reemplazo o mejora
- **Planificación**: Programación optimizada de mantenimientos

## Configuración y Personalización

### Configuración Inicial:
1. **Categorías de Equipos**: Definir tipos específicos HORECA
2. **Códigos PATCO**: Establecer nomenclatura estándar
3. **Ubicaciones**: Configurar zonas típicas de establecimientos
4. **Garantías**: Definir períodos estándar por tipo de equipo

### Personalización Avanzada:
- **Campos Adicionales**: Extensión según necesidades específicas
- **Validaciones Personalizadas**: Reglas de negocio específicas
- **Reportes Customizados**: Análisis según KPIs del cliente
- **Integraciones**: Conexión con sistemas externos

## Beneficios del Módulo

### Operacionales:
1. **Trazabilidad Completa**: Historial detallado de cada equipo
2. **Acceso Móvil**: Información instantánea vía código QR
3. **Automatización**: Reducción de tareas manuales
4. **Integración**: Flujo continuo desde incidencia hasta resolución

### Estratégicos:
1. **Optimización de Mantenimiento**: Datos para mejores decisiones
2. **Reducción de Costos**: Mantenimiento preventivo eficiente
3. **Mejora de Servicio**: Respuesta más rápida y efectiva
4. **Análisis Predictivo**: Base de datos para mantenimiento inteligente

## Casos de Uso según Documento Funcional

### Onboarding de Activos (Macro-proceso 1):
- Registro sistemático de equipos del cliente
- Generación automática de códigos de identificación
- Creación de códigos QR para acceso móvil
- Configuración de programas de mantenimiento

### Operaciones de Servicio (Macro-proceso 2):
- Vinculación directa de tickets con equipos específicos
- Información contextual para técnicos
- Historial de servicios para mejor diagnóstico
- Optimización de asignaciones basada en especialización

### Ejecución en Campo (Macro-proceso 3):
- Acceso móvil a información del equipo vía QR
- Datos técnicos disponibles en campo
- Registro de servicios vinculado al activo
- Actualización automática de estadísticas

## Mantenimiento y Soporte

### Tareas de Mantenimiento:
- **Limpieza de Datos**: Verificación periódica de códigos únicos
- **Actualización de QR**: Regeneración cuando sea necesario
- **Validación de Fechas**: Verificación de programaciones
- **Optimización**: Análisis de rendimiento de consultas

### Monitoreo:
- **Integridad de Datos**: Validación de relaciones entre modelos
- **Rendimiento**: Seguimiento de tiempos de respuesta
- **Uso**: Análisis de funcionalidades más utilizadas
- **Errores**: Monitoreo de logs y excepciones

---

**PATCO Customer Equipment** - Gestión inteligente de activos HORECA con tecnología QR