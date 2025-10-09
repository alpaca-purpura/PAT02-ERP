# Plan de Mejora FSM: Múltiples Activos y Técnicos

## 1. Análisis de la Situación Actual

### 1.1 Estructura Actual de FSM Order
Basado en el análisis de los archivos `patco_fsm/models/fsm_order.py` y `patco_equipment/models/fsm_order.py`, la implementación actual presenta las siguientes limitaciones:

**Limitaciones Identificadas:**
- Relación 1:1 entre orden de servicio y equipo (`x_equipment_id`)
- Asignación de un solo técnico por orden (`person_id`)
- Referencias a proyecto y tarea que no son necesarias para el flujo operativo
- Falta de jerarquía entre técnicos (líder vs. colaboradores)
- Cliente no está correctamente vinculado a la ubicación

### 1.2 Campos Actuales Relevantes
```python
# Campos existentes en fsm.order
x_equipment_id = fields.Many2one('maintenance.equipment')  # LIMITADO: Solo 1 equipo
person_id = fields.Many2one('hr.employee')  # LIMITADO: Solo 1 técnico
x_nature_id = fields.Many2one()  # OK: Naturaleza del trabajo
x_area_id = fields.Many2one()  # OK: Área de trabajo
x_complexity_id = fields.Many2one()  # OK: Complejidad
x_required_skill_types = fields.Many2many()  # OK: Habilidades requeridas
```

## 2. Propuesta de Nueva Arquitectura

### 2.1 Nuevos Modelos Requeridos

#### Modelo: `fsm.order.equipment` (Nuevo)
**Propósito:** Gestionar la relación muchos-a-muchos entre órdenes y equipos

```python
class FsmOrderEquipment(models.Model):
    _name = 'fsm.order.equipment'
    _description = 'Equipos asociados a orden de servicio'
    
    order_id = fields.Many2one('fsm.order', required=True, ondelete='cascade')
    equipment_id = fields.Many2one('maintenance.equipment', required=True)
    
    # Campos específicos por equipo
    priority = fields.Selection([('low', 'Baja'), ('normal', 'Normal'), ('high', 'Alta')])
    estimated_duration = fields.Float('Duración Estimada (horas)')
    specific_notes = fields.Text('Notas Específicas')
    
    # Habilidades requeridas específicas para este equipo
    required_skill_types = fields.Many2many('hr.skill.type')
    min_skill_level = fields.Integer('Nivel Mínimo Requerido')
    
    # Estado del trabajo en este equipo
    status = fields.Selection([
        ('pending', 'Pendiente'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completado'),
        ('blocked', 'Bloqueado')
    ], default='pending')
```

#### Modelo: `fsm.order.technician` (Nuevo)
**Propósito:** Gestionar la asignación de múltiples técnicos con roles específicos

```python
class FsmOrderTechnician(models.Model):
    _name = 'fsm.order.technician'
    _description = 'Técnicos asignados a orden de servicio'
    
    order_id = fields.Many2one('fsm.order', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', required=True)
    
    # Rol del técnico
    role = fields.Selection([
        ('leader', 'Líder Técnico'),
        ('specialist', 'Especialista'),
        ('assistant', 'Asistente'),
        ('trainee', 'Aprendiz')
    ], required=True)
    
    # Asignación específica a equipos
    assigned_equipment_ids = fields.Many2many(
        'fsm.order.equipment',
        string='Equipos Asignados'
    )
    
    # Control de tiempo
    estimated_hours = fields.Float('Horas Estimadas')
    actual_hours = fields.Float('Horas Reales', compute='_compute_actual_hours')
    
    # Validación de habilidades
    skill_match_status = fields.Selection([
        ('perfect', 'Perfecto'),
        ('adequate', 'Adecuado'),
        ('insufficient', 'Insuficiente')
    ], compute='_compute_skill_match')
    
    skill_warnings = fields.Text('Advertencias de Habilidades', readonly=True)
```

### 2.2 Modificaciones al Modelo FSM Order Principal

