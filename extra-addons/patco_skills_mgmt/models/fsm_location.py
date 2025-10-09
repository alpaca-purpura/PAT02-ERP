# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FSMLocation(models.Model):
    _inherit = 'fsm.location'

    default_skill_ids = fields.Many2many(
        'hr.skill',
        string='Habilidades por Defecto',
        help='Habilidades que se asignarán por defecto a las órdenes de servicio en esta ubicación'
    )
    skill_notes = fields.Text(
        string='Notas de Habilidades',
        help='Notas adicionales sobre las habilidades requeridas para esta ubicación'
    )