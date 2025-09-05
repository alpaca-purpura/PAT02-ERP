# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class FsmConsumePartsWizard(models.TransientModel):
    _name = 'fsm.consume.parts.wizard'
    _description = 'Wizard para Consumir Repuestos en Orden de Servicio'

    fsm_order_id = fields.Many2one(
        'fsm.order',
        string='Orden de Servicio',
        required=True,
        readonly=True
    )
    
    technician_id = fields.Many2one(
        'res.partner',
        string='Técnico',
        required=True,
        domain=[('is_company', '=', False)]
    )
    
    vehicle_location_id = fields.Many2one(
        'stock.location',
        string='Ubicación del Vehículo',
        required=True,
        domain=[('usage', '=', 'internal'), ('name', 'ilike', 'Vehículo')]
    )
    
    line_ids = fields.One2many(
        'fsm.consume.parts.wizard.line',
        'wizard_id',
        string='Repuestos a Consumir'
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        
        # Obtener la orden de servicio del contexto
        fsm_order_id = self.env.context.get('active_id')
        if fsm_order_id:
            fsm_order = self.env['fsm.order'].browse(fsm_order_id)
            res['fsm_order_id'] = fsm_order_id
            
            # Si hay un técnico asignado, usarlo por defecto
            if fsm_order.person_id:
                res['technician_id'] = fsm_order.person_id.id
                
                # Buscar la ubicación del vehículo del técnico
                vehicle_location = self.env['stock.location'].search([
                    ('name', 'ilike', f'Vehículo {fsm_order.person_id.name}'),
                    ('usage', '=', 'internal')
                ], limit=1)
                
                if vehicle_location:
                    res['vehicle_location_id'] = vehicle_location.id
        
        return res

    def action_consume_parts(self):
        """Procesar el consumo de repuestos"""
        if not self.line_ids:
            raise UserError(_('Debe agregar al menos un repuesto para consumir.'))
        
        # Crear picking de consumo
        picking_vals = {
            'partner_id': self.technician_id.id,
            'location_id': self.vehicle_location_id.id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'origin': f'Consumo FSM: {self.fsm_order_id.name}',
            'move_type': 'direct',
        }
        
        picking = self.env['stock.picking'].create(picking_vals)
        
        # Crear movimientos de stock para cada línea
        for line in self.line_ids:
            if line.quantity_consumed > 0:
                move_vals = {
                    'name': f'Consumo: {line.product_id.name}',
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity_consumed,
                    'product_uom': line.product_id.uom_id.id,
                    'location_id': self.vehicle_location_id.id,
                    'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                    'picking_id': picking.id,
                    'picking_type_id': picking.picking_type_id.id,
                }
                
                self.env['stock.move'].create(move_vals)
        
        # Confirmar y procesar el picking
        picking.action_confirm()
        picking.action_assign()
        
        # Procesar automáticamente si hay stock disponible
        for move in picking.move_ids:
            if move.state == 'assigned':
                move.quantity_done = move.product_uom_qty
        
        picking.button_validate()
        
        # Registrar el consumo en la orden de servicio
        consumption_note = "Repuestos consumidos:\n"
        for line in self.line_ids:
            if line.quantity_consumed > 0:
                consumption_note += f"- {line.product_id.name}: {line.quantity_consumed} {line.product_id.uom_id.name}\n"
        
        # Agregar nota a la orden
        if self.fsm_order_id.resolution:
            self.fsm_order_id.resolution += f"\n\n{consumption_note}"
        else:
            self.fsm_order_id.resolution = consumption_note
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Consumo Registrado'),
                'message': _('Los repuestos han sido consumidos exitosamente.'),
                'type': 'success',
            }
        }


class FsmConsumePartsWizardLine(models.TransientModel):
    _name = 'fsm.consume.parts.wizard.line'
    _description = 'Línea de Repuestos a Consumir'

    wizard_id = fields.Many2one(
        'fsm.consume.parts.wizard',
        string='Wizard',
        required=True,
        ondelete='cascade'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Repuesto',
        required=True,
        domain=[('type', '=', 'product')]
    )
    
    available_quantity = fields.Float(
        string='Cantidad Disponible',
        compute='_compute_available_quantity',
        readonly=True
    )
    
    quantity_consumed = fields.Float(
        string='Cantidad a Consumir',
        default=1.0
    )
    
    uom_id = fields.Many2one(
        related='product_id.uom_id',
        string='Unidad de Medida',
        readonly=True
    )

    @api.depends('product_id', 'wizard_id.vehicle_location_id')
    def _compute_available_quantity(self):
        for line in self:
            if line.product_id and line.wizard_id.vehicle_location_id:
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', line.product_id.id),
                    ('location_id', '=', line.wizard_id.vehicle_location_id.id)
                ])
                line.available_quantity = sum(quants.mapped('quantity'))
            else:
                line.available_quantity = 0.0

    @api.constrains('quantity_consumed', 'available_quantity')
    def _check_quantity_consumed(self):
        for line in self:
            if line.quantity_consumed > line.available_quantity:
                raise UserError(
                    _('No puede consumir más cantidad (%s) de la disponible (%s) para el producto %s.') %
                    (line.quantity_consumed, line.available_quantity, line.product_id.name)
                )