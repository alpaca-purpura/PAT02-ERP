# -*- coding: utf-8 -*-

import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class FsmPerson(models.Model):
    _inherit = 'fsm.person'

    # Campo para vincular con hr.employee
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        help='Empleado asociado en Recursos Humanos'
    )

    @api.model
    def create(self, vals):
        """Override create para buscar empleado asociado automáticamente."""
        fsm_person = super().create(vals)
        
        # Intentar encontrar empleado asociado por email o teléfono
        if fsm_person.partner_id:
            fsm_person._find_and_link_employee()
        
        return fsm_person

    def write(self, vals):
        """Override write para sincronizar cambios con hr.employee."""
        result = super().write(vals)
        
        # Si se actualiza el partner, sincronizar con empleado
        if 'partner_id' in vals:
            for fsm_person in self:
                if fsm_person.partner_id and not fsm_person.employee_id:
                    fsm_person._find_and_link_employee()
        
        # Si hay cambios en datos de contacto del partner, sincronizar
        partner_sync_fields = ['name', 'phone', 'email']
        if any(field in vals for field in partner_sync_fields):
            for fsm_person in self:
                if fsm_person.employee_id:
                    fsm_person._sync_to_employee()
        
        return result

    def _find_and_link_employee(self):
        """Buscar y vincular empleado asociado por email o teléfono."""
        self.ensure_one()
        
        if self.employee_id or not self.partner_id:
            return
        
        employee = None
        
        # Buscar por email
        if self.partner_id.email:
            employee = self.env['hr.employee'].search([
                ('work_email', '=', self.partner_id.email),
                ('is_field_technician', '=', True)
            ], limit=1)
        
        # Si no se encuentra por email, buscar por teléfono
        if not employee and self.partner_id.phone:
            employee = self.env['hr.employee'].search([
                '|',
                ('work_phone', '=', self.partner_id.phone),
                ('mobile_phone', '=', self.partner_id.phone),
                ('is_field_technician', '=', True)
            ], limit=1)
        
        # Si no se encuentra por teléfono, buscar por nombre
        if not employee and self.partner_id.name:
            employee = self.env['hr.employee'].search([
                ('name', '=', self.partner_id.name),
                ('is_field_technician', '=', True)
            ], limit=1)
        
        if employee:
            # Vincular ambos registros
            self.employee_id = employee.id
            employee.fsm_person_id = self.id
            
            _logger.info(
                f"Linked FSM Person {self.name} with employee {employee.name}"
            )

    def _sync_to_employee(self):
        """Sincronizar datos de fsm.person hacia hr.employee."""
        self.ensure_one()
        
        if not self.employee_id or not self.partner_id:
            return
        
        try:
            # Preparar valores para actualizar en el empleado
            employee_vals = {}
            
            # Sincronizar nombre si es diferente
            if self.partner_id.name != self.employee_id.name:
                employee_vals['name'] = self.partner_id.name
            
            # Sincronizar email si es diferente
            if (self.partner_id.email and 
                self.partner_id.email != self.employee_id.work_email):
                employee_vals['work_email'] = self.partner_id.email
            
            # Sincronizar teléfono si es diferente
            if (self.partner_id.phone and 
                self.partner_id.phone not in [self.employee_id.work_phone, self.employee_id.mobile_phone]):
                # Priorizar work_phone, usar mobile_phone como alternativa
                if not self.employee_id.work_phone:
                    employee_vals['work_phone'] = self.partner_id.phone
                elif not self.employee_id.mobile_phone:
                    employee_vals['mobile_phone'] = self.partner_id.phone
            
            # Actualizar empleado si hay cambios
            if employee_vals:
                # Evitar recursión desactivando temporalmente la sincronización
                self.employee_id.with_context(skip_fsm_sync=True).write(employee_vals)
                
                _logger.debug(
                    f"Synced FSM Person {self.name} data to employee {self.employee_id.name}"
                )
            
        except Exception as e:
            _logger.error(
                f"Error syncing FSM Person {self.name} to employee: {str(e)}"
            )

    def action_link_employee(self):
        """Acción manual para vincular con empleado."""
        for fsm_person in self:
            if fsm_person.employee_id:
                raise UserError(
                    _("La persona FSM %s ya está vinculada con el empleado %s") % 
                    (fsm_person.name, fsm_person.employee_id.name)
                )
            fsm_person._find_and_link_employee()
            
            if not fsm_person.employee_id:
                raise UserError(
                    _("No se encontró un empleado técnico de campo que coincida con %s") % 
                    fsm_person.name
                )
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Éxito'),
                'message': _('Empleado vinculado correctamente'),
                'type': 'success',
            }
        }

    @api.model
    def sync_all_with_employees(self):
        """Método para sincronizar todas las personas FSM con empleados.
        
        Este método es llamado por el cron job para mantener la sincronización.
        """
        _logger.info("Starting sync of all FSM persons with employees")
        
        # Buscar todas las personas FSM
        fsm_persons = self.search([])
        
        linked_count = 0
        synced_count = 0
        error_count = 0
        
        for fsm_person in fsm_persons:
            try:
                # Si no tiene empleado vinculado, intentar vincularlo
                if not fsm_person.employee_id:
                    fsm_person._find_and_link_employee()
                    if fsm_person.employee_id:
                        linked_count += 1
                else:
                    # Si ya tiene empleado, sincronizar datos
                    fsm_person._sync_to_employee()
                    synced_count += 1
            except Exception as e:
                _logger.error(
                    f"Error syncing FSM Person {fsm_person.name}: {str(e)}"
                )
                error_count += 1
        
        _logger.info(
            f"FSM sync completed: {linked_count} linked, {synced_count} synced, {error_count} errors"
        )
        
        return {
            'linked': linked_count,
            'synced': synced_count,
            'errors': error_count
        }

    def unlink(self):
        """Override unlink para limpiar referencia en hr.employee."""
        # Limpiar referencia en empleados antes de eliminar
        for fsm_person in self:
            if fsm_person.employee_id:
                fsm_person.employee_id.fsm_person_id = False
                _logger.info(
                    f"Cleared FSM Person reference from employee {fsm_person.employee_id.name}"
                )
        
        return super().unlink()