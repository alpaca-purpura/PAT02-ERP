# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    """Extensión del modelo res.partner para funcionalidades FSM"""
    
    _inherit = 'res.partner'
    
    # Campo para identificar técnicos
    x_is_technician = fields.Boolean(
        string='Es Técnico',
        default=False,
        help='Indica si este contacto es un técnico de servicio de campo'
    )
    
    # Campos FSM existentes (documentados en las vistas)
    fsm_location = fields.Boolean(
        string='Es Ubicación FSM',
        default=False,
        help='Indica si este contacto también es una ubicación de servicio'
    )
    
    service_location_id = fields.Many2one(
        'res.partner',
        string='Ubicación de Servicio Principal',
        domain=[('fsm_location', '=', True)],
        help='Ubicación principal donde se realizan los servicios para este cliente'
    )
    
    # El campo owned_location_ids ya está definido en los módulos OCA fieldservice
    # No necesitamos redefinirlo aquí ya que causa conflictos
    # owned_location_ids = fields.One2many(
    #     'fsm.location',
    #     'owner_id',
    #     string='Owned Locations',
    #     domain=[('fsm_parent_id', '=', False)],
    # )