# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import json
import base64
from datetime import datetime


class FSMWorksheet(models.Model):
    _name = 'fsm.worksheet'
    _description = 'Hoja de Trabajo Digital para Field Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char(
        string='Nombre',
        required=True,
        default=lambda self: _('Nueva Hoja de Trabajo'),
        tracking=True
    )
    
    order_id = fields.Many2one(
        'fsm.order',
        string='Orden de Servicio',
        required=True,
        ondelete='cascade',
        tracking=True
    )
    
    template_id = fields.Many2one(
        'fsm.worksheet.template',
        string='Plantilla',
        required=True,
        tracking=True
    )
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completada'),
        ('signed', 'Firmada'),
        ('cancelled', 'Cancelada')
    ], string='Estado', default='draft', tracking=True)
    
    # Información del técnico
    technician_id = fields.Many2one(
        'res.partner',
        string='Técnico',
        related='order_id.person_id',
        store=True,
        readonly=True
    )
    
    # Información del cliente
    customer_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        related='order_id.location_id.partner_id',
        store=True,
        readonly=True
    )
    
    # Fechas y tiempos
    start_datetime = fields.Datetime(
        string='Fecha/Hora Inicio',
        tracking=True
    )
    
    end_datetime = fields.Datetime(
        string='Fecha/Hora Fin',
        tracking=True
    )
    
    duration = fields.Float(
        string='Duración (horas)',
        compute='_compute_duration',
        store=True
    )
    
    # Contenido de la hoja de trabajo
    worksheet_data = fields.Text(
        string='Datos de la Hoja de Trabajo',
        help='Datos JSON con las respuestas del formulario'
    )
    
    # Firmas digitales
    technician_signature = fields.Binary(
        string='Firma del Técnico',
        attachment=True
    )
    
    technician_signature_date = fields.Datetime(
        string='Fecha Firma Técnico'
    )
    
    customer_signature = fields.Binary(
        string='Firma del Cliente',
        attachment=True
    )
    
    customer_signature_date = fields.Datetime(
        string='Fecha Firma Cliente'
    )
    
    customer_name = fields.Char(
        string='Nombre del Cliente que Firma',
        help='Nombre de la persona que firma por el cliente'
    )
    
    customer_position = fields.Char(
        string='Cargo del Cliente',
        help='Cargo de la persona que firma'
    )
    
    customer_document = fields.Char(
        string='Documento del Cliente',
        help='Número de documento de identidad del cliente'
    )
    
    customer_comments = fields.Text(
        string='Comentarios del Cliente',
        help='Observaciones o comentarios del cliente sobre el servicio'
    )
    
    approval_status = fields.Selection([
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado')
    ], string='Estado de Aprobación', default='pending')
    
    signed_pdf = fields.Binary(
        string='PDF Firmado',
        help='Documento PDF con las firmas del técnico y cliente'
    )
    
    signed_pdf_filename = fields.Char(
        string='Nombre del PDF',
        help='Nombre del archivo PDF firmado'
    )
    
    # Observaciones y notas
    observations = fields.Text(
        string='Observaciones',
        tracking=True
    )
    
    internal_notes = fields.Text(
        string='Notas Internas',
        help='Notas visibles solo para el equipo interno'
    )
    
    # Archivos adjuntos
    attachment_ids = fields.Many2many(
        'ir.attachment',
        string='Archivos Adjuntos',
        help='Fotos, documentos adicionales'
    )
    
    # PDF generado
    pdf_report = fields.Binary(
        string='Reporte PDF',
        attachment=True
    )
    
    pdf_filename = fields.Char(
        string='Nombre del PDF',
        default='worksheet.pdf'
    )
    
    @api.depends('start_datetime', 'end_datetime')
    def _compute_duration(self):
        """Calcula la duración en horas"""
        for record in self:
            if record.start_datetime and record.end_datetime:
                delta = record.end_datetime - record.start_datetime
                record.duration = delta.total_seconds() / 3600.0
            else:
                record.duration = 0.0
    
    @api.model
    def create(self, vals):
        """Genera nombre automático al crear"""
        if vals.get('name', _('Nueva Hoja de Trabajo')) == _('Nueva Hoja de Trabajo'):
            order = self.env['fsm.order'].browse(vals.get('order_id'))
            if order:
                vals['name'] = f"Hoja de Trabajo - {order.name}"
        return super().create(vals)
    
    def action_start_work(self):
        """Inicia el trabajo"""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_("Solo se puede iniciar trabajo desde estado borrador."))
        
        self.write({
            'state': 'in_progress',
            'start_datetime': fields.Datetime.now()
        })
        
        # Crear mensaje en el chatter
        self.message_post(
            body=_("Trabajo iniciado por %s") % self.technician_id.name,
            message_type='notification'
        )
    
    def action_complete_work(self):
        """Completa el trabajo"""
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_("Solo se puede completar trabajo en progreso."))
        
        if not self.end_datetime:
            self.end_datetime = fields.Datetime.now()
        
        self.state = 'completed'
        
        # Crear mensaje en el chatter
        self.message_post(
            body=_("Trabajo completado por %s") % self.technician_id.name,
            message_type='notification'
        )
    
    def action_sign_technician(self):
        """Abre wizard para firma del técnico"""
        self.ensure_one()
        if self.state not in ['completed']:
            raise UserError(_("El trabajo debe estar completado para firmar."))
        
        return {
            'name': _('Firma del Técnico'),
            'type': 'ir.actions.act_window',
            'res_model': 'fsm.worksheet.signature.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_worksheet_id': self.id,
                'signature_type': 'technician'
            }
        }
    
    def action_sign_customer(self):
        """Abre wizard para firma del cliente"""
        self.ensure_one()
        if not self.technician_signature:
            raise UserError(_("El técnico debe firmar primero."))
        
        return {
            'name': _('Firma del Cliente'),
            'type': 'ir.actions.act_window',
            'res_model': 'fsm.worksheet.signature.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_worksheet_id': self.id,
                'signature_type': 'customer'
            }
        }
    
    def action_generate_pdf(self):
        """Genera el PDF de la hoja de trabajo"""
        self.ensure_one()
        
        # Generar PDF usando el reporte
        report = self.env.ref('patco_core.action_report_fsm_worksheet')
        pdf_content, _ = report._render_qweb_pdf([self.id])
        
        # Guardar el PDF
        self.write({
            'pdf_report': base64.b64encode(pdf_content),
            'pdf_filename': f'worksheet_{self.order_id.name}_{self.id}.pdf'
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/fsm.worksheet/{self.id}/pdf_report/{self.pdf_filename}?download=true',
            'target': 'new'
        }
    
    def get_worksheet_data_dict(self):
        """Convierte los datos JSON en diccionario"""
        self.ensure_one()
        if self.worksheet_data:
            try:
                return json.loads(self.worksheet_data)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_worksheet_data_dict(self, data_dict):
        """Guarda diccionario como JSON"""
        self.ensure_one()
        self.worksheet_data = json.dumps(data_dict, ensure_ascii=False, indent=2)
    
    def action_customer_approval(self):
        """Abre el wizard para la conformidad del cliente"""
        self.ensure_one()
        
        return {
            'name': _('Conformidad del Cliente'),
            'type': 'ir.actions.act_window',
            'res_model': 'fsm.worksheet.customer.approval.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_worksheet_id': self.id,
                'default_customer_name': self.order_id.location_id.name if self.order_id.location_id else '',
            }
        }
    
    def action_approve_work(self, customer_name, customer_document, customer_signature, customer_comments=''):
        """Aprueba el trabajo con la firma del cliente"""
        self.ensure_one()
        
        self.write({
            'customer_signature': customer_signature,
            'customer_signature_date': fields.Datetime.now(),
            'customer_name': customer_name,
            'customer_document': customer_document,
            'customer_comments': customer_comments,
            'approval_status': 'approved'
        })
        
        # Generar PDF firmado
        self._generate_signed_pdf()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Trabajo Aprobado'),
                'message': _('El cliente ha aprobado el trabajo realizado.'),
                'type': 'success'
            }
        }
    
    def action_reject_work(self, customer_name, customer_document, customer_comments):
        """Rechaza el trabajo con comentarios del cliente"""
        self.ensure_one()
        
        self.write({
            'customer_name': customer_name,
            'customer_document': customer_document,
            'customer_comments': customer_comments,
            'approval_status': 'rejected'
        })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Trabajo Rechazado'),
                'message': _('El cliente ha rechazado el trabajo. Revise los comentarios.'),
                'type': 'warning'
            }
        }
    
    def _generate_signed_pdf(self):
        """Genera un PDF con las firmas del técnico y cliente"""
        self.ensure_one()
        
        # Generar el reporte PDF
        report = self.env.ref('patco_core.action_report_fsm_worksheet_signed')
        pdf_content, _ = report._render_qweb_pdf([self.id])
        
        # Guardar el PDF
        filename = f'hoja_trabajo_{self.order_id.name}_{self.id}_firmada.pdf'
        self.write({
            'signed_pdf': base64.b64encode(pdf_content),
            'signed_pdf_filename': filename
        })
    
    def action_download_signed_pdf(self):
        """Descarga el PDF firmado"""
        self.ensure_one()
        
        if not self.signed_pdf:
            raise UserError(_('No hay PDF firmado disponible. Primero debe obtener la conformidad del cliente.'))
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/fsm.worksheet/{self.id}/signed_pdf/{self.signed_pdf_filename}?download=true',
            'target': 'self',
        }
    
    @api.constrains('start_datetime', 'end_datetime')
    def _check_datetime_sequence(self):
        """Valida que la fecha de fin sea posterior al inicio"""
        for record in self:
            if record.start_datetime and record.end_datetime:
                if record.end_datetime <= record.start_datetime:
                    raise ValidationError(_("La fecha de fin debe ser posterior a la fecha de inicio."))


