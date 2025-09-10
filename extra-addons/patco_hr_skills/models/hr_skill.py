# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from collections import defaultdict


class HrSkillType(models.Model):
    """Tipos de habilidades (ej: COC - Cocina, REF - Refrigeración)"""
    _name = 'hr.skill.type'
    _description = 'Tipo de Habilidad'
    _order = 'name'

    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre del tipo de habilidad (ej: COC - Cocina)'
    )
    
    code = fields.Char(
        string='Código',
        required=True,
        help='Código corto del tipo (ej: COC, REF, LAV)'
    )
    
    description = fields.Text(
        string='Descripción',
        help='Descripción detallada del tipo de habilidad'
    )
    
    skill_ids = fields.One2many(
        'hr.skill',
        'skill_type_id',
        string='Habilidades'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True
    )

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'El código del tipo de habilidad debe ser único.')
    ]


class HrSkillLevel(models.Model):
    """Niveles de habilidad (N1, N2, N3)"""
    _name = 'hr.skill.level'
    _description = 'Nivel de Habilidad'
    _order = 'level_progress'

    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre del nivel (ej: N1 - Básico)'
    )
    
    level_progress = fields.Integer(
        string='Progreso',
        required=True,
        help='Valor numérico del nivel (1=N1, 2=N2, 3=N3)'
    )
    
    description = fields.Text(
        string='Descripción',
        help='Descripción del nivel de competencia'
    )
    
    # Campo eliminado: skill_type_id ya no es necesario para niveles genéricos
    
    active = fields.Boolean(
        string='Activo',
        default=True
    )

    _sql_constraints = [
        ('level_progress_positive', 'CHECK(level_progress > 0)', 'El progreso del nivel debe ser positivo.')
    ]


class HrSkill(models.Model):
    """Habilidades específicas (ej: Calentadores, Presión, Lavado)"""
    _name = 'hr.skill'
    _description = 'Habilidad'
    _order = 'skill_type_id, name'

    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre completo y descriptivo de la habilidad'
    )
    
    code = fields.Char(
        string='Código',
        help='Código corto o abreviatura de la habilidad'
    )
    
    skill_type_id = fields.Many2one(
        'hr.skill.type',
        string='Tipo de Habilidad',
        required=True
    )
    
    description = fields.Text(
        string='Descripción',
        help='Descripción detallada de la habilidad'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True
    )

    @api.depends('name', 'skill_type_id')
    def name_get(self):
        """Mostrar nombre con tipo de habilidad"""
        result = []
        for skill in self:
            name = f"[{skill.skill_type_id.code}] {skill.name}"
            result.append((skill.id, name))
        return result


class HrEmployeeSkill(models.Model):
    """Relación entre empleado y habilidad con nivel"""
    _name = 'hr.employee.skill'
    _description = 'Habilidad del Empleado'
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
        required=True
    )
    
    skill_level_id = fields.Many2one(
        'hr.skill.level',
        string='Nivel',
        required=True,
        domain="[('active', '=', True)]"
    )
    
    skill_type_id = fields.Many2one(
        'hr.skill.type',
        string='Tipo',
        related='skill_id.skill_type_id',
        store=True
    )
    
    level_progress = fields.Integer(
        string='Progreso',
        related='skill_level_id.level_progress',
        store=True
    )
    
    date_start = fields.Date(
        string='Fecha Inicio',
        default=fields.Date.context_today
    )
    
    date_end = fields.Date(
        string='Fecha Fin'
    )
    
    notes = fields.Text(
        string='Notas'
    )

    _sql_constraints = [
        ('employee_skill_uniq', 'unique(employee_id, skill_id)', 
         'El empleado ya tiene registrada esta habilidad.')
    ]

    def _create_logs(self):
        """Crear logs de habilidades para seguimiento histórico"""
        today = fields.Date.context_today(self)
        employee_skills = self.env['hr.employee.skill'].search([
            ('employee_id', 'in', self.employee_id.ids)
        ])
        employee_skill_logs = self.env['hr.employee.skill.log'].search([
            ('employee_id', 'in', self.employee_id.ids),
        ])

        skills_by_employees = defaultdict(lambda: self.env['hr.employee.skill'])
        for skill in employee_skills:
            skills_by_employees[skill.employee_id.id] |= skill

        logs_by_employees = defaultdict(lambda: self.env['hr.employee.skill.log'])
        for log in employee_skill_logs:
            logs_by_employees[log.employee_id.id] |= log

        skill_to_create_vals = []
        for employee in skills_by_employees:
            employee_logs = logs_by_employees[employee]
            for employee_skill in skills_by_employees[employee]:
                existing_log = employee_logs.filtered(lambda l: l.department_id == employee_skill.employee_id.department_id and l.skill_id == employee_skill.skill_id and l.date == today)
                if existing_log:
                    existing_log.write({'skill_level_id': employee_skill.skill_level_id.id})
                else:
                    skill_to_create_vals.append({
                        'employee_id': employee_skill.employee_id.id,
                        'skill_id': employee_skill.skill_id.id,
                        'skill_level_id': employee_skill.skill_level_id.id,
                        'department_id': employee_skill.employee_id.department_id.id,
                        'skill_type_id': employee_skill.skill_type_id.id,
                    })

        if skill_to_create_vals:
            self.env['hr.employee.skill.log'].create(skill_to_create_vals)

    @api.model_create_multi
    def create(self, vals_list):
        """Override create para generar logs automáticamente"""
        employee_skills = super().create(vals_list)
        employee_skills._create_logs()
        return employee_skills

    def write(self, vals):
        """Override write para generar logs automáticamente"""
        res = super().write(vals)
        self._create_logs()
        return res

    # Validación eliminada: Los niveles ahora son genéricos e independientes del tipo de habilidad


class HrEmployeeSkillLog(models.Model):
    """Historial de habilidades de empleados"""
    _name = 'hr.employee.skill.log'
    _description = 'Historial de Habilidades'
    _rec_name = 'skill_id'
    _order = 'employee_id,date'

    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado',
        required=True,
        ondelete='cascade'
    )
    
    department_id = fields.Many2one(
        'hr.department',
        string='Departamento'
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
        'hr.skill.type',
        string='Tipo de Habilidad',
        required=True,
        ondelete='cascade'
    )
    
    level_progress = fields.Integer(
        string='Progreso',
        related='skill_level_id.level_progress',
        store=True
    )
    
    date = fields.Date(
        string='Fecha',
        default=fields.Date.context_today
    )

    _sql_constraints = [
        ('_unique_skill_log', 'unique (employee_id, department_id, skill_id, date)', 
         'No se permiten dos niveles para la misma habilidad en el mismo día.')
    ]