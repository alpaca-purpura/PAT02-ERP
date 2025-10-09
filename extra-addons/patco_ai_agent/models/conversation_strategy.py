# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from odoo import models, fields, api
from .ai_response_templates import AIResponseTemplates
import logging

_logger = logging.getLogger(__name__)


class ConversationStrategy(ABC):
    """Estrategia abstracta para manejo de contextos de conversación"""
    
    def __init__(self, env, channel, author):
        self.env = env
        self.channel = channel
        self.author = author
    
    @abstractmethod
    def should_process(self):
        """Determina si este tipo de conversación debe procesarse"""
        pass
    
    @abstractmethod
    def prepare_context(self):
        """Prepara el contexto específico para el agente IA"""
        pass
    
    @abstractmethod
    def get_conversation_id(self):
        """Genera ID único para la conversación"""
        pass
    
    @abstractmethod
    def validate_permissions(self):
        """Valida permisos y condiciones para la conversación"""
        pass


class FSMConversationStrategy(ConversationStrategy):
    """Estrategia para conversaciones vinculadas a órdenes FSM"""
    
    def __init__(self, env, channel, author):
        super().__init__(env, channel, author)
        self.fsm_order = self._find_fsm_order()
    
    def _find_fsm_order(self):
        """Busca orden FSM asociada al canal"""
        return self.env['fsm.order'].search([
            ('x_ai_channel_id', '=', self.channel.id),
            ('x_ai_status', '=', 'active')
        ], limit=1)
    
    def should_process(self):
        """Procesa si hay orden FSM activa"""
        return bool(self.fsm_order)
    
    def prepare_context(self):
        """Prepara contexto completo de orden FSM"""
        if not self.fsm_order:
            return {}
        
        context = {
            'conversation_type': 'fsm_order',
            'fsm_order_id': self.fsm_order.id,
            'fsm_order_name': self.fsm_order.name,
            'technician_id': self.fsm_order.person_id.id,
            'technician_name': self.fsm_order.person_id.name,
            'client_name': self.fsm_order.partner_id.name,
            'equipment_ids': self.fsm_order.equipment_ids.ids,
            'channel_id': self.channel.id,
            'has_active_order': True
        }
        
        # Agregar información adicional si existe
        if hasattr(self.fsm_order, 'x_service_nature_id') and self.fsm_order.x_service_nature_id:
            context['service_nature'] = self.fsm_order.x_service_nature_id.name
            context['service_nature_id'] = self.fsm_order.x_service_nature_id.id
        
        if hasattr(self.fsm_order, 'x_service_area_id') and self.fsm_order.x_service_area_id:
            context['service_area'] = self.fsm_order.x_service_area_id.name
            context['service_area_id'] = self.fsm_order.x_service_area_id.id
        
        if hasattr(self.fsm_order, 'x_service_complexity_id') and self.fsm_order.x_service_complexity_id:
            context['complexity'] = self.fsm_order.x_service_complexity_id.name
            context['complexity_id'] = self.fsm_order.x_service_complexity_id.id
        
        return context
    
    def get_conversation_id(self):
        """ID basado en orden FSM"""
        return f"fsm_{self.fsm_order.id}" if self.fsm_order else None
    
    def validate_permissions(self):
        """Valida que el usuario tenga acceso a la orden"""
        if not self.fsm_order:
            return False, "No se encontró orden FSM activa"
        
        # Verificar que el usuario sea el técnico asignado o tenga permisos
        user = self.env.user
        if (self.fsm_order.person_id.user_id.id != user.id and 
            not user.has_group('fieldservice.group_fsm_manager')):
            return False, "No tienes permisos para esta orden de servicio"
        
        return True, "Permisos validados correctamente"


