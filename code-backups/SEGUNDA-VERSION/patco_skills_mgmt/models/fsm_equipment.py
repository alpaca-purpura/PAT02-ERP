# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FSMEquipment(models.Model):
    _inherit = 'fsm.equipment'

    required_skill_ids = fields.Many2many(
        'hr.skill',
        string='Habilidades Requeridas',
        help='Habilidades necesarias para trabajar con este equipo'
    )
    skill_notes = fields.Text(
        string='Notas de Habilidades',
        help='Notas adicionales sobre las habilidades requeridas para este equipo'
    )