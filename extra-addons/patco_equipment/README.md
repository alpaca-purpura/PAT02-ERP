# PATCO Equipment Management

## Descripción

Módulo avanzado para la gestión de equipos que extiende el sistema de mantenimiento estándar de Odoo con funcionalidades específicas para empresas de servicios técnicos. Proporciona gestión completa de equipos de clientes, categorías con checklists personalizables, herencia inteligente, generación automática de códigos QR, reportes de etiquetas e integración con FSM y Helpdesk.

**Versión:** 18.0.1.0.0  
**Categoría:** Maintenance  
**Autor:** PATCO  
**Licencia:** LGPL-3  
**Dependencias:** base, maintenance, maintenance_equipment_category_hierarchy

## Características Principales

### 🔧 Gestión Avanzada de Equipos
- **Código PATCO**: Generación automática de códigos únicos para identificación (formato: EQ000001)
- **Código QR**: Generación automática de códigos QR binarios para acceso móvil con URL específica
- **Gestión de Clientes**: Asignación de equipos a clientes específicos con validación de unicidad
- **Ubicación de Servicio**: Relación Many2one con res.partner para ubicaciones específicas
- **Integración FSM**: Conexión directa con órdenes de servicio de campo (fieldservice)
- **Integración Helpdesk**: Vinculación con tickets de soporte técnico
- **Estados de Equipo**: Control de estados operacionales (activo, mantenimiento, retirado)

### 📋 Categorías con Sistema de Herencia
- **Base de Conocimiento**: Documentación técnica asociada a cada categoría con contadores automáticos
- **Plantillas de Checklist**: Checklists HTML personalizables para entrada y salida de equipos
- **Herencia Inteligente**: Las subcategorías pueden heredar checklists y documentación de categorías padre
- **Jerarquía de Categorías**: Estructura organizacional con herencia automática de configuraciones
- **Checklists Efectivos**: Cálculo automático de plantillas efectivas considerando herencia
- **Contadores Inteligentes**: Seguimiento de documentos propios vs heredados

### 📊 Métricas y Seguimiento
- **Contador de Servicios FSM**: Seguimiento automático de órdenes de servicio de campo
- **Contador de Tickets**: Registro de tickets de soporte asociados
- **Fecha del Último Servicio**: Información de mantenimiento reciente calculada automáticamente
- **Métricas en Tiempo Real**: Campos computados que se actualizan dinámicamente

### 🏭 Categorías Predefinidas (Datos Maestros)
- **Cocina y Procesamiento de Alimentos**: Hornos, Freidoras, Planchas, Equipos de Cocción
- **Refrigeración y Climatización**: Refrigeración Comercial, Cámaras Frigoríficas, Aires Acondicionados  
- **Lavandería**: Lavadoras, Secadoras, Equipos de Lavandería Industrial
- **Sistemas Especializados**: Ventilación, Extracción, Sistemas Eléctricos
- **Estructura Jerárquica**: Categorías principales con subcategorías específicas
- **Carga Automática**: Se instalan automáticamente con el módulo

## Estructura del Módulo

```
patco_equipment/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   ├── maintenance_equipment_category.py  # Extensión con herencia y base de conocimiento
│   ├── maintenance_equipment.py          # Extensión completa del modelo de equipos PATCO
│   ├── fsm_order.py                      # Extensión de órdenes FSM
│   └── helpdesk_ticket.py                # Extensión de tickets de soporte
├── views/
│   ├── maintenance_equipment_category_views.xml  # Vistas de categorías con pestañas
│   ├── maintenance_equipment_views.xml           # Vistas principales de equipos
│   ├── fsm_order_views.xml                      # Extensiones de FSM
│   ├── helpdesk_ticket_views.xml                # Extensiones de Helpdesk
│   └── menus.xml                                # Menús "Gestión de Activos y Manuales"
├── data/
│   ├── maintenance_equipment_category_data.xml  # 50+ categorías predefinidas
│   └── sequences.xml                            # Secuencia para códigos PATCO
├── reports/
│   ├── equipment_label_report.xml              # Etiquetas individuales con QR
│   └── equipment_qr_labels.xml                 # Etiquetas QR estándar y compactas
├── security/
│   ├── ir.model.access.csv                     # Permisos de acceso por grupo
│   └── security_rules.xml                      # Reglas de seguridad y grupo "Gestor de Activos"
└── static/
    └── src/
        └── img/
            └── PATCO-Logo.png                   # Logo corporativo
```