class DirectConversationStrategy(ConversationStrategy):
    """Estrategia para conversaciones directas con el asistente IA"""
    
    def should_process(self):
        """Siempre procesa conversaciones directas con el AI partner"""
        ai_partner = self.env.ref('patco_ai_agent.ai_agent_partner', raise_if_not_found=False)
        return ai_partner and ai_partner.id in self.channel.channel_partner_ids.ids
    
    def prepare_context(self):
        """Prepara contexto para conversación directa"""
        # Buscar órdenes FSM activas del usuario
        active_orders = self._get_user_active_orders()
        
        context = {
            'conversation_type': 'direct_chat',
            'user_id': self.author.id,
            'user_name': self.author.name,
            'channel_id': self.channel.id,
            'has_active_order': len(active_orders) > 0,
            'active_orders_count': len(active_orders),
            'active_orders': [
                {
                    'id': order.id,
                    'name': order.name,
                    'partner_name': order.partner_id.name,
                    'equipment_count': len(order.equipment_ids)
                } for order in active_orders
            ]
        }
        
        return context
    
    def _get_user_active_orders(self):
        """Obtiene órdenes FSM activas del usuario actual"""
        user = self.env.user
        
        # Buscar órdenes donde el usuario es el técnico asignado
        orders = self.env['fsm.order'].search([
            ('person_id.user_id', '=', user.id),
            ('stage_id.is_closed', '=', False)  # Órdenes no cerradas
        ])
        
        return orders
    
    def get_conversation_id(self):
        """ID basado en usuario para conversación directa"""
        return f"direct_{self.author.id}"
    
    def validate_permissions(self):
        """Valida permisos básicos para conversación directa"""
        if not self.author:
            return False, "Usuario no identificado"
        
        # Verificar que el usuario tenga permisos básicos de FSM
        if not self.env.user.has_group('fieldservice.group_fsm_user'):
            return False, "No tienes permisos para usar el asistente IA"
        
        return True, "Permisos validados para conversación directa"


class ConversationContextFactory:
    """Factory para crear la estrategia de conversación apropiada"""
    
    @staticmethod
    def create_strategy(env, channel, author):
        """Crea la estrategia apropiada basada en el contexto"""
        
        # Intentar estrategia FSM primero
        fsm_strategy = FSMConversationStrategy(env, channel, author)
        if fsm_strategy.should_process():
            return fsm_strategy
        
        # Si no hay orden FSM, usar estrategia directa
        direct_strategy = DirectConversationStrategy(env, channel, author)
        if direct_strategy.should_process():
            return direct_strategy
        
        # Si ninguna estrategia aplica, retornar None
        return None


