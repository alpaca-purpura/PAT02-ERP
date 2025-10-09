# PATCO Stock FSM

**Versión:** 18.0.1.0.0  
**Autor:** PATCO  
**Categoría:** Field Service  
**Licencia:** LGPL-3  

Módulo especializado de gestión de stock para servicios de campo (Field Service Management) que permite controlar el inventario móvil en vehículos de técnicos, optimizando la distribución de repuestos y herramientas para servicios en campo.

## Modelos Implementados

### 📍 stock.location (Extensión)
**Archivo:** `models/stock_location.py`

**Campos agregados:**
- `is_vehicle_location` (Boolean): Marca la ubicación como vehículo de servicio
- `technician_id` (Many2one): Técnico asignado al vehículo (relación con hr.employee)
- `vehicle_code` (Char): Código único del vehículo (ej: VH-001)
- `max_capacity` (Float): Capacidad máxima en kg
- `current_weight` (Float): Peso actual calculado automáticamente
- `capacity_percentage` (Float): Porcentaje de capacidad utilizada

**Métodos principales:**
- `_compute_current_weight()`: Calcula peso actual basado en productos en stock
- `_compute_capacity_percentage()`: Calcula porcentaje de ocupación
- `_check_vehicle_code_unique()`: Valida unicidad del código de vehículo
- `_check_technician_unique()`: Previene asignación múltiple de técnicos a vehículos
- `get_available_capacity()`: Retorna capacidad disponible en kg
- `can_accommodate_weight(weight)`: Verifica si puede acomodar peso adicional
- `get_stock_summary()`: Obtiene resumen detallado de inventario por producto
- `get_vehicle_locations()`: Método estático para obtener todas las ubicaciones de vehículos
- `name_get()`: Personaliza la visualización del nombre con código de vehículo

### 📋 stock.transfer.request (Nuevo modelo)
**Archivo:** `models/stock_transfer_request.py`

**Campos principales:**
- `name` (Char): Número de secuencia automática (STR/YYYY/NNNN)
- `date` (Datetime): Fecha de solicitud (por defecto fecha actual)
- `technician_id` (Many2one): Técnico solicitante (hr.employee)
- `vehicle_location_id` (Many2one): Vehículo destino (stock.location con is_vehicle_location=True)
- `source_location_id` (Many2one): Ubicación origen (stock.location)
- `state` (Selection): Estado del workflow
- `line_ids` (One2many): Líneas de productos solicitados
- `picking_ids` (One2many): Transferencias generadas
- `picking_count` (Integer): Contador de transferencias
- `notes` (Text): Notas adicionales
- `company_id` (Many2one): Compañía

**Estados del workflow:**
- `draft`: Borrador
- `confirmed`: Confirmado
- `done`: Completado
- `cancelled`: Cancelado

**Métodos principales:**
- `create()`: Sobrescrito para generar secuencia automática
- `action_confirm()`: Confirma la solicitud y cambia estado
- `action_create_transfer()`: Genera picking de transferencia automáticamente
- `action_cancel()`: Cancela la solicitud
- `action_view_pickings()`: Visualiza transferencias relacionadas
- `_get_picking_type()`: Obtiene el tipo de picking para transferencias internas
- `_compute_picking_count()`: Calcula número de pickings relacionados

### 📦 stock.transfer.request.line (Nuevo modelo)
**Archivo:** `models/stock_transfer_request.py`

**Campos:**
- `request_id` (Many2one): Solicitud padre
- `product_id` (Many2one): Producto solicitado
- `quantity_requested` (Float): Cantidad solicitada
- `quantity_available` (Float): Cantidad disponible en origen (calculado)
- `uom_id` (Many2one): Unidad de medida
- `description` (Text): Descripción adicional

**Métodos:**
- `_compute_quantity_available()`: Calcula cantidad disponible en ubicación origen
- `_onchange_quantity_requested()`: Validación de cantidad solicitada vs disponible

