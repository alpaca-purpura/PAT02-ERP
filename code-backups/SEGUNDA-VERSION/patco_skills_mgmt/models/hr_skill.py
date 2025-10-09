# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from collections import defaultdict
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class HrSkillType(models.Model):
    """Extensión de tipos de habilidades para PATCO"""
    _inherit = 'hr.skill.type'
    
    code = fields.Char(
        string='Código',
        help='Código corto del tipo (ej: COC, REF, LAV)'
    )
    
    description = fields.Text(
        string='Descripción',
        help='Descripción detallada del tipo de habilidad'
    )
    
    skill_count = fields.Integer(
        string='Cantidad de Habilidades',
        compute='_compute_skill_count',
        help='Número total de habilidades de este tipo'
    )
    
    @api.depends('skill_ids')
    def _compute_skill_count(self):
        """Calcular el número de habilidades por tipo"""
        for skill_type in self:
            skill_type.skill_count = len(skill_type.skill_ids)


class HrSkillLevel(models.Model):
    """Extensión de niveles de habilidad para PATCO"""
    _inherit = 'hr.skill.level'
    
    description = fields.Text(
        string='Descripción',
        help='Descripción detallada del nivel de habilidad'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Si está marcado, el nivel está activo'
    )


class HrSkill(models.Model):
    """Extensión de habilidades para PATCO"""
    _inherit = 'hr.skill'
    
    code = fields.Char(
        string='Código',
        help='Código único de la habilidad'
    )
    
    description = fields.Text(
        string='Descripción',
        help='Descripción detallada de la habilidad'
    )
    
    employee_skill_ids = fields.One2many(
        'hr.employee.skill',
        'skill_id',
        string='Habilidades de Empleados'
    )
    
    employee_count = fields.Integer(
        string='Número de Empleados',
        compute='_compute_employee_count',
        help='Número de empleados que tienen esta habilidad'
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Si está marcado, la habilidad está activa'
    )
    
    @api.depends('employee_skill_ids')
    def _compute_employee_count(self):
        """Calcula el número de empleados que tienen esta habilidad"""
        for skill in self:
            skill.employee_count = len(skill.employee_skill_ids)

    @api.depends('name', 'skill_type_id')
    def name_get(self):
        """Mostrar nombre con tipo de habilidad"""
        result = []
        for skill in self:
            if skill.skill_type_id and skill.skill_type_id.code:
                name = f"[{skill.skill_type_id.code}] {skill.name}"
            else:
                name = skill.name
            result.append((skill.id, name))
        return result


