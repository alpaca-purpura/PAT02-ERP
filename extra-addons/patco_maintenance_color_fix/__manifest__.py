{
    'name': 'PATCO - Corrección de Colores para Maintenance',
    'version': '18.0.1.0.0',
    'category': 'Maintenance',
    'summary': 'Corrección para manejo de colores hexadecimales en categorías de equipos',
    'description': """
        Este módulo corrige el error de conversión de colores hexadecimales a enteros
        en el modelo maintenance.equipment.category. Proporciona una conversión robusta
        y compatible con el futuro de Odoo.
        
        Características:
        - Conversión automática de colores hexadecimales (#RRGGBB) a índices enteros (0-11)
        - Validación de formato de color hexadecimal
        - Mapeo inteligente de colores a la paleta estándar de Odoo
        - Compatibilidad con versiones futuras de Odoo
        - Logging detallado para debugging
    """,
    'author': 'PATCO',
    'website': 'https://patco.pe',
    'depends': [
        'base',
        'maintenance',
    ],
    'data': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}