## Funcionalidades Técnicas

### Modelo: maintenance.equipment (Extensión PATCO)

#### Campos Nuevos
- `x_patco_code`: Código único PATCO generado automáticamente (formato: EQ000001)
- `x_customer_id`: Relación Many2one con res.partner (cliente)
- `x_service_location_id`: Relación Many2one con res.partner (ubicación de servicio)
- `x_qr_code`: Código QR generado automáticamente (campo binario)
- `x_qr_url`: URL para acceso directo al equipo (computed)
- `x_service_order_ids`: Relación One2many con fsm.order (órdenes de servicio)
- `x_helpdesk_ticket_ids`: Relación One2many con helpdesk.ticket (tickets de soporte)
- `x_service_count`: Contador de servicios FSM (computed)
- `x_ticket_count`: Contador de tickets de soporte (computed)
- `x_installation_date`: Fecha de instalación del equipo
- `x_warranty_expiry`: Fecha de vencimiento de garantía
- `x_technical_specs`: Especificaciones técnicas (Text)
- `x_operating_conditions`: Condiciones de operación (Text)
- `x_last_service_date`: Fecha del último servicio FSM (computed)
- `maintenance_state`: Estado del equipo (Selection: active, maintenance, retired)

#### Métodos Principales
- `create()`: Genera código PATCO y QR automáticamente al crear
- `write()`: Regenera QR cuando cambian datos relevantes
- `_generate_qr_code()`: Genera código QR binario con URL de acceso
- `_compute_service_count()`: Calcula número de órdenes de servicio FSM
- `_compute_ticket_count()`: Calcula número de tickets de soporte
- `_compute_last_service_date()`: Obtiene fecha del último servicio FSM
- `action_view_service_orders()`: Vista de órdenes de servicio FSM asociadas
- `action_view_helpdesk_tickets()`: Vista de tickets de soporte asociados
- `action_activate()`: Activa el equipo (maintenance_state = 'active')
- `action_maintenance()`: Pone equipo en mantenimiento (maintenance_state = 'maintenance')
- `action_retire()`: Retira el equipo (maintenance_state = 'retired')
- `_check_serial_no_unique_per_customer()`: Valida unicidad de número de serie por cliente
- `regenerate_qr_code()`: Regenera código QR manualmente
- `get_entry_checklist_template()`: Obtiene plantilla de checklist de entrada
- `get_exit_checklist_template()`: Obtiene plantilla de checklist de salida
- `action_view_category_knowledge_base()`: Acceso a documentación de categoría

### Modelo: maintenance.equipment.category (Extensión)

#### Campos Nuevos
- `x_knowledge_base`: Relación One2many con documentos de base de conocimiento
- `x_entry_checklist_template`: Plantilla HTML para checklist de entrada
- `x_exit_checklist_template`: Plantilla HTML para checklist de salida
- `x_inherit_checklists`: Boolean - Heredar checklists de categoría padre
- `x_inherit_knowledge_base`: Boolean - Heredar documentación de categoría padre
- `x_effective_entry_checklist`: Plantilla efectiva de entrada (computed)
- `x_effective_exit_checklist`: Plantilla efectiva de salida (computed)
- `x_knowledge_base_count`: Contador de documentos propios (computed)
- `x_inherited_knowledge_count`: Contador de documentos heredados (computed)

#### Métodos Principales
- `_compute_effective_checklists()`: Calcula plantillas efectivas considerando herencia
- `_compute_knowledge_base_count()`: Cuenta documentos propios de la categoría
- `_compute_inherited_knowledge_count()`: Cuenta documentos heredados de categorías padre
- `action_view_knowledge_base()`: Vista de documentación completa de la categoría
- `action_view_inherited_knowledge_base()`: Vista de documentación heredada únicamente