class HrEmployeeSkill(models.Model):
    """Extensión de habilidades de empleado para PATCO"""
    _inherit = 'hr.employee.skill'
    
    is_certified = fields.Boolean(
        string='Certificado',
        default=False,
        help='Indica si el empleado tiene certificación en esta habilidad'
    )
    
    certification_date = fields.Date(
        string='Fecha de Certificación',
        help='Fecha en que el empleado obtuvo la certificación'
    )
    
    certification_body = fields.Char(
        string='Entidad Certificadora',
        help='Nombre de la entidad que otorgó la certificación'
    )
    
    date_start = fields.Date(
        string='Fecha de Inicio',
        help='Fecha en que el empleado comenzó a desarrollar esta habilidad'
    )
    
    date_end = fields.Date(
        string='Fecha de Fin',
        help='Fecha en que el empleado dejó de usar esta habilidad'
    )
    
    date_acquired = fields.Date(
        string='Fecha de Adquisición',
        default=fields.Date.today,
        help='Fecha en que el empleado adquirió esta habilidad'
    )
    
    notes = fields.Text(
        string='Notas',
        help='Observaciones adicionales sobre la habilidad del empleado'
    )
    
    # Campos relacionados para facilitar búsquedas
    skill_type_id = fields.Many2one(
        'hr.skill.type',
        string='Tipo de Habilidad',
        related='skill_id.skill_type_id',
        store=True
    )
    
    level_progress = fields.Integer(
        string='Progreso del Nivel',
        related='skill_level_id.level_progress',
        store=True
    )
    
    def _determine_change_type(self, old_progress, new_progress, employee_skill):
        """Determinar el tipo de cambio en la habilidad basado en el progreso y contexto"""
        try:
            # Si es la primera vez que se registra la habilidad
            if old_progress == 0 and new_progress > 0:
                if employee_skill.is_certified:
                    return 'certified'
                else:
                    return 'acquired'
            
            # Si hay mejora en el nivel
            elif new_progress > old_progress:
                if employee_skill.is_certified and not hasattr(employee_skill, '_was_certified_before'):
                    return 'certified'
                else:
                    return 'improved'
            
            # Si hay retroceso (poco común pero posible)
            elif new_progress < old_progress:
                # Verificar si la certificación expiró
                if employee_skill.certification_date and employee_skill.date_end:
                    if employee_skill.date_end <= fields.Date.today():
                        return 'expired'
                return 'improved'  # Cambio general
            
            # Sin cambio en progreso pero podría ser certificación
            else:
                if employee_skill.is_certified:
                    return 'certified'
                return 'improved'
                
        except Exception as e:
            _logger.warning(f"Error determinando tipo de cambio: {str(e)}")
            return 'improved'  # Valor por defecto seguro

    def _create_logs(self):
        """Crear logs de habilidades para seguimiento histórico con validaciones robustas"""
        if not self:
            _logger.warning("_create_logs llamado sin registros de habilidades")
            return
            
        try:
            today = fields.Date.context_today(self)
            _logger.info(f"Iniciando creación de logs para {len(self)} habilidades de empleado en fecha {today}")
            
            # Validar que todos los registros tengan empleado
            invalid_skills = self.filtered(lambda s: not s.employee_id)
            if invalid_skills:
                _logger.error(f"Encontradas {len(invalid_skills)} habilidades sin empleado asignado")
                return
            
            # Obtener habilidades actuales de los empleados
            employee_ids = self.employee_id.ids
            employee_skills = self.env['hr.employee.skill'].search([
                ('employee_id', 'in', employee_ids)
            ])
            
            # Obtener logs existentes del día actual
            employee_skill_logs = self.env['hr.employee.skill.log'].search([
                ('employee_id', 'in', employee_ids),
                ('date', '=', today)
            ])
            
            _logger.debug(f"Procesando {len(employee_skills)} habilidades de {len(employee_ids)} empleados")
            _logger.debug(f"Encontrados {len(employee_skill_logs)} logs existentes para hoy")

            # Agrupar por empleado para procesamiento eficiente
            skills_by_employees = defaultdict(lambda: self.env['hr.employee.skill'])
            for skill in employee_skills:
                skills_by_employees[skill.employee_id.id] |= skill

            logs_by_employees = defaultdict(lambda: self.env['hr.employee.skill.log'])
            for log in employee_skill_logs:
                logs_by_employees[log.employee_id.id] |= log

            skill_to_create_vals = []
            logs_updated = 0
            logs_created = 0
            
            for employee_id in skills_by_employees:
                try:
                    employee_logs = logs_by_employees[employee_id]
                    employee_skills_set = skills_by_employees[employee_id]
                    
                    for employee_skill in employee_skills_set:
                        # Validaciones de integridad
                        if not employee_skill.skill_id:
                            _logger.warning(f"Habilidad de empleado {employee_skill.employee_id.name} sin skill_id")
                            continue
                            
                        if not employee_skill.skill_level_id:
                            _logger.warning(f"Habilidad {employee_skill.skill_id.name} de empleado {employee_skill.employee_id.name} sin nivel")
                            continue
                        
                        # Buscar log existente para esta habilidad hoy
                        existing_log = employee_logs.filtered(
                            lambda l: l.department_id == employee_skill.employee_id.department_id and 
                                     l.skill_id == employee_skill.skill_id and 
                                     l.date == today
                        )
                        
                        if existing_log:
                            # Actualizar log existente si hay cambios
                            old_level_progress = existing_log.level_progress
                            new_level_progress = employee_skill.skill_level_id.level_progress
                            
                            if old_level_progress != new_level_progress:
                                change_type = self._determine_change_type(old_level_progress, new_level_progress, employee_skill)
                                existing_log.write({
                                    'skill_level_id': employee_skill.skill_level_id.id,
                                    'old_level_progress': old_level_progress,
                                    'new_level_progress': new_level_progress,
                                    'change_type': change_type,
                                    'notes': f"Actualizado automáticamente: {change_type}"
                                })
                                logs_updated += 1
                                _logger.debug(f"Log actualizado para {employee_skill.employee_id.name} - {employee_skill.skill_id.name}: {old_level_progress} -> {new_level_progress}")
                        else:
                            # Crear nuevo log
                            if not employee_skill.employee_id.department_id:
                                _logger.warning(f"Empleado {employee_skill.employee_id.name} sin departamento asignado")
                                department_id = False
                            else:
                                department_id = employee_skill.employee_id.department_id.id
                            
                            change_type = self._determine_change_type(0, employee_skill.skill_level_id.level_progress, employee_skill)
                            
                            skill_to_create_vals.append({
                                'employee_id': employee_skill.employee_id.id,
                                'skill_id': employee_skill.skill_id.id,
                                'skill_level_id': employee_skill.skill_level_id.id,
                                'department_id': department_id,
                                'skill_type_id': employee_skill.skill_type_id.id if employee_skill.skill_type_id else False,
                                'old_level_progress': 0,
                                'new_level_progress': employee_skill.skill_level_id.level_progress,
                                'change_type': change_type,
                                'notes': f"Registro inicial: {change_type}",
                                'date': today
                            })
                            
                except Exception as e:
                    _logger.error(f"Error procesando empleado {employee_id}: {str(e)}")
                    continue

            # Crear logs en lote para mejor rendimiento
            if skill_to_create_vals:
                try:
                    created_logs = self.env['hr.employee.skill.log'].create(skill_to_create_vals)
                    logs_created = len(created_logs)
                    _logger.info(f"Creados {logs_created} nuevos logs de habilidades")
                except Exception as e:
                    _logger.error(f"Error creando logs en lote: {str(e)}")
                    # Intentar crear uno por uno para identificar problemas
                    for vals in skill_to_create_vals:
                        try:
                            self.env['hr.employee.skill.log'].create(vals)
                            logs_created += 1
                        except Exception as individual_error:
                            _logger.error(f"Error creando log individual para empleado {vals.get('employee_id')}: {str(individual_error)}")
            
            _logger.info(f"Proceso de logging completado: {logs_created} logs creados, {logs_updated} logs actualizados")
            
        except Exception as e:
            _logger.error(f"Error crítico en _create_logs: {str(e)}")
            raise
    
    def generate_skill_change_report(self, date_from=None, date_to=None):
        """Generar reporte de cambios de habilidades en un período"""
        try:
            if not date_from:
                date_from = fields.Date.today() - timedelta(days=30)
            if not date_to:
                date_to = fields.Date.today()
                
            _logger.info(f"Generando reporte de cambios de habilidades desde {date_from} hasta {date_to}")
            
            # Buscar logs en el período especificado
            skill_logs = self.env['hr.employee.skill.log'].search([
                ('employee_id', 'in', self.employee_id.ids),
                ('date', '>=', date_from),
                ('date', '<=', date_to)
            ], order='date desc, employee_id')
            
            if not skill_logs:
                _logger.info("No se encontraron cambios de habilidades en el período especificado")
                return []
            
            # Agrupar por tipo de cambio
            changes_by_type = defaultdict(list)
            for log in skill_logs:
                changes_by_type[log.change_type or 'improved'].append({
                    'employee': log.employee_id.name,
                    'skill': log.skill_id.name,
                    'skill_type': log.skill_type_id.name if log.skill_type_id else 'Sin tipo',
                    'old_progress': log.old_level_progress,
                    'new_progress': log.new_level_progress,
                    'date': log.date,
                    'notes': log.notes
                })
            
            _logger.info(f"Reporte generado: {len(skill_logs)} cambios encontrados")
            return dict(changes_by_type)
            
        except Exception as e:
            _logger.error(f"Error generando reporte de cambios: {str(e)}")
            return {}
    
    def get_skill_statistics(self):
        """Obtener estadísticas de habilidades del empleado"""
        try:
            if not self.employee_id:
                _logger.warning("get_skill_statistics llamado sin empleado")
                return {}
            
            employee_skills = self.env['hr.employee.skill'].search([
                ('employee_id', '=', self.employee_id.id)
            ])
            
            if not employee_skills:
                return {
                    'total_skills': 0,
                    'certified_skills': 0,
                    'skills_by_type': {},
                    'average_level': 0
                }
            
            # Calcular estadísticas
            total_skills = len(employee_skills)
            certified_skills = len(employee_skills.filtered('is_certified'))
            
            # Agrupar por tipo de habilidad
            skills_by_type = defaultdict(int)
            total_progress = 0
            
            for skill in employee_skills:
                if skill.skill_type_id:
                    skills_by_type[skill.skill_type_id.name] += 1
                else:
                    skills_by_type['Sin tipo'] += 1
                total_progress += skill.skill_level_id.level_progress if skill.skill_level_id else 0
            
            average_level = total_progress / total_skills if total_skills > 0 else 0
            
            statistics = {
                'employee_name': self.employee_id.name,
                'total_skills': total_skills,
                'certified_skills': certified_skills,
                'certification_rate': (certified_skills / total_skills * 100) if total_skills > 0 else 0,
                'skills_by_type': dict(skills_by_type),
                'average_level': round(average_level, 2)
            }
            
            _logger.debug(f"Estadísticas generadas para {self.employee_id.name}: {statistics}")
            return statistics
            
        except Exception as e:
            _logger.error(f"Error obteniendo estadísticas de habilidades: {str(e)}")
            return {}
    
    def cleanup_old_logs(self, days_to_keep=365):
        """Limpiar logs antiguos para mantener rendimiento"""
        try:
            cutoff_date = fields.Date.today() - timedelta(days=days_to_keep)
            _logger.info(f"Iniciando limpieza de logs anteriores a {cutoff_date}")
            
            old_logs = self.env['hr.employee.skill.log'].search([
                ('date', '<', cutoff_date)
            ])
            
            if old_logs:
                count = len(old_logs)
                old_logs.unlink()
                _logger.info(f"Eliminados {count} logs antiguos")
                return count
            else:
                _logger.info("No se encontraron logs antiguos para eliminar")
                return 0
                
        except Exception as e:
            _logger.error(f"Error limpiando logs antiguos: {str(e)}")
            return 0

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
    
    old_level_progress = fields.Integer(
        string='Progreso Anterior',
        help='Nivel de progreso anterior'
    )
    
    new_level_progress = fields.Integer(
        string='Nuevo Progreso',
        help='Nuevo nivel de progreso'
    )
    
    change_type = fields.Selection([
        ('acquired', 'Adquirida'),
        ('improved', 'Mejorada'),
        ('certified', 'Certificada'),
        ('expired', 'Expirada')
    ], string='Tipo de Cambio', help='Tipo de cambio en la habilidad')
    
    notes = fields.Text(
        string='Notas',
        help='Observaciones sobre el cambio'
    )
    
    date = fields.Date(
        string='Fecha',
        default=fields.Date.context_today
    )

    _sql_constraints = [
        ('_unique_skill_log', 'unique (employee_id, department_id, skill_id, date)', 
         'No se permiten dos niveles para la misma habilidad en el mismo día.')
    ]