# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError


class HelpdeskTicket(models.Model):
    """Extensión del modelo helpdesk.ticket para agregar relación con equipos."""
    
    _inherit = 'helpdesk.ticket'
    
    x_equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Equipo',
        tracking=True,
        help='Equipo relacionado con este ticket de soporte'
    )
    
    x_fsm_order_id = fields.Many2one(
        'fsm.order',
        string='Orden de Servicio FSM',
        help='Orden de Servicio de Campo creada desde este ticket',
        readonly=True
    )
    
    def _get_default_partner_id(self):
        """Obtener cliente por defecto desde el equipo si está definido."""
        if self.x_equipment_id and self.x_equipment_id.partner_id:
            return self.x_equipment_id.partner_id.id
        return super()._get_default_partner_id()
    
    def action_create_fsm_order(self):
        """Convierte el ticket en una Orden de Servicio de Campo"""
        self.ensure_one()
        
        # Validaciones
        if self.x_fsm_order_id:
            raise UserError('Este ticket ya tiene una Orden de Servicio asociada.')
        
        if not self.x_equipment_id:
            raise UserError('Debe seleccionar un Activo de Cliente antes de crear la Orden de Servicio.')
        
        if not self.partner_id:
            raise UserError('Debe especificar un cliente para crear la Orden de Servicio.')
        
        # Buscar o crear fsm.location para el partner
        fsm_location = self.env['fsm.location'].search([('partner_id', '=', self.partner_id.id)], limit=1)
        if not fsm_location:
            fsm_location = self.env['fsm.location'].create({
                'partner_id': self.partner_id.id,
                'owner_id': self.partner_id.id,
            })
        
        # Crear la orden FSM
        fsm_order_vals = {
            'name': f"FSM-{self.name}",
            'location_id': fsm_location.id,
            'description': self.description or self.name,
        }
        
        # Agregar el equipo si existe
        if self.x_equipment_id:
            fsm_order_vals['x_equipment_id'] = self.x_equipment_id.id
        
        # Transferir campos de clasificación PATCO si existen
        if hasattr(self, 'x_nature_id') and self.x_nature_id:
            fsm_order_vals['x_nature_id'] = self.x_nature_id.id
        
        if hasattr(self, 'x_area_id') and self.x_area_id:
            fsm_order_vals['x_area_id'] = self.x_area_id.id
            
        if hasattr(self, 'x_complexity_id') and self.x_complexity_id:
            fsm_order_vals['x_complexity_id'] = self.x_complexity_id.id
        
        # Crear la orden FSM
        fsm_order = self.env['fsm.order'].create(fsm_order_vals)
        
        # Vincular el ticket con la orden FSM
        self.write({'x_fsm_order_id': fsm_order.id})
        
        # Retornar acción para abrir la orden FSM creada
        return {
            'type': 'ir.actions.act_window',
            'name': 'Orden de Servicio de Campo',
            'res_model': 'fsm.order',
            'res_id': fsm_order.id,
            'view_mode': 'form',
            'target': 'current',
        }