# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import re

_logger = logging.getLogger(__name__)


class DiscussChannel(models.Model):
    _inherit = 'discuss.channel'
    
    # Campos computados para información FSM
    fsm_order_id = fields.Many2one(
        'fsm.order',
        string='Orden FSM',
        compute='_compute_fsm_order_info',
        store=False,
        help='Orden FSM asociada al canal IA'
    )
    
    technician_id = fields.Many2one(
        'res.partner',
        string='Técnico',
        compute='_compute_fsm_order_info',
        store=False,
        help='Técnico asignado a la orden FSM'
    )
    
    client_name = fields.Char(
        string='Cliente',
        compute='_compute_fsm_order_info',
        store=False,
        help='Nombre del cliente de la orden FSM'
    )
    
    @api.depends('name')
    def _compute_fsm_order_info(self):
        """Computa información FSM basada en el nombre del canal"""
        for record in self:
            # Inicializar valores por defecto
            record.fsm_order_id = False
            record.technician_id = False
            record.client_name = False
            
            # Solo procesar canales IA
            if not record.name or '🤖 IA -' not in record.name:
                continue
                
            try:
                # Extraer información del nombre del canal
                # Formato esperado: "🤖 IA - FSM-XXXX - Técnico Name"
                pattern = r'🤖 IA - (FSM-\d+) - (.+)'
                match = re.search(pattern, record.name)
                
                if match:
                    fsm_order_name = match.group(1)
                    technician_name = match.group(2)
                    
                    # Buscar la orden FSM
                    fsm_order = self.env['fsm.order'].search([
                        ('name', '=', fsm_order_name)
                    ], limit=1)
                    
                    if fsm_order:
                        record.fsm_order_id = fsm_order.id
                        record.technician_id = fsm_order.person_id.id if fsm_order.person_id else False
                        record.client_name = fsm_order.partner_id.name if fsm_order.partner_id else False
                    else:
                        # Si no se encuentra la orden, buscar por técnico
                        technician = self.env['res.partner'].search([
                            ('name', 'ilike', technician_name),
                            ('is_company', '=', False)
                        ], limit=1)
                        
                        if technician:
                            record.technician_id = technician.id
                            
            except Exception as e:
                _logger.warning(f"Error computando información FSM para canal {record.name}: {e}")
                continue
    
    def action_open_fsm_order(self):
        """Acción para abrir la orden FSM asociada"""
        self.ensure_one()
        if not self.fsm_order_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sin Orden FSM',
                    'message': 'No hay orden FSM asociada a este canal.',
                    'type': 'warning',
                }
            }
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orden FSM',
            'res_model': 'fsm.order',
            'res_id': self.fsm_order_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def action_open_technician(self):
        """Acción para abrir el perfil del técnico"""
        self.ensure_one()
        if not self.technician_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sin Técnico',
                    'message': 'No hay técnico asociado a este canal.',
                    'type': 'warning',
                }
            }
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Técnico',
            'res_model': 'res.partner',
            'res_id': self.technician_id.id,
            'view_mode': 'form',
            'target': 'current',
        }