### 🚚 stock.picking (Extensión)
**Archivo:** `models/stock_transfer_request.py`

**Campos agregados:**
- `x_transfer_request_id` (Many2one): Referencia a solicitud de transferencia
- `fsm_order_id` (Many2one): Referencia a orden de servicio FSM

## Vistas Implementadas

### 🚛 Vistas de Ubicaciones de Vehículos
**Archivo:** `views/stock_location_views.xml`

- **Vista de formulario**: Campos específicos para vehículos (técnico, código, capacidad)
- **Vista de lista**: Información resumida con indicadores de capacidad
- **Vista de búsqueda**: Filtros por vehículos, técnicos y capacidad
- **Vista kanban**: Tarjetas visuales con información de ocupación
- **Filtros específicos**:
  - Ubicaciones de vehículos
  - Por técnico asignado
  - Por nivel de capacidad

### 📋 Vistas de Solicitudes de Transferencia
**Archivo:** `views/stock_transfer_views.xml`

- **Vista de formulario**: Workflow completo con botones de acción
- **Vista de lista**: Estados y información resumida
- **Vista de búsqueda**: Filtros por estado, técnico y fecha
- **Vista kanban**: Organización por estados del workflow
- **Botones de acción**:
  - Confirmar solicitud
  - Crear transferencia
  - Cancelar
  - Ver transferencias relacionadas

### 🎛️ Menús de Navegación
**Archivo:** `views/menu_views.xml`

**Estructura de menús:**
- **Menú principal**: "PATCO Stock FSM" (con logo PATCO)
  - **Gestión de Stock**:
    - Ubicaciones de Vehículos (vista lista/formulario)
    - Vehículos - Vista Kanban (vista kanban especializada)
  - **Transferencias**:
    - Solicitudes de Transferencia (gestión completa del workflow)

**Integraciones con otros módulos:**
- **Inventario**: Accesos directos desde menú principal de Stock
  - Ubicaciones de Vehículos
  - Solicitudes de Transferencia
- **Field Service**: Menús específicos para usuarios FSM
  - Stock de Vehículos (vista kanban)
  - Solicitudes de Stock
  - Restricción por grupos de seguridad FSM

## Datos Maestros

### 📍 Ubicaciones Predefinidas
**Archivo:** `data/stock_locations_data.xml`

**Vehículos de servicio (con noupdate="1"):**
- `VH-001`: Vehículo 1 (Capacidad: 500 kg)
- `VH-002`: Vehículo 2 (Capacidad: 500 kg)
- `VH-003`: Vehículo 3 (Capacidad: 750 kg)

**Ubicaciones operativas:**
- **Consumo en Campo**: Para registrar consumos directos en servicios
- **Taller Principal**: Ubicación central de mantenimiento
- **Repuestos Críticos**: Almacén especializado para partes críticas
- **Herramientas**: Ubicación específica para herramientas

### 🔐 Permisos de Acceso
**Archivo:** `security/ir.model.access.csv`

**Configuración de seguridad por modelo:**

**stock.transfer.request:**
- `base.group_user`: Lectura, escritura, creación (sin eliminación)
- `stock.group_stock_manager`: Acceso completo (CRUD)

**stock.transfer.request.line:**
- `base.group_user`: Lectura, escritura, creación (sin eliminación)
- `stock.group_stock_manager`: Acceso completo (CRUD)

**stock.location (extensión):**
- `base.group_user`: Solo lectura
- `stock.group_stock_user`: Lectura, escritura, creación (sin eliminación)
- `stock.group_stock_manager`: Acceso completo (CRUD)

## Dependencias

### Módulos Odoo Core
- `base`: Funcionalidades básicas de Odoo
- `stock`: Gestión de inventario y transferencias

### Módulos OCA
- `fieldservice`: Gestión de servicios de campo
- `fieldservice_stock`: Integración stock con FSM

### Módulos PATCO
- `patco_base`: Modelos y funcionalidades base del ecosistema PATCO

## Comandos de Instalación y Actualización

