# -*- coding: utf-8 -*-

import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Hook ejecutado después de la instalación del módulo.
    
    Realiza configuraciones adicionales y verificaciones para asegurar
    que todos los módulos PATCO estén correctamente instalados y configurados.
    """
    _logger.info('Iniciando configuración post-instalación de PATCO Suite')
    
    # Verificar que todos los módulos PATCO estén instalados
    patco_modules = [
        'patco_core',
        'patco_customer_equipment', 
        'patco_hr_skills'
    ]
    
    installed_modules = env['ir.module.module'].search([
        ('name', 'in', patco_modules),
        ('state', '=', 'installed')
    ])
    
    if len(installed_modules) == len(patco_modules):
        _logger.info('Todos los módulos PATCO instalados correctamente: %s', 
                    installed_modules.mapped('name'))
    else:
        missing = set(patco_modules) - set(installed_modules.mapped('name'))
        _logger.warning('Módulos PATCO faltantes: %s', missing)
    
    # Verificar que el campo fsm_order_id existe en account_analytic_line
    try:
        env['account.analytic.line']._fields.get('fsm_order_id')
        _logger.info('Campo fsm_order_id agregado correctamente a account.analytic.line')
    except Exception as e:
        _logger.error('Error verificando campo fsm_order_id: %s', e)
    
    _logger.info('Configuración post-instalación de PATCO Suite completada')