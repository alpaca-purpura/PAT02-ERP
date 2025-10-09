# -*- coding: utf-8 -*-
{
    'name': 'PATCO Skills Management',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Gestión avanzada de habilidades y competencias técnicas',
    'description': """
    PATCO Skills Management
    =======================
    
    Este módulo proporciona un sistema completo de gestión de habilidades y competencias
    técnicas para el personal de servicios de campo:
    
    Características principales:
    * Catálogo de habilidades técnicas por categorías
    * Niveles de competencia y certificaciones
    * Asignación de habilidades a empleados
    * Evaluación y seguimiento de competencias
    * Integración con órdenes de servicio FSM
    * Reportes de capacidades del equipo técnico
    
    Funcionalidades:
    * Gestión de habilidades requeridas por tipo de servicio
    * Matching automático de técnicos por competencias
    * Seguimiento de certificaciones y vencimientos
    * Planes de capacitación y desarrollo
    * Análisis de brechas de habilidades
    """,
    'author': 'PATCO',
    'website': 'https://www.patco.pe',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'hr',
        'hr_skills',
        'fieldservice',
        'patco_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_skill_type_data.xml',
        'data/hr_skill_level_data.xml',
        'data/hr_skill_data.xml',
        'data/hr_job_data.xml',
        'views/hr_skill_views.xml',
        'views/hr_employee_views.xml',
        'views/fsm_order_views.xml',
        'views/fieldservice_views.xml',
        'views/actions.xml',
        #'views/menu_views.xml',
        'views/patco_menus.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}