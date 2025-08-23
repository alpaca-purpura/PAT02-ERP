# -*- coding: utf-8 -*-

from odoo import api, fields, models


class FSMOrder(models.Model):
    """Extensión del modelo fsm.order para agregar relación con equipos."""
    
    _inherit = 'fsm.order'
    
    x_equipment_id = fields.Many2one(
        'patco.customer.equipment',
        string='Equipo',
        tracking=True,
        help='Equipo relacionado con esta orden de servicio'
    )
    
    @api.onchange('x_equipment_id')
    def _onchange_equipment_id(self):
        """Actualizar cliente y ubicación cuando se selecciona un equipo."""
        if self.x_equipment_id:
            # Actualizar cliente
            if self.x_equipment_id.partner_id:
                self.partner_id = self.x_equipment_id.partner_id
            
            # Actualizar ubicación si está definida
            if self.x_equipment_id.location_id:
                self.location_id = self.x_equipment_id.location_id