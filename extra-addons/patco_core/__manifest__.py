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
        'hr_timesheet',

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
        # 'hr_skills',  # Enterprise module, not available in Community
        # 'fieldservice_skill',  # Depends on hr_skills
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
        'security/patco_security.xml',
        'security/ir.model.access.csv',
        'security/patco_record_rules.xml',
        'data/patco_actions.xml',
        'data/patco_menu_visibility.xml',
        'data/patco_module_restrictions.xml',
        'views/fsm_order_views.xml',
        'views/fsm_worksheet_views.xml',
        'views/fsm_worksheet_signature_wizard_views.xml',
        'wizards/fsm_consume_parts_wizard_views.xml',
        'wizards/fsm_worksheet_customer_approval_wizard_views.xml',
        'views/account_analytic_line_views.xml',
        'views/patco_service_nature_views.xml',
        'views/patco_service_area_views.xml',
        'views/patco_service_complexity_views.xml',
        'views/patco_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}