#### Campos a Agregar
```python
# Relaciones múltiples
equipment_ids = fields.One2many('fsm.order.equipment', 'order_id', 'Equipos')
technician_ids = fields.One2many('fsm.order.technician', 'order_id', 'Técnicos')

# Cliente y ubicación
customer_id = fields.Many2one('res.partner', 'Cliente', domain=[('is_company', '=', True)])
service_location_id = fields.Many2one(
    'res.partner', 
    'Ubicación de Servicio',
    domain="[('parent_id', '=', customer_id)]"
)

# Líder técnico (campo computado)
lead_technician_id = fields.Many2one(
    'hr.employee',
    'Líder Técnico',
    compute='_compute_lead_technician',
    store=True
)

# Campos de control
total_estimated_duration = fields.Float(
    'Duración Total Estimada',
    compute='_compute_total_duration'
)

technician_count = fields.Integer(
    'Número de Técnicos',
    compute='_compute_technician_count'
)

equipment_count = fields.Integer(
    'Número de Equipos',
    compute='_compute_equipment_count'
)
```

#### Campos a Deprecar/Eliminar
```python
# Estos campos deben ser marcados como deprecated
x_equipment_id = fields.Many2one()  # DEPRECAR: Usar equipment_ids
person_id = fields.Many2one()  # DEPRECAR: Usar technician_ids
project_id = fields.Many2one()  # ELIMINAR: No necesario
task_id = fields.Many2one()  # ELIMINAR: No necesario
```

## 3. Cambios en Vistas

### 3.1 Vista de Formulario Principal

#### Sección Cliente y Ubicación (Nueva)
```xml
<group name="customer_location" string="Cliente y Ubicación">
    <field name="customer_id" options="{'no_create': True}"/>
    <field name="service_location_id" 
           domain="[('parent_id', '=', customer_id)]"
           options="{'no_create': True}"/>
    <field name="x_detailed_location" placeholder="Indicaciones específicas..."/>
</group>
```

#### Sección Equipos (Modificada)
```xml
<notebook>
    <page string="Equipos a Intervenir" name="equipment_page">
        <field name="equipment_ids" nolabel="1">
            <tree editable="bottom">
                <field name="equipment_id" domain="[('x_customer_id', '=', parent.customer_id)]"/>
                <field name="priority"/>
                <field name="estimated_duration" widget="float_time"/>
                <field name="required_skill_types" widget="many2many_tags"/>
                <field name="status"/>
            </tree>
        </field>
        <group>
            <field name="equipment_count" readonly="1"/>
            <field name="total_estimated_duration" widget="float_time" readonly="1"/>
        </group>
    </page>
</notebook>
```

#### Sección Técnicos (Nueva)
```xml
<page string="Asignación de Técnicos" name="technician_page">
    <field name="technician_ids" nolabel="1">
        <tree editable="bottom">
            <field name="employee_id"/>
            <field name="role"/>
            <field name="assigned_equipment_ids" widget="many2many_tags"/>
            <field name="estimated_hours" widget="float_time"/>
            <field name="skill_match_status" readonly="1"/>
        </tree>
    </field>
    <group>
        <field name="lead_technician_id" readonly="1"/>
        <field name="technician_count" readonly="1"/>
    </group>
</page>
```

### 3.2 Button Box Actualizado
```xml
<div class="oe_button_box" name="button_box">
    <button name="action_view_equipment" type="object" 
            class="oe_stat_button" icon="fa-cogs">
        <field name="equipment_count" widget="statinfo" string="Equipos"/>
    </button>
    <button name="action_view_technicians" type="object" 
            class="oe_stat_button" icon="fa-users">
        <field name="technician_count" widget="statinfo" string="Técnicos"/>
    </button>
    <!-- Botones existentes -->
</div>
```

## 4. Lógica de Negocio y Validaciones

### 4.1 Métodos de Validación

#### Validación de Habilidades por Equipo
```python
@api.constrains('technician_ids', 'equipment_ids')
def _check_technician_skills(self):
    """Validar que los técnicos tengan las habilidades requeridas."""
    for order in self:
        for equipment in order.equipment_ids:
            assigned_technicians = order.technician_ids.filtered(
                lambda t: equipment in t.assigned_equipment_ids
            )
            
            if not assigned_technicians:
                raise ValidationError(
                    f"El equipo {equipment.equipment_id.name} debe tener al menos un técnico asignado."
                )
            
            # Validar habilidades específicas
            for skill_type in equipment.required_skill_types:
                skilled_technicians = assigned_technicians.filtered(
                    lambda t: skill_type in t.employee_id.skill_ids.mapped('skill_type_id')
                )
                
                if not skilled_technicians:
                    raise ValidationError(
                        f"Ningún técnico asignado al equipo {equipment.equipment_id.name} "
                        f"tiene la habilidad requerida: {skill_type.name}"
                    )
```

