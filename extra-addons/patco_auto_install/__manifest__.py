# -*- coding: utf-8 -*-
{
    'name': 'PATCO Auto Install Modules',
    'version': '18.0.1.0.0',
    'category': 'Technical',
    'summary': 'Modulo para instalacion automatica de modulos esenciales',
    'description': """
        Este modulo configura automaticamente la estructura base de seguridad
        y datos maestros para PATCO al inicializar Odoo.
        
        Funcionalidades:
        - Grupos de seguridad: Administrador, Gerente, Tecnico Lider, Tecnico
        - Permisos granulares para cada rol
        - Datos maestros iniciales
        - Secuencias de numeracion
        - Instalacion automatica de modulos esenciales
    """,
    'author': 'PATCO Development Team',
    'website': 'https://www.patco.com',
    'license': 'LGPL-3',
    'depends': [
        # Módulos nativos de Odoo
        'base',
        'contacts',
        'account',
        'sale',
        'l10n_pe',
        'project',
        'maintenance',
        'stock',
        'hr',
        'purchase',
        'crm',
        'website',
        'portal',
        'board',
        'calendar',
        'mail',
        
        # Módulos OCA
        'web_responsive',
        'web_timeline',
        'maintenance_equipment_category_hierarchy',
        'project_task_stock',
        'account_payment_term_extension',
        'report_xlsx',
        'server_environment',
    ],
    'data': [
        'security/patco_security.xml',
        'data/patco_data.xml',
        'data/ir_sequence_data.xml',
        'data/patco_core_data.xml',
        # 'data/account_chart_pe.xml',  # Se agregará en módulo patco_accounting
    ],
    'demo': [],
    'auto_install': False,
    'installable': True,
    'application': False,
}