# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
import requests
import json
from datetime import datetime

_logger = logging.getLogger(__name__)


class AIConversation(models.Model):
    _name = 'ai.conversation'
    _description = 'Conversación con Agente IA'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    name = fields.Char('Nombre', compute='_compute_name', store=True)
    fsm_order_id = fields.Many2one('fsm.order', 'Orden FSM', required=True, tracking=True)
    technician_id = fields.Many2one('hr.employee', 'Técnico', required=True, tracking=True)
    channel_id = fields.Many2one('discuss.channel', 'Canal de Conversación')
    
    state = fields.Selection([
        ('initiated', 'Iniciado'),
        ('equipment_selected', 'Equipo Seleccionado'),
        ('checklist_entry', 'Checklist de Entrada'),
        ('work_in_progress', 'Trabajo en Progreso'),
        ('checklist_exit', 'Checklist de Salida'),
        ('report_generated', 'Reporte Generado'),
        ('completed', 'Completado'),
        ('archived', 'Archivado')
    ], default='initiated', tracking=True, string='Estado de Conversación')
    
    current_equipment_id = fields.Many2one('maintenance.equipment', 'Equipo Actual', tracking=True)
    context_data = fields.Json('Datos de Contexto', default=dict,
                              help='Contexto de la conversación para el agente IA')
    conversation_summary = fields.Text('Resumen de Conversación',
                                     help='Resumen automático generado por IA')
    
    # Métricas básicas
    message_count = fields.Integer('Número de Mensajes', default=0, compute='_compute_metrics', store=True)
    start_time = fields.Datetime('Hora de Inicio', default=fields.Datetime.now, tracking=True)
    end_time = fields.Datetime('Hora de Finalización', tracking=True)
    duration = fields.Float('Duración (horas)', compute='_compute_duration', store=True,
                           help='Duración total de la conversación en horas')
    
    # Resultados
    report_url = fields.Char('URL del Reporte', help='URL del reporte generado automáticamente')
    report_generated = fields.Boolean('Reporte Generado', default=False, tracking=True)
    
    # Campos adicionales para reportes OnlyOffice
    report_attachment_id = fields.Many2one(
        'ir.attachment', 
        string='Archivo de Reporte',
        help='Documento de reporte técnico generado automáticamente'
    )
    report_template_type = fields.Selection([
        ('servicio_general', 'Servicio General'),
        ('mantenimiento_preventivo', 'Mantenimiento Preventivo'),
        ('mantenimiento_correctivo', 'Mantenimiento Correctivo'),
        ('instalacion_equipo', 'Instalación de Equipo'),
        ('calibracion_tecnica', 'Calibración Técnica'),
        ('inspeccion_tecnica', 'Inspección Técnica')
    ], string='Tipo de Plantilla', default='servicio_general')
    
    report_generation_status = fields.Selection([
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('completed', 'Completado'),
        ('failed', 'Fallido')
    ], string='Estado de Generación', default='pending')
    
    report_error_message = fields.Text('Error de Generación')
    
    # Campos relacionados para facilitar búsquedas (comentados temporalmente para Fase 1)
    # partner_id = fields.Many2one(related='fsm_order_id.partner_id', string='Cliente', store=True, readonly=True)
    # location_id = fields.Many2one(related='fsm_order_id.location_id', string='Ubicación', store=True, readonly=True)
    # service_nature_id = fields.Many2one(related='fsm_order_id.x_service_nature_id', 
    #                                    string='Naturaleza del Servicio', store=True, readonly=True)
    
    @api.depends('fsm_order_id', 'technician_id')
    def _compute_name(self):
        """Computa el nombre de la conversación"""
        for record in self:
            if record.fsm_order_id and record.technician_id:
                record.name = f"IA-{record.fsm_order_id.name}-{record.technician_id.name}"
            else:
                record.name = "Nueva Conversación IA"
    
    @api.depends('channel_id.message_ids')
    def _compute_metrics(self):
        """Computa métricas de la conversación"""
        for record in self:
            if record.channel_id:
                # Contar mensajes del canal
                record.message_count = len(record.channel_id.message_ids)
            else:
                record.message_count = 0
    
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        """Computa la duración de la conversación"""
        for record in self:
            if record.start_time and record.end_time:
                delta = record.end_time - record.start_time
                record.duration = delta.total_seconds() / 3600.0
            else:
                record.duration = 0.0
    
    def action_start_conversation(self):
        """Inicia la conversación con el agente IA"""
        self.ensure_one()
        
        # Crear canal de discuss si no existe
        if not self.channel_id:
            channel = self.env['discuss.channel'].create({
                'name': f"🤖 Asistente IA - {self.fsm_order_id.name}",
                'channel_type': 'chat',
                'channel_partner_ids': [(4, self.technician_id.user_id.partner_id.id)]
            })
            self.channel_id = channel.id
        
        # Enviar mensaje inicial
        self._send_initial_message()
        
        # Actualizar estado
        self.state = 'equipment_selected'
        
        _logger.info(f"Conversación IA iniciada: {self.name}")
    
    def action_generate_report(self):
        """Acción manual para generar reporte"""
        self.ensure_one()
        
        if self.state not in ['work_in_progress', 'checklist_exit', 'completed']:
            raise UserError("La conversación debe estar en progreso o completada para generar reporte")
        
        # Llamar al servicio LangGraph para generar reporte
        self._trigger_report_generation()
    
    def _trigger_report_generation(self):
        """Dispara la generación de reporte vía LangGraph"""
        
        try:
            # URL del servidor LangGraph
            langgraph_url = self.env['ir.config_parameter'].sudo().get_param(
                'patco_ai_agent.langgraph_server_url', 
                'http://langgraph-server:8001'
            )
            
            # Preparar contexto para LangGraph
            context = self._prepare_report_context()
            
            # Preparar historial de mensajes
            messages = self._get_conversation_messages()
            
            # Payload para LangGraph
            payload = {
                "conversation_id": f"report_{self.id}",
                "action": "generate_report",
                "context": context,
                "messages": messages
            }
            
            # Actualizar estado
            self.report_generation_status = 'processing'
            
            # Llamada asíncrona a LangGraph
            response = requests.post(
                f"{langgraph_url}/conversation/{self.id}/generate_report",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self._handle_report_generation_success(result)
                else:
                    self._handle_report_generation_error(result.get("error", "Error desconocido"))
            else:
                self._handle_report_generation_error(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            _logger.error(f"Error disparando generación de reporte: {e}")
            self._handle_report_generation_error(str(e))
    
    def _prepare_report_context(self):
        """Prepara contexto para generación de reporte"""
        
        return {
            "fsm_order_id": self.fsm_order_id.id,
            "fsm_order": {
                "name": self.fsm_order_id.name,
                "partner_id": self.fsm_order_id.partner_id.name,
                "location_id": self.fsm_order_id.location_id.name if self.fsm_order_id.location_id else None,
                "service_nature": self.fsm_order_id.x_service_nature_id.name if self.fsm_order_id.x_service_nature_id else None,
                "service_area": self.fsm_order_id.x_service_area_id.name if self.fsm_order_id.x_service_area_id else None,
                "equipment_ids": [eq.id for eq in self.fsm_order_id.equipment_ids]
            },
            "technician_id": self.technician_id.id,
            "technician_name": self.technician_id.name,
            "conversation_id": self.id,
            "template_type": self.report_template_type,
            "equipment_category": self.current_equipment_id.category_id.name if self.current_equipment_id else None
        }
    
    def _get_conversation_messages(self):
        """Obtiene mensajes de la conversación desde discuss.channel"""
        
        messages = []
        if self.channel_id:
            # Obtener mensajes del canal
            channel_messages = self.env['mail.message'].search([
                ('res_id', '=', self.channel_id.id),
                ('model', '=', 'discuss.channel'),
                ('message_type', '=', 'comment')
            ], order='create_date asc')
            
            for msg in channel_messages:
                # Determinar rol del mensaje
                role = "assistant" if msg.author_id.name == "🤖 Asistente IA PATCO" else "user"
                
                messages.append({
                    "role": role,
                    "content": msg.body,
                    "timestamp": msg.create_date.isoformat(),
                    "author": msg.author_id.name
                })
        
        return messages
    
    def _handle_report_generation_success(self, result):
        """Maneja éxito en generación de reporte"""
        
        try:
            # Crear attachment si se proporcionó contenido
            if result.get("attachment_id"):
                attachment = self.env['ir.attachment'].browse(result["attachment_id"])
                if attachment.exists():
                    self.report_attachment_id = attachment.id
            
            # Actualizar estado
            self.report_generation_status = 'completed'
            self.state = 'report_generated'
            self.report_generated = True
            
            # Notificar en el canal
            if self.channel_id:
                self.channel_id.message_post(
                    body=f"✅ Reporte técnico generado exitosamente: {result.get('filename', 'reporte.docx')}",
                    message_type='notification'
                )
            
            _logger.info(f"Reporte generado exitosamente para conversación {self.id}")
            
        except Exception as e:
            _logger.error(f"Error procesando éxito de reporte: {e}")
            self._handle_report_generation_error(str(e))
    
    def _handle_report_generation_error(self, error_message):
        """Maneja error en generación de reporte"""
        
        self.report_generation_status = 'failed'
        self.report_error_message = error_message
        
        # Notificar error en el canal
        if self.channel_id:
            self.channel_id.message_post(
                body=f"❌ Error generando reporte: {error_message}",
                message_type='notification'
            )
        
        _logger.error(f"Error generando reporte para conversación {self.id}: {error_message}")
    
    def action_view_report(self):
        """Acción para ver el reporte generado"""
        self.ensure_one()
        
        if not self.report_attachment_id:
            raise UserError("No hay reporte generado para esta conversación")
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self.report_attachment_id.id}?download=true',
            'target': 'new'
        }
    
    def action_regenerate_report(self):
        """Acción para regenerar reporte"""
        self.ensure_one()
        
        # Limpiar reporte anterior
        if self.report_attachment_id:
            self.report_attachment_id.unlink()
            self.report_attachment_id = False
        
        self.report_generation_status = 'pending'
        self.report_error_message = False
        
        # Generar nuevo reporte
        self._trigger_report_generation()
        
        return self.action_open_conversation()
    
    def _send_initial_message(self):
        """Envía mensaje inicial del agente IA"""
        message = f"""
        ¡Hola {self.technician_id.name}! 👋
        
        Soy tu asistente IA para la orden de servicio **{self.fsm_order_id.name}**.
        
        📋 **Detalles del servicio:**
        - Cliente: {self.fsm_order_id.partner_id.name}
        - Ubicación: {self.fsm_order_id.location_id.name if self.fsm_order_id.location_id else 'No especificada'}
        - Equipos asignados: {len(self.fsm_order_id.equipment_ids)} equipos
        - Naturaleza: {self.fsm_order_id.x_service_nature_id.name if self.fsm_order_id.x_service_nature_id else 'No especificada'}
        
        Te ayudaré durante todo el proceso. ¿Has llegado al sitio y estás listo para comenzar?
        """
        
        # Crear partner para el agente IA si no existe
        ai_partner = self.env.ref('patco_ai_agent.ai_agent_partner', raise_if_not_found=False)
        if not ai_partner:
            ai_partner = self.env['res.partner'].create({
                'name': '🤖 Asistente IA PATCO',
                'is_company': False,
                'email': 'ai-agent@patco.com.pe',
                'phone': '+51-1-234-5678',
                'supplier_rank': 0,
                'customer_rank': 0
            })
            # Crear referencia externa
            self.env['ir.model.data'].create({
                'name': 'ai_agent_partner',
                'module': 'patco_ai_agent',
                'model': 'res.partner',
                'res_id': ai_partner.id,
            })
        
        self.channel_id.message_post(
            body=message,
            author_id=ai_partner.id,
            message_type='comment'
        )
    
    def action_open_conversation(self):
        """Abre la conversación en el chat"""
        self.ensure_one()
        
        if not self.channel_id:
            raise UserError("No hay canal de conversación asociado")
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Conversación IA - {self.fsm_order_id.name}',
            'res_model': 'discuss.channel',
            'res_id': self.channel_id.id,
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'active_id': self.channel_id.id,
                'default_res_model': 'discuss.channel',
                'default_res_id': self.channel_id.id,
            }
        }
    
    def action_complete_conversation(self):
        """Completa la conversación y genera reporte"""
        self.ensure_one()
        
        if self.state == 'completed':
            raise UserError("La conversación ya está completada")
        
        # Actualizar tiempos
        self.end_time = fields.Datetime.now()
        
        # Cambiar estado
        self.state = 'completed'
        
        # Enviar mensaje de finalización
        self._send_completion_message()
        
        _logger.info(f"Conversación IA completada: {self.name}")
        
        return True
    
    def _send_completion_message(self):
        """Envía mensaje de finalización"""
        if not self.channel_id:
            return
        
        message = f"""
        ✅ **Conversación completada**
        
        Resumen del servicio:
        - Duración: {self.duration:.2f} horas
        - Mensajes intercambiados: {self.message_count}
        - Estado final: {dict(self._fields['state'].selection)[self.state]}
        
        ¡Gracias por usar el asistente IA PATCO! 🤖
        """
        
        ai_partner = self.env.ref('patco_ai_agent.ai_agent_partner', raise_if_not_found=False)
        if ai_partner:
            self.channel_id.message_post(
                body=message,
                author_id=ai_partner.id,
                message_type='comment'
            )
    
    def action_archive_conversation(self):
        """Archiva la conversación"""
        self.ensure_one()
        
        if self.state != 'completed':
            raise UserError("Solo se pueden archivar conversaciones completadas")
        
        self.state = 'archived'
        
        _logger.info(f"Conversación IA archivada: {self.name}")
        
    def search_knowledge_base(self, query, **kwargs):
        """
        Busca en la base de conocimiento usando el contexto de la conversación.
        
        Args:
            query: Consulta de búsqueda
            **kwargs: Parámetros adicionales de búsqueda
            
        Returns:
            Resultados de búsqueda con contexto aplicado
        """
        
        # Construir contexto desde la conversación
        context = self._build_search_context()
        
        # Usar el servicio RAG avanzado
        from ..services.vector_service import VectorSearchService
        
        vector_service = VectorSearchService(self.env)
        results = vector_service.search_knowledge_base(
            query=query,
            context=context,
            **kwargs
        )
        
        # Registrar la búsqueda en el contexto de la conversación
        self._log_search_activity(query, len(results))
        
        return results
    
    def _build_search_context(self):
        """Construye contexto de búsqueda desde la conversación actual"""
        
        context = {}
        
        # Información de la orden FSM
        if self.fsm_order_id:
            context.update({
                'fsm_order_id': self.fsm_order_id.id,
                'fsm_state': self.fsm_order_id.stage_id.name if self.fsm_order_id.stage_id else None,
                'equipment_ids': self.fsm_order_id.equipment_ids.ids,
                'service_nature_id': self.fsm_order_id.x_service_nature_id.id if self.fsm_order_id.x_service_nature_id else None,
                'service_area_id': self.fsm_order_id.x_service_area_id.id if self.fsm_order_id.x_service_area_id else None,
                'service_complexity_id': self.fsm_order_id.x_service_complexity_id.id if self.fsm_order_id.x_service_complexity_id else None,
            })
            
            # Categorías de equipos
            if self.fsm_order_id.equipment_ids:
                equipment_categories = self.fsm_order_id.equipment_ids.mapped('category_id.id')
                if equipment_categories:
                    context['equipment_category_ids'] = equipment_categories
                    # Si hay una sola categoría, usarla como principal
                    if len(equipment_categories) == 1:
                        context['equipment_category_id'] = equipment_categories[0]
        
        # Información del equipo actual
        if self.current_equipment_id:
            context.update({
                'current_equipment_id': self.current_equipment_id.id,
                'equipment_category_id': self.current_equipment_id.category_id.id if self.current_equipment_id.category_id else None,
            })
        
        # Estado de la conversación
        context['conversation_state'] = self.state
        
        # Información del técnico
        if self.technician_id:
            context.update({
                'technician_id': self.technician_id.id,
                'technician_skills': self.technician_id.x_skill_ids.ids if hasattr(self.technician_id, 'x_skill_ids') else []
            })
        
        # Datos adicionales del contexto JSON
        if self.context_data:
            context.update(self.context_data)
        
        return context
    
    def _log_search_activity(self, query, results_count):
        """Registra actividad de búsqueda en el contexto de la conversación"""
        
        if not self.context_data:
            self.context_data = {}
        
        if 'search_history' not in self.context_data:
            self.context_data['search_history'] = []
        
        # Agregar búsqueda al historial
        search_entry = {
            'timestamp': fields.Datetime.now().isoformat(),
            'query': query,
            'results_count': results_count,
            'conversation_state': self.state
        }
        
        self.context_data['search_history'].append(search_entry)
        
        # Mantener solo las últimas 10 búsquedas
        if len(self.context_data['search_history']) > 10:
            self.context_data['search_history'] = self.context_data['search_history'][-10:]
        
        # Actualizar estadísticas
        if 'search_stats' not in self.context_data:
            self.context_data['search_stats'] = {
                'total_searches': 0,
                'total_results': 0
            }
        
        self.context_data['search_stats']['total_searches'] += 1
        self.context_data['search_stats']['total_results'] += results_count
    
    def action_complete_conversation(self):
        """Completa la conversación IA"""
        self.ensure_one()
        
        if self.state == 'completed':
            raise UserError("La conversación ya está completada")
        
        # Actualizar estado y tiempo de finalización
        self.write({
            'state': 'completed',
            'end_time': fields.Datetime.now()
        })
        
        # Enviar mensaje de finalización
        self._send_completion_message()
        
        _logger.info(f"Conversación IA completada: {self.name}")
        
        return True
    
    @api.model
    def create_service_conversation(self, fsm_order):
        """Crea conversación automática para una orden FSM"""
        if not fsm_order.person_id:
            _logger.warning(f"No se puede crear conversación IA para orden {fsm_order.name}: sin técnico asignado")
            return False
        
        # Verificar si ya existe conversación activa
        existing = self.search([
            ('fsm_order_id', '=', fsm_order.id),
            ('state', 'not in', ['completed', 'archived'])
        ], limit=1)
        
        if existing:
            _logger.info(f"Ya existe conversación IA activa para orden {fsm_order.name}")
            return existing
        
        # Crear nueva conversación
        conversation = self.create({
            'fsm_order_id': fsm_order.id,
            'technician_id': fsm_order.person_id.id,
            'context_data': {
                'equipment_ids': fsm_order.equipment_ids.ids,
                'service_nature_id': fsm_order.x_service_nature_id.id if fsm_order.x_service_nature_id else None,
                'service_area_id': fsm_order.x_service_area_id.id if fsm_order.x_service_area_id else None,
                'complexity_id': fsm_order.x_service_complexity_id.id if fsm_order.x_service_complexity_id else None,
                'created_automatically': True
            }
        })
        
        _logger.info(f"Conversación IA creada automáticamente: {conversation.name}")
        
        return conversation
    
    def _process_ai_message(self, message, actions=None):
        """Procesa mensaje recibido desde el agente IA"""
        self.ensure_one()
        
        if not self.channel_id:
            return False
        
        # Obtener partner del agente IA
        ai_partner = self.env.ref('patco_ai_agent.ai_agent_partner', raise_if_not_found=False)
        if not ai_partner:
            return False
        
        # Enviar mensaje al canal
        new_message = self.channel_id.message_post(
            body=message,
            author_id=ai_partner.id,
            message_type='comment'
        )
        
        # Notificar a los usuarios del canal para actualización en tiempo real
        if self.channel_id.channel_partner_ids:
            # Enviar notificación del bus para actualizar la interfaz automáticamente
            self.env['bus.bus']._sendone(
                self.channel_id.channel_partner_ids[0],  # Partner del técnico
                'discuss.channel/new_message',
                {
                    'id': new_message.id,
                    'channel_id': self.channel_id.id,
                    'body': message,
                    'author_id': ai_partner.id,
                    'author_name': ai_partner.name,
                    'date': new_message.date.isoformat(),
                    'message_type': 'comment'
                }
            )
        
        # Procesar acciones si las hay
        if actions:
            self._execute_ai_actions(actions)
        
        return True
    
    def _execute_ai_actions(self, actions):
        """Ejecuta acciones solicitadas por el agente IA"""
        self.ensure_one()
        
        for action in actions:
            action_type = action.get('type')
            
            if action_type == 'update_state':
                new_state = action.get('state')
                if new_state in dict(self._fields['state'].selection):
                    self.state = new_state
            
            elif action_type == 'set_equipment':
                equipment_id = action.get('equipment_id')
                if equipment_id:
                    self.current_equipment_id = equipment_id
            
            elif action_type == 'update_context':
                context_update = action.get('context', {})
                current_context = self.context_data or {}
                current_context.update(context_update)
                self.context_data = current_context
            
            elif action_type == 'generate_report':
                self._trigger_report_generation()
        
        _logger.info(f"Ejecutadas {len(actions)} acciones IA para conversación {self.name}")
    
    def _trigger_report_generation(self):
        """Dispara la generación de reporte"""
        self.ensure_one()
        
        # Por ahora solo marcar como pendiente
        # En fases posteriores se integrará con LangGraph
        self.report_generated = False
        
        _logger.info(f"Generación de reporte disparada para conversación {self.name}")
    
    def _send_message_to_ai(self, message, user_id):
        """Envía mensaje del usuario al agente IA (LangGraph server)"""
        self.ensure_one()
        
        try:
            import requests
            import json
            
            # Obtener URL del servidor LangGraph
            langgraph_url = self.env['ir.config_parameter'].sudo().get_param(
                'patco_ai_agent.langgraph_server_url', 
                'http://langgraph-server:8001'
            )
            
            # Preparar contexto para el agente IA
            context = self._prepare_ai_context()
            
            # Preparar payload para LangGraph
            payload = {
                'conversation_id': f"order-{self.fsm_order_id.id}-tech-{self.technician_id.id}",
                'message': {
                    'role': 'user',
                    'content': message,
                    'timestamp': fields.Datetime.now().isoformat()
                },
                'context': context
            }
            
            # Enviar mensaje al servidor LangGraph
            response = requests.post(
                f"{langgraph_url}/conversation/{payload['conversation_id']}/message",
                json=payload,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Registrar mensaje del usuario en el canal
                if self.channel_id:
                    self.channel_id.message_post(
                        body=message,
                        author_id=self.technician_id.user_id.partner_id.id,
                        message_type='comment'
                    )
                
                _logger.info(f"Mensaje enviado exitosamente a LangGraph desde conversación {self.name}")
                
                return {
                    'response': result.get('response', 'Respuesta recibida del agente IA'),
                    'actions': result.get('actions', []),
                    'conversation_state': result.get('conversation_state', self.state)
                }
            else:
                _logger.error(f"Error en servidor LangGraph: {response.status_code} - {response.text}")
                return {
                    'response': 'Lo siento, hay un problema temporal con el asistente IA. Inténtalo de nuevo.',
                    'actions': []
                }
                
        except requests.exceptions.RequestException as e:
            _logger.error(f"Error de conexión con LangGraph server: {e}")
            return {
                'response': 'No puedo conectar con el asistente IA en este momento. Verifica la conexión.',
                'actions': []
            }
        except Exception as e:
            _logger.error(f"Error enviando mensaje a IA: {e}")
            return {
                'response': 'Ocurrió un error inesperado. Por favor, inténtalo de nuevo.',
                'actions': []
            }
    
    def _prepare_ai_context(self):
        """Prepara contexto para el agente IA"""
        self.ensure_one()
        
        context = {
            'fsm_order_id': self.fsm_order_id.id,
            'technician_id': self.technician_id.id,
            'conversation_state': self.state,
            'equipment_ids': self.fsm_order_id.equipment_ids.ids,
        }
        
        # Agregar información de naturaleza de servicio si existe
        if hasattr(self.fsm_order_id, 'x_service_nature_id') and self.fsm_order_id.x_service_nature_id:
            context['service_nature_id'] = self.fsm_order_id.x_service_nature_id.id
            context['service_nature_name'] = self.fsm_order_id.x_service_nature_id.name
        
        # Agregar información de área de servicio si existe
        if hasattr(self.fsm_order_id, 'x_service_area_id') and self.fsm_order_id.x_service_area_id:
            context['service_area_id'] = self.fsm_order_id.x_service_area_id.id
            context['service_area_name'] = self.fsm_order_id.x_service_area_id.name
        
        # Agregar información de complejidad si existe
        if hasattr(self.fsm_order_id, 'x_service_complexity_id') and self.fsm_order_id.x_service_complexity_id:
            context['complexity_id'] = self.fsm_order_id.x_service_complexity_id.id
            context['complexity_name'] = self.fsm_order_id.x_service_complexity_id.name
        
        # Agregar información de equipos
        if self.fsm_order_id.equipment_ids:
            equipment_info = []
            for equipment in self.fsm_order_id.equipment_ids:
                equipment_info.append({
                    'id': equipment.id,
                    'name': equipment.name,
                    'category_id': equipment.category_id.id if equipment.category_id else None,
                    'category_name': equipment.category_id.name if equipment.category_id else None
                })
            context['equipment_details'] = equipment_info
            
            # Si hay un equipo actual seleccionado
            if self.current_equipment_id:
                context['current_equipment_id'] = self.current_equipment_id.id
                context['current_equipment_name'] = self.current_equipment_id.name
                if self.current_equipment_id.category_id:
                    context['equipment_category_id'] = self.current_equipment_id.category_id.id
        
        # Agregar contexto adicional almacenado
        if self.context_data:
            context.update(self.context_data)
        
        return context