class FSMWorksheetTemplate(models.Model):
    _name = 'fsm.worksheet.template'
    _description = 'Plantilla de Hoja de Trabajo'
    _order = 'sequence, name'
    
    name = fields.Char(
        string='Nombre',
        required=True
    )
    
    description = fields.Text(
        string='Descripción'
    )
    
    sequence = fields.Integer(
        string='Secuencia',
        default=10
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True
    )
    
    # Configuración de campos
    field_config = fields.Text(
        string='Configuración de Campos',
        help='JSON con la configuración de campos del formulario',
        default='{}'
    )
    
    # Categorías de equipos aplicables
    equipment_category_ids = fields.Many2many(
        'maintenance.equipment.category',
        string='Categorías de Equipos',
        help='Categorías de equipos para las que aplica esta plantilla'
    )
    
    # Tipos de servicio aplicables
    service_nature_ids = fields.Many2many(
        'patco_base.service.nature',
        string='Naturalezas de Servicio',
        help='Tipos de servicio para los que aplica esta plantilla'
    )
    
    def get_field_config_dict(self):
        """Convierte la configuración JSON en diccionario"""
        self.ensure_one()
        if self.field_config:
            try:
                return json.loads(self.field_config)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_field_config_dict(self, config_dict):
        """Guarda diccionario como JSON"""
        self.ensure_one()
        self.field_config = json.dumps(config_dict, ensure_ascii=False, indent=2)