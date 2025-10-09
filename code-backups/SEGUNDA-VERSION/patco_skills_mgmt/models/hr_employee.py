# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Campo de habilidades técnicas (no existe en Odoo 18 Community)
    employee_skill_ids = fields.One2many(
        'hr.employee.skill',
        'employee_id',
        string='Habilidades',
        help='Habilidades técnicas del empleado'
    )
    
    # Campo computado para mostrar habilidades principales
    main_skills = fields.Char(
        string='Habilidades Principales',
        compute='_compute_main_skills',
        store=True,
        help='Resumen de las principales habilidades técnicas'
    )
    
    # Campo para indicar si es técnico de campo
    is_field_technician = fields.Boolean(
        string='Técnico de Campo',
        default=False,
        help='Indica si el empleado es un técnico de campo para servicios'
    )

    fsm_order_ids = fields.One2many(
        'fsm.order', 'person_id',
        string='Órdenes de Servicio',
        help='Órdenes de servicio asignadas a este empleado'
    )
    
    # Campo computado para contar órdenes de servicio
    fsm_order_count = fields.Integer(
        string='Órdenes de Servicio',
        compute='_compute_fsm_order_count',
        help='Número de órdenes de servicio asignadas'
    )
    
    # Campos para integración FSM
    fsm_person_id = fields.Many2one(
        'fsm.person',
        string='Persona FSM',
        help='Persona asociada en el módulo FSM'
    )
    
    fsm_sync_date = fields.Datetime(
        string='Fecha de Sincronización',
        help='Última fecha de sincronización con FSM'
    )
    
    fsm_sync_status = fields.Selection([
        ('pending', 'Pendiente'),
        ('synced', 'Sincronizado'),
        ('error', 'Error')
    ], string='Estado de Sincronización', default='pending',
       help='Estado de la sincronización con FSM')

    @api.model
    def write(self, vals):
        """Override write para crear/actualizar fsm.person automáticamente."""
        # Validaciones previas
        if not isinstance(vals, dict):
            raise ValidationError("Los valores deben ser un diccionario")
        
        # Validar campos críticos
        if 'name' in vals and not vals['name']:
            raise ValidationError("El nombre del empleado no puede estar vacío")
        
        if 'work_email' in vals and vals['work_email']:
            # Validación básica de email
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, vals['work_email']):
                raise ValidationError("El formato del email de trabajo no es válido")
        
        result = super().write(vals)
        
        # Si se marca como técnico de campo, crear fsm.person
        if 'is_field_technician' in vals and vals['is_field_technician']:
            for employee in self:
                try:
                    if not employee.fsm_person_id:
                        employee._create_fsm_person()
                    else:
                        employee._sync_to_fsm_person()
                except Exception as e:
                    _logger.error(f"Error procesando técnico de campo {employee.name}: {str(e)}")
                    # No interrumpir el proceso, solo registrar el error
                    employee.write({'fsm_sync_status': 'error'})
        
        # Si se actualizan datos de contacto, sincronizar con fsm.person
        sync_fields = ['name', 'work_phone', 'work_email', 'mobile_phone']
        if any(field in vals for field in sync_fields):
            for employee in self:
                if employee.fsm_person_id:
                    try:
                        employee._sync_to_fsm_person()
                    except Exception as e:
                        _logger.error(f"Error sincronizando datos de contacto para {employee.name}: {str(e)}")
                        employee.write({'fsm_sync_status': 'error'})
        
        return result
    
    @api.depends('fsm_order_ids')
    def _compute_fsm_order_count(self):
        """Computa el número de órdenes de servicio"""
        for employee in self:
            employee.fsm_order_count = len(employee.fsm_order_ids)
    def action_view_fsm_orders(self):
        """Acción para ver las órdenes de servicio del empleado"""
        action = self.env.ref('fieldservice.action_fsm_order').read()[0]
        action['domain'] = [('person_id', '=', self.id)]
        action['context'] = {'default_person_id': self.id}
        return action
    
    @api.depends('employee_skill_ids.skill_id', 'employee_skill_ids.skill_level_id')
    def _compute_main_skills(self):
        """Computa las habilidades principales del empleado"""
        for employee in self:
            skills = []
            for skill_line in employee.employee_skill_ids:
                if skill_line.skill_id and skill_line.skill_level_id:
                    skill_text = f"{skill_line.skill_id.name} ({skill_line.skill_level_id.name})"
                    skills.append(skill_text)
            employee.main_skills = ', '.join(skills[:3])  # Mostrar solo las 3 principales
    
    def get_skills_by_type(self, skill_type_name):
        """Obtiene las habilidades del empleado por tipo.
        
        Args:
            skill_type_name (str): Nombre del tipo de habilidad
            
        Returns:
            recordset: Habilidades del empleado del tipo especificado
        """
        # Validaciones de entrada
        if not skill_type_name:
            _logger.warning(f"skill_type_name no proporcionado para empleado {self.name}")
            return self.env['hr.employee.skill'].browse()
        
        if not isinstance(skill_type_name, str):
            _logger.warning(f"skill_type_name debe ser string para empleado {self.name}")
            return self.env['hr.employee.skill'].browse()
        
        # Verificar que el empleado existe
        if not self.exists():
            _logger.warning("Empleado no existe en la base de datos")
            return self.env['hr.employee.skill'].browse()
        
        try:
            return self.employee_skill_ids.filtered(
                lambda s: s.skill_id and 
                         s.skill_id.skill_type_id and 
                         s.skill_id.skill_type_id.name == skill_type_name
            )
        except Exception as e:
            _logger.error(f"Error obteniendo habilidades por tipo '{skill_type_name}' para empleado {self.name}: {str(e)}")
            return self.env['hr.employee.skill'].browse()
    
    def has_skill_level(self, skill_id, min_level=1):
        """Verifica si el empleado tiene una habilidad con el nivel mínimo requerido."""
        # Validaciones de entrada
        if not skill_id:
            _logger.warning(f"skill_id no proporcionado para empleado {self.name}")
            return False
        
        if not isinstance(min_level, (int, float)) or min_level < 0:
            _logger.warning(f"min_level inválido ({min_level}) para empleado {self.name}")
            return False
        
        # Verificar que el empleado existe
        if not self.exists():
            _logger.warning("Empleado no existe en la base de datos")
            return False
        
        try:
            skill_line = self.employee_skill_ids.filtered(
                lambda s: s.skill_id.id == skill_id and 
                         s.skill_level_id and 
                         s.skill_level_id.level_progress >= min_level
            )
            return bool(skill_line)
        except Exception as e:
            _logger.error(f"Error verificando habilidad {skill_id} para empleado {self.name}: {str(e)}")
            return False
    
    @api.model
    def action_sync_all_field_technicians(self):
        """Acción para sincronizar todos los técnicos de campo con FSM."""
        field_technicians = self.env['hr.employee'].search([('is_field_technician', '=', True)])
        
        if not field_technicians:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sincronización FSM',
                    'message': 'No se encontraron técnicos de campo para sincronizar.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        # Ejecutar sincronización en background
        field_technicians.sync_all_field_technicians()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Sincronización Iniciada',
                'message': f'Se ha iniciado la sincronización de {len(field_technicians)} técnicos de campo.',
                'type': 'success',
                'sticky': False,
            }
        }
    
    def sync_all_field_technicians(self):
        """Sincronizar todos los técnicos de campo (llamado por cron job)."""
        success_count = 0
        error_count = 0
        
        _logger.info("Iniciando sincronización masiva de técnicos de campo")
        
        for employee in self:
            if not employee.is_field_technician:
                continue
                
            try:
                if not employee.fsm_person_id:
                    employee._create_fsm_person()
                    _logger.info(f"FSM person creado para {employee.name}")
                else:
                    employee._sync_to_fsm_person()
                    _logger.info(f"FSM person actualizado para {employee.name}")
                
                # Sincronizar habilidades si existen
                if employee.skill_ids:
                    employee._sync_skills_to_fsm()
                
                success_count += 1
                
            except Exception as e:
                error_count += 1
                _logger.error(f"Error sincronizando {employee.name}: {str(e)}")
                employee.write({'fsm_sync_status': 'error'})
        
        _logger.info(f"Sincronización completada: {success_count} éxitos, {error_count} errores")
        
        # Notificar administradores si hay errores
        if error_count > 0:
            admin_users = self.env['res.users'].search([('groups_id', 'in', [self.env.ref('base.group_system').id])])
            for admin in admin_users:
                self.env['mail.message'].create({
                    'subject': 'Errores en Sincronización FSM',
                    'body': f'Se encontraron {error_count} errores durante la sincronización masiva de técnicos de campo.',
                    'partner_ids': [(4, admin.partner_id.id)],
                    'message_type': 'notification',
                })
    
    def migrate_existing_technicians(self):
        """Migrar técnicos existentes a FSM (ejecutar una sola vez)."""
        technicians_without_fsm = self.env['hr.employee'].search([
            ('is_field_technician', '=', True),
            ('fsm_person_id', '=', False)
        ])
        
        if not technicians_without_fsm:
            _logger.info("No hay técnicos para migrar")
            return
        
        _logger.info(f"Migrando {len(technicians_without_fsm)} técnicos existentes")
        
        success_count = 0
        error_count = 0
        
        for technician in technicians_without_fsm:
            try:
                technician._create_fsm_person()
                
                # Sincronizar habilidades si existen
                if technician.skill_ids:
                    technician._sync_skills_to_fsm()
                
                success_count += 1
                _logger.info(f"Técnico migrado: {technician.name}")
                
            except Exception as e:
                error_count += 1
                _logger.error(f"Error migrando técnico {technician.name}: {str(e)}")
                technician.write({'fsm_sync_status': 'error'})
        
        _logger.info(f"Migración completada: {success_count} éxitos, {error_count} errores")
    

    
    def action_sync_selected_employees(self):
        """Sincroniza los empleados seleccionados con FSM
        
        Returns:
            dict: Resultado de la acción con notificación
        """
        try:
            # Filtrar solo técnicos de campo
            field_technicians = self.filtered('is_field_technician')
            
            if not field_technicians:
                raise UserError("Seleccione al menos un técnico de campo para sincronizar")
            
            synced_count = 0
            error_count = 0
            
            for employee in field_technicians:
                try:
                    if not employee.fsm_person_id:
                        employee._create_fsm_person()
                    else:
                        employee._sync_to_fsm_person()
                    synced_count += 1
                except Exception as e:
                    employee.fsm_sync_status = 'error'
                    error_count += 1
                    _logger.error(f"Error sincronizando empleado {employee.name}: {str(e)}")
            
            # Mostrar notificación de resultado
            if error_count == 0:
                message = f"Se sincronizaron {synced_count} técnicos correctamente"
                title = "Sincronización Completada"
            else:
                message = f"Se sincronizaron {synced_count} técnicos. {error_count} con errores"
                title = "Sincronización Completada con Errores"
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': title,
                    'message': message,
                    'type': 'success' if error_count == 0 else 'warning',
                    'sticky': False,
                }
            }
            
        except Exception as e:
             raise UserError(f"Error sincronizando empleados seleccionados: {str(e)}")
    
    def _create_fsm_person(self):
        """Crea un registro fsm.person para el empleado."""
        # Validaciones previas
        if not self.exists():
            _logger.error("Empleado no existe en la base de datos")
            return False
        
        if not self.is_field_technician:
            _logger.warning(f"Empleado {self.name} no está marcado como técnico de campo")
            return False
        
        if not self.name:
            _logger.error(f"Empleado {self.id} no tiene nombre definido")
            return False
        
        if self.fsm_person_id:
            _logger.warning(f"Empleado {self.name} ya tiene fsm.person asociado")
            return self.fsm_person_id
        
        try:
            # Verificar si ya existe un partner para este empleado
            partner = self.env['res.partner'].search([
                ('name', '=', self.name),
                ('is_company', '=', False),
                ('supplier_rank', '>', 0)
            ], limit=1)
            
            if not partner:
                # Crear partner si no existe
                partner_vals = {
                    'name': self.name,
                    'email': self.work_email or '',
                    'phone': self.work_phone or self.mobile_phone or '',
                    'is_company': False,
                    'supplier_rank': 1,  # Marcar como proveedor
                    'category_id': [(6, 0, [])],  # Sin categorías por defecto
                }
                partner = self.env['res.partner'].create(partner_vals)
                _logger.info(f"Creado partner {partner.name} para empleado {self.name}")
            
            # Crear fsm.person
            fsm_person_vals = {
                'name': self.name,
                'partner_id': partner.id,
            }
            fsm_person = self.env['fsm.person'].create(fsm_person_vals)
            
            # Vincular con el empleado
            self.fsm_person_id = fsm_person.id
            
            _logger.info(f"Creado fsm.person para empleado {self.name}")
            return fsm_person
            
        except Exception as e:
            _logger.error(f"Error creando fsm.person para empleado {self.name}: {str(e)}")
            return False
    
    def _sync_to_fsm_person(self):
        """Sincronizar datos del empleado con fsm.person."""
        # Validaciones previas
        if not self.exists():
            _logger.error("Empleado no existe en la base de datos")
            return False
        
        if not self.fsm_person_id:
            _logger.warning(f"Empleado {self.name} no tiene fsm.person asociado")
            return False
        
        if not self.fsm_person_id.exists():
            _logger.error(f"fsm.person asociado al empleado {self.name} no existe")
            self.fsm_person_id = False
            return False
        
        if not self.name:
            _logger.error(f"Empleado {self.id} no tiene nombre definido")
            return False
        
        try:
            # Verificar que el partner existe
            if not self.fsm_person_id.partner_id or not self.fsm_person_id.partner_id.exists():
                _logger.error(f"Partner asociado a fsm.person del empleado {self.name} no existe")
                return False
            
            # Actualizar datos del partner
            partner_vals = {
                'name': self.name,
                'email': self.work_email or '',
                'phone': self.work_phone or self.mobile_phone or '',
            }
            self.fsm_person_id.partner_id.write(partner_vals)
            
            # Actualizar fsm.person
            fsm_vals = {
                'name': self.name,
            }
            self.fsm_person_id.write(fsm_vals)
            
            # Actualizar estado de sincronización
            sync_vals = {
                'fsm_sync_date': fields.Datetime.now(),
                'fsm_sync_status': 'synced'
            }
            self.write(sync_vals)
            
            _logger.info(f"Sincronizado empleado {self.name} con FSM")
            return True
            
        except Exception as e:
            _logger.error(f"Error sincronizando empleado {self.name}: {str(e)}")
            try:
                self.write({'fsm_sync_status': 'error'})
            except:
                _logger.error(f"Error adicional actualizando estado de sincronización para {self.name}")
            return False
    
    def _sync_skills_to_fsm(self):
        """Sincronizar habilidades del empleado con fsm.person."""
        if not self.fsm_person_id:
            raise UserError("El empleado no tiene un registro FSM asociado.")
        
        try:
            # Obtener habilidades del empleado
            employee_skills = self.skill_ids
            
            if not employee_skills:
                _logger.info(f"No hay habilidades para sincronizar para {self.name}")
                return True
            
            # Sincronizar cada habilidad
            synced_count = 0
            for skill in employee_skills:
                try:
                    # Buscar si ya existe la habilidad en FSM
                    existing_skill = self.env['fsm.person.skill'].search([
                        ('person_id', '=', self.fsm_person_id.id),
                        ('skill_id', '=', skill.skill_id.id)
                    ], limit=1)
                    
                    skill_vals = {
                        'person_id': self.fsm_person_id.id,
                        'skill_id': skill.skill_id.id,
                        'level_id': skill.level_id.id if skill.level_id else False,
                    }
                    
                    if existing_skill:
                        existing_skill.write(skill_vals)
                    else:
                        self.env['fsm.person.skill'].create(skill_vals)
                    
                    synced_count += 1
                    
                except Exception as skill_error:
                    _logger.error(f"Error sincronizando habilidad {skill.skill_id.name}: {str(skill_error)}")
                    continue
            
            _logger.info(f"Sincronizadas {synced_count} habilidades para {self.name}")
            return True
            
        except Exception as e:
            _logger.error(f"Error sincronizando habilidades para {self.name}: {str(e)}")
            raise UserError(f"Error al sincronizar habilidades: {str(e)}")
    
    def action_sync_to_fsm_person(self):
        """Acción para sincronizar el empleado individual con FSM
        
        Returns:
            dict: Resultado de la acción con notificación
        """
        self.ensure_one()
        
        if not self.is_field_technician:
            raise UserError("Solo los técnicos de campo pueden ser sincronizados con FSM")
        
        try:
            if not self.fsm_person_id:
                self._create_fsm_person()
                message = f"Persona FSM creada para {self.name}"
            else:
                self._sync_to_fsm_person()
                message = f"Persona FSM actualizada para {self.name}"
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sincronización Exitosa',
                    'message': message,
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error de Sincronización',
                    'message': f"Error sincronizando {self.name}: {str(e)}",
                    'type': 'danger',
                    'sticky': True,
                }
            }
    
    def action_sync_skills_to_fsm(self):
        """Acción para sincronizar habilidades del empleado con FSM."""
        success_count = 0
        error_count = 0
        messages = []
        
        for employee in self:
            if not employee.is_field_technician:
                messages.append(f"⚠️ {employee.name}: No es técnico de campo")
                continue
                
            if not employee.fsm_person_id:
                messages.append(f"❌ {employee.name}: No tiene registro FSM")
                error_count += 1
                continue
            
            try:
                # Sincronizar habilidades usando el método privado
                employee._sync_skills_to_fsm()
                
                skill_count = len(employee.skill_ids)
                if skill_count > 0:
                    messages.append(f"✅ {employee.name}: {skill_count} habilidades sincronizadas")
                    success_count += 1
                else:
                    messages.append(f"ℹ️ {employee.name}: Sin habilidades para sincronizar")
                
            except Exception as e:
                messages.append(f"❌ {employee.name}: Error - {str(e)}")
                error_count += 1
                _logger.error(f"Error sincronizando habilidades para {employee.name}: {str(e)}")
        
        # Preparar mensaje de resultado
        title = "Sincronización de Habilidades FSM"
        if error_count == 0:
            message_type = 'success'
            summary = f"✅ Sincronización completada: {success_count} empleados procesados"
        else:
            message_type = 'warning'
            summary = f"⚠️ Sincronización con errores: {success_count} éxitos, {error_count} errores"
        
        full_message = f"{summary}\n\nDetalle:\n" + "\n".join(messages)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': full_message,
                'type': message_type,
                'sticky': True,
            }
        }