#### Validación de Líder Técnico
```python
@api.constrains('technician_ids')
def _check_single_leader(self):
    """Asegurar que solo haya un líder técnico por orden."""
    for order in self:
        leaders = order.technician_ids.filtered(lambda t: t.role == 'leader')
        if len(leaders) > 1:
            raise ValidationError("Solo puede haber un líder técnico por orden de servicio.")
        elif len(leaders) == 0 and order.technician_ids:
            raise ValidationError("Debe asignar un líder técnico cuando hay técnicos asignados.")
```

### 4.2 Métodos Computados

```python
@api.depends('technician_ids.role')
def _compute_lead_technician(self):
    """Identificar automáticamente el líder técnico."""
    for order in self:
        leader = order.technician_ids.filtered(lambda t: t.role == 'leader')
        order.lead_technician_id = leader.employee_id if leader else False

@api.depends('equipment_ids.estimated_duration')
def _compute_total_duration(self):
    """Calcular duración total estimada."""
    for order in self:
        order.total_estimated_duration = sum(order.equipment_ids.mapped('estimated_duration'))

@api.onchange('customer_id')
def _onchange_customer_id(self):
    """Limpiar ubicación cuando cambia el cliente."""
    if self.customer_id:
        self.service_location_id = False
        # Filtrar equipos del cliente
        return {
            'domain': {
                'service_location_id': [('parent_id', '=', self.customer_id.id)]
            }
        }
```

## 5. Plan de Implementación

### Fase 1: Preparación (Semana 1)
1. **Backup de datos actuales**
2. **Crear modelos nuevos** (`fsm.order.equipment`, `fsm.order.technician`)
3. **Agregar campos nuevos** al modelo `fsm.order` principal
4. **Migración de datos existentes**:
   - Convertir `x_equipment_id` → `equipment_ids`
   - Convertir `person_id` → `technician_ids` con rol 'leader'

### Fase 2: Vistas y UX (Semana 2)
1. **Actualizar vista de formulario** con nuevas secciones
2. **Crear vistas de lista** para modelos relacionados
3. **Implementar botones de acción** para navegación
4. **Agregar wizards** para asignación masiva de técnicos

### Fase 3: Lógica de Negocio (Semana 3)
1. **Implementar validaciones** de habilidades y roles
2. **Crear métodos computados** para campos derivados
3. **Desarrollar reportes** de asignación y carga de trabajo
4. **Integrar con timesheet** para múltiples técnicos

### Fase 4: Testing y Refinamiento (Semana 4)
1. **Pruebas unitarias** de validaciones
2. **Pruebas de integración** con módulos existentes
3. **Pruebas de usuario** con casos reales
4. **Optimización de rendimiento** para consultas complejas

## 6. Consideraciones Técnicas

### 6.1 Rendimiento
- Usar `store=True` en campos computados críticos
- Implementar índices en campos de búsqueda frecuente
- Optimizar dominios con `domain` en lugar de filtros Python

### 6.2 Seguridad
- Mantener reglas de acceso existentes
- Agregar reglas específicas para modelos nuevos
- Validar permisos en métodos de asignación

### 6.3 Compatibilidad
- Mantener campos deprecados por compatibilidad temporal
- Crear métodos de migración automática
- Documentar cambios en README del módulo

## 7. Beneficios Esperados

### 7.1 Operativos
- **Flexibilidad**: Múltiples equipos y técnicos por visita
- **Especialización**: Asignación basada en habilidades específicas
- **Supervisión**: Clara jerarquía con líder técnico
- **Eficiencia**: Mejor planificación de recursos

### 7.2 Técnicos
- **Escalabilidad**: Arquitectura preparada para crecimiento
- **Mantenibilidad**: Separación clara de responsabilidades
- **Extensibilidad**: Fácil agregar nuevas funcionalidades
- **Trazabilidad**: Mejor seguimiento de asignaciones

---

*Documento técnico para Proyecto PATCO - Odoo 18 Community Edition*
*Versión: 1.0 | Fecha: Diciembre 2024*