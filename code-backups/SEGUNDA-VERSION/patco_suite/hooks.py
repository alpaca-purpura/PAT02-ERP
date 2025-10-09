# -*- coding: utf-8 -*-

import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """
    Hook ejecutado después de la instalación del módulo.
    Verifica que los módulos PATCO consolidados estén correctamente instalados.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info("Iniciando configuración post-instalación de PATCO Suite")
    
    # Lista de módulos PATCO consolidados que deben estar instalados
    patco_modules = [
        'patco_base',
        'patco_skills_mgmt',
        'patco_equipment',
        'patco_fsm',
        'patco_stock_fsm',
        'patco_timesheet',
    ]
    
    # Verificar instalación de módulos PATCO
    for module_name in patco_modules:
        module = env['ir.module.module'].search([('name', '=', module_name)])
        if module and module.state == 'installed':
            _logger.info(f"✓ Módulo {module_name} instalado correctamente")
        else:
            _logger.warning(f"⚠ Módulo {module_name} no está instalado o tiene problemas")
    
    # Verificar que el campo fsm_order_id existe en account.analytic.line
    try:
        cr.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='account_analytic_line' 
            AND column_name='fsm_order_id'
        """)
        if cr.fetchone():
            _logger.info("✓ Campo fsm_order_id encontrado en account.analytic.line")
        else:
            _logger.warning("⚠ Campo fsm_order_id no encontrado en account.analytic.line")
    except Exception as e:
        _logger.error(f"Error verificando campo fsm_order_id: {e}")
    
    _logger.info("Configuración post-instalación de PATCO Suite completada")