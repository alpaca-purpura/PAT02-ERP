# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class FsmOrder(models.Model):
    """Extensión del modelo fsm.order para integración con habilidades técnicas"""
    _inherit = 'fsm.order'

    # Habilidades requeridas para la orden
    required_skill_ids = fields.Many2many(
        'hr.skill',
        'fsm_order_skill_rel',
        'order_id',
        'skill_id',
        string='Habilidades Requeridas',
        help='Habilidades técnicas necesarias para completar esta orden'
    )
    
    required_skill_types = fields.Many2many(
        'hr.skill.type',
        'fsm_order_skill_type_rel',
        'order_id',
        'skill_type_id',
        string='Tipos de Habilidades Requeridas',
        help='Tipos de habilidades técnicas necesarias'
    )
    
    # Nivel mínimo requerido
    min_skill_level = fields.Integer(
        string='Nivel Mínimo Requerido',
        default=1,
        help='Nivel mínimo de competencia requerido (1-10)'
    )
    
    # Campos computados para análisis de competencias
    technician_skill_match = fields.Float(
        string='Compatibilidad de Habilidades (%)',
        compute='_compute_skill_match',
        store=True,
        help='Porcentaje de compatibilidad entre habilidades requeridas y del técnico'
    )
    
    missing_skills = fields.Text(
        string='Habilidades Faltantes',
        compute='_compute_skill_match',
        store=True,
        help='Lista de habilidades que el técnico no posee'
    )
    
    technician_has_required_skills = fields.Boolean(
        string='Técnico Calificado',
        compute='_compute_skill_match',
        store=True,
        help='Indica si el técnico tiene todas las habilidades requeridas'
    )
    
    # Campos para sugerencias de técnicos
    suggested_technician_ids = fields.Many2many(
        'hr.employee',
        'fsm_order_suggested_technician_rel',
        'order_id',
        'employee_id',
        string='Técnicos Sugeridos',
        compute='_compute_suggested_technicians',
        help='Técnicos sugeridos basados en habilidades requeridas'
    )
    
    # Campo para prioridad basada en habilidades
    skill_priority = fields.Selection([
        ('low', 'Baja - Habilidades Básicas'),
        ('medium', 'Media - Habilidades Intermedias'),
        ('high', 'Alta - Habilidades Avanzadas'),
        ('critical', 'Crítica - Habilidades Especializadas')
    ], string='Prioridad por Habilidades', default='medium',
       help='Prioridad basada en la complejidad de habilidades requeridas')
    
    # Campos de seguimiento de capacitación
    requires_training = fields.Boolean(
        string='Requiere Capacitación',
        default=False,
        help='Indica si el técnico necesita capacitación adicional'
    )
    
    training_notes = fields.Text(
        string='Notas de Capacitación',
        help='Observaciones sobre capacitación necesaria'
    )

    @api.depends('person_id', 'required_skill_ids', 'min_skill_level')
    def _compute_skill_match(self):
        """Computa la compatibilidad de habilidades entre técnico y orden"""
        for order in self:
            # Verificar inicialización de campos many2many
            required_skills = order.required_skill_ids or []
            
            if not order.person_id or not required_skills:
                order.technician_skill_match = 0.0
                order.missing_skills = ''
                order.technician_has_required_skills = False
                continue
            
            technician = order.person_id
            min_level = order.min_skill_level or 1
            
            # Obtener habilidades del técnico
            technician_skills = technician.employee_skill_ids
            
            matched_skills = 0
            missing_skills_list = []
            
            for required_skill in required_skills:
                # Buscar si el técnico tiene esta habilidad
                tech_skill = technician_skills.filtered(
                    lambda s: s.skill_id.id == required_skill.id
                )
                
                if tech_skill and tech_skill.level_progress >= min_level:
                    matched_skills += 1
                else:
                    if tech_skill:
                        missing_skills_list.append(
                            f"{required_skill.name} (Nivel actual: {tech_skill.level_progress}, Requerido: {min_level})"
                        )
                    else:
                        missing_skills_list.append(
                            f"{required_skill.name} (No posee la habilidad)"
                        )
            
            # Calcular porcentaje de compatibilidad
            total_required = len(required_skills)
            if total_required > 0:
                match_percentage = (matched_skills / total_required) * 100
                order.technician_skill_match = match_percentage
                order.technician_has_required_skills = (matched_skills == total_required)
            else:
                order.technician_skill_match = 100.0
                order.technician_has_required_skills = True
            
            order.missing_skills = '\n'.join(missing_skills_list) if missing_skills_list else ''

    @api.depends('required_skill_ids', 'required_skill_types', 'min_skill_level')
    def _compute_suggested_technicians(self):
        """Calcula técnicos sugeridos basados en habilidades requeridas"""
        for order in self:
            # Verificar inicialización de campos many2many
            required_skills = order.required_skill_ids or []
            required_skill_types = order.required_skill_types or []
            
            if not required_skills and not required_skill_types:
                order.suggested_technician_ids = [(5, 0, 0)]
                continue
            
            # Obtener todos los técnicos disponibles
            technicians = self.env['hr.employee'].search([
                ('is_fsm_technician', '=', True)
            ])
            
            suitable_technicians = []
            min_level = order.min_skill_level or 1
            
            for technician in technicians:
                score = 0
                total_required = 0
                
                # Evaluar habilidades específicas
                if required_skills:
                    total_required += len(required_skills)
                    for required_skill in required_skills:
                        tech_skill = technician.employee_skill_ids.filtered(
                            lambda s: s.skill_id.id == required_skill.id
                        )
                        if tech_skill and tech_skill.level_progress >= min_level:
                            score += tech_skill.level_progress
                
                # Evaluar tipos de habilidades
                if required_skill_types:
                    for skill_type in required_skill_types:
                        type_skills = technician.employee_skill_ids.filtered(
                            lambda s: s.skill_id.skill_type_id.id == skill_type.id and s.level_progress >= min_level
                        )
                        if type_skills:
                            # Tomar la mejor habilidad de este tipo
                            best_skill = max(type_skills, key=lambda s: s.level_progress)
                            score += best_skill.level_progress
                            total_required += 1
                
                # Calcular puntuación promedio
                if score > 0:
                    avg_score = score / max(total_required, 1)
                    suitable_technicians.append((technician.id, avg_score))
            
            # Ordenar por puntuación descendente y tomar los mejores
            suitable_technicians.sort(key=lambda x: x[1], reverse=True)
            top_technicians = [tech_id for tech_id, score in suitable_technicians[:10]]
            
            order.suggested_technician_ids = [(6, 0, top_technicians)]

    @api.constrains('min_skill_level')
    def _check_min_skill_level(self):
        """Valida que el nivel mínimo esté en rango válido"""
        for order in self:
            if order.min_skill_level and not (1 <= order.min_skill_level <= 10):
                raise ValidationError(
                    _("El nivel mínimo de habilidad debe estar entre 1 y 10.")
                )

    @api.onchange('required_skill_types')
    def _onchange_required_skill_types(self):
        """Actualiza habilidades específicas basadas en tipos seleccionados"""
        # Verificar inicialización de campos many2many
        required_skill_types = self.required_skill_types or []
        
        if required_skill_types:
            # Sugerir habilidades específicas de los tipos seleccionados
            skill_domain = [('skill_type_id', 'in', required_skill_types.ids)]
            return {'domain': {'required_skill_ids': skill_domain}}
        else:
            return {'domain': {'required_skill_ids': []}}

    def action_suggest_technicians(self):
        """Acción para abrir wizard de sugerencia de técnicos"""
        self.ensure_one()
        # Verificar inicialización de campos many2many
        required_skills = self.required_skill_ids or []
        
        return {
            'name': 'Sugerir Técnico',
            'type': 'ir.actions.act_window',
            'res_model': 'suggest.technician.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_fsm_order_id': self.id,
                'default_required_skill_ids': [(6, 0, required_skills.ids)],
                'default_min_skill_level': self.min_skill_level
            }
        }

    def action_view_technician_skills(self):
        """Acción para ver las habilidades del técnico asignado"""
        self.ensure_one()
        if not self.person_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'No hay técnico asignado a esta orden.',
                    'type': 'warning'
                }
            }
        
        return {
            'name': f'Habilidades - {self.person_id.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee.skill',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.person_id.id)],
            'context': {
                'search_default_group_by_skill_type': 1
            }
        }

    def validate_technician_skills(self):
        """Valida que el técnico asignado tenga las habilidades requeridas"""
        self.ensure_one()
        
        if not self.person_id:
            return {
                'valid': False,
                'message': 'No hay técnico asignado.',
                'missing_skills': []
            }
        
        # Verificar inicialización de campos many2many
        required_skills = self.required_skill_ids or []
        
        if not required_skills:
            return {
                'valid': True,
                'message': 'No se requieren habilidades específicas.',
                'missing_skills': []
            }
        
        technician = self.person_id
        missing_skills = []
        min_level = self.min_skill_level or 1
        
        for required_skill in required_skills:
            tech_skill = technician.employee_skill_ids.filtered(
                lambda s: s.skill_id.id == required_skill.id
            )
            
            if not tech_skill:
                missing_skills.append({
                    'skill': required_skill.name,
                    'required_level': min_level,
                    'current_level': 0,
                    'status': 'missing'
                })
            elif tech_skill.level_progress < min_level:
                missing_skills.append({
                    'skill': required_skill.name,
                    'required_level': min_level,
                    'current_level': tech_skill.level_progress,
                    'status': 'insufficient'
                })
        
        is_valid = len(missing_skills) == 0
        
        return {
            'valid': is_valid,
            'message': 'Técnico calificado' if is_valid else f'Faltan {len(missing_skills)} habilidades',
            'missing_skills': missing_skills,
            'match_percentage': self.technician_skill_match
        }

    def auto_assign_best_technician(self):
        """Asigna automáticamente el mejor técnico disponible"""
        self.ensure_one()
        
        # Verificar inicialización de campos many2many
        required_skills = self.required_skill_ids or []
        required_skill_types = self.required_skill_types or []
        
        if not required_skills and not required_skill_types:
            return {
                'success': False,
                'message': 'No se han definido habilidades requeridas para la asignación automática.'
            }
        
        # Forzar recálculo de técnicos sugeridos
        self._compute_suggested_technicians()
        
        # Verificar inicialización de suggested_technician_ids
        suggested_technicians = self.suggested_technician_ids or []
        
        if not suggested_technicians:
            return {
                'success': False,
                'message': 'No se encontraron técnicos disponibles con las habilidades requeridas.'
            }
        
        # Asignar el primer técnico sugerido (mejor puntuado)
        best_technician = suggested_technicians[0]
        self.person_id = best_technician
        
        # Recalcular compatibilidad
        self._compute_skill_match()
        
        return {
            'success': True,
            'message': f'Técnico {best_technician.name} asignado automáticamente.',
            'technician_id': best_technician.id,
            'match_percentage': self.technician_skill_match
        }

    @api.model
    def get_orders_by_skill_requirements(self, skill_type_codes=None, min_level=1):
        """Obtiene órdenes que requieren tipos de habilidades específicos
        
        Args:
            skill_type_codes (list): Lista de códigos de tipos de habilidades
            min_level (int): Nivel mínimo requerido
            
        Returns:
            recordset: Órdenes filtradas
        """
        domain = []
        
        if skill_type_codes:
            domain.append(('required_skill_types.code', 'in', skill_type_codes))
        
        if min_level > 1:
            domain.append(('min_skill_level', '>=', min_level))
        
        return self.search(domain)

    def create_skill_training_plan(self):
        """Crea un plan de capacitación basado en habilidades faltantes"""
        self.ensure_one()
        
        if not self.person_id or not self.missing_skills:
            return {
                'success': False,
                'message': 'No hay técnico asignado o no faltan habilidades.'
            }
        
        # Marcar que requiere capacitación
        self.requires_training = True
        
        # Generar notas de capacitación
        training_notes = f"Plan de capacitación para orden {self.name}:\n\n"
        training_notes += "Habilidades a desarrollar:\n"
        training_notes += self.missing_skills
        training_notes += f"\n\nNivel mínimo requerido: {self.min_skill_level}\n"
        training_notes += f"Fecha de generación: {fields.Datetime.now()}\n"
        
        self.training_notes = training_notes
        
        return {
            'success': True,
            'message': 'Plan de capacitación creado exitosamente.',
            'training_notes': training_notes
        }