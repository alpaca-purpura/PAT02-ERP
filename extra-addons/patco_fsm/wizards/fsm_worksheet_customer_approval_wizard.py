# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class FSMWorksheetCustomerApprovalWizard(models.TransientModel):
    _name = 'fsm.worksheet.customer.approval.wizard'
    _description = 'Wizard para Conformidad del Cliente'
    
    worksheet_id = fields.Many2one(
        'fsm.worksheet',
        string='Hoja de Trabajo',
        required=True
    )
    
    customer_name = fields.Char(
        string='Nombre del Cliente',
        required=True,
        help='Nombre completo de la persona que firma la conformidad'
    )
    
    customer_document = fields.Char(
        string='Documento de Identidad',
        required=True,
        help='Número de documento de identidad del cliente'
    )
    
    customer_signature = fields.Binary(
        string='Firma del Cliente',
        required=True,
        help='Firma digital del cliente'
    )
    
    customer_comments = fields.Text(
        string='Comentarios del Cliente',
        help='Observaciones o comentarios del cliente sobre el servicio realizado'
    )
    
    approval_action = fields.Selection([
        ('approve', 'Aprobar Trabajo'),
        ('reject', 'Rechazar Trabajo')
    ], string='Acción', required=True, default='approve')
    
    def action_confirm_approval(self):
        """Confirma la aprobación o rechazo del cliente"""
        self.ensure_one()
        
        if not self.worksheet_id:
            raise UserError(_('No se encontró la hoja de trabajo.'))
        
        if self.approval_action == 'approve':
            if not self.customer_signature:
                raise UserError(_('La firma del cliente es requerida para aprobar el trabajo.'))
            
            return self.worksheet_id.action_approve_work(
                customer_name=self.customer_name,
                customer_document=self.customer_document,
                customer_signature=self.customer_signature,
                customer_comments=self.customer_comments or ''
            )
        else:
            return self.worksheet_id.action_reject_work(
                customer_name=self.customer_name,
                customer_document=self.customer_document,
                customer_comments=self.customer_comments or 'Trabajo rechazado por el cliente'
            )
    
    def action_cancel(self):
        """Cancela el wizard sin realizar cambios"""
        return {'type': 'ir.actions.act_window_close'}