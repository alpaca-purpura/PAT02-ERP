# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class FSMOrder(models.Model):
    _inherit = 'fsm.order'
    
    # Campos de clasificación PATCO
    x_nature_id = fields.Many2one(
        'patco.service.nature',
        string='Naturaleza del Servicio',
        help='Tipo de naturaleza del servicio según clasificación PATCO'
    )
    
    x_area_id = fields.Many2one(
        'patco.service.area',
        string='Área del Servicio',
        help='Área técnica del servicio según clasificación PATCO'
    )
    
    x_complexity_id = fields.Many2one(
        'patco.service.complexity',
        string='Complejidad del Servicio',
        help='Nivel de complejidad del servicio según clasificación PATCO'
    )
    
    x_classification_code = fields.Char(
        string='Código de Clasificación',
        compute='_compute_classification_code',
        store=True,
        help='Código automático generado basado en la clasificación PATCO'
    )
    
    # Campos para checklists heredados de la categoría del equipo
    x_entry_checklist = fields.Html(
        string='Checklist de Entrada',
        help='Checklist que debe completarse al iniciar el servicio'
    )
    
    x_exit_checklist = fields.Html(
        string='Checklist de Salida',
        help='Checklist que debe completarse al finalizar el servicio'
    )
    
    # Campo relacionado para mostrar la base de conocimiento
    x_equipment_category_id = fields.Many2one(
        'maintenance.equipment.category',
        string='Categoría del Equipo',
        compute='_compute_equipment_category',
        store=True,
        readonly=True
    )
    
    x_knowledge_base_count = fields.Integer(
        related='x_equipment_category_id.x_knowledge_base_count',
        string='Documentos Disponibles'
    )
    
    # Campos para gestión de stock en vehículos
    x_vehicle_location_id = fields.Many2one(
        'stock.location',
        string='Ubicación del Vehículo',
        domain="[('is_vehicle_location', '=', True), ('technician_id', '=', person_id)]",
        help='Ubicación de stock del vehículo del técnico asignado'
    )
    
    x_consumed_parts_ids = fields.One2many(
        'fsm.order.consumed.part',
        'order_id',
        string='Repuestos Consumidos'
    )
    
    x_total_parts_cost = fields.Float(
        string='Costo Total de Repuestos',
        compute='_compute_total_parts_cost',
        store=True
    )

    @api.depends('x_consumed_parts_ids.total_cost')
    def _compute_total_parts_cost(self):
        """Calcula el costo total de repuestos consumidos"""
        for record in self:
            record.x_total_parts_cost = sum(record.x_consumed_parts_ids.mapped('total_cost'))
    
    @api.depends('x_nature_id.code', 'x_area_id.code', 'x_complexity_id.code')
    def _compute_classification_code(self):
        """Genera el código de clasificación automáticamente"""
        for record in self:
            if record.x_nature_id and record.x_area_id and record.x_complexity_id:
                nature_code = record.x_nature_id.code
                area_code = record.x_area_id.code
                complexity_code = record.x_complexity_id.code
                
                record.x_classification_code = (
                    f"{nature_code}-{area_code}-{complexity_code}"
                )
            else:
                record.x_classification_code = False
    
    @api.depends('equipment_id')
    def _compute_equipment_category(self):
        """Calcula la categoría del equipo"""
        for record in self:
            if record.equipment_id and hasattr(record.equipment_id, 'category_id'):
                record.x_equipment_category_id = record.equipment_id.category_id
            else:
                record.x_equipment_category_id = False

    @api.onchange('person_id')
    def _onchange_person_id(self):
        """Actualiza la ubicación del vehículo cuando se asigna un técnico"""
        if hasattr(super(), '_onchange_person_id'):
            super()._onchange_person_id()
        if self.person_id:
            # Buscar la ubicación de vehículo del técnico
            vehicle_location = self.env['stock.location'].search([
                ('is_vehicle_location', '=', True),
                ('technician_id', '=', self.person_id.id)
            ], limit=1)
            if vehicle_location:
                self.x_vehicle_location_id = vehicle_location.id
        else:
            self.x_vehicle_location_id = False
    
    @api.onchange('equipment_id')
    def _onchange_equipment_id(self):
        """Hereda las plantillas de checklist de la categoría del equipo"""
        if hasattr(super(), '_onchange_equipment_id'):
            super()._onchange_equipment_id()
        if self.equipment_id and hasattr(self.equipment_id, 'category_id') and self.equipment_id.category_id:
            category = self.equipment_id.category_id
            # Solo heredar si los campos están vacíos
            if not self.x_entry_checklist and hasattr(category, 'x_entry_checklist_template') and category.x_entry_checklist_template:
                self.x_entry_checklist = category.x_entry_checklist_template
            if not self.x_exit_checklist and hasattr(category, 'x_exit_checklist_template') and category.x_exit_checklist_template:
                self.x_exit_checklist = category.x_exit_checklist_template
    
    def action_view_equipment_knowledge_base(self):
        """Acción para ver la base de conocimiento de la categoría del equipo"""
        self.ensure_one()
        if not self.x_equipment_category_id:
            return {'type': 'ir.actions.act_window_close'}
        
        return self.x_equipment_category_id.action_view_knowledge_base()
    
    def action_consume_parts(self):
        """Acción para abrir el wizard de consumo de repuestos"""
        self.ensure_one()
        if not self.person_id:
            raise UserError(_('Debe asignar un técnico para consumir repuestos.'))
        
        return {
            'name': _('Consumir Repuestos'),
            'type': 'ir.actions.act_window',
            'res_model': 'fsm.consume.parts.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_fsm_order_id': self.id,
            }
        }
    
    def action_view_consumed_parts(self):
        """Acción para ver los repuestos consumidos"""
        self.ensure_one()
        return {
            'name': _('Repuestos Consumidos'),
            'type': 'ir.actions.act_window',
            'res_model': 'fsm.order.consumed.part',
            'view_mode': 'tree,form',
            'domain': [('order_id', '=', self.id)],
            'context': {'default_order_id': self.id},
            'target': 'current',
        }
    
    # Integración con fieldservice_skill
    x_required_skill_types = fields.Many2many(
        'hr.skill.type',
        string='Tipos de Habilidad Requeridos',
        help='Tipos de habilidades necesarias para esta orden'
    )
    
    # Hojas de trabajo digitales
    worksheet_ids = fields.One2many(
        'fsm.worksheet',
        'order_id',
        string='Hojas de Trabajo',
        help='Hojas de trabajo digitales asociadas a esta orden'
    )
    
    worksheet_count = fields.Integer(
        string='Número de Hojas de Trabajo',
        compute='_compute_worksheet_count'
    )
    
    has_signed_worksheet = fields.Boolean(
        string='Tiene Hoja Firmada',
        compute='_compute_worksheet_status',
        store=True,
        help='Indica si hay al menos una hoja de trabajo firmada por el cliente'
    )
    
    worksheet_completion_rate = fields.Float(
        string='% Completitud Hojas',
        compute='_compute_worksheet_status',
        store=True,
        help='Porcentaje de hojas de trabajo completadas'
    )
    
    # Campos relacionados con timesheet
    timesheet_ids = fields.One2many(
        'account.analytic.line',
        'fsm_order_id',
        string='Registros de Tiempo',
        domain=[('project_id', '!=', False)]
    )
    
    timesheet_count = fields.Integer(
        string='Registros de Tiempo',
        compute='_compute_timesheet_count'
    )
    
    total_timesheet_time = fields.Float(
        string='Tiempo Total (Horas)',
        compute='_compute_timesheet_time'
    )
    
    is_timer_running = fields.Boolean(
        string='Timer Activo',
        compute='_compute_timer_status'
    )
    
    current_timesheet_id = fields.Many2one(
        'account.analytic.line',
        string='Timesheet Actual',
        compute='_compute_timer_status'
    )
    
    # Campos de facturación
    invoice_policy = fields.Selection([
        ('manual', 'Manual'),
        ('auto_on_close', 'Automática al Cerrar'),
        ('auto_on_done', 'Automática al Completar')
    ], string='Política de Facturación', default='manual')
    
    service_product_id = fields.Many2one(
        'product.product',
        string='Producto de Servicio',
        domain=[('type', '=', 'service')],
        help='Producto que se facturará por las horas de servicio'
    )
    
    auto_invoice_time = fields.Boolean(
        string='Facturar Tiempo Automáticamente',
        default=True,
        help='Si está marcado, se facturarán automáticamente las horas registradas'
    )
    
    auto_invoice_materials = fields.Boolean(
        string='Facturar Materiales Automáticamente',
        default=True,
        help='Si está marcado, se facturarán automáticamente los repuestos consumidos'
    )
    
    x_min_skill_level = fields.Many2one(
        'hr.skill.level',
        string='Nivel Mínimo Requerido',
        help='Nivel mínimo de habilidad requerido'
    )
    
    x_available_technicians = fields.Many2many(
        'res.partner',
        string='Técnicos Disponibles',
        compute='_compute_available_technicians',
        help='Técnicos que cumplen con las habilidades requeridas'
    )
    
    x_skill_match_warning = fields.Text(
        string='Advertencia de Habilidades',
        compute='_compute_skill_match_warning',
        help='Advertencias sobre compatibilidad de habilidades'
    )
    
    # Campos computados para información contextual del activo
    x_equipment_category_name = fields.Char(
        string='Categoría del Equipo',
        compute='_compute_equipment_info',
        help='Nombre de la categoría del equipo'
    )
    x_equipment_location_name = fields.Char(
        string='Ubicación del Equipo',
        compute='_compute_equipment_info',
        help='Ubicación actual del equipo'
    )
    x_equipment_brand_model = fields.Char(
        string='Marca y Modelo',
        compute='_compute_equipment_info',
        help='Marca y modelo del equipo'
    )
    
    # Campo computado para contar repuestos consumidos
    consumed_parts_count = fields.Integer(
        string='Repuestos Consumidos',
        compute='_compute_consumed_parts_count',
        store=False
    )
    
    @api.depends('x_required_skill_types', 'x_min_skill_level', 'location_id')
    def _compute_available_technicians(self):
        """Calcula los técnicos disponibles basado en habilidades y ubicación"""
        for order in self:
            available_technicians = self.env['fsm.person']
            
            if not order.x_required_skill_types:
                # Si no hay habilidades requeridas, mostrar todos los técnicos
                available_technicians = self.env['fsm.person'].search([])
            else:
                # Buscar técnicos con las habilidades requeridas
                min_level = int(order.x_min_skill_level or '1')
                
                for skill_type in order.x_required_skill_types:
                    # Buscar técnicos con habilidades de este tipo y nivel mínimo
                    person_skills = self.env['fsm.person.skill'].search([
                        ('skill_type_id', '=', skill_type.id),
                        ('level_progress', '>=', min_level * 25)  # Asumiendo 25 puntos por nivel
                    ])
                    
                    skill_technicians = person_skills.mapped('person_id')
                    
                    if not available_technicians:
                        available_technicians = skill_technicians
                    else:
                        # Intersección - técnicos que tienen TODAS las habilidades
                        available_technicians = available_technicians & skill_technicians
            
            # Filtrar por ubicación si está configurado
            if order.location_id and available_technicians:
                # Aquí se podría agregar lógica adicional de filtrado por ubicación
                pass
            
            order.x_available_technicians = available_technicians
    
    @api.depends('x_required_skill_types', 'x_available_technicians', 'person_id')
    def _compute_skill_match_warning(self):
        """Calcula advertencias sobre compatibilidad de habilidades"""
        for order in self:
            warnings = []
            
            if order.x_required_skill_types and not order.x_available_technicians:
                warnings.append('⚠️ No hay técnicos disponibles con las habilidades requeridas.')
            
            if order.person_id and order.x_required_skill_types:
                if order.person_id not in order.x_available_technicians:
                    warnings.append(f'⚠️ El técnico asignado ({order.person_id.name}) no cumple con todos los requisitos de habilidades.')
            
            if order.x_required_skill_types and len(order.x_available_technicians) < 3:
                warnings.append(f'⚠️ Pocos técnicos disponibles ({len(order.x_available_technicians)}). Considere capacitar más personal.')
            
            order.x_skill_match_warning = '\n'.join(warnings) if warnings else False
    
    @api.onchange('x_equipment_category_id')
    def _onchange_equipment_category_skills(self):
        """Actualiza las habilidades requeridas basado en la categoría del equipo"""
        if self.x_equipment_category_id:
            # Mapeo de categorías a tipos de habilidades
            category_skill_mapping = {
                # Aquí se pueden definir mapeos específicos
                # Por ejemplo: 'Aire Acondicionado': ['Refrigeración', 'Electricidad']
            }
            
            category_name = self.x_equipment_category_id.name
            if category_name in category_skill_mapping:
                skill_type_names = category_skill_mapping[category_name]
                skill_types = self.env['hr.skill.type'].search([('name', 'in', skill_type_names)])
                self.x_required_skill_types = skill_types
    
    def action_suggest_technician(self):
        """Acción para sugerir técnico basado en habilidades"""
        if not self.x_required_skill_types:
            raise UserError("Debe especificar al menos un tipo de habilidad requerida.")
        
        # Buscar técnicos con las habilidades requeridas
        available_techs = self.x_available_technicians
        
        if not available_techs:
            raise UserError("No se encontraron técnicos con las habilidades requeridas.")
        
        # Si hay técnicos disponibles, mostrar wizard de selección
        return {
            'type': 'ir.actions.act_window',
            'name': 'Seleccionar Técnico',
            'res_model': 'fsm.wizard.assign.person',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': self.id,
                'available_technicians': available_techs.ids,
            }
        }
    
    def action_suggest_technicians(self):
        """Abre wizard para sugerir técnicos basado en habilidades"""
        self.ensure_one()
        return {
            'name': _('Técnicos Sugeridos'),
            'type': 'ir.actions.act_window',
            'res_model': 'fsm.technician.suggestion.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_id': self.id,
                'default_required_skill_ids': [(6, 0, self.required_skill_ids.ids)]
            }
        }
    
    @api.depends('worksheet_ids')
    def _compute_worksheet_count(self):
        """Calcula el número de hojas de trabajo"""
        for order in self:
            order.worksheet_count = len(order.worksheet_ids)
    
    @api.depends('x_consumed_parts_ids')
    def _compute_consumed_parts_count(self):
        """Computar el número de repuestos consumidos"""
        for record in self:
            record.consumed_parts_count = len(record.x_consumed_parts_ids)
    
    @api.depends('worksheet_ids', 'worksheet_ids.state')
    def _compute_worksheet_status(self):
        """Calcula el estado de las hojas de trabajo"""
        for order in self:
            worksheets = order.worksheet_ids
            if not worksheets:
                order.has_signed_worksheet = False
                order.worksheet_completion_rate = 0.0
            else:
                signed_count = len(worksheets.filtered(lambda w: w.state == 'signed'))
                order.has_signed_worksheet = signed_count > 0
                order.worksheet_completion_rate = (signed_count / len(worksheets)) * 100
    
    @api.depends('timesheet_ids')
    def _compute_timesheet_count(self):
        """Calcula el número de registros de tiempo"""
        for order in self:
            order.timesheet_count = len(order.timesheet_ids)
    
    @api.depends('timesheet_ids', 'timesheet_ids.unit_amount')
    def _compute_timesheet_time(self):
        """Calcula el tiempo total registrado"""
        for order in self:
            order.total_timesheet_time = sum(order.timesheet_ids.mapped('unit_amount'))
    
    @api.depends('timesheet_ids', 'timesheet_ids.date_time')
    def _compute_timer_status(self):
        """Verifica si hay un timer activo"""
        for order in self:
            running_timesheet = order.timesheet_ids.filtered(
                lambda t: not t.unit_amount and t.date_time
            )
            order.is_timer_running = bool(running_timesheet)
            order.current_timesheet_id = running_timesheet[:1] if running_timesheet else False
    
    def action_view_worksheets(self):
        """Abre la vista de hojas de trabajo"""
        self.ensure_one()
        action = self.env.ref('patco_core.action_fsm_worksheet').read()[0]
        
        if len(self.worksheet_ids) > 1:
            action['domain'] = [('order_id', '=', self.id)]
        elif len(self.worksheet_ids) == 1:
            action['views'] = [(self.env.ref('patco_core.view_fsm_worksheet_form').id, 'form')]
            action['res_id'] = self.worksheet_ids.id
        else:
            # No hay hojas de trabajo, crear una nueva
            return self.action_create_worksheet()
        
        action['context'] = {
            'default_order_id': self.id,
            'search_default_order_id': self.id
        }
        return action
    
    def action_create_invoice(self):
        """Crea una factura basada en tiempo y materiales"""
        self.ensure_one()
        
        if not self.location_id:
            raise UserError(_('Debe especificar una ubicación para crear la factura.'))
        
        # Crear la factura
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.location_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [],
        }
        
        invoice_lines = []
        
        # Agregar líneas por tiempo si está habilitado
        if self.auto_invoice_time and self.service_product_id:
            timesheet_lines = self.env['account.analytic.line'].search([
                ('fsm_order_id', '=', self.id)
            ])
            
            total_hours = sum(timesheet_lines.mapped('unit_amount'))
            if total_hours > 0:
                invoice_lines.append((0, 0, {
                    'product_id': self.service_product_id.id,
                    'name': f'Servicio técnico - {self.name}',
                    'quantity': total_hours,
                    'price_unit': self.service_product_id.list_price,
                    'product_uom_id': self.service_product_id.uom_id.id,
                }))
        
        # Agregar líneas por materiales si está habilitado
        if self.auto_invoice_materials:
            consumed_parts = self.env['fsm.order.consumed.part'].search([
                ('order_id', '=', self.id),
                ('state', '=', 'confirmed')
            ])
            
            for part in consumed_parts:
                invoice_lines.append((0, 0, {
                    'product_id': part.product_id.id,
                    'name': f'Material - {part.product_id.name}',
                    'quantity': part.quantity,
                    'price_unit': part.unit_cost,
                    'product_uom_id': part.product_uom_id.id,
                }))
        
        if not invoice_lines:
            raise UserError(_('No hay elementos para facturar. Verifique que tenga tiempo registrado o materiales consumidos.'))
        
        invoice_vals['invoice_line_ids'] = invoice_lines
        
        # Crear la factura
        invoice = self.env['account.move'].create(invoice_vals)
        
        return {
            'name': _('Factura Creada'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',
        }
    
    def _auto_invoice_on_stage_change(self):
        """Crea factura automáticamente según la política configurada"""
        for record in self:
            if record.invoice_policy == 'auto_on_done' and record.stage_id.is_closed:
                record.action_create_invoice()
            elif record.invoice_policy == 'auto_on_close' and record.stage_id.is_closed:
                 record.action_create_invoice()
    
    def write(self, vals):
        """Sobrescribir write para activar facturación automática"""
        result = super(FSMOrder, self).write(vals)
        
        # Si se cambió el stage_id, verificar facturación automática
        if 'stage_id' in vals:
            self._auto_invoice_on_stage_change()
        
        return result
    
    def action_view_timesheet(self):
        """Acción para ver los registros de tiempo"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Registros de Tiempo',
            'res_model': 'account.analytic.line',
            'view_mode': 'tree,form',
            'domain': [('fsm_order_id', '=', self.id)],
            'context': {
                'default_fsm_order_id': self.id,
                'default_project_id': self.project_id.id if self.project_id else False,
                'default_task_id': self.task_id.id if self.task_id else False,
                'default_name': f'Trabajo en {self.location_id.name or self.name}',
            },
        }
    
    def action_start_timer(self):
        """Inicia el timer de trabajo"""
        self.ensure_one()
        if self.is_timer_running:
            raise UserError(_("Ya hay un timer activo para esta orden."))
        
        # Crear nuevo registro de timesheet
        timesheet_vals = {
            'fsm_order_id': self.id,
            'project_id': self.project_id.id if self.project_id else False,
            'task_id': self.task_id.id if self.task_id else False,
            'name': f'Trabajo en {self.location_id.name or self.name}',
            'date': fields.Date.today(),
            'date_time': fields.Datetime.now(),
            'user_id': self.env.user.id,
            'employee_id': self.env.user.employee_id.id if self.env.user.employee_id else False,
        }
        
        timesheet = self.env['account.analytic.line'].create(timesheet_vals)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': _("Timer iniciado correctamente."),
                'type': 'success',
                'sticky': False,
            }
        }
    
    def action_stop_timer(self):
        """Detiene el timer de trabajo"""
        self.ensure_one()
        if not self.is_timer_running:
            raise UserError(_("No hay timer activo para esta orden."))
        
        current_timesheet = self.current_timesheet_id
        if current_timesheet and current_timesheet.date_time:
            # Calcular tiempo transcurrido
            start_time = current_timesheet.date_time
            end_time = fields.Datetime.now()
            duration = (end_time - start_time).total_seconds() / 3600  # Convertir a horas
            
            current_timesheet.write({
                'unit_amount': duration,
                'date_time': False,  # Limpiar para indicar que terminó
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': _("Timer detenido. Tiempo registrado: %.2f horas.") % duration,
                    'type': 'success',
                    'sticky': False,
                }
            }
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': _("Error al detener el timer."),
                'type': 'warning',
                'sticky': False,
            }
        }
    
    def action_create_worksheet(self):
        """Crea una nueva hoja de trabajo"""
        self.ensure_one()
        
        # Buscar plantilla por defecto o por categoría de equipo
        template = self._get_default_worksheet_template()
        
        if not template:
            raise UserError(_("No se encontró una plantilla de hoja de trabajo adecuada. "
                            "Configure plantillas en el menú de Field Service."))
        
        # Crear la hoja de trabajo
        worksheet = self.env['fsm.worksheet'].create({
            'order_id': self.id,
            'template_id': template.id,
            'name': f"Hoja de Trabajo - {self.name}"
        })
        
        # Abrir la hoja de trabajo creada
        return {
            'name': _('Nueva Hoja de Trabajo'),
            'type': 'ir.actions.act_window',
            'res_model': 'fsm.worksheet',
            'res_id': worksheet.id,
            'view_mode': 'form',
            'target': 'current'
        }
    
    def _get_default_worksheet_template(self):
        """Obtiene la plantilla por defecto para esta orden"""
        self.ensure_one()
        
        # Buscar por categoría de equipo
        if self.equipment_id and self.equipment_id.category_id:
            template = self.env['fsm.worksheet.template'].search([
                ('equipment_category_ids', 'in', self.equipment_id.category_id.id),
                ('active', '=', True)
            ], limit=1)
            if template:
                return template
        
        # Buscar por naturaleza del servicio
        if hasattr(self, 'service_nature_id') and self.service_nature_id:
            template = self.env['fsm.worksheet.template'].search([
                ('service_nature_ids', 'in', self.service_nature_id.id),
                ('active', '=', True)
            ], limit=1)
            if template:
                return template
        
        # Plantilla por defecto
        return self.env['fsm.worksheet.template'].search([
            ('active', '=', True)
        ], limit=1)
    
    @api.depends('equipment_id')
    def _compute_equipment_info(self):
        """Computar información contextual del activo"""
        for record in self:
            if record.equipment_id:
                equipment = record.equipment_id
                
                # Categoría del equipo
                record.x_equipment_category_name = equipment.category_id.name if equipment.category_id else 'Sin categoría'
                
                # Ubicación del equipo
                if hasattr(equipment, 'location_id') and equipment.location_id:
                    record.x_equipment_location_name = equipment.location_id.name
                elif hasattr(equipment, 'partner_id') and equipment.partner_id:
                    record.x_equipment_location_name = f"Cliente: {equipment.partner_id.name}"
                else:
                    record.x_equipment_location_name = 'Ubicación no definida'
                
                # Marca y modelo
                brand = getattr(equipment, 'brand', '') or ''
                model = getattr(equipment, 'model', '') or ''
                if brand and model:
                    record.x_equipment_brand_model = f"{brand} - {model}"
                elif brand:
                    record.x_equipment_brand_model = brand
                elif model:
                    record.x_equipment_brand_model = model
                else:
                    record.x_equipment_brand_model = 'No especificado'
            else:
                record.x_equipment_category_name = ''
                record.x_equipment_location_name = ''
                record.x_equipment_brand_model = ''