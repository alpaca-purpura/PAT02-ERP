# -*- coding: utf-8 -*-
from odoo import models, fields

class PatcoServiceComplexity(models.Model):
    _name = 'patco.service.complexity'
    _description = 'Service Order Complexity Level'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(
        string='Complexity', 
        required=True, 
        translate=True,
        help="Nivel de complejidad del servicio (ej: Básico, Intermedio, Avanzado)"
    )
    code = fields.Char(
        string='Code', 
        required=True, 
        help="Código corto para clasificación, ej: N1, N2, N3"
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
        help="Descripción detallada del nivel de complejidad"
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