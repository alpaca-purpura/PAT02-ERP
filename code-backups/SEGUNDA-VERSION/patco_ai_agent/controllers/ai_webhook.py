# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)


class AIWebhookController(http.Controller):
    
    @http.route('/ai/webhook/message', type='json', auth='user', methods=['POST'])
    def receive_ai_message(self, **kwargs):
        """Recibe mensajes desde el agente IA (LangGraph server)"""
        
        try:
            data = request.jsonrequest
            
            conversation_id = data.get('conversation_id')
            message = data.get('message')
            actions = data.get('actions', [])
            
            if not conversation_id or not message:
                return {'error': 'Faltan parámetros requeridos: conversation_id, message'}
            
            # Buscar conversación
            conversation = request.env['ai.conversation'].search([
                ('id', '=', int(conversation_id))
            ], limit=1)
            
            if not conversation:
                return {'error': f'Conversación no encontrada: {conversation_id}'}
            
            # Procesar mensaje del agente IA (incluye notificación del bus)
            success = conversation._process_ai_message(message, actions)
            
            if success:
                return {'success': True, 'message': 'Mensaje procesado correctamente'}
            else:
                return {'error': 'Error procesando mensaje del agente IA'}
            
        except Exception as e:
            _logger.error(f"Error procesando mensaje IA: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/webhook/user_message', type='json', auth='user', methods=['POST'])
    def send_user_message(self, **kwargs):
        """Envía mensaje del usuario al agente IA (LangGraph server)"""
        
        try:
            data = request.jsonrequest
            
            conversation_id = data.get('conversation_id')
            message = data.get('message')
            user_id = data.get('user_id')
            
            if not all([conversation_id, message, user_id]):
                return {'error': 'Faltan parámetros requeridos: conversation_id, message, user_id'}
            
            # Buscar conversación
            conversation = request.env['ai.conversation'].search([
                ('id', '=', int(conversation_id))
            ], limit=1)
            
            if not conversation:
                return {'error': f'Conversación no encontrada: {conversation_id}'}
            
            # Enviar mensaje al LangGraph server
            response = conversation._send_message_to_ai(message, user_id)
            
            return {'success': True, 'response': response}
            
        except Exception as e:
            _logger.error(f"Error enviando mensaje a IA: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/conversation/<int:conversation_id>/status', type='json', auth='user')
    def get_conversation_status(self, conversation_id, **kwargs):
        """Obtiene estado actual de conversación"""
        
        try:
            conversation = request.env['ai.conversation'].browse(conversation_id)
            
            if not conversation.exists():
                return {'error': f'Conversación no encontrada: {conversation_id}'}
            
            return {
                'conversation_id': conversation.id,
                'state': conversation.state,
                'fsm_order': conversation.fsm_order_id.name,
                'technician': conversation.technician_id.name,
                'current_equipment': conversation.current_equipment_id.name if conversation.current_equipment_id else None,
                'message_count': conversation.message_count,
                'duration': conversation.duration,
                'report_generated': conversation.report_generated,
                'report_url': conversation.report_url
            }
            
        except Exception as e:
            _logger.error(f"Error obteniendo estado de conversación: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/conversation/get_active', type='json', auth='user', methods=['POST'])
    def get_active_conversation(self, **kwargs):
        """Obtiene conversación activa para una orden FSM"""
        
        try:
            data = request.jsonrequest
            fsm_order_id = data.get('fsm_order_id')
            
            if not fsm_order_id:
                return {'error': 'Falta parámetro requerido: fsm_order_id'}
            
            # Buscar conversación activa
            conversation = request.env['ai.conversation'].search([
                ('fsm_order_id', '=', fsm_order_id),
                ('state', 'not in', ['completed', 'archived'])
            ], limit=1)
            
            if conversation:
                return {
                    'conversation_id': conversation.id,
                    'state': conversation.state,
                    'channel_id': conversation.channel_id.id if conversation.channel_id else None
                }
            else:
                return {'conversation_id': None}
            
        except Exception as e:
            _logger.error(f"Error obteniendo conversación activa: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/conversation/create', type='json', auth='user', methods=['POST'])
    def create_conversation(self, **kwargs):
        """Crea nueva conversación IA"""
        
        try:
            data = request.jsonrequest
            fsm_order_id = data.get('fsm_order_id')
            technician_id = data.get('technician_id')
            
            if not all([fsm_order_id, technician_id]):
                return {'error': 'Faltan parámetros requeridos: fsm_order_id, technician_id'}
            
            # Verificar que la orden FSM existe
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            if not fsm_order.exists():
                return {'error': f'Orden FSM no encontrada: {fsm_order_id}'}
            
            # Crear conversación usando el método del modelo
            conversation = request.env['ai.conversation'].create_service_conversation(fsm_order)
            
            if conversation:
                return {
                    'conversation_id': conversation.id,
                    'fsm_order_id': fsm_order_id,
                    'technician_id': technician_id,
                    'status': 'created'
                }
            else:
                return {'error': 'No se pudo crear la conversación IA'}
            
        except Exception as e:
            _logger.error(f"Error creando conversación: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/conversation/history', type='json', auth='user', methods=['POST'])
    def get_conversation_history(self, **kwargs):
        """Obtiene historial de conversación"""
        
        try:
            data = request.jsonrequest
            conversation_id = data.get('conversation_id')
            
            if not conversation_id:
                return {'error': 'Falta parámetro requerido: conversation_id'}
            
            conversation = request.env['ai.conversation'].browse(conversation_id)
            
            if not conversation.exists():
                return {'error': f'Conversación no encontrada: {conversation_id}'}
            
            # Obtener mensajes del canal
            messages = []
            if conversation.channel_id:
                for message in conversation.channel_id.message_ids.sorted('create_date'):
                    messages.append({
                        'id': message.id,
                        'author': message.author_id.name,
                        'body': message.body,
                        'date': message.create_date.isoformat(),
                        'is_ai': message.author_id.id == request.env.ref('patco_ai_agent.ai_agent_partner').id
                    })
            
            return {
                'conversation_id': conversation_id,
                'messages': messages,
                'state': conversation.state
            }
            
        except Exception as e:
            _logger.error(f"Error obteniendo historial: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/health', type='json', auth='none', methods=['GET'])
    def health_check(self, **kwargs):
        """Endpoint de salud para el módulo IA"""
        
        try:
            # Verificar configuración básica
            ai_enabled = request.env['ir.config_parameter'].sudo().get_param(
                'patco_ai_agent.ai_enabled', 'False'
            )
            
            # Contar conversaciones activas
            active_conversations = request.env['ai.conversation'].sudo().search_count([
                ('state', 'not in', ['completed', 'archived'])
            ])
            
            # Contar documentos indexados
            indexed_docs = request.env['ir.attachment'].sudo().search_count([
                ('x_is_indexed', '=', True)
            ])
            
            return {
                'status': 'healthy',
                'service': 'patco-ai-agent',
                'ai_enabled': ai_enabled == 'True',
                'active_conversations': active_conversations,
                'indexed_documents': indexed_docs,
                'timestamp': http.request.env.cr.now().isoformat()
            }
            
        except Exception as e:
            _logger.error(f"Error en health check: {e}")
            return {
                'status': 'error',
                'service': 'patco-ai-agent',
                'error': str(e)
            }