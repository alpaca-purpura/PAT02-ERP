# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SuggestTechnicianWizard(models.TransientModel):
    _name = 'suggest.technician.wizard'
    _description = 'Wizard para Sugerir Técnicos'
    
    fsm_order_id = fields.Many2one(
        'fsm.order',
        string='Orden de Servicio',
        required=True
    )
    
    equipment_category = fields.Char(
        string='Categoría del Equipo',
        compute='_compute_equipment_category',
        readonly=True
    )
    
    required_skills = fields.Text(
        string='Habilidades Requeridas',
        help='Lista de habilidades requeridas separadas por comas'
    )
    
    suggested_technician_ids = fields.Many2many(
        'hr.employee',
        string='Técnicos Sugeridos',
        compute='_compute_suggested_technicians',
        store=False
    )
    
    selected_technician_id = fields.Many2one(
        'hr.employee',
        string='Técnico Seleccionado'
    )
    
    @api.depends('fsm_order_id')
    def _compute_equipment_category(self):
        """Computa la categoría del equipo basándose en la orden de servicio"""
        for wizard in self:
            if wizard.fsm_order_id and hasattr(wizard.fsm_order_id, 'x_equipment_id') and wizard.fsm_order_id.x_equipment_id:
                # Si existe el campo x_equipment_id, usar su categoría
                equipment = wizard.fsm_order_id.x_equipment_id
                if hasattr(equipment, 'category_id') and equipment.category_id:
                    wizard.equipment_category = equipment.category_id.name
                else:
                    wizard.equipment_category = 'Sin categoría'
            else:
                wizard.equipment_category = 'No especificado'
    
    @api.depends('fsm_order_id', 'required_skills')
    def _compute_suggested_technicians(self):
        """Computa los técnicos sugeridos basado en habilidades"""
        for wizard in self:
            if not wizard.fsm_order_id:
                wizard.suggested_technician_ids = False
                continue
            
            # Si hay habilidades específicas requeridas
            if wizard.required_skills:
                skills_list = [skill.strip() for skill in wizard.required_skills.split(',')]
                suggested = wizard.fsm_order_id.get_suitable_technicians(skills_list)
            else:
                # Sugerir basado en el equipo
                suggested = wizard.fsm_order_id.suggest_technician_by_equipment()
            
            wizard.suggested_technician_ids = suggested
    
    def assign_technician(self):
        """Asigna el técnico seleccionado a la orden de servicio"""
        if self.selected_technician_id:
            self.fsm_order_id.person_id = self.selected_technician_id
        
        return {'type': 'ir.actions.act_window_close'}
    
    @api.model
    def default_get(self, fields_list):
        """Valores por defecto del wizard"""
        res = super().default_get(fields_list)
        
        # Obtener la orden de servicio del contexto
        fsm_order_id = self.env.context.get('active_id')
        if fsm_order_id:
            res['fsm_order_id'] = fsm_order_id
            
            # Pre-llenar habilidades basadas en el equipo
            fsm_order = self.env['fsm.order'].browse(fsm_order_id)
            if hasattr(fsm_order, 'x_equipment_id') and fsm_order.x_equipment_id:
                equipment = fsm_order.x_equipment_id
                if hasattr(equipment, 'category_id') and equipment.category_id:
                    category_name = equipment.category_id.name.lower()
                else:
                    category_name = ''
                
                # Mapeo de categorías a habilidades sugeridas
                if category_name:
                    skill_suggestions = {
                        'cocina': 'COC-CAL, COC-PRE',
                        'refrigeración': 'REF-COM, AC',
                        'lavandería': 'LAV-LAV, LAV-SEC',
                        'eléctrico': 'ELEC-BT',
                        'fontanería': 'FONT-AGUA'
                    }
                    
                    for category, skills in skill_suggestions.items():
                        if category in category_name:
                            res['required_skills'] = skills
                            break