### Extensiones de Integración

#### fsm.order (Extensión)
**Campos Agregados:**
- `x_equipment_id`: Relación Many2one con maintenance.equipment
- `x_equipment_code`: Código PATCO del equipo (related)
- `x_customer_equipment`: Relación Many2one con patco.customer.equipment (Boolean)
- `x_equipment_ids`: Relación Many2many con maintenance.equipment (múltiples equipos)

**Métodos:**
- `_onchange_x_equipment_id()`: Actualiza ubicación y cliente al seleccionar equipo
- `create()`: Actualiza campos automáticamente al crear orden
- `write()`: Actualiza campos automáticamente al modificar orden

#### helpdesk.ticket (Extensión)
**Campos Agregados:**
- `x_equipment_id`: Relación Many2one con maintenance.equipment
- `x_equipment_code`: Código PATCO del equipo (related)
- `x_customer_equipment`: Relación Many2one con patco.customer.equipment (Boolean)
- `x_equipment_location`: Ubicación del equipo (related)
- `x_fsm_order_id`: Relación Many2one con fsm.order (orden de servicio creada)

**Métodos:**
- `_onchange_equipment_id()`: Actualiza campos relacionados al seleccionar equipo
- `action_create_fsm_order()`: Crea orden de servicio FSM desde ticket
- `create()`: Sobrescribe creación para manejar equipos automáticamente

## Dependencias

### Módulos Odoo Core
- `base`: Funcionalidades básicas de Odoo
- `maintenance`: Módulo de mantenimiento estándar de Odoo

### Módulos OCA
- `maintenance_equipment_category_hierarchy`: Jerarquía de categorías de equipos (OCA/maintenance)

### Integración Opcional
- `fieldservice`: Para integración con órdenes de servicio FSM (si está instalado)
- `helpdesk`: Para integración con tickets de soporte (si está instalado)

**Nota:** Las integraciones con FSM y Helpdesk son opcionales. El módulo funciona sin ellas, pero si están instaladas, se activan automáticamente las funcionalidades de integración.

## Instalación

### Instalación Recomendada (via patco_suite)
```bash
# Instalar el suite completo que incluye patco_equipment
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_suite --stop-after-init
```

### Instalación Individual
```bash
# Solo si necesitas instalar patco_equipment por separado
docker exec odoo-patco-app python3 /opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -d odoo_patco -i patco_equipment --stop-after-init
```

### Verificación Post-Instalación
1. **Verificar Categorías**: Mantenimiento → Configuración → Categorías de Equipos
2. **Verificar Secuencias**: Configuración → Secuencias → PATCO Equipment Code
3. **Verificar Permisos**: Configuración → Usuarios y Compañías → Grupos

## Uso

### Gestión de Equipos

1. **Crear Equipo**:
   - Ir a Mantenimiento → Equipos → Crear
   - Seleccionar categoría (se cargan automáticamente las plantillas)
   - Asignar cliente y ubicación de servicio
   - El código PATCO y QR se generan automáticamente

2. **Configurar Categorías**:
   - Ir a Mantenimiento → Configuración → Categorías de Equipos
   - Definir plantillas de checklist HTML para entrada y salida
   - Configurar herencia de plantillas desde categorías padre
   - Adjuntar documentación técnica en la base de conocimiento

3. **Gestión de Servicios**:
   - Desde el equipo, acceder a "Servicios" para ver órdenes FSM
   - Usar "Tickets" para gestionar soporte técnico
   - Regenerar código QR si es necesario

### Ejemplos Prácticos

#### Crear un Equipo con Código PATCO Automático
```python
# El código PATCO se genera automáticamente al crear
equipment = self.env['maintenance.equipment'].create({
    'name': 'Refrigerador Industrial Samsung',
    'category_id': category_id,
    'x_customer_id': customer_id,
    'x_location': 'Cocina Principal - Área Fría',
    'serial_no': 'RF2024-001'
})
# equipment.x_patco_code será 'PATCO-2024-0001' (generado automáticamente)
# equipment.x_qr_code contendrá el QR binario del código PATCO
```

