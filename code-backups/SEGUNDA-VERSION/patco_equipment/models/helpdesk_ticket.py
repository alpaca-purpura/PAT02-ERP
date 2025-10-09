# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HelpdeskTicket(models.Model):
    """Extensión del modelo helpdesk.ticket para relacionar con equipos PATCO."""
    
    _inherit = 'helpdesk.ticket'
    
    x_equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Activo del Cliente',
        tracking=True,
        help='Activo del Cliente relacionado con este ticket de soporte'
    )
    
    x_equipment_code = fields.Char(
        string='Código del Activo',
        related='x_equipment_id.x_patco_code',
        readonly=True,
        store=True,
        help='Código PATCO del activo'
    )
    
    x_customer_equipment = fields.Many2one(
        'res.partner',
        string='Dueño del Activo',
        related='x_equipment_id.x_customer_id',
        readonly=True,
        store=True,
        help='Cliente propietario del activo'
    )
    
    x_equipment_location = fields.Many2one(
        'res.partner',
        string='Ubicación del Activo',
        related='x_equipment_id.x_service_location_id',
        readonly=True,
        store=True,
        help='Ubicación donde se encuentra el activo'
    )
    
    @api.onchange('x_equipment_id')
    def _onchange_equipment_id(self):
        """Actualizar campos relacionados cuando se selecciona un equipo."""
        if self.x_equipment_id:
            # Actualizar cliente si no está definido
            if not self.partner_id and self.x_equipment_id.x_customer_id:
                self.partner_id = self.x_equipment_id.x_customer_id
            
            # Actualizar nombre del ticket con información del equipo
            if not self.name or self.name == _('New'):
                equipment_name = self.x_equipment_id.name or ''
                equipment_code = self.x_equipment_id.x_patco_code or ''
                self.name = f"Soporte - {equipment_name} ({equipment_code})"
    
    x_fsm_order_id = fields.Many2one(
        'fsm.order',
        string='Orden de Servicio FSM',
        help='Orden de Servicio de Campo creada desde este ticket',
        readonly=True
    )
    
    def _get_default_partner_id(self):
        """Obtener cliente por defecto desde el equipo si está definido."""
        if self.x_equipment_id and self.x_equipment_id.x_customer_id:
            return self.x_equipment_id.x_customer_id.id
        return super()._get_default_partner_id()
    
    def action_create_fsm_order(self):
        """Convierte el ticket en una Orden de Servicio de Campo"""
        self.ensure_one()
        
        # Validaciones
        if self.x_fsm_order_id:
            raise UserError('Este ticket ya tiene una Orden de Servicio asociada.')
        
        if not self.x_equipment_id:
            raise UserError('Debe seleccionar un Equipo antes de crear la Orden de Servicio.')
        
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
    
    @api.model
    def create(self, vals):
        """Sobrescribir create para manejar relaciones automáticas."""
        # Si se especifica un equipo, actualizar campos relacionados
        if vals.get('x_equipment_id'):
            equipment = self.env['maintenance.equipment'].browse(vals['x_equipment_id'])
            
            # Actualizar cliente si no está definido
            if not vals.get('partner_id') and equipment.x_customer_id:
                vals['partner_id'] = equipment.x_customer_id.id
            
            # Actualizar nombre del ticket si no está definido
            if not vals.get('name') or vals.get('name') == _('New'):
                equipment_name = equipment.name or ''
                equipment_code = equipment.x_patco_code or ''
                vals['name'] = f"Soporte - {equipment_name} ({equipment_code})"
        
        return super().create(vals)