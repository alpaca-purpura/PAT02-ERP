# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class FSMOrder(models.Model):
    """Extensión del modelo fsm.order para relacionar con Activos de Clientes de PATCO.
    
    Esta extensión agrega soporte para múltiples equipos y mejora la integración
    con el sistema de gestión de activos de PATCO.
    """
    
    _inherit = 'fsm.order'
    
    # Campo principal de equipo (compatibilidad hacia atrás)
    x_equipment_id = fields.Many2one(
        'maintenance.equipment',
        string='Activo Principal',
        tracking=True,
        help='Activo principal relacionado con esta orden de servicio'
    )
    
    x_equipment_code = fields.Char(
        string='Código de Activo Principal',
        related='x_equipment_id.x_patco_code',
        readonly=True,
        store=True,
        help='Código PATCO del activo principal'
    )
    
    x_customer_equipment = fields.Many2one(
        'res.partner',
        string='Cliente del Activo',
        related='x_equipment_id.x_customer_id',
        readonly=True,
        store=True,
        help='Cliente propietario del activo principal'
    )
    
    # Campos para múltiples equipos
    x_equipment_ids = fields.Many2many(
        'maintenance.equipment',
        'fsm_order_equipment_rel',
        'order_id',
        'equipment_id',
        string='Múltiples Equipos',
        help='Todos los equipos involucrados en esta orden de servicio'
    )
    
    x_equipment_count = fields.Integer(
        string='Cantidad de Equipos',
        compute='_compute_equipment_stats',
        help='Número total de equipos asignados a esta orden'
    )
    
    x_equipment_categories = fields.Many2many(
        'maintenance.equipment.category',
        string='Categorías de Equipos',
        compute='_compute_equipment_stats',
        help='Categorías de todos los equipos involucrados'
    )    
    x_all_equipment_codes = fields.Char(
        string='Códigos de Equipos',
        compute='_compute_equipment_stats',
        help='Códigos de todos los equipos separados por comas'
    )
    
    @api.depends('x_equipment_ids', 'x_equipment_id')
    def _compute_equipment_stats(self):
        """Computar estadísticas de equipos asignados"""
        for record in self:
            # Inicializar con recordset vacío del modelo correcto
            all_equipment = self.env['maintenance.equipment']
            
            # Agregar equipos del campo many2many
            if record.x_equipment_ids:
                all_equipment = record.x_equipment_ids
            
            # Agregar equipo principal si existe y no está ya incluido
            if record.x_equipment_id and record.x_equipment_id not in all_equipment:
                all_equipment = all_equipment | record.x_equipment_id
            
            record.x_equipment_count = len(all_equipment)
            
            # Obtener categorías únicas
            categories = all_equipment.mapped('category_id')
            record.x_equipment_categories = categories            
            # Obtener códigos de equipos
            codes = all_equipment.mapped('x_patco_code')
            record.x_all_equipment_codes = ', '.join(filter(None, codes))
    
    @api.onchange('x_equipment_id')
    def _onchange_equipment_id(self):
        """Actualizar campos relacionados cuando se selecciona un activo principal."""
        if self.x_equipment_id:
            # Verificar que el campo many2many esté inicializado
            equipment_ids = self.x_equipment_ids or []
            
            # Agregar el equipo principal a la lista de múltiples equipos
            if self.x_equipment_id not in equipment_ids:
                self.x_equipment_ids = [(4, self.x_equipment_id.id)]
            
            # Actualizar ubicación si el equipo tiene una ubicación de servicio
            if self.x_equipment_id.x_service_location_id:
                self.location_id = self.x_equipment_id.x_service_location_id
            
            # Actualizar cliente si no está definido
            if not self.partner_id and self.x_equipment_id.x_customer_id:
                self.partner_id = self.x_equipment_id.x_customer_id
            
            # Sincronizar con el campo x_multiple_assets_ids del módulo base
            if hasattr(self, 'x_multiple_assets_ids'):
                multiple_assets = self.x_multiple_assets_ids or []
                if self.x_equipment_id not in multiple_assets:
                    self.x_multiple_assets_ids = [(4, self.x_equipment_id.id)]
    
    @api.onchange('x_equipment_ids')
    def _onchange_equipment_ids(self):
        """Actualizar información cuando se cambian los múltiples equipos"""
        # Verificar que el campo many2many esté inicializado
        equipment_ids = self.x_equipment_ids or []
        
        if equipment_ids:
            # Si solo hay un equipo, establecerlo como principal
            if len(equipment_ids) == 1 and not self.x_equipment_id:
                self.x_equipment_id = equipment_ids[0]
            
            # Sincronizar con el campo x_multiple_assets_ids del módulo base
            if hasattr(self, 'x_multiple_assets_ids'):
                # Verificar que el campo many2many esté inicializado
                multiple_assets = self.x_multiple_assets_ids or []
                
                # Agregar equipos que no estén en x_multiple_assets_ids
                for equipment in equipment_ids:
                    if equipment not in multiple_assets:
                        self.x_multiple_assets_ids = [(4, equipment.id)]
            
            # Actualizar cliente basado en el primer equipo si no está definido
            if not self.partner_id:
                first_equipment = equipment_ids[0]
                if first_equipment.x_customer_id:
                    self.partner_id = first_equipment.x_customer_id
    
    def action_view_all_equipment(self):
        """Ver todos los equipos asignados a esta orden"""
        self.ensure_one()
        
        # Combinar equipo principal con múltiples equipos
        all_equipment_ids = list(self.x_equipment_ids.ids)
        if self.x_equipment_id and self.x_equipment_id.id not in all_equipment_ids:
            all_equipment_ids.append(self.x_equipment_id.id)
        
        if not all_equipment_ids:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'No hay equipos asignados a esta orden.',
                    'type': 'warning',
                }
            }
        
        return {
            'name': 'Equipos de la Orden',
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.equipment',
            'view_mode': 'list,form',
            'domain': [('id', 'in', all_equipment_ids)],
            'context': {
                'search_default_group_by_category': 1,
            }
        }
    
    def action_sync_equipment_fields(self):
        """Sincronizar campos de equipos entre módulos"""
        self.ensure_one()
        
        # Sincronizar x_equipment_ids con x_multiple_assets_ids
        if hasattr(self, 'x_multiple_assets_ids'):
            # Agregar equipos de x_equipment_ids a x_multiple_assets_ids
            for equipment in self.x_equipment_ids:
                if equipment not in self.x_multiple_assets_ids:
                    self.x_multiple_assets_ids = [(4, equipment.id)]
            
            # Agregar equipo principal si no está
            if self.x_equipment_id and self.x_equipment_id not in self.x_multiple_assets_ids:
                self.x_multiple_assets_ids = [(4, self.x_equipment_id.id)]
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': 'Campos de equipos sincronizados correctamente.',
                'type': 'success',
            }
        }
    
    @api.model
    def create(self, vals):
        """Sobrescribir create para manejar relaciones automáticas y múltiples equipos."""
        # Si se especifica un equipo principal, actualizar campos relacionados
        if vals.get('x_equipment_id'):
            equipment = self.env['maintenance.equipment'].browse(vals['x_equipment_id'])
            
            # Actualizar ubicación si no está definida
            if not vals.get('location_id') and equipment.x_service_location_id:
                vals['location_id'] = equipment.x_service_location_id.id
            
            # Actualizar cliente si no está definido
            if not vals.get('partner_id') and equipment.x_customer_id:
                vals['partner_id'] = equipment.x_customer_id.id
            
            # Agregar el equipo principal a la lista de múltiples equipos
            if not vals.get('x_equipment_ids'):
                vals['x_equipment_ids'] = [(6, 0, [vals['x_equipment_id']])]
            else:
                # Asegurar que el equipo principal esté en la lista
                equipment_ids = vals['x_equipment_ids']
                if isinstance(equipment_ids, list) and equipment_ids:
                    if equipment_ids[0][0] == 6:  # Comando (6, 0, [ids])
                        if vals['x_equipment_id'] not in equipment_ids[0][2]:
                            equipment_ids[0][2].append(vals['x_equipment_id'])
        
        # Si se especifican múltiples equipos pero no hay equipo principal
        elif vals.get('x_equipment_ids') and not vals.get('x_equipment_id'):
            equipment_ids = vals['x_equipment_ids']
            if isinstance(equipment_ids, list) and equipment_ids:
                if equipment_ids[0][0] == 6 and equipment_ids[0][2]:  # Comando (6, 0, [ids])
                    # Establecer el primer equipo como principal
                    first_equipment_id = equipment_ids[0][2][0]
                    vals['x_equipment_id'] = first_equipment_id
                    
                    # Actualizar campos basados en el primer equipo
                    equipment = self.env['maintenance.equipment'].browse(first_equipment_id)
                    if not vals.get('location_id') and equipment.x_service_location_id:
                        vals['location_id'] = equipment.x_service_location_id.id
                    if not vals.get('partner_id') and equipment.x_customer_id:
                        vals['partner_id'] = equipment.x_customer_id.id
        
        return super().create(vals)