class ConversationProcessor:
    """Procesador principal que utiliza las estrategias"""
    
    def __init__(self, env, message):
        self.env = env
        self.message = message
        self.channel = env['discuss.channel'].browse(message.res_id)
        self.author = message.author_id
    
    def should_process_with_ai(self):
        """Determina si el mensaje debe procesarse con IA usando estrategias"""
        
        # Filtros básicos
        if not self._basic_validation():
            return False
        
        # Obtener estrategia apropiada
        strategy = ConversationContextFactory.create_strategy(
            self.env, self.channel, self.author
        )
        
        return strategy is not None
    
    def process_message(self):
        """Procesa el mensaje usando la estrategia apropiada"""
        
        try:
            # Obtener estrategia
            strategy = ConversationContextFactory.create_strategy(
                self.env, self.channel, self.author
            )
            
            if not strategy:
                _logger.warning(f"No se encontró estrategia para mensaje {self.message.id}")
                return False
            
            # Validar permisos
            is_valid, validation_message = strategy.validate_permissions()
            if not is_valid:
                self._send_validation_error(validation_message)
                return False
            
            # Preparar contexto
            context = strategy.prepare_context()
            conversation_id = strategy.get_conversation_id()
            
            # Para conversaciones directas sin orden activa, enviar mensaje informativo
            if (isinstance(strategy, DirectConversationStrategy) and 
                not context.get('has_active_order', False)):
                
                response = AIResponseTemplates.no_active_order_response(
                    self.author.name, 
                    context.get('active_orders_count', 0)
                )
                self._send_direct_response(response)
                return True
            
            # Para conversaciones directas con órdenes activas, informar sobre el uso correcto
            elif (isinstance(strategy, DirectConversationStrategy) and 
                  context.get('has_active_order', False)):
                
                response = AIResponseTemplates.no_active_order_response(
                    self.author.name, 
                    context.get('active_orders_count', 0)
                )
                self._send_direct_response(response)
                return True
            
            # Para conversaciones FSM, procesar normalmente
            else:
                # Marcar como procesándose
                self.message.x_ai_response_pending = True
                
                # Enviar al servidor LangGraph
                return self._send_to_langgraph_server(conversation_id, context)
            
        except Exception as e:
            _logger.error(f"Error procesando mensaje con estrategia: {e}")
            self.message.x_ai_response_pending = False
            return False
    
    def _basic_validation(self):
        """Validaciones básicas del mensaje"""
        
        # No procesar mensajes del bot
        if self.author and self.author.email == 'ai-bot@patco.com.pe':
            return False
        
        # Solo procesar mensajes en canales
        if self.message.model != 'discuss.channel':
            return False
        
        return True
    
    def _send_direct_response(self, response_text):
        """Envía respuesta directa al canal sin procesar con LangGraph"""
        
        try:
            bot = self.env['ai.bot.user'].get_or_create_bot_user()
            
            self.channel.with_user(bot.user_id).message_post(
                body=response_text,
                message_type='comment',
                subtype_xmlid='mail.mt_comment'
            )
            
            _logger.info(f"Respuesta directa enviada al canal {self.channel.id}")
            
        except Exception as e:
            _logger.error(f"Error enviando respuesta directa: {e}")
    
    def _send_validation_error(self, error_message):
        """Envía mensaje de error de validación al canal"""
        
        try:
            bot = self.env['ai.bot.user'].get_or_create_bot_user()
            
            error_response = f"""
            ❌ **{error_message}**
            
            Si necesitas ayuda, contacta con tu supervisor o administrador del sistema.
            """
            
            self.channel.with_user(bot.user_id).message_post(
                body=error_response,
                message_type='comment',
                subtype_xmlid='mail.mt_comment'
            )
            
        except Exception as e:
            _logger.error(f"Error enviando mensaje de validación: {e}")
    
    def _send_to_langgraph_server(self, conversation_id, context):
        """Envía mensaje al servidor LangGraph"""
        
        try:
            import requests
            import json
            
            langgraph_url = self.env['ir.config_parameter'].sudo().get_param(
                'patco_ai_agent.langgraph_server_url', 
                'http://langgraph-server:8001'
            )
            
            payload = {
                'conversation_id': conversation_id,
                'message': {
                    'role': 'user',
                    'content': self.message.body,
                    'timestamp': self.message.date.isoformat(),
                    'author_id': self.author.id,
                    'author_name': self.author.name
                },
                'context': context
            }
            
            response = requests.post(
                f"{langgraph_url}/conversation/{conversation_id}/message",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Procesar respuesta
                if result.get('response'):
                    self._send_ai_response(result['response'])
                
                # Ejecutar acciones si las hay
                if result.get('actions'):
                    self._execute_ai_actions(result['actions'], context)
                
                self.message.x_processed_by_ai = True
                self.message.x_ai_response_pending = False
                return True
                
            else:
                _logger.error(f"Error en servidor LangGraph: {response.status_code}")
                self.message.x_ai_response_pending = False
                return False
                
        except Exception as e:
            _logger.error(f"Error enviando a LangGraph: {e}")
            self.message.x_ai_response_pending = False
            return False
    
    def _send_ai_response(self, response_text):
        """Envía respuesta del agente IA al canal"""
        
        try:
            bot = self.env['ai.bot.user'].get_or_create_bot_user()
            
            self.channel.with_user(bot.user_id).message_post(
                body=response_text,
                message_type='comment',
                subtype_xmlid='mail.mt_comment'
            )
            
        except Exception as e:
            _logger.error(f"Error enviando respuesta IA: {e}")
    
    def _execute_ai_actions(self, actions, context):
        """Ejecuta acciones solicitadas por el agente IA"""
        
        try:
            for action in actions:
                action_type = action.get('type')
                
                if action_type == 'update_fsm_order' and context.get('fsm_order_id'):
                    fsm_order = self.env['fsm.order'].browse(context['fsm_order_id'])
                    values = action.get('values', {})
                    if values and fsm_order.exists():
                        fsm_order.write(values)
                        _logger.info(f"Orden FSM {fsm_order.name} actualizada por IA: {values}")
                
                elif action_type == 'suggest_order_selection':
                    # Para conversaciones directas, sugerir selección de orden
                    _logger.info(f"IA sugiere selección de orden para usuario {context.get('user_name')}")
                
                # Agregar más tipos de acciones según necesidad
                
        except Exception as e:
            _logger.error(f"Error ejecutando acciones IA: {e}")