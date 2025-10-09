# -*- coding: utf-8 -*-

class AIResponseTemplates:
    """Plantillas de respuesta para el asistente IA PATCO"""
    
    @staticmethod
    def no_active_order_response(user_name, active_orders_count=0):
        """Respuesta cuando no hay orden FSM activa"""
        
        if active_orders_count == 0:
            return f"""
🤖 **Hola {user_name}, soy el Asistente IA de PATCO** 👋

Gracias por contactarme. He revisado tu perfil y actualmente **no tienes órdenes de servicio activas asignadas**.

📋 **¿Cómo funciona el sistema?**
• El asistente IA está diseñado para apoyarte durante el trabajo en campo
• Necesitas tener una **orden de servicio activa** para poder conversar conmigo
• Una vez asignada una orden, podrás preguntarme sobre:
  - Información del cliente y equipos
  - Procedimientos técnicos
  - Registro de actividades
  - Consultas sobre el servicio

💡 **¿Qué puedes hacer ahora?**
• Contacta con tu supervisor para que te asigne una orden de servicio
• Revisa el módulo de **Órdenes de Servicio** en el sistema
• Una vez tengas una orden activa, podrás conversar conmigo desde el chat de esa orden

¡Estaré aquí para ayudarte cuando tengas una orden de servicio asignada! 🔧⚡
            """.strip()
        
        else:
            return f"""
🤖 **Hola {user_name}, soy el Asistente IA de PATCO** 👋

Veo que tienes **{active_orders_count} orden(es) de servicio activa(s)**, pero estás escribiendo desde el chat general.

📋 **Para una mejor experiencia:**
• Ve a la **orden de servicio específica** en la que estás trabajando
• Desde ahí podrás acceder al **chat de la orden** donde podré ayudarte con:
  - Información detallada del cliente y equipos
  - Procedimientos específicos para esa orden
  - Registro de actividades y observaciones
  - Consultas técnicas contextualizadas

💡 **¿Cómo acceder al chat de la orden?**
1. Ve al módulo **Órdenes de Servicio**
2. Abre la orden en la que estás trabajando
3. Busca el botón **"Chat IA"** o la pestaña **"Conversación"**

¡Te espero en el chat de tu orden de servicio para brindarte la mejor asistencia! 🔧⚡
            """.strip()
    
    @staticmethod
    def permission_denied_response(error_message):
        """Respuesta cuando no se tienen permisos"""
        
        return f"""
❌ **Acceso Denegado**

{error_message}

💡 **¿Necesitas ayuda?**
• Contacta con tu supervisor
• Verifica que tengas los permisos correctos
• Asegúrate de estar asignado a la orden de servicio

Si el problema persiste, contacta al administrador del sistema.
        """.strip()
    
    @staticmethod
    def system_error_response():
        """Respuesta cuando hay error del sistema"""
        
        return f"""
⚠️ **Error Temporal del Sistema**

Lo siento, estoy experimentando dificultades técnicas en este momento.

💡 **¿Qué puedes hacer?**
• Intenta nuevamente en unos minutos
• Si el problema persiste, contacta al soporte técnico
• Mientras tanto, puedes continuar con tu trabajo y registrar manualmente las actividades

¡Estaré disponible nuevamente pronto! 🔧
        """.strip()
    
    @staticmethod
    def welcome_fsm_order_response(fsm_order_name, client_name, technician_name):
        """Respuesta de bienvenida para orden FSM"""
        
        return f"""
🤖 **¡Hola {technician_name}!** 👋

Estoy aquí para asistirte con la **{fsm_order_name}** para el cliente **{client_name}**.

💡 **¿En qué puedo ayudarte?**
• Información sobre equipos y especificaciones técnicas
• Procedimientos y protocolos de servicio
• Registro de actividades y observaciones
• Consultas sobre el historial del cliente
• Recomendaciones técnicas

¡Pregúntame lo que necesites para completar exitosamente tu servicio! 🔧⚡
        """.strip()