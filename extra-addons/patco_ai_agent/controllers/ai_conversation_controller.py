from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class AIConversationController(http.Controller):
    
    @http.route('/ai/conversation/get_active', type='json', auth='user', methods=['POST'])
    def get_active_conversation(self, **kwargs):
        """Obtiene conversación IA activa para una orden FSM"""
        
        try:
            data = request.jsonrequest
            fsm_order_id = data.get('fsm_order_id')
            
            if not fsm_order_id:
                return {'error': 'fsm_order_id requerido'}
            
            # Buscar orden FSM con canal IA activo
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if fsm_order.x_ai_channel_id and fsm_order.x_ai_status == 'active':
                return {
                    'conversation_id': f"fsm_{fsm_order_id}",
                    'channel_id': fsm_order.x_ai_channel_id.id,
                    'channel_name': fsm_order.x_ai_channel_id.name,
                    'status': fsm_order.x_ai_status
                }
            else:
                return {'conversation_id': None}
                
        except Exception as e:
            _logger.error(f"Error obteniendo conversación activa: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/conversation/create', type='json', auth='user', methods=['POST'])
    def create_conversation(self, **kwargs):
        """Crea nueva conversación IA para orden FSM"""
        
        try:
            data = request.jsonrequest
            fsm_order_id = data.get('fsm_order_id')
            
            if not fsm_order_id:
                return {'error': 'fsm_order_id requerido'}
            
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if not fsm_order.exists():
                return {'error': 'Orden FSM no encontrada'}
            
            # Crear canal IA si no existe
            if not fsm_order.x_ai_channel_id:
                fsm_order._create_ai_channel()
            
            return {
                'conversation_id': f"fsm_{fsm_order_id}",
                'channel_id': fsm_order.x_ai_channel_id.id,
                'status': 'created'
            }
            
        except Exception as e:
            _logger.error(f"Error creando conversación: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/conversation/history', type='json', auth='user', methods=['POST'])
    def get_conversation_history(self, **kwargs):
        """Obtiene historial de mensajes de conversación"""
        
        try:
            data = request.jsonrequest
            conversation_id = data.get('conversation_id')
            
            if not conversation_id:
                return {'error': 'conversation_id requerido'}
            
            # Extraer fsm_order_id del conversation_id
            fsm_order_id = int(conversation_id.replace('fsm_', ''))
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if not fsm_order.x_ai_channel_id:
                return {'messages': []}
            
            # Obtener mensajes del canal
            messages = request.env['mail.message'].search([
                ('res_model', '=', 'discuss.channel'),
                ('res_id', '=', fsm_order.x_ai_channel_id.id)
            ], order='date asc')
            
            message_list = []
            for msg in messages:
                # Determinar rol del mensaje
                role = 'assistant' if msg.author_id.email == 'ai-bot@patco.com.pe' else 'user'
                
                message_list.append({
                    'role': role,
                    'content': msg.body,
                    'timestamp': msg.date.isoformat(),
                    'author_name': msg.author_id.name
                })
            
            return {'messages': message_list}
            
        except Exception as e:
            _logger.error(f"Error obteniendo historial: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/conversation/send_message', type='json', auth='user', methods=['POST'])
    def send_message(self, **kwargs):
        """Envía mensaje del usuario al canal IA"""
        
        try:
            data = request.jsonrequest
            conversation_id = data.get('conversation_id')
            message = data.get('message')
            
            if not conversation_id or not message:
                return {'error': 'conversation_id y message requeridos'}
            
            # Extraer fsm_order_id del conversation_id
            fsm_order_id = int(conversation_id.replace('fsm_', ''))
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if not fsm_order.x_ai_channel_id:
                return {'error': 'Canal IA no encontrado'}
            
            # Enviar mensaje al canal
            fsm_order.x_ai_channel_id.message_post(
                body=message,
                message_type='comment',
                subtype_xmlid='mail.mt_comment'
            )
            
            return {'success': True, 'message': 'Mensaje enviado'}
            
        except Exception as e:
            _logger.error(f"Error enviando mensaje: {e}")
            return {'error': str(e)}
    
    @http.route('/ai/conversation/status', type='json', auth='user', methods=['POST'])
    def get_conversation_status(self, **kwargs):
        """Obtiene estado de conversación IA"""
        
        try:
            data = request.jsonrequest
            conversation_id = data.get('conversation_id')
            
            if not conversation_id:
                return {'error': 'conversation_id requerido'}
            
            # Extraer fsm_order_id del conversation_id
            fsm_order_id = int(conversation_id.replace('fsm_', ''))
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if not fsm_order.exists():
                return {'error': 'Orden FSM no encontrada'}
            
            return {
                'conversation_id': conversation_id,
                'fsm_order_name': fsm_order.name,
                'technician_name': fsm_order.person_id.name if fsm_order.person_id else None,
                'ai_status': fsm_order.x_ai_status,
                'channel_id': fsm_order.x_ai_channel_id.id if fsm_order.x_ai_channel_id else None,
                'message_count': fsm_order.x_ai_message_count,
                'duration': fsm_order.x_ai_duration
            }
            
        except Exception as e:
            _logger.error(f"Error obteniendo estado: {e}")
            return {'error': str(e)}

class MobileAIController(http.Controller):
    
    @http.route('/api/mobile/ai/conversation/start', type='json', auth='user', methods=['POST'])
    def mobile_start_conversation(self, **kwargs):
        """API móvil para iniciar conversación IA"""
        
        try:
            data = request.jsonrequest
            fsm_order_id = data.get('fsm_order_id')
            
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if not fsm_order.exists():
                return {'success': False, 'error': 'Orden no encontrada'}
            
            # Crear canal IA si no existe
            if not fsm_order.x_ai_channel_id:
                fsm_order._create_ai_channel()
            
            return {
                'success': True,
                'conversation_id': f"fsm_{fsm_order_id}",
                'channel_id': fsm_order.x_ai_channel_id.id,
                'welcome_message': f"¡Hola! Soy tu asistente IA para la orden {fsm_order.name}. ¿En qué puedo ayudarte?"
            }
            
        except Exception as e:
            _logger.error(f"Error en API móvil: {e}")
            return {'success': False, 'error': str(e)}
    
    @http.route('/api/mobile/ai/conversation/messages', type='json', auth='user', methods=['POST'])
    def mobile_get_messages(self, **kwargs):
        """API móvil para obtener mensajes"""
        
        try:
            data = request.jsonrequest
            conversation_id = data.get('conversation_id')
            last_message_id = data.get('last_message_id', 0)
            
            # Extraer fsm_order_id
            fsm_order_id = int(conversation_id.replace('fsm_', ''))
            fsm_order = request.env['fsm.order'].browse(fsm_order_id)
            
            if not fsm_order.x_ai_channel_id:
                return {'success': False, 'error': 'Canal no encontrado'}
            
            # Obtener mensajes nuevos
            domain = [
                ('res_model', '=', 'discuss.channel'),
                ('res_id', '=', fsm_order.x_ai_channel_id.id),
                ('id', '>', last_message_id)
            ]
            
            messages = request.env['mail.message'].search(domain, order='date asc')
            
            message_list = []
            for msg in messages:
                role = 'assistant' if msg.author_id.email == 'ai-bot@patco.com.pe' else 'user'
                
                message_list.append({
                    'id': msg.id,
                    'role': role,
                    'content': msg.body,
                    'timestamp': msg.date.isoformat(),
                    'author_name': msg.author_id.name,
                    'has_attachments': bool(msg.attachment_ids)
                })
            
            return {
                'success': True,
                'messages': message_list,
                'last_message_id': messages[-1].id if messages else last_message_id
            }
            
        except Exception as e:
            _logger.error(f"Error obteniendo mensajes móvil: {e}")
            return {'success': False, 'error': str(e)}