### Instalación Automática (Recomendada)
```bash
# Instalar suite completa PATCO (incluye patco_stock_fsm automáticamente)
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_suite --stop-after-init
```

### Actualización del Módulo
```bash
# Actualizar módulo después de cambios en código
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -u patco_suite --stop-after-init
```

### Instalación Manual (Solo para desarrollo)
```bash
# Instalar módulo individual (no recomendado para producción)
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_stock_fsm --stop-after-init
```

### Reinstalación Completa (Limpieza de datos)
```bash
# Si necesitas limpiar completamente la base de datos
docker compose down -v
docker compose up -d
# Esperar que el contenedor esté listo, luego:
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_suite --stop-after-init
```

## Uso y Ejemplos Prácticos

### 🚛 Configuración de Vehículos
1. **Crear ubicación de vehículo**:
   - Ir a Inventario → Stock FSM → Ubicaciones de Vehículos
   - Marcar "Es ubicación de vehículo"
   - Asignar técnico responsable
   - Definir código único (ej: VH-004)
   - Establecer capacidad máxima

2. **Monitoreo de capacidad**:
   - El sistema calcula automáticamente el peso actual
   - Indicador visual del porcentaje de ocupación
   - Alertas cuando se acerca al límite de capacidad

### 📋 Gestión de Transferencias
1. **Crear solicitud**:
   - Ir a Inventario → Stock FSM → Solicitudes de Transferencia
   - Seleccionar técnico y vehículo destino
   - Agregar productos y cantidades necesarias
   - Confirmar solicitud

2. **Procesar transferencia**:
   - El sistema valida disponibilidad de stock
   - Genera automáticamente el picking de transferencia
   - Seguimiento completo hasta completar la transferencia

### 📊 Casos de Uso Típicos
- **Preparación de ruta**: Cargar vehículo con repuestos para múltiples servicios del día
- **Reabastecimiento en campo**: Solicitar productos específicos para técnico que agotó stock
- **Control de inventario móvil**: Monitorear stock disponible en cada vehículo en tiempo real
- **Optimización de carga**: Gestionar capacidad de peso para maximizar eficiencia de transporte
- **Transferencias de emergencia**: Mover stock crítico entre vehículos según necesidades urgentes
- **Planificación de rutas**: Asegurar que cada técnico tenga los repuestos necesarios antes de salir

### 🔗 Integración con FSM
- Las transferencias se pueden vincular automáticamente con órdenes de servicio FSM
- Los técnicos pueden solicitar repuestos directamente desde órdenes FSM (si módulo FSM está instalado)
- Trazabilidad completa desde solicitud hasta consumo en campo
- Integración con menús específicos para usuarios de Field Service
- Control de acceso por grupos de seguridad FSM

### 🚨 Validaciones y Controles
- **Capacidad de vehículos**: El sistema previene sobrecargar vehículos más allá de su capacidad máxima
- **Unicidad de códigos**: Cada vehículo debe tener un código único
- **Asignación de técnicos**: Un técnico solo puede estar asignado a un vehículo a la vez
- **Stock disponible**: Validación automática de disponibilidad antes de crear transferencias
- **Estados de workflow**: Control estricto de estados en solicitudes de transferencia

### 📈 Indicadores y Reportes
- **Porcentaje de capacidad**: Indicador visual del nivel de ocupación de cada vehículo
- **Peso actual vs máximo**: Control en tiempo real del peso transportado
- **Stock por vehículo**: Resumen detallado de productos en cada ubicación móvil
- **Historial de transferencias**: Seguimiento completo de movimientos de stock
- **Vista kanban**: Visualización rápida del estado de todos los vehículos

---

**Desarrollado por PATCO** - Sistema integral de gestión empresarial para MYPES

---

**Versión**: 18.0.1.0.0  
**Autor**: PATCO  
**Licencia**: LGPL-3  
**Categoría**: Inventory/Field Service  
**Dependencias**: base, stock, fieldservice, fieldservice_stock, patco_base