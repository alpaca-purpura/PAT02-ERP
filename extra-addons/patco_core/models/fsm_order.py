# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class FSMOrder(models.Model):
    _inherit = 'fsm.order'
    
    # Campos de clasificación PATCO
    x_nature_id = fields.Many2one(
        'patco.service.nature',
        string='Naturaleza del Servicio',
        help='Tipo de naturaleza del servicio según clasificación PATCO'
    )
    
    x_area_id = fields.Many2one(
        'patco.service.area',
        string='Área del Servicio',
        help='Área técnica del servicio según clasificación PATCO'
    )
    
    x_complexity_id = fields.Many2one(
        'patco.service.complexity',
        string='Complejidad del Servicio',
        help='Nivel de complejidad del servicio según clasificación PATCO'
    )
    
    x_classification_code = fields.Char(
        string='Código de Clasificación',
        compute='_compute_classification_code',
        store=True,
        help='Código automático generado basado en la clasificación PATCO'
    )
    
    # Campos para checklists heredados de la categoría del equipo
    x_entry_checklist = fields.Html(
        string='Checklist de Entrada',
        help='Checklist que debe completarse al iniciar el servicio'
    )
    
    x_exit_checklist = fields.Html(
        string='Checklist de Salida',
        help='Checklist que debe completarse al finalizar el servicio'
    )
    
    # Campo relacionado para mostrar la base de conocimiento
    x_equipment_category_id = fields.Many2one(
        'maintenance.equipment.category',
        string='Categoría del Equipo',
        compute='_compute_equipment_category',
        store=True,
        readonly=True
    )
    
    x_knowledge_base_count = fields.Integer(
        related='x_equipment_category_id.x_knowledge_base_count',
        string='Documentos Disponibles'
    )
    
    # Campos para gestión de stock en vehículos
    x_vehicle_location_id = fields.Many2one(
        'stock.location',
        string='Ubicación del Vehículo',
        domain="[('is_vehicle_location', '=', True), ('technician_id', '=', person_id)]",
        help='Ubicación de stock del vehículo del técnico asignado'
    )
    
    x_consumed_parts_ids = fields.One2many(
        'fsm.order.consumed.part',
        'order_id',
        string='Repuestos Consumidos'
    )
    
    x_total_parts_cost = fields.Float(
        string='Costo Total de Repuestos',
        compute='_compute_total_parts_cost',
        store=True
    )

    @api.depends('x_consumed_parts_ids.total_cost')
    def _compute_total_parts_cost(self):
        """Calcula el costo total de repuestos consumidos"""
        for record in self:
            record.x_total_parts_cost = sum(record.x_consumed_parts_ids.mapped('total_cost'))
    
    @api.depends('x_nature_id.code', 'x_area_id.code', 'x_complexity_id.code')
    def _compute_classification_code(self):
        """Genera el código de clasificación automáticamente"""
        for record in self:
            if record.x_nature_id and record.x_area_id and record.x_complexity_id:
                nature_code = record.x_nature_id.code
                area_code = record.x_area_id.code
                complexity_code = record.x_complexity_id.code
                
                record.x_classification_code = (
                    f"{nature_code}-{area_code}-{complexity_code}"
                )
            else:
                record.x_classification_code = False
    
    @api.depends('equipment_id')
    def _compute_equipment_category(self):
        """Calcula la categoría del equipo"""
        for record in self:
            if record.equipment_id and hasattr(record.equipment_id, 'category_id'):
                record.x_equipment_category_id = record.equipment_id.category_id
            else:
                record.x_equipment_category_id = False

    @api.onchange('person_id')
    def _onchange_person_id(self):
        """Actualiza la ubicación del vehículo cuando se asigna un técnico"""
        if hasattr(super(), '_onchange_person_id'):
            super()._onchange_person_id()
        if self.person_id:
            # Buscar la ubicación de vehículo del técnico
            vehicle_location = self.env['stock.location'].search([
                ('is_vehicle_location', '=', True),
                ('technician_id', '=', self.person_id.id)
            ], limit=1)
            if vehicle_location:
                self.x_vehicle_location_id = vehicle_location.id
        else:
            self.x_vehicle_location_id = False
    
    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        """Hereda las plantillas de checklist de la categoría del equipo"""
        if hasattr(super(), '_onchange_equipment_id'):
            super()._onchange_equipment_id()
        if self.equipment_id and hasattr(self.equipment_id, 'category_id') and self.equipment_id.category_id:
            category = self.equipment_id.category_id
            # Solo heredar si los campos están vacíos
            if not self.x_entry_checklist and hasattr(category, 'x_entry_checklist_template') and category.x_entry_checklist_template:
                self.x_entry_checklist = category.x_entry_checklist_template
            if not self.x_exit_checklist and hasattr(category, 'x_exit_checklist_template') and category.x_exit_checklist_template:
                self.x_exit_checklist = category.x_exit_checklist_template
    
    def action_view_equipment_knowledge_base(self):
        """Acción para ver la base de conocimiento de la categoría del equipo"""
        self.ensure_one()
        if not self.x_equipment_category_id:
            return {'type': 'ir.actions.act_window_close'}
        
        return self.x_equipment_category_id.action_view_knowledge_base()
    
    def action_consume_parts(self):
        """Acción para abrir el wizard de consumo de repuestos"""
        self.ensure_one()
        if not self.x_vehicle_location_id:
            raise UserError(_('Debe asignar un técnico con vehículo para consumir repuestos.'))
        
        return {
            'name': _('Consumir Repuestos'),
            'type': 'ir.actions.act_window',
            'res_model': 'fsm.order.consume.parts.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': self.id,
                'default_location_id': self.x_vehicle_location_id.id,
            }
        }
    
    def action_view_consumed_parts(self):
        """Acción para ver los repuestos consumidos"""
        self.ensure_one()
        return {
            'name': _('Repuestos Consumidos'),
            'type': 'ir.actions.act_window',
            'res_model': 'fsm.order.consumed.part',
            'view_mode': 'tree,form',
            'domain': [('order_id', '=', self.id)],
            'context': {'default_order_id': self.id},
            'target': 'current',
        }
    
    # Integración con fieldservice_skill
    x_required_skill_types = fields.Many2many(
        'hr.skill.type',
        string='Tipos de Habilidad Requeridos',
        help='Tipos de habilidades necesarias para esta orden'
    )
    
    x_min_skill_level = fields.Many2one(
        'hr.skill.level',
        string='Nivel Mínimo Requerido',
        help='Nivel mínimo de habilidad requerido'
    )
    
    x_available_technicians = fields.Many2many(
        'res.partner',
        string='Técnicos Disponibles',
        compute='_compute_available_technicians',
        help='Técnicos que cumplen con las habilidades requeridas'
    )
    
    x_skill_match_warning = fields.Text(
        string='Advertencia de Habilidades',
        compute='_compute_skill_match_warning',
        help='Advertencias sobre compatibilidad de habilidades'
    )
    
    # Campos computados para información contextual del activo
    x_equipment_category_name = fields.Char(
        string='Categoría del Equipo',
        compute='_compute_equipment_info',
        help='Nombre de la categoría del equipo'
    )
    x_equipment_location_name = fields.Char(
        string='Ubicación del Equipo',
        compute='_compute_equipment_info',
        help='Ubicación actual del equipo'
    )
    x_equipment_brand_model = fields.Char(
        string='Marca y Modelo',
        compute='_compute_equipment_info',
        help='Marca y modelo del equipo'
    )
    
    @api.depends('x_required_skill_types', 'x_min_skill_level', 'location_id')
    def _compute_available_technicians(self):
        """Calcula los técnicos disponibles basado en habilidades y ubicación"""
        for order in self:
            available_technicians = self.env['fsm.person']
            
            if not order.x_required_skill_types:
                # Si no hay habilidades requeridas, mostrar todos los técnicos
                available_technicians = self.env['fsm.person'].search([])
            else:
                # Buscar técnicos con las habilidades requeridas
                min_level = int(order.x_min_skill_level or '1')
                
                for skill_type in order.x_required_skill_types:
                    # Buscar técnicos con habilidades de este tipo y nivel mínimo
                    person_skills = self.env['fsm.person.skill'].search([
                        ('skill_type_id', '=', skill_type.id),
                        ('level_progress', '>=', min_level * 25)  # Asumiendo 25 puntos por nivel
                    ])
                    
                    skill_technicians = person_skills.mapped('person_id')
                    
                    if not available_technicians:
                        available_technicians = skill_technicians
                    else:
                        # Intersección - técnicos que tienen TODAS las habilidades
                        available_technicians = available_technicians & skill_technicians
            
            # Filtrar por ubicación si está configurado
            if order.location_id and available_technicians:
                # Aquí se podría agregar lógica adicional de filtrado por ubicación
                pass
            
            order.x_available_technicians = available_technicians
    
    @api.depends('x_required_skill_types', 'x_available_technicians', 'person_id')
    def _compute_skill_match_warning(self):
        """Calcula advertencias sobre compatibilidad de habilidades"""
        for order in self:
            warnings = []
            
            if order.x_required_skill_types and not order.x_available_technicians:
                warnings.append('⚠️ No hay técnicos disponibles con las habilidades requeridas.')
            
            if order.person_id and order.x_required_skill_types:
                if order.person_id not in order.x_available_technicians:
                    warnings.append(f'⚠️ El técnico asignado ({order.person_id.name}) no cumple con todos los requisitos de habilidades.')
            
            if order.x_required_skill_types and len(order.x_available_technicians) < 3:
                warnings.append(f'⚠️ Pocos técnicos disponibles ({len(order.x_available_technicians)}). Considere capacitar más personal.')
            
            order.x_skill_match_warning = '\n'.join(warnings) if warnings else False
    
    @api.onchange('x_equipment_category_id')
    def _onchange_equipment_category_skills(self):
        """Actualiza las habilidades requeridas basado en la categoría del equipo"""
        if self.x_equipment_category_id:
            # Mapeo de categorías a tipos de habilidades
            category_skill_mapping = {
                # Aquí se pueden definir mapeos específicos
                # Por ejemplo: 'Aire Acondicionado': ['Refrigeración', 'Electricidad']
            }
            
            category_name = self.x_equipment_category_id.name
            if category_name in category_skill_mapping:
                skill_type_names = category_skill_mapping[category_name]
                skill_types = self.env['hr.skill.type'].search([('name', 'in', skill_type_names)])
                self.x_required_skill_types = skill_types
    
    def action_suggest_technician(self):
        """Acción para sugerir técnico basado en habilidades"""
        if not self.x_required_skill_types:
            raise UserError("Debe especificar al menos un tipo de habilidad requerida.")
        
        # Buscar técnicos con las habilidades requeridas
        available_techs = self.x_available_technicians
        
        if not available_techs:
            raise UserError("No se encontraron técnicos con las habilidades requeridas.")
        
        # Si hay técnicos disponibles, mostrar wizard de selección
        return {
            'type': 'ir.actions.act_window',
            'name': 'Seleccionar Técnico',
            'res_model': 'fsm.wizard.assign.person',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': self.id,
                'available_technicians': available_techs.ids,
            }
        }
    
    @api.depends('equipment_id')
    def _compute_equipment_info(self):
        """Computar información contextual del activo"""
        for record in self:
            if record.equipment_id:
                equipment = record.equipment_id
                
                # Categoría del equipo
                record.x_equipment_category_name = equipment.category_id.name if equipment.category_id else 'Sin categoría'
                
                # Ubicación del equipo
                if hasattr(equipment, 'location_id') and equipment.location_id:
                    record.x_equipment_location_name = equipment.location_id.name
                elif hasattr(equipment, 'partner_id') and equipment.partner_id:
                    record.x_equipment_location_name = f"Cliente: {equipment.partner_id.name}"
                else:
                    record.x_equipment_location_name = 'Ubicación no definida'
                
                # Marca y modelo
                brand = getattr(equipment, 'brand', '') or ''
                model = getattr(equipment, 'model', '') or ''
                if brand and model:
                    record.x_equipment_brand_model = f"{brand} - {model}"
                elif brand:
                    record.x_equipment_brand_model = brand
                elif model:
                    record.x_equipment_brand_model = model
                else:
                    record.x_equipment_brand_model = 'No especificado'
            else:
                record.x_equipment_category_name = ''
                record.x_equipment_location_name = ''
                record.x_equipment_brand_model = ''