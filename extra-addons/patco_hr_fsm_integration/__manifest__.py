# -*- coding: utf-8 -*-
{
    'name': 'PATCO HR FSM Integration',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Integración automática entre HR Employee y FSM Person',
    'description': """
    Módulo de integración que sincroniza automáticamente empleados de HR
    con trabajadores de Field Service (FSM).
    
    Funcionalidades:
    - Creación automática de fsm.person al marcar is_field_technician=True
    - Sincronización bidireccional de datos (nombre, teléfono, email)
    - Cron job para mantener sincronización periódica
    - Método de migración para datos existentes
    
    Este módulo implementa el principio de alta cohesión y bajo acoplamiento,
    evitando duplicar funcionalidades existentes en patco_hr_skills y patco_core.
    """,
    'author': 'PATCO',
    'website': 'https://www.patco.com',
    'depends': [
        'hr',
        'fieldservice',
        'fieldservice_skill',
        'patco_hr_skills',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/hr_employee_views.xml',
        'views/fsm_person_skill.xml',
    ],
    'demo': [],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}