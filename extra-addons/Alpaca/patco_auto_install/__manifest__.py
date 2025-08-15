# -*- coding: utf-8 -*-
{
    'name': 'PATCO Auto Install Modules',
    'version': '18.0.1.0.0',
    'category': 'Technical',
    'summary': 'Módulo para instalación automática de módulos esenciales',
    'description': """
        Este módulo se encarga de instalar automáticamente los módulos
        esenciales para PATCO al inicializar Odoo.
        
        Módulos que instala automáticamente:
        - web_responsive: Interfaz responsiva para dispositivos móviles
    """,
    'author': 'PATCO Development Team',
    'website': 'https://www.patco.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web_responsive',
    ],
    'data': [],
    'demo': [],
    'auto_install': True,
    'installable': True,
    'application': False,
}