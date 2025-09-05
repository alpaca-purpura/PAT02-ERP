# -*- coding: utf-8 -*-

from odoo import models, fields, api


class FSMOrderConsumedPart(models.Model):
    _name = 'fsm.order.consumed.part'
    _description = 'Repuestos Consumidos en Orden de Servicio'
    _order = 'order_id, sequence, id'
    
    sequence = fields.Integer(string='Secuencia', default=10)
    order_id = fields.Many2one(
        'fsm.order',
        string='Orden de Servicio',
        required=True,
        ondelete='cascade'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Repuesto',
        required=True,
        domain="[('type', '=', 'product')]"
    )
    
    product_uom_id = fields.Many2one(
        'uom.uom',
        string='Unidad de Medida',
        related='product_id.uom_id',
        readonly=True
    )
    
    quantity = fields.Float(
        string='Cantidad',
        required=True,
        default=1.0,
        digits='Product Unit of Measure'
    )
    
    unit_cost = fields.Float(
        string='Costo Unitario',
        compute='_compute_unit_cost',
        store=True
    )
    
    total_cost = fields.Float(
        string='Costo Total',
        compute='_compute_total_cost',
        store=True
    )
    
    location_id = fields.Many2one(
        'stock.location',
        string='Ubicación de Origen',
        required=True
    )
    
    move_id = fields.Many2one(
        'stock.move',
        string='Movimiento de Stock',
        readonly=True,
        help='Movimiento de stock generado para este consumo'
    )
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('done', 'Realizado'),
        ('cancel', 'Cancelado')
    ], string='Estado', default='draft', required=True)
    
    notes = fields.Text(string='Notas')
    
    @api.depends('product_id')
    def _compute_unit_cost(self):
        """Calcula el costo unitario del producto"""
        for record in self:
            if record.product_id:
                record.unit_cost = record.product_id.standard_price
            else:
                record.unit_cost = 0.0
    
    @api.depends('quantity', 'unit_cost')
    def _compute_total_cost(self):
        """Calcula el costo total"""
        for record in self:
            record.total_cost = record.quantity * record.unit_cost
    
    def action_confirm(self):
        """Confirma el consumo y genera el movimiento de stock"""
        for record in self:
            if record.state != 'draft':
                continue
            
            # Crear movimiento de stock
            move_vals = {
                'name': f'Consumo FSM: {record.order_id.name}',
                'product_id': record.product_id.id,
                'product_uom': record.product_uom_id.id,
                'product_uom_qty': record.quantity,
                'location_id': record.location_id.id,
                'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                'origin': record.order_id.name,
                'company_id': record.order_id.company_id.id,
            }
            
            move = self.env['stock.move'].create(move_vals)
            move._action_confirm()
            move._action_assign()
            move.move_line_ids.write({'qty_done': record.quantity})
            move._action_done()
            
            record.write({
                'move_id': move.id,
                'state': 'confirmed'
            })
    
    def action_cancel(self):
        """Cancela el consumo"""
        for record in self:
            if record.move_id and record.move_id.state == 'done':
                # Crear movimiento de devolución
                return_move_vals = {
                    'name': f'Devolución FSM: {record.order_id.name}',
                    'product_id': record.product_id.id,
                    'product_uom': record.product_uom_id.id,
                    'product_uom_qty': record.quantity,
                    'location_id': self.env.ref('stock.stock_location_customers').id,
                    'location_dest_id': record.location_id.id,
                    'origin': f'Devolución {record.order_id.name}',
                    'company_id': record.order_id.company_id.id,
                }
                
                return_move = self.env['stock.move'].create(return_move_vals)
                return_move._action_confirm()
                return_move._action_assign()
                return_move.move_line_ids.write({'qty_done': record.quantity})
                return_move._action_done()
            
            record.state = 'cancel'