#### Configurar Categoría con Sistema de Herencia
```python
# Categoría padre con checklist base
parent_category = self.env['maintenance.equipment.category'].create({
    'name': 'Refrigeración',
    'x_entry_checklist_template': '<ul><li>Verificar temperatura</li><li>Revisar sellos</li></ul>'
})

# Categoría hija que hereda automáticamente
child_category = self.env['maintenance.equipment.category'].create({
    'name': 'Refrigeradores Industriales',
    'parent_id': parent_category.id,
    'x_inherit_checklists': True,
    'x_entry_checklist_template': '<ul><li>Verificar compresor</li></ul>'
})
# child_category.x_effective_entry_checklist combinará ambos checklists
```

#### Gestión de Estados del Equipo
```python
# Activar equipo
equipment.action_activate_equipment()
# equipment.x_equipment_status = 'active'

# Poner en mantenimiento
equipment.action_maintenance_equipment()
# equipment.x_equipment_status = 'maintenance'

# Retirar equipo
equipment.action_retire_equipment()
# equipment.x_equipment_status = 'retired'
```

#### Obtener Plantillas de Checklist
```python
# Obtener plantillas efectivas (con herencia)
templates = equipment.get_checklist_templates()
entry_checklist = templates.get('entry')
exit_checklist = templates.get('exit')
```

#### Consultar Métricas del Equipo
```python
# Obtener información de servicios y tickets
num_servicios = equipment.fsm_order_count
num_tickets = equipment.helpdesk_ticket_count
ultimo_servicio = equipment.last_service_date
```

## Integración con Otros Módulos

### patco_fsm
- Creación automática de órdenes de servicio desde equipos
- Seguimiento de servicios realizados por equipo
- Integración de checklists en órdenes de trabajo

### patco_helpdesk (Opcional)
- Creación de tickets de soporte desde equipos
- Historial de incidencias por equipo
- Escalamiento automático según criticidad

### patco_base
- Utiliza clasificaciones de naturaleza, área y complejidad
- Integración con sistema de grupos de seguridad

## Reportes Incluidos

### 1. Etiquetas de Equipos (equipment_label_report)
- **Archivo**: `reports/equipment_label_report.xml`
- **Tipo**: PDF
- **Descripción**: Genera etiquetas completas con información del equipo
- **Campos incluidos**:
  - Nombre del equipo
  - Código PATCO
  - Cliente
  - Área/Ubicación
  - Modelo y número de serie
  - Código QR
- **Uso**: Desde vista de equipos → Imprimir → Etiquetas de Equipos

### 2. Etiquetas QR de Equipos (equipment_qr_labels)
- **Archivo**: `reports/equipment_qr_labels.xml`
- **Tipo**: PDF
- **Descripción**: Genera etiquetas con código QR y información básica
- **Campos incluidos**:
  - Código PATCO
  - Nombre del equipo
  - Modelo y serie
  - Cliente
  - Código QR con URL
- **Formato**: Optimizado para etiquetas pequeñas
- **Uso**: Desde vista de equipos → Imprimir → Etiquetas QR

### 3. Etiquetas QR Compactas (equipment_qr_labels_compact)
- **Archivo**: `reports/equipment_qr_labels.xml` (template adicional)
- **Tipo**: PDF
- **Descripción**: Versión compacta para múltiples etiquetas por página
- **Características**:
  - Diseño minimalista
  - Múltiples etiquetas por hoja
  - Solo información esencial
  - Código QR prominente

### Reporte de Servicios
- Historial completo de servicios por equipo
- Métricas de rendimiento y mantenimiento
- Análisis de frecuencia de servicios

## Configuración de Seguridad

### Grupos de Usuarios
- **Gestor de Activos** (`group_asset_manager`): Acceso completo a equipos y configuraciones
- **Usuario Base**: Acceso limitado según reglas de cliente

### Permisos de Acceso (ir.model.access.csv)
| Modelo | Usuario General | Gestor de Activos |
|--------|----------------|-------------------|
| `maintenance.equipment.category` | Lectura | Completo |
| `maintenance.equipment` | Lectura/Escritura limitada | Completo |

