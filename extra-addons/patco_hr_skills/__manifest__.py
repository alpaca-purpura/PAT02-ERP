# -*- coding: utf-8 -*-
{
    'name': 'PATCO Profile: Field Service',
    'version': '18.0.1.0.0',
    'category': 'Technical/Profiles',
    'summary': 'Instala y configura el perfil de negocio para Field Service.',
    'author': 'PATCO Development Team',
    'website': 'https://www.patcoperu.com',
    'depends': [
        # 1. La dependencia clave es el módulo base
        #'patco_core',

        # 2. Módulos específicos de Field Service (OCA)
        #'fieldservice',
        #'fieldservice_account',
        #'fieldservice_stock',
        #'fieldservice_sale',
        # 'fieldservice_skill', ya no viene en la versión 18, tengo que migrarla maualmente
        # 'hr_skills',
        # 'fieldservice_tag',
        # 'fieldservice_asset',
        #'fieldservice_calendar',
        # 'fieldservice_geoengine',
        #'fieldservice_project',
        # 'base_geolocalize',
        # 'hr_skill',
        # 'base_asset_mro',
    ],
    # Si tienes datos específicos para este perfil, los agregas aquí
    'data': [],
    'installable': True,
    'application': True, # Este es el módulo que buscarás para instalar
    'auto_install': False,
}