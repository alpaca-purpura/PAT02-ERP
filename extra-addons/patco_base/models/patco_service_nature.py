# -*- coding: utf-8 -*-
from odoo import models, fields

class PatcoServiceNature(models.Model):
    _name = 'patco.service.nature'
    _description = 'Service Order Nature'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(
        string='Nature', 
        required=True, 
        translate=True,
        help="Naturaleza del servicio (ej: Mantenimiento, Instalación, Reparación)"
    )
    code = fields.Char(
        string='Code', 
        required=True, 
        help="Código corto para clasificación, ej: M1, I1, R1"
    )
    active = fields.Boolean(
        string='Active', 
        default=True,
        help="Si está desactivado, no aparecerá en las selecciones"
    )
    sequence = fields.Integer(
        string='Sequence', 
        default=10,
        help="Orden de aparición en las listas"
    )
    description = fields.Text(
        string='Description',
        translate=True,
        help="Descripción detallada de la naturaleza del servicio"
    )

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'El código debe ser único.'),
        ('name_unique', 'UNIQUE(name)', 'El nombre debe ser único.'),
    ]

    def name_get(self):
        """Personaliza la visualización del nombre incluyendo el código"""
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}"
            result.append((record.id, name))
        return result