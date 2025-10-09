# -*- coding: utf-8 -*-

from . import models


def _post_init_hook(env):
    """Hook ejecutado después de la instalación del módulo."""
    # Generar códigos QR para equipos existentes que no los tengan
    equipments = env['maintenance.equipment'].search([('x_qr_code', '=', False)])
    for equipment in equipments:
        equipment._generate_qr_code()