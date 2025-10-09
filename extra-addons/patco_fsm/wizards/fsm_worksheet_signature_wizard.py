# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import logging

_logger = logging.getLogger(__name__)


class FsmWorksheetSignatureWizard(models.TransientModel):
    """Wizard para captura de firmas digitales en hojas de trabajo FSM"""
    _name = 'fsm.worksheet.signature.wizard'
    _description = 'Wizard de Firma Digital para Hojas de Trabajo'

    worksheet_id = fields.Many2one(
        'fsm.worksheet',
        string='Hoja de Trabajo',
        required=True,
        readonly=True
    )
    
    signature_type = fields.Selection([
        ('technician', 'Firma del Técnico'),
        ('customer', 'Firma del Cliente')
    ], string='Tipo de Firma', required=True, readonly=True)
    
    signature = fields.Binary(
        string='Firma Digital',
        required=True,
        help='Captura de la firma digital'
    )
    
    # Campos específicos para firma del cliente
    customer_name = fields.Char(
        string='Nombre del Cliente',
        help='Nombre completo de la persona que firma'
    )
    
    customer_position = fields.Char(
        string='Cargo/Posición',
        help='Cargo o posición de la persona que firma'
    )
    
    customer_id_number = fields.Char(
        string='Número de Identificación',
        help='DNI, RUC u otro documento de identificación'
    )
    
    observations = fields.Text(
        string='Observaciones',
        help='Comentarios adicionales sobre el servicio'
    )

    @api.model
    def default_get(self, fields_list):
        """Establecer valores por defecto basados en el contexto"""
        res = super().default_get(fields_list)
        
        # Obtener worksheet_id del contexto
        worksheet_id = self.env.context.get('active_id')
        if worksheet_id:
            res['worksheet_id'] = worksheet_id
            
        # Obtener tipo de firma del contexto
        signature_type = self.env.context.get('signature_type', 'technician')
        res['signature_type'] = signature_type
        
        return res

    def action_save_signature(self):
        """Guardar la firma en la hoja de trabajo"""
        self.ensure_one()
        
        if not self.signature:
            raise UserError(_('Debe capturar una firma antes de guardar.'))
            
        worksheet = self.worksheet_id
        
        try:
            if self.signature_type == 'technician':
                worksheet.write({
                    'technician_signature': self.signature,
                    'technician_signature_date': fields.Datetime.now()
                })
                message = _('Firma del técnico guardada exitosamente.')
                
            elif self.signature_type == 'customer':
                # Validar campos requeridos para firma del cliente
                if not self.customer_name:
                    raise UserError(_('El nombre del cliente es requerido.'))
                    
                worksheet.write({
                    'customer_signature': self.signature,
                    'customer_signature_date': fields.Datetime.now(),
                    'customer_name': self.customer_name,
                    'customer_position': self.customer_position,
                    'customer_id_number': self.customer_id_number,
                    'customer_observations': self.observations
                })
                message = _('Firma del cliente guardada exitosamente.')
                
            # Registrar en el chatter
            worksheet.message_post(
                body=message,
                message_type='notification'
            )
            
            _logger.info(f"Firma {self.signature_type} guardada para worksheet {worksheet.id}")
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Éxito'),
                    'message': message,
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            _logger.error(f"Error al guardar firma: {str(e)}")
            raise UserError(_('Error al guardar la firma: %s') % str(e))

    def action_cancel(self):
        """Cancelar el wizard sin guardar"""
        return {'type': 'ir.actions.act_window_close'}


class FsmWorksheetDataWizard(models.TransientModel):
    """Wizard para captura de datos dinámicos en hojas de trabajo"""
    _name = 'fsm.worksheet.data.wizard'
    _description = 'Wizard de Datos para Hojas de Trabajo'

    worksheet_id = fields.Many2one(
        'fsm.worksheet',
        string='Hoja de Trabajo',
        required=True,
        readonly=True
    )
    
    template_id = fields.Many2one(
        'fsm.worksheet.template',
        string='Plantilla',
        readonly=True
    )
    
    dynamic_data = fields.Text(
        string='Datos Dinámicos',
        help='Datos en formato JSON basados en la plantilla'
    )

    @api.model
    def default_get(self, fields_list):
        """Establecer valores por defecto"""
        res = super().default_get(fields_list)
        
        worksheet_id = self.env.context.get('active_id')
        if worksheet_id:
            worksheet = self.env['fsm.worksheet'].browse(worksheet_id)
            res['worksheet_id'] = worksheet_id
            res['template_id'] = worksheet.template_id.id
            res['dynamic_data'] = worksheet.dynamic_data or '{}'
            
        return res

    def action_save_data(self):
        """Guardar los datos en la hoja de trabajo"""
        self.ensure_one()
        
        try:
            # Validar que sea JSON válido
            import json
            json.loads(self.dynamic_data or '{}')
            
            self.worksheet_id.write({
                'dynamic_data': self.dynamic_data
            })
            
            self.worksheet_id.message_post(
                body=_('Datos de la hoja de trabajo actualizados.'),
                message_type='notification'
            )
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Éxito'),
                    'message': _('Datos guardados exitosamente.'),
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except json.JSONDecodeError:
            raise UserError(_('Los datos deben estar en formato JSON válido.'))
        except Exception as e:
            _logger.error(f"Error al guardar datos: {str(e)}")
            raise UserError(_('Error al guardar los datos: %s') % str(e))

    def action_cancel(self):
        """Cancelar el wizard sin guardar"""
        return {'type': 'ir.actions.act_window_close'}