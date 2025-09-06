# -*- coding: utf-8 -*-
{
    'name': 'PATCO HR Skills',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Gestión de habilidades técnicas para PATCO',
    'description': """
    Módulo para gestionar las habilidades técnicas de los empleados de PATCO.
    Incluye tipos de habilidades específicas para el sector HORECA:
    - COC (Cocina): Calentadores, Presión, Lavado
    - REF (Refrigeración): Comercial, Aire Acondicionado
    - LAV (Lavandería): Lavadoras, Secadoras, Planchadoras
    - ELEC (Eléctrico): Baja Tensión, Generadores
    - FONT (Fontanería): Agua, Gas
    
    Integra con fieldservice_skill para asignación automática de técnicos.
    """,
    'author': 'PATCO',
    'website': 'https://www.patco.com',
    'depends': [
        'hr',
        # 'hr_skills',  # Enterprise module, not available in Community
    ],
    'data': [
        'security/ir.model.access.csv',
        # 'views/hr_employee_views.xml',
        # 'views/fsm_order_views.xml',
        # 'data/hr_skill_level_data.xml',
        # 'data/hr_skill_type_data.xml',
        # 'data/hr_skill_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}