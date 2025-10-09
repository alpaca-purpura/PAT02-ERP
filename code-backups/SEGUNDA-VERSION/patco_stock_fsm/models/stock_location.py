# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class StockLocation(models.Model):
    """Extensión del modelo stock.location para gestión de vehículos."""
    _inherit = 'stock.location'

    # Campos específicos para vehículos
    is_vehicle_location = fields.Boolean(
        string='Es Ubicación de Vehículo',
        default=False,
        help='Marca si esta ubicación corresponde a un vehículo de servicio'
    )
    
    technician_id = fields.Many2one(
        'res.partner',
        string='Técnico Asignado',
        domain=[('is_company', '=', False)],
        help='Técnico responsable de este vehículo'
    )
    
    vehicle_code = fields.Char(
        string='Código de Vehículo',
        help='Código único del vehículo (ej: VEH-001)'
    )
    
    max_capacity = fields.Float(
        string='Capacidad Máxima (kg)',
        default=500.0,
        help='Capacidad máxima de carga del vehículo en kilogramos'
    )
    
    current_weight = fields.Float(
        string='Peso Actual (kg)',
        compute='_compute_current_weight',
        store=False,
        help='Peso actual del stock en el vehículo'
    )
    
    capacity_percentage = fields.Float(
        string='Porcentaje de Capacidad',
        compute='_compute_capacity_percentage',
        store=False,
        help='Porcentaje de capacidad utilizada'
    )

    @api.depends('quant_ids', 'quant_ids.quantity')
    def _compute_current_weight(self):
        """Calcula el peso actual basado en los productos almacenados."""
        for location in self:
            total_weight = 0.0
            if location.is_vehicle_location:
                for quant in location.quant_ids:
                    if quant.quantity > 0 and quant.product_id.weight:
                        total_weight += quant.quantity * quant.product_id.weight
            location.current_weight = total_weight

    @api.depends('current_weight', 'max_capacity')
    def _compute_capacity_percentage(self):
        """Calcula el porcentaje de capacidad utilizada."""
        for location in self:
            if location.max_capacity > 0:
                location.capacity_percentage = (location.current_weight / location.max_capacity) * 100
            else:
                location.capacity_percentage = 0.0

    @api.constrains('vehicle_code')
    def _check_vehicle_code_unique(self):
        """Valida que el código de vehículo sea único."""
        for location in self:
            if location.vehicle_code and location.is_vehicle_location:
                existing = self.search([
                    ('vehicle_code', '=', location.vehicle_code),
                    ('is_vehicle_location', '=', True),
                    ('id', '!=', location.id)
                ])
                if existing:
                    raise ValidationError(
                        _("Ya existe un vehículo con el código '%s'. "
                          "Los códigos de vehículo deben ser únicos.") % location.vehicle_code
                    )

    @api.constrains('technician_id')
    def _check_technician_unique(self):
        """Valida que un técnico no esté asignado a múltiples vehículos activos."""
        for location in self:
            if location.technician_id and location.is_vehicle_location and location.active:
                existing = self.search([
                    ('technician_id', '=', location.technician_id.id),
                    ('is_vehicle_location', '=', True),
                    ('active', '=', True),
                    ('id', '!=', location.id)
                ])
                if existing:
                    raise ValidationError(
                        _("El técnico '%s' ya está asignado al vehículo '%s'. "
                          "Un técnico solo puede estar asignado a un vehículo activo.") % 
                        (location.technician_id.name, existing[0].name)
                    )

    def get_available_capacity(self):
        """Retorna la capacidad disponible en kilogramos."""
        self.ensure_one()
        return max(0, self.max_capacity - self.current_weight)

    def can_accommodate_weight(self, weight):
        """Verifica si el vehículo puede acomodar el peso especificado."""
        self.ensure_one()
        return self.get_available_capacity() >= weight

    def get_stock_summary(self):
        """Retorna un resumen del stock actual en el vehículo."""
        self.ensure_one()
        if not self.is_vehicle_location:
            return {}
        
        summary = {}
        for quant in self.quant_ids.filtered(lambda q: q.quantity > 0):
            product = quant.product_id
            summary[product.id] = {
                'product_name': product.name,
                'quantity': quant.quantity,
                'uom': product.uom_id.name,
                'weight': quant.quantity * product.weight if product.weight else 0,
            }
        
        return summary

    @api.model
    def get_vehicle_locations(self):
        """Retorna todas las ubicaciones de vehículos activas."""
        return self.search([
            ('is_vehicle_location', '=', True),
            ('active', '=', True)
        ])

    def name_get(self):
        """Personaliza la visualización del nombre para vehículos."""
        result = []
        for location in self:
            if location.is_vehicle_location and location.vehicle_code:
                name = f"[{location.vehicle_code}] {location.name}"
                if location.technician_id:
                    name += f" - {location.technician_id.name}"
            else:
                name = location.name
            result.append((location.id, name))
        return result