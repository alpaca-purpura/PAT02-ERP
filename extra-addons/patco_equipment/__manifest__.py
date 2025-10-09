# -*- coding: utf-8 -*-
{
    'name': 'PATCO Equipment Management',
    'version': '18.0.1.0.0',
    'category': 'Maintenance',
    'summary': 'Gestión avanzada de equipos y categorías para servicios técnicos',
    'description': """
    PATCO Equipment Management
    ==========================
    
    Este módulo proporciona funcionalidades avanzadas para la gestión de equipos:
    
    Características principales:
    * Categorías de equipos con plantillas de checklist personalizables
    * Base de conocimiento integrada por categoría de equipo
    * Herencia inteligente de checklists y documentación
    * Plantillas HTML para checklists de entrada y salida
    * Gestión de documentación técnica mediante adjuntos
    * Integración con módulos de mantenimiento y FSM
    
    Herencia Inteligente:
    * Las categorías hijas pueden heredar checklists de categorías padre
    * Herencia configurable independiente para checklists y documentación
    * Plantillas efectivas que combinan configuración local y heredada
    * Vista unificada de documentación incluyendo categorías padre
    
    Categorías predefinidas:
    * Cocina y Procesamiento de Alimentos
    * Refrigeración y Climatización
    * Lavandería Industrial
    * Equipos de Bar y Cafetería
    * Sistemas Eléctricos y Fontanería
    
    Funcionalidades técnicas:
    * Extensión del modelo maintenance.equipment.category con jerarquía
    * Campos personalizados para plantillas de checklist con herencia
    * Contador de documentos propios e inherited
    * Acciones para gestión de adjuntos y herencia
    * Métodos de equipos para acceso a plantillas efectivas
    """,
    'author': 'PATCO',
    'website': 'https://www.patco.pe',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'patco_base',
        'maintenance',
        'maintenance_equipment_category_hierarchy',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/security_rules.xml',

        # Views
        'views/maintenance_equipment_category_views.xml',
        'views/maintenance_equipment_views.xml',
        #'views/menus.xml',
        'views/fsm_order_views.xml',
        'views/helpdesk_ticket_views.xml',
        'views/patco_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}