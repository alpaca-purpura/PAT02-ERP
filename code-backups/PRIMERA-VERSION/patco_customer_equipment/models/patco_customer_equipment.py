# -*- coding: utf-8 -*-

import base64
import io
import logging
import qrcode
from PIL import Image

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MaintenanceEquipment(models.Model):
    """Extensión del modelo maintenance.equipment para funcionalidades PATCO."""
    
    _inherit = 'maintenance.equipment'
    
    # Campos adicionales específicos de PATCO
    x_patco_code = fields.Char(
        string='Código PATCO',
        copy=False,
        readonly=True,
        default=lambda self: _('Nuevo'),
        tracking=True,
        help='Código único PATCO del equipo'
    )
    
    # Información del cliente y ubicación (usando campos existentes de maintenance.equipment)
    # partner_id ya existe en maintenance.equipment como 'company_id'
    # Agregamos campo específico para cliente
    x_customer_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        tracking=True,
        help='Cliente propietario del equipo'
    )
    
    x_service_location_id = fields.Many2one(
        'res.partner',
        string='Ubicación de Servicio',
        tracking=True,
        help='Ubicación donde se encuentra el equipo para servicios'
    )
    
    # Código QR
    x_qr_code = fields.Binary(
        string='Código QR',
        readonly=True,
        help='Código QR generado automáticamente para el equipo'
    )
    
    x_qr_url = fields.Char(
        string='URL del QR',
        readonly=True,
        help='URL contenida en el código QR'
    )
    
    # Relaciones con servicios
    x_service_order_ids = fields.One2many(
        'fsm.order',
        'x_equipment_id',
        string='Órdenes de Servicio',
        help='Órdenes de servicio relacionadas con este equipo'
    )
    
    x_helpdesk_ticket_ids = fields.One2many(
        'helpdesk.ticket',
        'x_equipment_id',
        string='Tickets de Soporte',
        help='Tickets de soporte relacionados con este equipo'
    )
    
    # Sobrescribir el campo state para usar los estados correctos
    maintenance_state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activo'),
        ('maintenance', 'En Mantenimiento'),
        ('retired', 'Retirado')
    ], string='Estado PATCO', default='draft', tracking=True)
    
    # Campos computados
    x_service_count = fields.Integer(
        string='Servicios',
        compute='_compute_service_count',
        store=True,
        help='Número total de servicios realizados'
    )
    
    x_ticket_count = fields.Integer(
        string='Tickets',
        compute='_compute_ticket_count',
        store=True,
        help='Número total de tickets de soporte'
    )
    
    x_last_service_date = fields.Datetime(
        string='Último Servicio',
        compute='_compute_last_service_date',
        help='Fecha del último servicio realizado'
    )
    
    # Campo de descripción
    description = fields.Text(
        string='Descripción',
        help='Descripción detallada del equipo'
    )
    
    @api.model
    def create(self, vals):
        """Sobrescribir create para generar código PATCO y QR automáticamente."""
        if vals.get('x_patco_code', _('Nuevo')) == _('Nuevo'):
            vals['x_patco_code'] = self.env['ir.sequence'].next_by_code('maintenance.equipment.patco') or _('Nuevo')
        
        equipment = super().create(vals)
        equipment._generate_qr_code()
        return equipment
    
    def write(self, vals):
        """Sobrescribir write para regenerar QR si cambian datos relevantes."""
        result = super().write(vals)
        
        # Regenerar QR si cambian campos relevantes
        qr_fields = ['name', 'x_patco_code', 'x_customer_id', 'x_service_location_id']
        if any(field in vals for field in qr_fields):
            self._generate_qr_code()
        
        return result
    
    def _generate_qr_code(self):
        """Generar código QR con URL única para el equipo."""
        for record in self:
            try:
                # Construir URL del equipo
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                equipment_url = f"{base_url}/web#id={record.id}&model=maintenance.equipment&view_type=form"
                
                # Generar código QR
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(equipment_url)
                qr.make(fit=True)
                
                # Crear imagen
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Convertir a bytes
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                qr_image = base64.b64encode(buffer.getvalue())
                
                # Actualizar campos
                record.sudo().write({
                    'x_qr_code': qr_image,
                    'x_qr_url': equipment_url
                })
                
                _logger.info("Código QR generado para equipo %s", record.x_patco_code)
                
            except Exception as e:
                _logger.error("Error generando código QR para equipo %s: %s", record.x_patco_code, str(e))
    
    @api.depends('x_service_order_ids')
    def _compute_service_count(self):
        """Calcular el número total de órdenes de servicio."""
        for record in self:
            record.x_service_count = len(record.x_service_order_ids)
    
    @api.depends('x_helpdesk_ticket_ids')
    def _compute_ticket_count(self):
        """Calcular el número total de tickets de soporte."""
        for record in self:
            record.x_ticket_count = len(record.x_helpdesk_ticket_ids)
    
    @api.depends('x_service_order_ids.date_start', 'x_helpdesk_ticket_ids.create_date')
    def _compute_last_service_date(self):
        """Calcular la fecha del último servicio."""
        for record in self:
            dates = []
            
            # Fechas de órdenes de servicio
            if record.x_service_order_ids:
                service_dates = record.x_service_order_ids.mapped('date_start')
                dates.extend([d for d in service_dates if d])
            
            # Fechas de tickets
            if record.x_helpdesk_ticket_ids:
                ticket_dates = record.x_helpdesk_ticket_ids.mapped('create_date')
                dates.extend([d for d in ticket_dates if d])
            
            record.x_last_service_date = max(dates) if dates else False
    
    @api.constrains('serial_no', 'x_customer_id')
    def _check_unique_serial_per_customer(self):
        """Validar que el número de serie sea único por cliente."""
        for record in self:
            if record.serial_no and record.x_customer_id:
                existing = self.search([
                    ('id', '!=', record.id),
                    ('serial_no', '=', record.serial_no),
                    ('x_customer_id', '=', record.x_customer_id.id)
                ])
                if existing:
                    raise ValidationError(
                        _("Ya existe un equipo con el número de serie '%s' para el cliente '%s'.") % 
                        (record.serial_no, record.x_customer_id.name)
                    )
    
    def action_activate(self):
        """Activar el equipo."""
        self.write({'maintenance_state': 'active'})
        return True
    
    def action_maintenance(self):
        """Poner el equipo en mantenimiento."""
        self.write({'maintenance_state': 'maintenance'})
        return True
    
    def action_retire(self):
        """Retirar el equipo."""
        self.write({'maintenance_state': 'retired'})
        return True
    
    def action_view_service_orders(self):
        """Abrir vista de servicios relacionados."""
        self.ensure_one()
        
        # Combinar IDs de órdenes de servicio y tickets
        service_ids = self.x_service_order_ids.ids
        ticket_ids = self.x_helpdesk_ticket_ids.ids
        
        if service_ids and ticket_ids:
            # Si hay ambos tipos, mostrar un wizard o vista combinada
            return {
                'name': _('Órdenes de Servicio'),
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': 'fsm.order',
                'domain': [('id', 'in', service_ids)],
                'context': {'default_x_equipment_id': self.id}
            }
        elif service_ids:
            return {
                'name': _('Órdenes de Servicio'),
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': 'fsm.order',
                'domain': [('id', 'in', service_ids)],
                'context': {'default_x_equipment_id': self.id}
            }
        elif ticket_ids:
            return {
                'name': _('Tickets de Soporte'),
                'type': 'ir.actions.act_window',
                'view_mode': 'list,form',
                'res_model': 'helpdesk.ticket',
                'domain': [('id', 'in', ticket_ids)],
                'context': {'default_x_equipment_id': self.id}
            }
        else:
            return {
                'name': _('Sin Servicios'),
                'type': 'ir.actions.act_window',
                'view_mode': 'list',
                'res_model': 'fsm.order',
                'domain': [('id', 'in', [])],
                'context': {'default_x_equipment_id': self.id}
            }
    
    def action_view_helpdesk_tickets(self):
        """Abrir vista de tickets de soporte relacionados."""
        self.ensure_one()
        
        ticket_ids = self.x_helpdesk_ticket_ids.ids
        
        return {
            'name': _('Tickets de Soporte'),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'helpdesk.ticket',
            'domain': [('id', 'in', ticket_ids)],
            'context': {'default_x_equipment_id': self.id}
        }
    
    def regenerate_qr_code(self):
        """Acción manual para regenerar código QR."""
        self._generate_qr_code()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Código QR Regenerado'),
                'message': _('El código QR ha sido regenerado exitosamente.'),
                'type': 'success',
            }
        }