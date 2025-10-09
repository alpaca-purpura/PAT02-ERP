# -*- coding: utf-8 -*-
{
    'name': 'PATCO AI Agent with RAG',
    'version': '18.0.1.0.0',
    'category': 'Artificial Intelligence',
    'summary': 'AI Agent with RAG capabilities for PATCO Suite',
    'description': """
        Agente IA conversacional integrado con capacidades RAG para guiar
        técnicos de campo durante servicios, con generación automática de reportes.
        
        Características principales:
        - Conversaciones IA integradas con órdenes FSM
        - Base de conocimiento vectorial con búsqueda semántica
        - Generación automática de reportes técnicos
        - Integración nativa con discuss.channel de Odoo
        - Soporte para múltiples tipos de documentos técnicos
    """,
    'author': 'PATCO',
    'website': 'https://patco.com.pe',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'maintenance',
        'fieldservice',
        'patco_base',
        'web_notify',
        'web_notify_channel_message',
        'patco_maintenance_color_fix',
    ],
    'external_dependencies': {
        'python': [
            'requests',
        ]
    },
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',

        'data/ai_agent_data.xml',
        'data/ai_agent_config.xml',

        'views/ai_conversation_views.xml',
        'views/fsm_order_views.xml',
        'views/ir_attachment_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 100,
}