# -*- coding: utf-8 -*-
{
    'name': 'PATCO - Gestión de Activos de Cliente',
    'version': '18.0.1.0.0',
    'category': 'Services/Field Service',
    'summary': 'Gestión de equipos de clientes con códigos QR y trazabilidad de servicios',
    'description': """
    Módulo para la gestión de activos/equipos de clientes que incluye:
    
    * Registro de equipos de clientes con información detallada
    * Generación automática de códigos QR únicos para cada equipo
    * Vinculación de equipos con órdenes de servicio y tickets de soporte
    * Reportes de etiquetas QR para impresión
    * Trazabilidad completa del historial de servicios por equipo
    
    Este módulo extiende las funcionalidades de Field Service Management
    y Helpdesk para proporcionar una gestión integral de activos.
    """,
    'author': 'PATCO',
    'website': 'https://www.patco.com.pe',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'maintenance',
        'maintenance_equipment_category_hierarchy',
        'patco_base',
        'fieldservice',
        'helpdesk_mgmt',
        'helpdesk_mgmt_sale',
    ],
    'external_dependencies': {
        'python': ['qrcode', 'PIL'],
    },
    'data': [
        # Security
        'security/security_rules.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/sequences.xml',
        
        # Views
        'views/patco_customer_equipment_views.xml',
        'views/helpdesk_ticket_views.xml',
        'views/fsm_order_views.xml',
        'views/menus.xml',
        
        # Reports
        'reports/equipment_label_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'patco_customer_equipment/static/src/css/patco_equipment.css',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'post_init_hook': '_post_init_hook',
}