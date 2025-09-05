# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class FSMConsumePartsWizard(models.TransientModel):
    _name = 'fsm.order.consume.parts.wizard'
    _description = 'Wizard para Consumo de Repuestos en FSM'
    
    order_id = fields.Many2one(
        'fsm.order',
        string='Orden de Servicio',
        required=True
    )
    
    location_id = fields.Many2one(
        'stock.location',
        string='Ubicación del Vehículo',
        required=True,
        domain="[('is_vehicle_location', '=', True)]"
    )
    
    line_ids = fields.One2many(
        'fsm.order.consume.parts.wizard.line',
        'wizard_id',
        string='Repuestos a Consumir'
    )
    
    @api.model
    def default_get(self, fields_list):
        """Valores por defecto del wizard"""
        res = super().default_get(fields_list)
        
        if 'order_id' in res and res['order_id']:
            order = self.env['fsm.order'].browse(res['order_id'])
            if order.x_vehicle_location_id:
                res['location_id'] = order.x_vehicle_location_id.id
        
        return res
    
    def action_consume_parts(self):
        """Procesa el consumo de repuestos"""
        self.ensure_one()
        
        if not self.line_ids:
            raise UserError(_('Debe agregar al menos un repuesto para consumir.'))
        
        consumed_parts = []
        for line in self.line_ids:
            if line.quantity <= 0:
                continue
            
            # Verificar stock disponible
            available_qty = self._get_available_quantity(line.product_id, self.location_id)
            if available_qty < line.quantity:
                raise UserError(_(
                    'Stock insuficiente para el producto %s.\n'
                    'Disponible: %s, Solicitado: %s'
                ) % (line.product_id.name, available_qty, line.quantity))
            
            # Crear registro de consumo
            consumed_part_vals = {
                'order_id': self.order_id.id,
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'location_id': self.location_id.id,
                'notes': line.notes,
            }
            
            consumed_part = self.env['fsm.order.consumed.part'].create(consumed_part_vals)
            consumed_part.action_confirm()
            consumed_parts.append(consumed_part.id)
        
        # Retornar acción para ver los repuestos consumidos
        if len(consumed_parts) == 1:
            return {
                'name': _('Repuesto Consumido'),
                'type': 'ir.actions.act_window',
                'res_model': 'fsm.order.consumed.part',
                'res_id': consumed_parts[0],
                'view_mode': 'form',
                'target': 'current',
            }
        else:
            return {
                'name': _('Repuestos Consumidos'),
                'type': 'ir.actions.act_window',
                'res_model': 'fsm.order.consumed.part',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', consumed_parts)],
                'target': 'current',
            }
    
    def _get_available_quantity(self, product, location):
        """Obtiene la cantidad disponible de un producto en una ubicación"""
        quants = self.env['stock.quant'].search([
            ('product_id', '=', product.id),
            ('location_id', '=', location.id)
        ])
        return sum(quants.mapped('quantity')) - sum(quants.mapped('reserved_quantity'))


class FSMConsumePartsWizardLine(models.TransientModel):
    _name = 'fsm.order.consume.parts.wizard.line'
    _description = 'Línea del Wizard de Consumo de Repuestos'
    
    wizard_id = fields.Many2one(
        'fsm.order.consume.parts.wizard',
        string='Wizard',
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
    
    available_qty = fields.Float(
        string='Disponible',
        compute='_compute_available_qty',
        digits='Product Unit of Measure'
    )
    
    unit_cost = fields.Float(
        string='Costo Unitario',
        related='product_id.standard_price',
        readonly=True
    )
    
    total_cost = fields.Float(
        string='Costo Total',
        compute='_compute_total_cost',
        digits='Product Price'
    )
    
    notes = fields.Char(string='Notas')
    
    @api.depends('product_id', 'wizard_id.location_id')
    def _compute_available_qty(self):
        """Calcula la cantidad disponible del producto en la ubicación"""
        for line in self:
            if line.product_id and line.wizard_id.location_id:
                line.available_qty = line.wizard_id._get_available_quantity(
                    line.product_id, line.wizard_id.location_id
                )
            else:
                line.available_qty = 0.0
    
    @api.depends('quantity', 'unit_cost')
    def _compute_total_cost(self):
        """Calcula el costo total"""
        for line in self:
            line.total_cost = line.quantity * line.unit_cost