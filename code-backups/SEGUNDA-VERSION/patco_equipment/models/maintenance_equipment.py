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
    
    # Información del cliente y ubicación
    x_customer_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        # domain=[('is_company', '=', True)],
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
    
    # Estado personalizado para PATCO
    x_maintenance_state = fields.Selection([
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
    
    x_fsm_order_count = fields.Integer(
        string='Órdenes FSM',
        compute='_compute_fsm_order_count',
        store=True,
        help='Número total de órdenes FSM relacionadas'
    )
    
    x_assigned_technician_count = fields.Integer(
        string='Técnicos Asignados',
        compute='_compute_assigned_technician_count',
        store=True,
        help='Número de técnicos únicos asignados a este activo'
    )
    
    x_multi_asset_order_count = fields.Integer(
        string='Órdenes Multi-Activo',
        compute='_compute_multi_asset_order_count',
        store=True,
        help='Número de órdenes que involucran múltiples activos'
    )
    
    x_last_service_date = fields.Datetime(
        string='Último Servicio',
        compute='_compute_last_service_date',
        help='Fecha del último servicio realizado'
    )
    
    # Información técnica adicional
    x_installation_date = fields.Date(
        string='Fecha de Instalación',
        tracking=True,
        help='Fecha de instalación del equipo'
    )
    
    x_warranty_expiry = fields.Date(
        string='Vencimiento de Garantía',
        tracking=True,
        help='Fecha de vencimiento de la garantía'
    )
    
    x_technical_specs = fields.Text(
        string='Especificaciones Técnicas',
        help='Especificaciones técnicas detalladas del equipo'
    )
    
    x_operating_conditions = fields.Text(
        string='Condiciones de Operación',
        help='Condiciones ambientales y operativas del equipo'
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
    
    @api.depends('x_service_order_ids')
    def _compute_fsm_order_count(self):
        """Calcular el número total de órdenes FSM relacionadas."""
        for record in self:
            # Contar todas las órdenes FSM relacionadas con este equipo
            record.x_fsm_order_count = len(record.x_service_order_ids)
    
    @api.depends('x_service_order_ids', 'x_service_order_ids.person_id')
    def _compute_assigned_technician_count(self):
        """Calcular el número de técnicos únicos asignados a este activo."""
        for record in self:
            # Obtener todos los técnicos únicos de todas las órdenes
            technician_ids = set()
            service_orders = record.x_service_order_ids if record.x_service_order_ids else self.env['fsm.order']
            for order in service_orders:
                # Agregar técnicos del equipo
                team_technicians = order.x_team_technician_ids if hasattr(order, 'x_team_technician_ids') and order.x_team_technician_ids else self.env['res.partner']
                if team_technicians:
                    technician_ids.update(team_technicians.ids)
                # Agregar técnico líder
                if hasattr(order, 'x_lead_technician_id') and order.x_lead_technician_id:
                    technician_ids.add(order.x_lead_technician_id.id)
                # Agregar técnico principal (campo estándar FSM)
                if hasattr(order, 'person_id') and order.person_id:
                    technician_ids.add(order.person_id.id)
            record.x_assigned_technician_count = len(technician_ids)
    
    @api.depends('x_service_order_ids')
    def _compute_multi_asset_order_count(self):
        """Calcular el número de órdenes que involucran múltiples activos."""
        for record in self:
            # Contar órdenes que tienen más de un activo asignado
            multi_asset_count = 0
            service_orders = record.x_service_order_ids if record.x_service_order_ids else self.env['fsm.order']
            for order in service_orders:
                multiple_assets = order.x_multiple_assets_ids if hasattr(order, 'x_multiple_assets_ids') and order.x_multiple_assets_ids else self.env['maintenance.equipment']
                if len(multiple_assets) > 1:
                    multi_asset_count += 1
            record.x_multi_asset_order_count = multi_asset_count
    
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
    
    def action_view_fsm_orders(self):
        """Abrir vista de órdenes FSM relacionadas."""
        self.ensure_one()
        
        fsm_order_ids = self.x_service_order_ids.ids
        
        return {
            'name': _('Órdenes FSM'),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'fsm.order',
            'domain': [('id', 'in', fsm_order_ids)],
            'context': {'default_x_equipment_id': self.id}
        }
    
    def action_view_assigned_technicians(self):
        """Abrir vista de técnicos asignados a este activo."""
        self.ensure_one()
        
        # Obtener todos los técnicos únicos de todas las órdenes
        technician_ids = set()
        service_orders = self.x_service_order_ids if self.x_service_order_ids else self.env['fsm.order']
        for order in service_orders:
            # Agregar técnicos del equipo
            team_technicians = order.x_team_technician_ids if hasattr(order, 'x_team_technician_ids') and order.x_team_technician_ids else self.env['res.partner']
            if team_technicians:
                technician_ids.update(team_technicians.ids)
            # Agregar técnico líder
            if hasattr(order, 'x_lead_technician_id') and order.x_lead_technician_id:
                technician_ids.add(order.x_lead_technician_id.id)
            # Agregar técnico principal (campo estándar FSM)
            if hasattr(order, 'person_id') and order.person_id:
                technician_ids.add(order.person_id.id)
        
        return {
            'name': _('Técnicos Asignados'),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'res.partner',
            'domain': [('id', 'in', list(technician_ids))],
            'context': {'default_equipment_id': self.id}
        }
    
    def action_view_multi_asset_orders(self):
        """Abrir vista de órdenes que involucran múltiples activos."""
        self.ensure_one()
        
        # Obtener órdenes que tienen más de un activo asignado
        multi_asset_order_ids = []
        service_orders = self.x_service_order_ids if self.x_service_order_ids else self.env['fsm.order']
        for order in service_orders:
            multiple_assets = order.x_multiple_assets_ids if hasattr(order, 'x_multiple_assets_ids') and order.x_multiple_assets_ids else self.env['maintenance.equipment']
            if len(multiple_assets) > 1:
                multi_asset_order_ids.append(order.id)
        
        return {
            'name': _('Órdenes Multi-Activo'),
            'type': 'ir.actions.act_window',
            'view_mode': 'list,form',
            'res_model': 'fsm.order',
            'domain': [('id', 'in', multi_asset_order_ids)],
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
    
    def get_entry_checklist_template(self):
        """Obtener plantilla de checklist de entrada efectiva (con herencia)."""
        self.ensure_one()
        if self.category_id:
            return self.category_id.x_effective_entry_checklist
        return False
    
    def get_exit_checklist_template(self):
        """Obtener plantilla de checklist de salida efectiva (con herencia)."""
        self.ensure_one()
        if self.category_id:
            return self.category_id.x_effective_exit_checklist
        return False
    
    def action_view_category_knowledge_base(self):
        """Ver base de conocimiento de la categoría (incluyendo herencia)."""
        self.ensure_one()
        if not self.category_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Sin Categoría'),
                    'message': _('Este equipo no tiene una categoría asignada.'),
                    'type': 'warning',
                }
            }
        
        return self.category_id.action_view_knowledge_base()
    
    def has_entry_checklist(self):
        """Verificar si el equipo tiene plantilla de checklist de entrada."""
        self.ensure_one()
        return bool(self.get_entry_checklist_template())
    
    def has_exit_checklist(self):
        """Verificar si el equipo tiene plantilla de checklist de salida."""
        self.ensure_one()
        return bool(self.get_exit_checklist_template())
    
    def get_category_hierarchy_info(self):
        """Obtener información de la jerarquía de categorías."""
        self.ensure_one()
        if not self.category_id:
            return {
                'category_name': False,
                'complete_name': False,
                'parent_categories': [],
                'has_inheritance': False
            }
        
        category = self.category_id
        parent_categories = category._get_parent_categories() if hasattr(category, '_get_parent_categories') else []
        
        return {
            'category_name': category.name,
            'complete_name': category.complete_name if hasattr(category, 'complete_name') else category.name,
            'parent_categories': [{'id': p.id, 'name': p.name} for p in parent_categories],
            'has_inheritance': bool(category.x_inherit_checklists or category.x_inherit_knowledge_base) if hasattr(category, 'x_inherit_checklists') else False
        }