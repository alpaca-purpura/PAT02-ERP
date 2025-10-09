# -*- coding: utf-8 -*-
{
    'name': 'PATCO Stock FSM',
    'version': '18.0.1.0.0',
    'category': 'Field Service',
    'summary': 'Gestión de Stock para Servicios de Campo PATCO',
    'description': """
    Módulo de gestión de stock especializado para servicios de campo PATCO.
    
    Funcionalidades principales:
    * Gestión de ubicaciones de vehículos
    * Transferencias de stock a vehículos
    * Control de inventario móvil
    * Integración con órdenes de servicio FSM
    """,
    'author': 'PATCO',
    'website': 'https://www.patco.pe',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'stock',
        # 'asset-management', #OCA
        'fieldservice',
        'fieldservice_stock',  # Requerido para campos fsm_order_id en stock
        'patco_base',
    ],
    'data': [
        # Seguridad
        'security/ir.model.access.csv',
        
        # Datos
        'data/stock_locations_data.xml',
        
        # Vistas
        'views/stock_location_views.xml',
        'views/stock_transfer_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}