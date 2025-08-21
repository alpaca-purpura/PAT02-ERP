# -*- coding: utf-8 -*-
{
    'name': 'PATCO Auto Install Modules',
    'version': '18.0.1.0.0',
    'category': 'Technical',
    'summary': 'Modulo para instalacion automatica de modulos esenciales',
    'author': 'PATCO Development Team',
    'depends': [
        'base', 'account', 'sale', 'contacts', 'project',
        'maintenance', 'stock', 'hr', 'purchase', 'crm', 'website',
        'portal', 'board', 'calendar', 'mail', 'web_responsive',
        'web_timeline', 'maintenance_equipment_category_hierarchy',
        'project_task_stock', 'account_payment_term_extension',
        'report_xlsx', 'server_environment',
    ],
    'data': [
        'security/patco_security.xml',
        'data/patco_core_data.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}