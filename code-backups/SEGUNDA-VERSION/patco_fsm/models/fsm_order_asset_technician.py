# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FSMOrderAssetTechnician(models.Model):
    """Modelo intermedio para gestionar la relación entre órdenes de servicio,
    activos y técnicos asignados. Permite múltiples activos por orden y
    asignación específica de técnicos por activo."""
    
    _name = 'fsm.order.asset.technician'
    _description = 'Asignación Activo-Técnico en Orden FSM'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'order_id, sequence, asset_id'
    _rec_name = 'display_name'
    
    # Campos principales de relación
    order_id = fields.Many2one(
        'fsm.order',
        string='Orden de Servicio',
        required=True,
        ondelete='cascade',
        help='Orden de servicio a la que pertenece esta asignación'
    )
    
    asset_id = fields.Many2one(
        'maintenance.equipment',
        string='Activo/Equipo',
        required=True,
        help='Equipo o activo a ser atendido'
    )
    
    technician_id = fields.Many2one(
        'res.partner',
        string='Técnico Asignado',
        required=True,
        domain=[('is_company', '=', False), ('x_is_technician', '=', True)],
        help='Técnico responsable de este activo en la orden'
    )
    
    # Campos de control y estado
    sequence = fields.Integer(
        string='Secuencia',
        default=10,
        help='Orden de prioridad en la ejecución'
    )
    
    is_lead = fields.Boolean(
        string='Es Líder Técnico',
        default=False,
        help='Indica si este técnico es el líder de la orden'
    )
    
    status = fields.Selection([
        ('pending', 'Pendiente'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completado'),
        ('blocked', 'Bloqueado'),
        ('cancelled', 'Cancelado')
    ], string='Estado', default='pending', required=True,
       help='Estado actual del trabajo en este activo')
    
    # Campos de información adicional
    notes = fields.Text(
        string='Observaciones',
        help='Notas específicas para este activo y técnico'
    )
    
    estimated_hours = fields.Float(
        string='Horas Estimadas',
        help='Tiempo estimado para completar el trabajo en este activo'
    )
    
    actual_hours = fields.Float(
        string='Horas Reales',
        compute='_compute_actual_hours',
        store=True,
        help='Tiempo real invertido en este activo'
    )
    
    # Campos relacionados para facilitar consultas
    customer_id = fields.Many2one(
        related='order_id.location_id.owner_id',
        string='Cliente',
        store=True,
        readonly=True
    )
    
    asset_category_id = fields.Many2one(
        related='asset_id.category_id',
        string='Categoría del Activo',
        store=True,
        readonly=True
    )
    
    asset_location = fields.Char(
        related='asset_id.x_service_location_id.name',
        string='Ubicación del Activo',
        store=True,
        readonly=True
    )
    
    # Campo computado para nombre de visualización
    display_name = fields.Char(
        string='Nombre',
        compute='_compute_display_name',
        store=True
    )
    
    # Campos de fechas
    date_start = fields.Datetime(
        string='Fecha Inicio',
        help='Fecha y hora de inicio del trabajo en este activo'
    )
    
    date_end = fields.Datetime(
        string='Fecha Fin',
        help='Fecha y hora de finalización del trabajo en este activo'
    )
    
    # Campos de checklist específicos por activo
    entry_checklist_completed = fields.Boolean(
        string='Checklist Entrada Completado',
        default=False,
        help='Indica si se completó el checklist de entrada para este activo'
    )
    
    exit_checklist_completed = fields.Boolean(
        string='Checklist Salida Completado',
        default=False,
        help='Indica si se completó el checklist de salida para este activo'
    )
    
    # Campos de materiales específicos por activo
    consumed_parts_ids = fields.One2many(
        'fsm.order.consumed.part',
        'asset_technician_id',
        string='Repuestos Consumidos',
        help='Repuestos utilizados específicamente en este activo'
    )
    
    parts_cost = fields.Float(
        string='Costo Repuestos',
        compute='_compute_parts_cost',
        store=True,
        help='Costo total de repuestos para este activo'
    )
    
    estimated_cost = fields.Float(
        string='Costo Estimado',
        help='Costo estimado total para el trabajo en este activo'
    )
    
    actual_cost = fields.Float(
        string='Costo Real',
        help='Costo real total para el trabajo en este activo'
    )
    
    @api.depends('order_id.name', 'asset_id.name', 'technician_id.name')
    def _compute_display_name(self):
        """Computa el nombre de visualización de la asignación."""
        for record in self:
            if record.order_id and record.asset_id and record.technician_id:
                lead_text = " (Líder)" if record.is_lead else ""
                record.display_name = f"{record.order_id.name} - {record.asset_id.name} - {record.technician_id.name}{lead_text}"
            else:
                record.display_name = "Nueva Asignación"
    
    @api.depends('consumed_parts_ids.total_cost')
    def _compute_parts_cost(self):
        """Calcula el costo total de repuestos para este activo."""
        for record in self:
            record.parts_cost = sum(record.consumed_parts_ids.mapped('total_cost'))
    
    @api.depends('date_start', 'date_end')
    def _compute_actual_hours(self):
        """Calcula las horas reales basadas en fechas de inicio y fin."""
        for record in self:
            if record.date_start and record.date_end:
                delta = record.date_end - record.date_start
                record.actual_hours = delta.total_seconds() / 3600.0
            else:
                record.actual_hours = 0.0
    
    @api.constrains('order_id', 'asset_id', 'technician_id')
    def _check_unique_assignment(self):
        """Valida que no haya asignaciones duplicadas del mismo técnico al mismo activo en la misma orden."""
        for record in self:
            domain = [
                ('order_id', '=', record.order_id.id),
                ('asset_id', '=', record.asset_id.id),
                ('technician_id', '=', record.technician_id.id),
                ('id', '!=', record.id)
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    _("El técnico %s ya está asignado al activo %s en esta orden.") % 
                    (record.technician_id.name, record.asset_id.name)
                )
    
    @api.constrains('is_lead', 'order_id')
    def _check_single_lead_per_order(self):
        """Valida que solo haya un líder técnico por orden."""
        for record in self:
            if record.is_lead:
                domain = [
                    ('order_id', '=', record.order_id.id),
                    ('is_lead', '=', True),
                    ('id', '!=', record.id)
                ]
                if self.search_count(domain) > 0:
                    raise ValidationError(
                        _("Solo puede haber un líder técnico por orden de servicio.")
                    )
    
    @api.constrains('asset_id', 'order_id')
    def _check_asset_customer_match(self):
        """Valida que el activo pertenezca al cliente de la orden."""
        for record in self:
            if record.asset_id and record.order_id and record.order_id.location_id:
                if record.asset_id.x_customer_id != record.order_id.location_id.owner_id:
                    raise ValidationError(
                        _("El activo %s no pertenece al cliente %s de la orden.") % 
                        (record.asset_id.name, record.order_id.location_id.owner_id.name)
                    )
    
    def action_start_work(self):
        """Inicia el trabajo en este activo."""
        self.ensure_one()
        if self.status != 'pending':
            raise ValidationError(_("Solo se puede iniciar trabajo en estado 'Pendiente'."))
        
        self.write({
            'status': 'in_progress',
            'date_start': fields.Datetime.now()
        })
        
        return True
    
    def action_complete_work(self):
        """Completa el trabajo en este activo."""
        self.ensure_one()
        if self.status != 'in_progress':
            raise ValidationError(_("Solo se puede completar trabajo en estado 'En Progreso'."))
        
        self.write({
            'status': 'completed',
            'date_end': fields.Datetime.now()
        })
        
        # Verificar si todos los activos de la orden están completados
        order_assignments = self.search([('order_id', '=', self.order_id.id)])
        if all(assignment.status == 'completed' for assignment in order_assignments):
            # Opcional: cambiar estado de la orden principal
            pass
        
        return True
    
    def action_block_work(self):
        """Bloquea el trabajo en este activo."""
        self.ensure_one()
        self.status = 'blocked'
        return True
    
    def action_cancel_work(self):
        """Cancela el trabajo en este activo."""
        self.ensure_one()
        self.status = 'cancelled'
        return True
    
    def action_reset_to_pending(self):
        """Resetea el trabajo a estado pendiente."""
        self.ensure_one()
        self.write({
            'status': 'pending',
            'date_start': False,
            'date_end': False
        })
        return True