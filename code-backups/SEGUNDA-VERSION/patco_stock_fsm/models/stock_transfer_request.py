# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date

import logging
_logger = logging.getLogger(__name__)


class StockTransferRequest(models.Model):
    """Modelo para gestionar solicitudes de transferencia de stock a vehículos."""
    _name = 'stock.transfer.request'
    _description = 'Solicitud de Transferencia de Stock'
    _order = 'date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Número',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('Nuevo')
    )
    
    date = fields.Datetime(
        string='Fecha de Solicitud',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )
    
    technician_id = fields.Many2one(
        'res.partner',
        string='Técnico Solicitante',
        required=True,
        domain=[('is_company', '=', False)],
        tracking=True
    )
    
    vehicle_location_id = fields.Many2one(
        'stock.location',
        string='Ubicación del Vehículo',
        required=True,
        domain=[('is_vehicle_location', '=', True), ('active', '=', True)],
        tracking=True
    )
    
    source_location_id = fields.Many2one(
        'stock.location',
        string='Ubicación de Origen',
        required=True,
        default=lambda self: self.env.ref('stock.stock_location_stock', raise_if_not_found=False),
        domain=[('usage', '=', 'internal')]
    )
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('done', 'Completado'),
        ('cancelled', 'Cancelado')
    ], string='Estado', default='draft', tracking=True)
    
    line_ids = fields.One2many(
        'stock.transfer.request.line',
        'request_id',
        string='Líneas de Transferencia'
    )
    
    picking_ids = fields.One2many(
        'stock.picking',
        'x_transfer_request_id',
        string='Transferencias Generadas'
    )
    
    picking_count = fields.Integer(
        string='Número de Transferencias',
        compute='_compute_picking_count'
    )
    
    notes = fields.Text(
        string='Notas'
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        required=True,
        default=lambda self: self.env.company
    )

    @api.depends('picking_ids')
    def _compute_picking_count(self):
        """Calcula el número de transferencias generadas."""
        for request in self:
            request.picking_count = len(request.picking_ids)

    @api.model
    def create(self, vals):
        """Genera secuencia automática al crear."""
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.transfer.request') or _('Nuevo')
        return super().create(vals)

    def action_confirm(self):
        """Confirma la solicitud de transferencia."""
        for request in self:
            if not request.line_ids:
                raise UserError(_('No se puede confirmar una solicitud sin líneas de productos.'))
            
            # Validar disponibilidad de stock
            for line in request.line_ids:
                if line.quantity_to_transfer > line.quantity_available:
                    raise UserError(
                        _('No hay suficiente stock disponible para el producto %s. '
                          'Disponible: %s, Solicitado: %s') % 
                        (line.product_id.name, line.quantity_available, line.quantity_to_transfer)
                    )
            
            request.state = 'confirmed'
            request.message_post(body=_('Solicitud confirmada'))

    def action_create_transfer(self):
        """Crea las transferencias de stock correspondientes."""
        for request in self:
            if request.state != 'confirmed':
                raise UserError(_('Solo se pueden crear transferencias para solicitudes confirmadas.'))
            
            # Crear picking
            picking_vals = {
                'picking_type_id': self._get_picking_type().id,
                'location_id': request.source_location_id.id,
                'location_dest_id': request.vehicle_location_id.id,
                'origin': request.name,
                'x_transfer_request_id': request.id,
                'company_id': request.company_id.id,
            }
            
            picking = self.env['stock.picking'].create(picking_vals)
            
            # Crear líneas de movimiento
            for line in request.line_ids.filtered(lambda l: l.quantity_to_transfer > 0):
                move_vals = {
                    'name': line.product_id.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity_to_transfer,
                    'product_uom': line.product_uom_id.id,
                    'picking_id': picking.id,
                    'location_id': request.source_location_id.id,
                    'location_dest_id': request.vehicle_location_id.id,
                    'company_id': request.company_id.id,
                }
                self.env['stock.move'].create(move_vals)
            
            # Confirmar el picking
            picking.action_confirm()
            picking.action_assign()
            
            request.state = 'done'
            request.message_post(
                body=_('Transferencia creada: %s') % picking.name
            )

    def action_cancel(self):
        """Cancela la solicitud de transferencia."""
        for request in self:
            if request.state == 'done':
                raise UserError(_('No se puede cancelar una solicitud completada.'))
            request.state = 'cancelled'
            request.message_post(body=_('Solicitud cancelada'))

    def action_view_pickings(self):
        """Abre la vista de las transferencias generadas."""
        self.ensure_one()
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        
        if len(self.picking_ids) > 1:
            action['domain'] = [('id', 'in', self.picking_ids.ids)]
        elif len(self.picking_ids) == 1:
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = self.picking_ids.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        
        return action

    def _get_picking_type(self):
        """Obtiene el tipo de picking para transferencias internas."""
        picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'internal'),
            ('company_id', '=', self.company_id.id)
        ], limit=1)
        
        if not picking_type:
            raise UserError(_('No se encontró un tipo de picking para transferencias internas.'))
        
        return picking_type


class StockTransferRequestLine(models.Model):
    """Líneas de solicitud de transferencia de stock."""
    _name = 'stock.transfer.request.line'
    _description = 'Línea de Solicitud de Transferencia'
    _order = 'sequence, id'

    sequence = fields.Integer(
        string='Secuencia',
        default=10
    )
    
    request_id = fields.Many2one(
        'stock.transfer.request',
        string='Solicitud',
        required=True,
        ondelete='cascade'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Producto',
        required=True,
        domain=[('type', 'in', ['product', 'consu'])]
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
        default=1.0
    )
    
    quantity_available = fields.Float(
        string='Cantidad Disponible',
        compute='_compute_quantity_available',
        store=False
    )
    
    quantity_to_transfer = fields.Float(
        string='Cantidad a Transferir',
        required=True,
        default=0.0
    )
    
    notes = fields.Char(
        string='Notas'
    )

    @api.depends('product_id', 'request_id.source_location_id')
    def _compute_quantity_available(self):
        """Calcula la cantidad disponible en la ubicación de origen."""
        for line in self:
            if line.product_id and line.request_id.source_location_id:
                quants = self.env['stock.quant'].search([
                    ('product_id', '=', line.product_id.id),
                    ('location_id', '=', line.request_id.source_location_id.id)
                ])
                line.quantity_available = sum(quants.mapped('quantity'))
            else:
                line.quantity_available = 0.0

    @api.onchange('quantity_requested', 'quantity_available')
    def _onchange_quantity_requested(self):
        """Actualiza la cantidad a transferir basada en la solicitada y disponible."""
        if self.quantity_requested and self.quantity_available:
            self.quantity_to_transfer = min(self.quantity_requested, self.quantity_available)


# Extensión del modelo stock.picking para relacionar con solicitudes
class StockPicking(models.Model):
    """Extensión del modelo stock.picking."""
    _inherit = 'stock.picking'

    x_transfer_request_id = fields.Many2one(
        'stock.transfer.request',
        string='Solicitud de Transferencia',
        readonly=True
    )
    
    fsm_order_id = fields.Many2one(
        'fsm.order',
        string='Orden FSM',
        help='Orden de servicio de campo relacionada con esta transferencia'
    )