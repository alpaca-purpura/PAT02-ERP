# -*- coding: utf-8 -*-
from odoo import models, fields, api


class HrSkillType(models.Model):
    """Tipo de habilidad técnica"""
    _name = 'hr.skill.type'
    _description = 'Tipo de Habilidad'
    _order = 'name'

    name = fields.Char('Nombre', required=True, translate=True)
    active = fields.Boolean('Activo', default=True)
    color = fields.Integer('Color', default=0, help='Índice de color para la visualización')
    skill_ids = fields.One2many('hr.skill', 'skill_type_id', string='Habilidades')
    skill_level_ids = fields.Many2many(
        'hr.skill.level',
        string='Niveles de Competencia',
        help='Niveles de competencia disponibles para este tipo de habilidad'
    )


# class HrSkillLevel(models.Model):
#     """Extensión del nivel de competencia para habilidades"""
#     _inherit = 'hr.skill.level'

#     level_progress = fields.Integer(
#         'Progreso (%)',
#         required=True,
#         help='Porcentaje de progreso (0-100)'
#     )

#     @api.constrains('level_progress')
#     def _check_level_progress(self):
#         for record in self:
#             if not 0 <= record.level_progress <= 100:
#                 raise models.ValidationError(
#                     'El progreso debe estar entre 0 y 100%'
#                 )


class HrSkill(models.Model):
    """Extensión de habilidad técnica"""
    _inherit = 'hr.skill'

    skill_type_id = fields.Many2one(
        'hr.skill.type',
        string='Tipo de Habilidad',
        required=True,
        ondelete='cascade'
    )
    
    def get_color_class(self):
        """Obtiene la clase CSS para el color de la habilidad"""
        colors = [
            'primary', 'secondary', 'success', 'danger', 
            'warning', 'info', 'light', 'dark'
        ]
        # Usar el campo color si existe (definido por fieldservice_skill)
        color_value = getattr(self, 'color', 0) or 0
        return colors[color_value % len(colors)]


class HrEmployeeSkill(models.Model):
    """Habilidad de empleado - Relación entre empleado y habilidad con nivel"""
    _name = 'hr.employee.skill'
    _description = 'Habilidad de Empleado'
    _rec_name = 'skill_id'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado',
        required=True,
        ondelete='cascade'
    )
    skill_id = fields.Many2one(
        'hr.skill',
        string='Habilidad',
        required=True,
        ondelete='cascade'
    )
    skill_level_id = fields.Many2one(
        'hr.skill.level',
        string='Nivel',
        required=True,
        ondelete='cascade'
    )
    skill_type_id = fields.Many2one(
        related='skill_id.skill_type_id',
        string='Tipo de Habilidad',
        store=True,
        readonly=True
    )

    _sql_constraints = [
        ('unique_employee_skill', 'unique(employee_id, skill_id)',
         'Un empleado no puede tener la misma habilidad duplicada.')
    ]