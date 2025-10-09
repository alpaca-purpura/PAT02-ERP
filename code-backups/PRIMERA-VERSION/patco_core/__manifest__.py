# -*- coding: utf-8 -*-
{
    'name': 'PATCO Core - FSM Extensions',
    'version': '18.0.1.0.0',
    'category': 'Field Service',
    'summary': 'Extensiones específicas de Field Service Management para PATCO.',
    'author': 'PATCO Development Team',
    'website': 'https://www.patcoperu.com', # Opcional, pero recomendado
    'depends': [
        # --- Odoo Standard Apps ---
        'base',
        'hr_timesheet',
        'sale_management',
        'maintenance',
        
        # --- OCA Dependencies ---
        'fieldservice',
        'fieldservice_account',
        'fieldservice_stock',
        'fieldservice_sale',
        'fieldservice_skill',
        'agreement',
        'agreement_sale',
        'helpdesk_mgmt',
        'helpdesk_mgmt_sale',
        'maintenance_equipment_category_hierarchy',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/patco_security.xml',
        'security/patco_record_rules.xml',
        # Data
        'data/patco_security_groups.xml',
        'data/patco_actions.xml',
        'data/patco_module_restrictions.xml',
        'data/patco_menu_visibility.xml',
        'data/fsm_worksheet_template_data.xml',
        'data/maintenance_equipment_category_data.xml',
        'data/stock_locations_data.xml',
        'data/stock_rules_data.xml',
        'data/stock_vehicle_data.xml',
        # Views
        'views/account_analytic_line_views.xml',
        'views/fsm_order_views.xml',
        'views/fsm_order_checklist_views.xml',
        'views/fsm_consumed_parts_views.xml',
        'views/fsm_worksheet_views.xml',
        'views/fsm_worksheet_signature_wizard_views.xml',
        'views/helpdesk_ticket_views.xml',
        'views/maintenance_equipment_category_views.xml',
        'views/service_order_views.xml',
        'views/stock_location_views.xml',
        'views/stock_transfer_views.xml',
        'views/patco_menus.xml',
        'views/clientes_menu.xml',
        'views/sales_menu_structure.xml',
        # Wizards
        'wizards/fsm_consume_parts_wizard_views.xml',
        'wizards/fsm_worksheet_customer_approval_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}