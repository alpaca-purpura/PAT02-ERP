# -*- coding: utf-8 -*-
{
    'name': 'PATCO Timesheet',
    'version': '18.0.1.0.0',
    'category': 'Services/Timesheets',
    'summary': 'Extensiones de timesheet para Field Service Management PATCO',
    'description': """
    PATCO Timesheet - Extensiones de Registro de Tiempo
    ===================================================
    
    Módulo especializado que proporciona extensiones para el registro de tiempo
    en el contexto de Field Service Management (FSM) de PATCO.
    
    Características principales:
    * Extensiones del modelo account.analytic.line con campos FSM
    * Sistema de timer integrado para técnicos de campo
    * Reportes de análisis de timesheet con datos FSM
    * Integración con órdenes de servicio FSM
    * Vistas especializadas para registro de tiempo en campo
    
    Dependencias:
    * patco_base: Configuraciones base del sistema PATCO
    * patco_fsm: Órdenes de servicio y gestión FSM
    * hr_timesheet: Funcionalidad base de timesheet de Odoo
    * fieldservice: Módulo base de Field Service Management
    """,
    'author': 'PATCO',
    'website': 'https://www.patco.pe',
    'license': 'LGPL-3',
    'depends': [
        'patco_base',
        'patco_fsm',
        'hr_timesheet',
        'fieldservice',
    ],
    'data': [
        # Seguridad
        'security/ir.model.access.csv',
        
        # Datos
        'data/timesheet_data.xml',
        
        # Vistas
        'views/account_analytic_line_views.xml',
        # 'views/timesheets_analysis_report_views.xml',  # Deshabilitado temporalmente
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}