# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockTransferRequest(models.Model):
    _name = 'stock.transfer.request'
    _description = 'Solicitud de Transferencia de Stock a Vehículo'
    _order = 'date desc, id desc'
    _rec_name = 'display_name'
    
    display_name = fields.Char(
        string='Nombre',
        compute='_compute_display_name',
        store=True
    )
    
    date = fields.Datetime(
        string='Fecha de Solicitud',
        default=fields.Datetime.now,
        required=True
    )
    
    technician_id = fields.Many2one(
        'res.partner',
        string='Técnico',
        required=True,
        domain="[('is_company', '=', False), ('supplier_rank', '=', 0)]"
    )
    
    vehicle_location_id = fields.Many2one(
        'stock.location',
        string='Ubicación del Vehículo',
        required=True,
        domain="[('is_vehicle_location', '=', True)]"
    )
    
    source_location_id = fields.Many2one(
        'stock.location',
        string='Ubicación de Origen',
        required=True,
        default=lambda self: self._get_default_source_location()
    )
    
    line_ids = fields.One2many(
        'stock.transfer.request.line',
        'request_id',
        string='Productos a Transferir'
    )
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('partial', 'Parcialmente Transferido'),
        ('done', 'Completado'),
        ('cancel', 'Cancelado')
    ], string='Estado', default='draft', required=True)
    
    picking_ids = fields.One2many(
        'stock.picking',
        'x_transfer_request_id',
        string='Transferencias Generadas'
    )
    
    picking_count = fields.Integer(
        string='Número de Transferencias',
        compute='_compute_picking_count'
    )
    
    notes = fields.Text(string='Notas')
    
    @api.depends('technician_id', 'date')
    def _compute_display_name(self):
        """Calcula el nombre de visualización"""
        for record in self:
            if record.technician_id and record.date:
                date_str = record.date.strftime('%Y-%m-%d')
                record.display_name = f'Transferencia {record.technician_id.name} - {date_str}'
            else:
                record.display_name = 'Nueva Transferencia'
    
    @api.depends('picking_ids')
    def _compute_picking_count(self):
        """Calcula el número de transferencias"""
        for record in self:
            record.picking_count = len(record.picking_ids)
    
    def _get_default_source_location(self):
        """Obtiene la ubicación de origen por defecto (Stock Central)"""
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=1)
        if warehouse:
            return warehouse.lot_stock_id.id
        return False
    
    @api.onchange('technician_id')
    def _onchange_technician_id(self):
        """Actualiza la ubicación del vehículo cuando se selecciona un técnico"""
        if self.technician_id:
            vehicle_location = self.env['stock.location'].search([
                ('is_vehicle_location', '=', True),
                ('technician_id', '=', self.technician_id.id)
            ], limit=1)
            if vehicle_location:
                self.vehicle_location_id = vehicle_location.id
            else:
                self.vehicle_location_id = False
        else:
            self.vehicle_location_id = False
    
    def action_confirm(self):
        """Confirma la solicitud de transferencia"""
        for record in self:
            if not record.line_ids:
                raise UserError(_('Debe agregar al menos un producto para transferir.'))
            record.state = 'confirmed'
    
    def action_create_transfer(self):
        """Crea las transferencias de stock"""
        self.ensure_one()
        
        if self.state != 'confirmed':
            raise UserError(_('Solo se pueden crear transferencias desde solicitudes confirmadas.'))
        
        # Crear picking
        picking_vals = {
            'picking_type_id': self._get_picking_type().id,
            'location_id': self.source_location_id.id,
            'location_dest_id': self.vehicle_location_id.id,
            'origin': self.display_name,
            'x_transfer_request_id': self.id,
        }
        
        picking = self.env['stock.picking'].create(picking_vals)
        
        # Crear movimientos de stock
        for line in self.line_ids:
            if line.quantity_to_transfer <= 0:
                continue
            
            move_vals = {
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
                'product_uom_qty': line.quantity_to_transfer,
                'picking_id': picking.id,
                'location_id': self.source_location_id.id,
                'location_dest_id': self.vehicle_location_id.id,
            }
            
            self.env['stock.move'].create(move_vals)
        
        # Confirmar el picking
        picking.action_confirm()
        
        return {
            'name': _('Transferencia de Stock'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'res_id': picking.id,
            'view_mode': 'form',
            'target': 'current',
        }
    
    def _get_picking_type(self):
        """Obtiene el tipo de picking para transferencias internas"""
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=1)
        if warehouse:
            return warehouse.int_type_id
        else:
            return self.env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)
    
    def action_view_pickings(self):
        """Acción para ver las transferencias generadas"""
        self.ensure_one()
        
        if self.picking_count == 1:
            return {
                'name': _('Transferencia de Stock'),
                'type': 'ir.actions.act_window',
                'res_model': 'stock.picking',
                'res_id': self.picking_ids[0].id,
                'view_mode': 'form',
                'target': 'current',
            }
        else:
            return {
                'name': _('Transferencias de Stock'),
                'type': 'ir.actions.act_window',
                'res_model': 'stock.picking',
                'view_mode': 'list,form',
                'domain': [('id', 'in', self.picking_ids.ids)],
                'target': 'current',
            }


class StockTransferRequestLine(models.Model):
    _name = 'stock.transfer.request.line'
    _description = 'Línea de Solicitud de Transferencia'
    _order = 'request_id, sequence, id'
    
    sequence = fields.Integer(string='Secuencia', default=10)
    
    request_id = fields.Many2one(
        'stock.transfer.request',
        string='Solicitud de Transferencia',
        required=True,
        ondelete='cascade'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Producto',
        required=True,
        domain="[('type', '=', 'product')]"
    )
    
    product_uom_id = fields.Many2one(
        'uom.uom',
        string='Unidad de Medida',
        related='product_id.uom_id',
        readonly=True
    )
    
    quantity_requested = fields.Float(
        string='Cantidad Solicitada',
        required=True,
        default=1.0,
        digits='Product Unit of Measure'
    )
    
    quantity_available = fields.Float(
        string='Disponible en Origen',
        compute='_compute_quantity_available',
        digits='Product Unit of Measure'
    )
    
    quantity_to_transfer = fields.Float(
        string='Cantidad a Transferir',
        digits='Product Unit of Measure'
    )
    
    notes = fields.Char(string='Notas')
    
    @api.depends('product_id', 'request_id.source_location_id')
    def _compute_quantity_available(self):
        """Calcula la cantidad disponible en la ubicación de origen"""
        for line in self:
            if line.product_id and line.request_id.source_location_id:
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', line.product_id.id),
                    ('location_id', '=', line.request_id.source_location_id.id)
                ])
                available = sum(quants.mapped('quantity')) - sum(quants.mapped('reserved_quantity'))
                line.quantity_available = max(0, available)
            else:
                line.quantity_available = 0.0
    
    @api.onchange('quantity_requested', 'quantity_available')
    def _onchange_quantity_requested(self):
        """Actualiza la cantidad a transferir basada en la solicitada y disponible"""
        if self.quantity_requested and self.quantity_available:
            self.quantity_to_transfer = min(self.quantity_requested, self.quantity_available)
        else:
            self.quantity_to_transfer = 0.0


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    x_transfer_request_id = fields.Many2one(
        'stock.transfer.request',
        string='Solicitud de Transferencia',
        readonly=True
    )