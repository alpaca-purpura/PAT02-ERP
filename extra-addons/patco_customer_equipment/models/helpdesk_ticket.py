# -*- coding: utf-8 -*-

from odoo import fields, models


class HelpdeskTicket(models.Model):
    """Extensión del modelo helpdesk.ticket para agregar relación con equipos."""
    
    _inherit = 'helpdesk.ticket'
    
    x_equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Equipo',
        tracking=True,
        help='Equipo relacionado con este ticket de soporte'
    )
    
    def _get_default_partner_id(self):
        """Obtener cliente por defecto desde el equipo si está definido."""
        if self.x_equipment_id and self.x_equipment_id.partner_id:
            return self.x_equipment_id.partner_id.id
        return super()._get_default_partner_id()