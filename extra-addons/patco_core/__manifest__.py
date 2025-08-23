# -*- coding: utf-8 -*-
{
    'name': 'PATCO Core',
    'version': '18.0.1.0.0',
    'category': 'Technical/Base',
    'summary': 'Módulo base con configuraciones y dependencias comunes de PATCO.',
    'author': 'PATCO Development Team',
    'website': 'https://www.patcoperu.com', # Opcional, pero recomendado
    'depends': [
        # --- Odoo Standard Apps ---
        'base',
        'sale_management',

        # 2. Módulos específicos de Field Service (OCA)
        'fieldservice',
        'helpdesk_mgmt',
        #'fieldservice_account',
        #'fieldservice_stock',
        #'fieldservice_sale',
        #'fieldservice_skill', ya no viene en la versión 18, tengo que migrarla maualmente
        #'hr_skills',
        #'fieldservice_tag',
        #'fieldservice_asset',
        #'fieldservice_calendar',
        #'fieldservice_geoengine',
        #'fieldservice_project',
        #'base_geolocalize',
        #'hr_skill',
        #'base_asset_mro',
        'web_responsive',


        #'contacts',
        #'stock',
        #'account',
        #'hr',
        #'project',
        #'base_automation',
        #'base_geolocalize',
    ],
    'data': [
        # 1. Cargar la seguridad PRIMERO.
        'security/ir.model.access.csv',

        # 2. Cargar los datos iniciales SEGUNDO.
        'data/patco_service_nature_data.xml',
        'data/patco_service_area_data.xml',
        'data/patco_service_complexity_data.xml',

        # 3. Cargar las vistas y menús DESPUÉS.
        'views/patco_service_nature_views.xml',
        'views/patco_service_area_views.xml',
        'views/patco_service_complexity_views.xml',
        #views/helpdesk_ticket_views.xml',
        #views/fsm_order_views.xml',
        'views/patco_menus.xml',
    ],
    'installable': True,
    'application': False, # Lo hacemos aplicación para encontrarlo fácil
    'auto_install': False,
}