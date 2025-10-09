# -*- coding: utf-8 -*-
# Copyright 2024 PATCO
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountAnalyticLine(models.Model):
    """Extensión del modelo account.analytic.line para agregar campo order_id."""
    _inherit = 'account.analytic.line'

    fsm_order_id = fields.Many2one(
        'fsm.order',
        string='FSM Order',
        help='Orden de servicio de campo relacionada con esta línea analítica',
        ondelete='cascade',
        index=True
    )