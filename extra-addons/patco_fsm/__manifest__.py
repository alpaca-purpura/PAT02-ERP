# -*- coding: utf-8 -*-
{
    'name': 'PATCO Field Service Management',
    'version': '18.0.1.0.0',
    'category': 'Field Service',
    'summary': 'Extensiones PATCO para Field Service Management',
    'description': """
    Módulo PATCO para Field Service Management
    =========================================
    
    Este módulo contiene las extensiones específicas de PATCO para:
    - Órdenes de servicio en campo (FSM)
    - Listas de verificación personalizadas
    - Consumo de partes y materiales
    - Hojas de trabajo digitales
    - Integración con equipos de clientes
    
    Migrado desde patco_core como parte de la reestructuración modular.
    """,
    'author': 'PATCO',
    'website': 'https://www.patco.pe',
    'depends': [
        'base',
        'patco_base',
        'patco_equipment',
        'patco_skills_mgmt',
        'fieldservice',
        'fieldservice_sale',
        'fieldservice_calendar',
        'fieldservice_availability',
        # 'fieldservice_geoengine',  # No disponible en OCA
        'fieldservice_route',
        'fieldservice_project', #para vista Gantt
        'fieldservice_skill',
        'maintenance',
        'helpdesk_mgmt',
        'helpdesk_mgmt_fieldservice',
        'helpdesk_mgmt_fieldservice_equipment',
        'fieldservice_activity',
        'fieldservice_agreement',
        'fieldservice_recurring',
        'fieldservice_sale_recurring',
        'hr_timesheet',
        'project_timesheet_time_control',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/fsm_configuration_data.xml',
        'data/fsm_worksheet_template_data.xml',
        'views/fsm_order_views.xml',
        'views/fsm_consumed_parts_views.xml',
        'views/fsm_order_checklist_views.xml',
        'views/fsm_order_asset_technician_views.xml',
        'views/suggest_technician_wizard_views.xml',
        'views/fsm_worksheet_views.xml',
        'views/fsm_worksheet_customer_approval_wizard_views.xml',
        'views/fsm_worksheet_signature_wizard_views.xml',
        'views/res_partner_views.xml',
        # 'views/fsm_menus.xml',
        'views/patco_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}