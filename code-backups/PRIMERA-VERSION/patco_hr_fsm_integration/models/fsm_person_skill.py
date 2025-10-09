# -*- coding: utf-8 -*-
# Copyright (C) 2024 PATCO
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models
from odoo.exceptions import ValidationError


class FSMPersonSkill(models.Model):
    """Extensión del modelo fsm.person.skill para corregir validaciones."""
    _inherit = "fsm.person.skill"

    @api.constrains("skill_level_id")
    def _check_skill_level(self):
        """Validación corregida para niveles de habilidad genéricos.
        
        Reemplaza la validación original que dependía de skill_type_id.skill_level_ids
        por una validación que solo verifica que el nivel esté activo.
        """
        for record in self:
            if not record.skill_level_id.active:
                raise ValidationError(
                    self.env._(
                        "The skill level '%(skilllevel)s' is not active",
                        skilllevel=record.skill_level_id.name,
                    )
                )