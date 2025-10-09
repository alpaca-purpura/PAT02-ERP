# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SuggestTechnicianWizard(models.TransientModel):
    _name = 'suggest.technician.wizard'
    _description = 'Wizard para Sugerir Técnicos Basado en Habilidades'
    
    fsm_order_id = fields.Many2one(
        'fsm.order',
        string='Orden FSM',
        required=True
    )
    
    equipment_category = fields.Many2one(
        'maintenance.equipment.category',
        string='Categoría de Equipo',
        compute='_compute_equipment_category',
        readonly=True
    )
    
    required_skills = fields.Many2many(
        'hr.skill',
        string='Habilidades Requeridas',
        related='fsm_order_id.required_skill_ids',
        readonly=True
    )
    
    min_skill_level = fields.Integer(
        string='Nivel Mínimo',
        related='fsm_order_id.min_skill_level',
        readonly=True
    )
    
    suggested_technician_ids = fields.Many2many(
        'hr.employee',
        'suggest_technician_wizard_employee_rel',
        'wizard_id',
        'employee_id',
        string='Técnicos Sugeridos',
        compute='_compute_suggested_technicians',
        store=False
    )
    
    selected_technician_id = fields.Many2one(
        'hr.employee',
        string='Técnico Seleccionado',
        domain="[('id', 'in', suggested_technician_ids)]"
    )
    
    suggestion_criteria = fields.Text(
        string='Criterios de Sugerencia',
        compute='_compute_suggestion_criteria',
        readonly=True
    )

    @api.depends('fsm_order_id')
    def _compute_equipment_category(self):
        """Computa la categoría del equipo basándose en la orden de servicio"""
        for wizard in self:
            equipment = None
            
            # Intentar obtener el equipo desde diferentes campos posibles
            if wizard.fsm_order_id:
                # Primero intentar con x_equipment_id (módulo patco_equipment)
                if hasattr(wizard.fsm_order_id, 'x_equipment_id') and wizard.fsm_order_id.x_equipment_id:
                    equipment = wizard.fsm_order_id.x_equipment_id
                # Luego intentar con equipment_id (campo estándar)
                elif hasattr(wizard.fsm_order_id, 'equipment_id') and wizard.fsm_order_id.equipment_id:
                    equipment = wizard.fsm_order_id.equipment_id
                # Finalmente intentar con equipment_ids (múltiples equipos)
                elif hasattr(wizard.fsm_order_id, 'equipment_ids') and wizard.fsm_order_id.equipment_ids:
                    equipment = wizard.fsm_order_id.equipment_ids[0]
            
            if equipment and hasattr(equipment, 'category_id') and equipment.category_id:
                wizard.equipment_category = equipment.category_id
            else:
                wizard.equipment_category = False

    @api.depends('fsm_order_id', 'required_skills', 'min_skill_level')
    def _compute_suggested_technicians(self):
        """Calcula técnicos sugeridos basado en habilidades y disponibilidad"""
        for wizard in self:
            if not wizard.fsm_order_id or not wizard.required_skills:
                wizard.suggested_technician_ids = False
                continue
            
            # Buscar empleados con habilidades coincidentes
            domain = [
                ('skill_ids.skill_id', 'in', wizard.required_skills.ids),
                ('skill_ids.level_progress', '>=', wizard.min_skill_level or 1)
            ]
            
            employees = self.env['hr.employee'].search(domain)
            
            # Filtrar por disponibilidad (no asignados a otras órdenes activas)
            available_employees = employees.filtered(
                lambda emp: not self._is_employee_busy(emp, wizard.fsm_order_id.date_start)
            )
            
            # Ordenar por coincidencia de habilidades
            sorted_employees = self._sort_by_skill_match(
                available_employees, 
                wizard.required_skills,
                wizard.min_skill_level
            )
            
            wizard.suggested_technician_ids = sorted_employees
    
    @api.depends('required_skills', 'min_skill_level', 'suggested_technician_ids')
    def _compute_suggestion_criteria(self):
        """Genera texto explicativo de los criterios de sugerencia"""
        for wizard in self:
            criteria = []
            
            if wizard.required_skills:
                skills_text = ', '.join(wizard.required_skills.mapped('name'))
                criteria.append(f"Habilidades requeridas: {skills_text}")
            
            if wizard.min_skill_level:
                criteria.append(f"Nivel mínimo: {wizard.min_skill_level}")
            
            if wizard.equipment_category:
                criteria.append(f"Categoría de equipo: {wizard.equipment_category.name}")
            
            criteria.append(f"Técnicos encontrados: {len(wizard.suggested_technician_ids)}")
            
            wizard.suggestion_criteria = '\n'.join(criteria)
    
    def _is_employee_busy(self, employee, order_date):
        """Verifica si el empleado está ocupado en la fecha de la orden"""
        if not order_date:
            return False
        
        # Buscar órdenes FSM activas del empleado en la misma fecha
        busy_orders = self.env['fsm.order'].search([
            ('person_id', '=', employee.id),
            ('stage_id.is_closed', '=', False),
            ('date_start', '<=', order_date),
            ('date_end', '>=', order_date)
        ])
        
        return bool(busy_orders)
    
    def _sort_by_skill_match(self, employees, required_skills, min_level):
        """Ordena empleados por coincidencia de habilidades"""
        def skill_score(employee):
            score = 0
            employee_skills = employee.skill_ids
            
            for required_skill in required_skills:
                matching_skills = employee_skills.filtered(
                    lambda s: s.skill_id == required_skill
                )
                
                if matching_skills:
                    # Puntuación basada en el nivel de habilidad
                    max_level = max(matching_skills.mapped('level_progress'))
                    score += max_level
                    
                    # Bonificación si supera el nivel mínimo
                    if max_level > min_level:
                        score += (max_level - min_level) * 2
            
            return score
        
        return employees.sorted(key=skill_score, reverse=True)
    
    def action_assign_technician(self):
        """Asigna el técnico seleccionado a la orden FSM"""
        self.ensure_one()
        
        if not self.selected_technician_id:
            raise UserError(_("Debe seleccionar un técnico para asignar."))
        
        # Asignar técnico a la orden
        self.fsm_order_id.write({
            'person_id': self.selected_technician_id.id
        })
        
        # Crear mensaje en el chatter
        self.fsm_order_id.message_post(
            body=_("Técnico asignado: %s") % self.selected_technician_id.name,
            message_type='notification'
        )
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Técnico Asignado'),
                'message': _("Se ha asignado %s a la orden %s") % (
                    self.selected_technician_id.name,
                    self.fsm_order_id.name
                ),
                'type': 'success'
            }
        }
    
    def action_view_technician_skills(self):
        """Abre la vista de habilidades del técnico seleccionado"""
        self.ensure_one()
        
        if not self.selected_technician_id:
            raise UserError(_("Debe seleccionar un técnico primero."))
        
        return {
            'type': 'ir.actions.act_window',
            'name': _("Habilidades de %s") % self.selected_technician_id.name,
            'res_model': 'hr.employee.skill',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.selected_technician_id.id)],
            'context': {'default_employee_id': self.selected_technician_id.id}
        }
    
    def action_refresh_suggestions(self):
        """Refresca las sugerencias de técnicos"""
        self.ensure_one()
        self._compute_suggested_technicians()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': _('Sugerencias actualizadas'),
                'type': 'info'
            }
        }