from odoo import models, fields, api
import logging
import requests
import json

_logger = logging.getLogger(__name__)

class MailMessage(models.Model):
    _inherit = 'mail.message'
    
    x_processed_by_ai = fields.Boolean('Procesado por IA', default=False)
    x_ai_response_pending = fields.Boolean('Respuesta IA Pendiente', default=False)
    
    @api.model_create_multi
    def create(self, vals_list):
        """Sobrescribir create para detectar mensajes en canales IA"""
        
        messages = super().create(vals_list)
        
        # Procesar mensajes en canales IA
        for message in messages:
            if message._should_process_with_ai():
                message._process_message_with_ai()
        
        return messages
    
    def _should_process_with_ai(self):
        """Determina si un mensaje debe ser procesado por el agente IA usando Strategy pattern"""
        from .conversation_strategy import ConversationProcessor
        
        processor = ConversationProcessor(self.env, self)
        return processor.should_process_with_ai()
    
    def _process_message_with_ai(self):
        """Procesa el mensaje con el agente IA usando Strategy pattern"""
        from .conversation_strategy import ConversationProcessor
        
        processor = ConversationProcessor(self.env, self)
        return processor.process_message()
    
    # Método legacy mantenido para compatibilidad
    def _send_to_langgraph_server(self, context):
        """Método legacy - ahora manejado por ConversationProcessor"""
        _logger.warning("Método _send_to_langgraph_server es legacy - usar ConversationProcessor")
        return False
    
    # Métodos legacy mantenidos para compatibilidad
    def _send_ai_response(self, response_text, context):
        """Método legacy - ahora manejado por ConversationProcessor"""
        _logger.warning("Método _send_ai_response es legacy - usar ConversationProcessor")
        return False
    
    def _execute_ai_actions(self, actions, context):
        """Método legacy - ahora manejado por ConversationProcessor"""
        _logger.warning("Método _execute_ai_actions es legacy - usar ConversationProcessor")
        return False