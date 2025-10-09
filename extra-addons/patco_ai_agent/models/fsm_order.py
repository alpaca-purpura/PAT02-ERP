# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class FsmOrder(models.Model):
    _inherit = 'fsm.order'
    
    # Campos para integración con IA - Enfoque de canales nativos
    x_ai_channel_id = fields.Many2one(
        'discuss.channel', 
        string='Canal IA',
        help='Canal de conversación con el asistente IA'
    )
    x_ai_enabled = fields.Boolean(
        'IA Habilitada', 
        default=True,
        help='Habilitar asistente IA para esta orden de servicio'
    )
    x_ai_status = fields.Selection([
        ('not_started', 'No Iniciado'),
        ('active', 'Activo'),
        ('completed', 'Completado'),
        ('error', 'Error')
    ], string='Estado IA', default='not_started',
       help='Estado actual del asistente IA para esta orden')
    
    x_ai_auto_start = fields.Boolean(
        'Inicio Automático IA',
        default=True,
        help='Iniciar automáticamente conversación IA al asignar técnico'
    )
    
    # Campos para compatibilidad con implementación anterior
    x_ai_conversation_id = fields.Many2one(
        'ai.conversation', 
        string='Conversación IA (Legacy)',
        help='Conversación IA - Campo de compatibilidad'
    )
    
    # Campos relacionados para facilitar acceso
    x_ai_channel_name = fields.Char(
        related='x_ai_channel_id.name',
        string='Nombre Canal IA',
        readonly=True
    )
    x_ai_message_count = fields.Integer(
        string='Mensajes IA',
        compute='_compute_ai_metrics',
        store=False
    )
    x_ai_duration = fields.Float(
        string='Duración IA (horas)',
        compute='_compute_ai_metrics',
        store=False
    )
    
    @api.depends('x_ai_channel_id')
    def _compute_ai_metrics(self):
        """Calcula métricas de IA basadas en el canal"""
        for record in self:
            if record.x_ai_channel_id:
                # Contar mensajes en el canal
                messages = self.env['mail.message'].search([
                    ('res_model', '=', 'discuss.channel'),
                    ('res_id', '=', record.x_ai_channel_id.id)
                ])
                record.x_ai_message_count = len(messages)
                
                # Calcular duración aproximada (primer y último mensaje)
                if messages:
                    first_msg = messages[0]
                    last_msg = messages[-1]
                    if first_msg.date and last_msg.date:
                        delta = last_msg.date - first_msg.date
                        record.x_ai_duration = delta.total_seconds() / 3600.0
                    else:
                        record.x_ai_duration = 0.0
                else:
                    record.x_ai_duration = 0.0
            else:
                record.x_ai_message_count = 0
                record.x_ai_duration = 0.0

    @api.model
    def create(self, vals):
        """Sobrescribir create para disparar IA automáticamente si está habilitada"""
        
        order = super().create(vals)
        
        # Disparar IA si hay técnico asignado y está habilitada
        if order.person_id and order.x_ai_enabled and order.x_ai_auto_start:
            order._create_ai_channel()
        
        return order

    def write(self, vals):
        """Sobrescribir write para detectar asignación de técnico"""
        
        result = super().write(vals)
        
        # Si se asigna técnico, crear canal IA automáticamente
        if 'person_id' in vals and vals['person_id']:
            for order in self:
                if order.x_ai_enabled and order.x_ai_auto_start and not order.x_ai_channel_id:
                    order._create_ai_channel()
        
        return result

    def _create_ai_channel(self):
        """Crea canal privado de IA para la orden FSM"""
        
        try:
            if not self.person_id:
                _logger.warning(f"No se puede crear canal IA para orden {self.name}: sin técnico asignado")
                return
            
            # Obtener usuario bot IA
            bot = self.env['ai.bot.user'].get_or_create_bot_user()
            
            # Crear canal privado
            channel = self.env['discuss.channel'].create({
                'name': f"🤖 IA - {self.name} - {self.person_id.name}",
                'channel_type': 'chat',
                'public': 'private',
                'description': f'Canal de asistente IA para orden {self.name}',
                'channel_partner_ids': [
                    (4, self.person_id.user_id.partner_id.id),  # Técnico
                    (4, bot.partner_id.id)  # Bot IA
                ]
            })
            
            # Vincular canal a la orden
            self.x_ai_channel_id = channel.id
            self.x_ai_status = 'active'
            
            # Enviar mensaje inicial del bot
            self._send_initial_ai_message(channel, bot)
            
            _logger.info(f"Canal IA creado para orden {self.name} - Canal ID: {channel.id}")
            
        except Exception as e:
            _logger.error(f"Error creando canal IA para orden {self.name}: {e}")
            self.x_ai_status = 'error'

    def _send_initial_ai_message(self, channel, bot):
        """Envía mensaje inicial del asistente IA"""
        
        message = f"""¡Hola {self.person_id.name}! 👋

Soy tu asistente IA para la orden de servicio **{self.name}**.

📋 **Detalles del servicio:**
• Cliente: {self.partner_id.name}
• Ubicación: {self.location_id.name if self.location_id else 'No especificada'}
• Equipos asignados: {len(self.equipment_ids)} equipos

Te ayudaré durante todo el proceso con:
🔍 Búsqueda en manuales técnicos
📝 Checklists dinámicos
🛠️ Procedimientos paso a paso
📊 Generación automática de reportes

¿Has llegado al sitio y estás listo para comenzar?"""
        
        # Enviar mensaje como usuario bot
        channel.with_user(bot.user_id).message_post(
            body=message,
            message_type='comment',
            subtype_xmlid='mail.mt_comment'
        )

    def action_open_ai_channel(self):
        """Acción para abrir el canal IA"""
        self.ensure_one()
        
        if not self.x_ai_channel_id:
            raise UserError("No hay canal IA activo para esta orden")
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Chat IA - {self.name}',
            'res_model': 'discuss.channel',
            'res_id': self.x_ai_channel_id.id,
            'view_mode': 'form',
            'target': 'current'
        }

    def action_create_ai_channel(self):
        """Acción manual para crear canal IA"""
        self.ensure_one()
        
        if not self.person_id:
            raise UserError("Debe asignar un técnico antes de activar la IA")
        
        if self.x_ai_channel_id:
            raise UserError("Ya existe un canal IA para esta orden")
        
        self._create_ai_channel()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Canal IA Creado',
                'message': f'Se ha creado el canal IA para la orden {self.name}',
                'type': 'success',
                'sticky': False,
            }
        }
    
    # Métodos de compatibilidad con implementación anterior
    def _trigger_ai_conversation(self):
        """Método legacy - usar _create_ai_channel() en su lugar"""
        return self._create_ai_channel()
    
    def action_start_ai_conversation(self):
        """Método legacy - usar action_create_ai_channel() en su lugar"""
        return self.action_create_ai_channel()
    
    def action_view_ai_conversation(self):
        """Método legacy - usar action_open_ai_channel() en su lugar"""
        return self.action_open_ai_channel()
    
    def action_complete_ai_conversation(self):
        """Método para completar conversación IA"""
        self.ensure_one()
        
        if self.x_ai_channel_id:
            # Marcar canal como archivado
            self.x_ai_channel_id.is_archived = True
            self.x_ai_status = 'completed'
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Conversación IA Completada',
                    'message': f'La conversación IA para la orden {self.name} ha sido completada.',
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            raise UserError("No hay conversación IA activa para completar")
    
    def action_disable_ai(self):
        """Acción para deshabilitar IA"""
        
        self.ensure_one()
        
        self.x_ai_enabled = False
        self.x_ai_status = 'not_started'
        
        # Archivar canal si existe (no eliminar para mantener historial)
        if self.x_ai_channel_id:
            self.x_ai_channel_id.write({
                'active': False,
                'description': f'Canal IA archivado para orden {self.name}'
            })
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'IA Deshabilitada',
                'message': f'El asistente IA ha sido deshabilitado para la orden {self.name}',
                'type': 'info',
                'sticky': False,
            }
        }

    def action_enable_ai(self):
        """Acción para habilitar IA"""
        
        self.ensure_one()
        
        self.x_ai_enabled = True
        
        # Si hay técnico asignado y no hay canal, crear uno
        if self.person_id and not self.x_ai_channel_id:
            self._create_ai_channel()
        elif self.x_ai_channel_id and not self.x_ai_channel_id.active:
            # Reactivar canal existente
            self.x_ai_channel_id.write({
                'active': True,
                'description': f'Canal de asistente IA para orden {self.name}'
            })
            self.x_ai_status = 'active'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'IA Habilitada',
                'message': f'El asistente IA ha sido habilitado para la orden {self.name}',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def _get_ai_context(self):
        """Obtiene contexto para el agente IA"""
        
        self.ensure_one()
        
        return {
            'fsm_order_id': self.id,
            'fsm_order_name': self.name,
            'technician_id': self.person_id.id if self.person_id else None,
            'technician_name': self.person_id.name if self.person_id else None,
            'client_name': self.partner_id.name,
            'location': self.location_id.name if self.location_id else None,
            'equipment_ids': self.equipment_ids.ids,
            'equipment_names': [eq.name for eq in self.equipment_ids],
            'service_nature': self.x_service_nature_id.name if hasattr(self, 'x_service_nature_id') and self.x_service_nature_id else None,
            'service_area': self.x_service_area_id.name if hasattr(self, 'x_service_area_id') and self.x_service_area_id else None,
            'service_complexity': self.x_service_complexity_id.name if hasattr(self, 'x_service_complexity_id') and self.x_service_complexity_id else None,
            'channel_id': self.x_ai_channel_id.id if self.x_ai_channel_id else None,
            'stage': self.stage_id.name if self.stage_id else None,
            'priority': self.priority,
            'description': self.description or ''
        }
    
    @api.model
    def get_ai_statistics(self):
        """Obtiene estadísticas de uso de IA"""
        
        # Órdenes con IA habilitada
        total_orders = self.search_count([])
        ai_enabled_orders = self.search_count([('x_ai_enabled', '=', True)])
        active_ai_orders = self.search_count([('x_ai_status', '=', 'active')])
        completed_ai_orders = self.search_count([('x_ai_status', '=', 'completed')])
        
        # Canales IA activos
        active_channels = self.env['discuss.channel'].search_count([
            ('name', 'ilike', '🤖 IA -'),
            ('active', '=', True)
        ])
        
        # Mensajes procesados por IA
        ai_messages = self.env['mail.message'].search_count([
            ('x_processed_by_ai', '=', True)
        ])
        
        return {
            'total_orders': total_orders,
            'ai_enabled_orders': ai_enabled_orders,
            'ai_enabled_percentage': (ai_enabled_orders / total_orders * 100) if total_orders > 0 else 0,
            'active_ai_orders': active_ai_orders,
            'completed_ai_orders': completed_ai_orders,
            'active_channels': active_channels,
            'ai_messages_processed': ai_messages
        }

    def action_view_ai_statistics(self):
        """Acción para ver estadísticas de IA"""
        
        stats = self.get_ai_statistics()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Estadísticas IA PATCO',
                'message': f"""
                Órdenes con IA: {stats['ai_enabled_orders']}/{stats['total_orders']} ({stats['ai_enabled_percentage']:.1f}%)
                Conversaciones activas: {stats['active_ai_orders']}
                Conversaciones completadas: {stats['completed_ai_orders']}
                Canales activos: {stats['active_channels']}
                Mensajes procesados: {stats['ai_messages_processed']}
                """,
                'type': 'info',
                'sticky': True,
            }
        }