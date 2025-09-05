# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockLocation(models.Model):
    _inherit = 'stock.location'
    
    # Campo para identificar ubicaciones de vehículos/técnicos
    is_vehicle_location = fields.Boolean(
        string='Es Ubicación de Vehículo',
        default=False,
        help='Marca esta ubicación como específica para un vehículo o técnico'
    )
    
    # Relación con el técnico/empleado responsable
    technician_id = fields.Many2one(
        'hr.employee',
        string='Técnico Responsable',
        help='Técnico asignado a esta ubicación de vehículo'
    )
    
    # Código del vehículo
    vehicle_code = fields.Char(
        string='Código de Vehículo',
        help='Código identificador del vehículo'
    )
    
    # Capacidad máxima de stock
    max_capacity = fields.Float(
        string='Capacidad Máxima',
        help='Capacidad máxima de stock en esta ubicación'
    )
    
    @api.model
    def create_vehicle_location(self, technician_id, vehicle_code):
        """Método para crear ubicaciones de vehículo automáticamente"""
        # Buscar ubicación padre para vehículos
        parent_location = self.env.ref('stock.stock_location_locations', raise_if_not_found=False)
        if not parent_location:
            parent_location = self.env['stock.location'].search([('usage', '=', 'internal')], limit=1)
        
        technician = self.env['hr.employee'].browse(technician_id)
        location_name = f"Vehículo - {technician.name} ({vehicle_code})"
        
        # Verificar si ya existe
        existing = self.search([
            ('technician_id', '=', technician_id),
            ('vehicle_code', '=', vehicle_code),
            ('is_vehicle_location', '=', True)
        ])
        
        if existing:
            return existing[0]
        
        return self.create({
            'name': location_name,
            'location_id': parent_location.id,
            'usage': 'internal',
            'is_vehicle_location': True,
            'technician_id': technician_id,
            'vehicle_code': vehicle_code,
            'max_capacity': 100.0,  # Capacidad por defecto
        })
    
    @api.constrains('technician_id', 'vehicle_code')
    def _check_unique_vehicle_location(self):
        """Validar que no haya ubicaciones duplicadas por técnico/vehículo"""
        for record in self:
            if record.is_vehicle_location and record.technician_id and record.vehicle_code:
                existing = self.search([
                    ('id', '!=', record.id),
                    ('technician_id', '=', record.technician_id.id),
                    ('vehicle_code', '=', record.vehicle_code),
                    ('is_vehicle_location', '=', True)
                ])
                if existing:
                    raise models.ValidationError(
                        f"Ya existe una ubicación para el técnico {record.technician_id.name} "
                        f"y vehículo {record.vehicle_code}"
                    )