# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FSMOrder(models.Model):
    _inherit = 'fsm.order'
    
    required_skills = fields.Text(
        string='Habilidades Requeridas',
        help='Habilidades técnicas requeridas para esta orden de servicio'
    )
    
    @api.model
    def get_suitable_technicians(self, skill_requirements=None):
        """Obtiene técnicos adecuados basado en habilidades requeridas
        
        Args:
            skill_requirements (list): Lista de habilidades requeridas
            
        Returns:
            recordset: Empleados que cumplen con los requisitos
        """
        if not skill_requirements:
            return self.env['hr.employee'].search([('is_field_technician', '=', True)])
        
        suitable_technicians = self.env['hr.employee']
        
        for employee in self.env['hr.employee'].search([('is_field_technician', '=', True)]):
            matches = 0
            for skill_req in skill_requirements:
                if employee.has_skill_level(skill_req, min_level=2):  # N2 mínimo
                    matches += 1
            
            # Si cumple con al menos el 70% de los requisitos
            if matches >= len(skill_requirements) * 0.7:
                suitable_technicians |= employee
                
        return suitable_technicians
    
    def suggest_technician_by_equipment(self):
        """Sugiere técnicos basado en el tipo de equipo
        
        Returns:
            recordset: Técnicos sugeridos
        """
        if not self.x_equipment_id:
            return self.env['hr.employee']
        
        # Mapeo de categorías de equipo a habilidades
        equipment_skill_mapping = {
            'cocina': ['COC-CAL', 'COC-PRE', 'COC-LAV'],
            'refrigeración': ['REF-COM', 'AC'],
            'lavandería': ['LAV-LAV', 'LAV-SEC', 'LAV-PLA'],
            'eléctrico': ['ELEC-BT', 'ELEC-GEN'],
            'fontanería': ['FONT-AGUA', 'FONT-GAS'],
        }
        
        equipment_category = self.x_equipment_id.category_id.name.lower() if self.x_equipment_id.category_id else ''
        
        for category, skills in equipment_skill_mapping.items():
            if category in equipment_category:
                return self.get_suitable_technicians(skills)
        
        # Si no hay mapeo específico, devolver todos los técnicos
        return self.env['hr.employee'].search([('is_field_technician', '=', True)])