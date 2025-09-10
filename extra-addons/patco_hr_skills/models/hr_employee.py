# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Campo de habilidades técnicas (no existe en Odoo 18 Community)
    employee_skill_ids = fields.One2many(
        'hr.employee.skill',
        'employee_id',
        string='Habilidades',
        help='Habilidades técnicas del empleado'
    )
    
    # Campo computado para mostrar habilidades principales
    main_skills = fields.Char(
        string='Habilidades Principales',
        compute='_compute_main_skills',
        store=True,
        help='Resumen de las principales habilidades técnicas'
    )
    
    # Campo para indicar si es técnico de campo
    is_field_technician = fields.Boolean(
        string='Técnico de Campo',
        default=False,
        help='Indica si el empleado es un técnico de campo para servicios'
    )
    
    # Campo computado para contar órdenes de servicio
    fsm_order_count = fields.Integer(
        string='Órdenes de Servicio',
        compute='_compute_fsm_order_count',
        help='Número de órdenes de servicio asignadas'
    )
    
    def _compute_fsm_order_count(self):
        """Computa el número de órdenes de servicio del empleado"""
        for employee in self:
            # Por ahora establecemos en 0, se implementará cuando esté disponible FSM
            employee.fsm_order_count = 0
    
    @api.depends('employee_skill_ids.skill_id', 'employee_skill_ids.skill_level_id')
    def _compute_main_skills(self):
        """Computa las habilidades principales del empleado"""
        for employee in self:
            skills = []
            for skill_line in employee.employee_skill_ids:
                if skill_line.skill_id and skill_line.skill_level_id:
                    skill_text = f"{skill_line.skill_id.name} ({skill_line.skill_level_id.name})"
                    skills.append(skill_text)
            employee.main_skills = ', '.join(skills[:3])  # Mostrar solo las 3 principales
    
    def get_skills_by_type(self, skill_type_name):
        """Obtiene las habilidades del empleado por tipo
        
        Args:
            skill_type_name (str): Nombre del tipo de habilidad (ej: 'COC - Cocina')
            
        Returns:
            recordset: Habilidades del empleado del tipo especificado
        """
        return self.employee_skill_ids.filtered(
            lambda s: s.skill_id.skill_type_id.name == skill_type_name
        )
    
    def has_skill_level(self, skill_name, min_level=2):
        """Verifica si el empleado tiene una habilidad con nivel mínimo
        
        Args:
            skill_name (str): Nombre de la habilidad
            min_level (int): Nivel mínimo requerido (1=N1, 2=N2, 3=N3)
            
        Returns:
            bool: True si tiene la habilidad con el nivel mínimo
        """
        skill = self.employee_skill_ids.filtered(
            lambda s: skill_name in s.skill_id.name
        )
        if not skill:
            return False
        
        # Mapeo de niveles
        level_mapping = {
            'N1': 1,
            'N2': 2, 
            'N3': 3
        }
        
        current_level = 0
        for level_name, level_num in level_mapping.items():
            if level_name in skill[0].skill_level_id.name:
                current_level = level_num
                break
                
        return current_level >= min_level