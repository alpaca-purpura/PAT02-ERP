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
        'maintenance',
        'product',
        'stock',

        # --- OCA Agreement Management ---
        'agreement',
        'agreement_sale',

        # --- OCA Maintenance ---
        'maintenance_equipment_category_hierarchy',

        # --- OCA Field Service ---
        'fieldservice',
        'helpdesk_mgmt',
        'fieldservice_account',
        'fieldservice_stock',
        'fieldservice_sale',
        'hr_skills',  # Requerido para matriz de competencias
        'fieldservice_skill',  # Disponible en OCA v18
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
        #'account',
        #'hr',
        #'project',
        #'base_automation',
        #'base_geolocalize',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/stock_locations_data.xml',
        # 'data/product_spare_parts_data.xml',  # Temporalmente comentado
        'data/service_catalog_data.xml',
        'data/agreement_type_data.xml',
        'data/maintenance_equipment_category_data.xml',
        'data/patco_service_nature_data.xml',
        'data/patco_service_area_data.xml',
        'data/patco_service_complexity_data.xml',
        # 'data/stock_rules_data.xml',  # Temporalmente comentado - depende de productos
        # 'data/stock_initial_data.xml',  # Temporalmente comentado - depende de productos
        # 'data/stock_vehicle_data.xml',  # Temporalmente comentado - contiene productos
        'views/fsm_order_views.xml',
        'views/maintenance_equipment_category_views.xml',
        'views/patco_service_nature_views.xml',
        'views/patco_service_area_views.xml',
        'views/patco_service_complexity_views.xml',
        'views/patco_menus.xml',
    ],
    'installable': True,
    'application': False, # Lo hacemos aplicación para encontrarlo fácil
    'auto_install': False,
}