### Reglas de Seguridad (ir.rule)
1. **Equipos por Cliente**: Los usuarios solo ven equipos de sus clientes asociados
2. **Acceso de Gestores**: Los gestores de activos tienen acceso total
3. **Portal**: Usuarios del portal solo lectura de equipos públicos

### Configuración de Acceso
```xml
<!-- Ejemplo de regla de seguridad -->
<record id="equipment_user_rule" model="ir.rule">
    <field name="name">Equipment: User Access</field>
    <field name="model_id" ref="maintenance.model_maintenance_equipment"/>
    <field name="domain_force">[('customer_id', 'in', user.partner_id.child_ids.ids + [user.partner_id.id])]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
</record>
```

## Configuración Avanzada

### Personalización de Plantillas de Checklist
Las plantillas de checklist se pueden personalizar por categoría de equipo:

```python
# Ejemplo de personalización de checklist
category = self.env['maintenance.equipment.category'].browse(category_id)
entry_template = category.get_entry_checklist_template()
exit_template = category.get_exit_checklist_template()
```

### Configuración de Códigos QR
Los códigos QR se generan automáticamente y apuntan a:
- URL base: Configurable en parámetros del sistema
- Formato: `{base_url}/equipment/{patco_code}`
- Regeneración: Disponible desde la vista de equipo

### Integración con Módulos Externos
El módulo está preparado para integrarse con:
- **FSM (Field Service Management)**: Órdenes de servicio automáticas
- **Helpdesk**: Tickets de soporte vinculados a equipos
- **Portal**: Acceso de clientes a información de equipos

### Parámetros del Sistema
| Parámetro | Descripción | Valor por Defecto |
|-----------|-------------|-------------------|
| `patco.equipment.qr_base_url` | URL base para códigos QR | `http://localhost:8069` |
| `patco.equipment.auto_sequence` | Secuencia automática de códigos | `True` |
### Ejemplos de Plantillas de Checklist

```html
<!-- Ejemplo de plantilla de entrada -->
<div class="checklist-template">
    <h3>Checklist de Entrada - {category_name}</h3>
    <ul>
        <li>☐ Verificar estado físico del equipo</li>
        <li>☐ Documentar accesorios incluidos</li>
        <li>☐ Registrar lecturas iniciales</li>
        <li>☐ Tomar fotografías del estado actual</li>
    </ul>
</div>
```

```html
<!-- Ejemplo de plantilla de salida -->
<div class="checklist-template">
    <h3>Checklist de Salida - {category_name}</h3>
    <ul>
        <li>☐ Limpieza completa del equipo</li>
        <li>☐ Verificar funcionamiento correcto</li>
        <li>☐ Documentar trabajos realizados</li>
        <li>☐ Entrega de documentación al cliente</li>
    </ul>
</div>
```

### Configuración de Herencia
- **Herencia de Checklists**: Permite que subcategorías hereden plantillas de categorías padre
- **Herencia de Documentación**: Acceso a documentos técnicos de toda la jerarquía
- **Plantillas Efectivas**: Combinación automática de configuración local y heredada

## Soporte

- **Autor**: PATCO
- **Versión**: 18.0.1.0.0
- **Licencia**: LGPL-3
- **Compatibilidad**: Odoo Community 18.0+
- **Repositorio**: Parte del ecosistema patco_suite

## Notas de Desarrollo

### Arquitectura
- Sigue el patrón de extensión de Odoo sin modificar código core
- Utiliza herencia de modelos y vistas para máxima compatibilidad
- Implementa hooks de creación/escritura para automatización
- Campos computados para métricas en tiempo real

### Mejores Prácticas Implementadas
- Validaciones de unicidad por cliente
- Generación automática de códigos únicos
- Integración opcional con módulos FSM y Helpdesk
- Estructura modular para fácil mantenimiento
- Documentación técnica completa

### Consideraciones de Rendimiento
- Campos computados con store=False para datos dinámicos
- Índices en campos de búsqueda frecuente
- Lazy loading de códigos QR
- Optimización de consultas en contadores
