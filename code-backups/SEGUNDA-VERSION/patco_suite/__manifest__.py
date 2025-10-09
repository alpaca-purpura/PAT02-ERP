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

* **patco_base**: Modelos fundamentales y clasificaciones base
* **patco_skills_mgmt**: Gestión avanzada de habilidades técnicas
* **patco_equipment**: Gestión integral de equipos con códigos QR

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
        # PATCO Modules - Nueva estructura consolidada
        'patco_base',
        'patco_skills_mgmt',
        'patco_equipment',
        'patco_fsm',
        'patco_stock_fsm',
        'patco_timesheet',

        # PATCO IA Module
        'patco_ai_agent',

        # OnlyOffice
        'onlyoffice_odoo',
        'onlyoffice_odoo_templates',
        
        
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