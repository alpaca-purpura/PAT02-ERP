# -*- coding: utf-8 -*-
{
    'name': 'PATCO Suite - Solución Completa de Mantenimiento HORECA',
    'version': '18.0.1.0.0',
    'category': 'Services/Field Service',
    'summary': 'Suite completa de módulos PATCO para gestión de mantenimiento en sector HORECA',
    'description': """
PATCO Suite - Solución Completa de Mantenimiento HORECA
=======================================================

Este módulo orquestador instala automáticamente toda la suite PATCO:

* **patco_core**: Funcionalidades base y configuraciones centrales
* **patco_customer_equipment**: Gestión de equipos de clientes
* **patco_hr_skills**: Gestión de habilidades de técnicos

Características principales:
---------------------------
* Instalación automática de dependencias OCA en orden correcto
* Configuración de campos faltantes (fsm_order_id en account_analytic_line)
* Gestión centralizada de la suite completa
* Cumple con documento_funcional_wannabe.md

Uso:
----
Simplemente instale este módulo y automáticamente se instalarán todos
los módulos PATCO necesarios con sus dependencias en el orden correcto.

Nota: Los módulos individuales PATCO no son instalables directamente.
Use siempre este módulo orquestador.
    """,
    'author': 'PATCO',
    'website': 'https://www.patco.pe',
    'license': 'LGPL-3',
    'depends': [
        # Módulos base de Odoo
        'base',
        'sale_management',
        'account',
        'hr',
        'maintenance',
        'contacts',
        
        # Módulos OCA - HR primero (orden crítico)
        'hr_skills',
        
        # Módulos PATCO - HR Skills debe instalarse antes que fieldservice_skill
        'patco_hr_skills',
        
        # Módulos OCA - Field Service (después de patco_hr_skills)
        'fieldservice',
        'fieldservice_account',
        'fieldservice_sale',
        'fieldservice_skill',
        'fieldservice_stock',
        'fieldservice_sale_timesheet',
        
        # Módulos OCA - Otros
        'agreement',
        'helpdesk_mgmt',
        'maintenance_equipment_category_hierarchy',
        
        # Módulos PATCO restantes
        'patco_core',
        'patco_customer_equipment',
    ],
    'data': [
        'data/suite_configuration.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 1,
    'post_init_hook': 'post_init_hook',
}