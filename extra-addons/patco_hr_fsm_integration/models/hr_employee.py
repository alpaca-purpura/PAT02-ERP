# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Campo para vincular con fsm.person
    fsm_person_id = fields.Many2one(
        'fsm.person',
        string='FSM Person',
        help='Persona asociada en Field Service Management'
    )
    
    # Campos de estado de sincronización
    fsm_sync_date = fields.Datetime(
        string='Última Sincronización FSM',
        help='Fecha y hora de la última sincronización con FSM'
    )
    
    fsm_sync_status = fields.Selection([
        ('pending', 'Pendiente'),
        ('synced', 'Sincronizado'),
        ('error', 'Error')
    ], string='Estado Sincronización FSM', default='pending', help='Estado actual de la sincronización con FSM')

    @api.model
    def write(self, vals):
        """Override write para crear/actualizar fsm.person automáticamente."""
        result = super().write(vals)
        
        # Si se marca como técnico de campo, crear fsm.person
        if 'is_field_technician' in vals and vals['is_field_technician']:
            for employee in self:
                if not employee.fsm_person_id:
                    employee._create_fsm_person()
                else:
                    employee._sync_to_fsm_person()
        
        # Si se actualizan datos de contacto, sincronizar con fsm.person
        sync_fields = ['name', 'work_phone', 'work_email', 'mobile_phone']
        if any(field in vals for field in sync_fields):
            for employee in self:
                if employee.fsm_person_id:
                    employee._sync_to_fsm_person()
        
        return result

    def _create_fsm_person(self):
        """Crear fsm.person para técnicos de campo"""
        for employee in self.filtered(lambda e: e.is_field_technician and not e.fsm_person_id):
            try:
                _logger.info(f"Iniciando creación de FSM Person para empleado: {employee.name} (ID: {employee.id})")
                
                # Crear partner si no existe
                if not employee.work_contact_id:
                    _logger.info(f"Creando partner para empleado: {employee.name}")
                    partner = self.env['res.partner'].create({
                        'name': employee.name,
                        'email': employee.work_email,
                        'phone': employee.work_phone,
                        'is_company': False,
                    })
                    employee.work_contact_id = partner.id
                    _logger.info(f"Partner creado con ID: {partner.id}")
                
                # Crear fsm.person
                _logger.info(f"Creando FSM Person para partner ID: {employee.work_contact_id.id}")
                fsm_person = self.env['fsm.person'].create({
                    'partner_id': employee.work_contact_id.id,
                })
                
                employee.fsm_person_id = fsm_person.id
                employee.work_contact_id.fsm_person = True
                
                # Actualizar estado de sincronización
                employee.fsm_sync_date = fields.Datetime.now()
                employee.fsm_sync_status = 'synced'
                
                _logger.info(f"FSM Person creado exitosamente con ID: {fsm_person.id} para empleado: {employee.name}")
                
            except Exception as e:
                _logger.error(f"Error al crear FSM Person para empleado {employee.name} (ID: {employee.id}): {str(e)}")
                employee.fsm_sync_date = fields.Datetime.now()
                employee.fsm_sync_status = 'error'
                raise UserError(f"Error al crear FSM Person para {employee.name}: {str(e)}")

    def _sync_to_fsm_person(self):
        """Sincronizar datos del empleado con fsm.person existente"""
        for employee in self.filtered('fsm_person_id'):
            try:
                _logger.info(f"Iniciando sincronización de empleado: {employee.name} (ID: {employee.id}) con FSM Person ID: {employee.fsm_person_id.id}")
                
                fsm_person = employee.fsm_person_id
                partner = employee.work_contact_id
                
                # Registrar datos antes de la actualización
                _logger.debug(f"Datos actuales del partner - Nombre: {partner.name}, Email: {partner.email}, Teléfono: {partner.phone}")
                _logger.debug(f"Nuevos datos del empleado - Nombre: {employee.name}, Email: {employee.work_email}, Teléfono: {employee.work_phone}")
                
                # Actualizar datos del partner
                partner.write({
                    'name': employee.name,
                    'email': employee.work_email,
                    'phone': employee.work_phone,
                })
                
                # Actualizar estado de sincronización
                employee.fsm_sync_date = fields.Datetime.now()
                employee.fsm_sync_status = 'synced'
                
                _logger.info(f"Sincronización completada exitosamente para empleado: {employee.name}")
                
            except Exception as e:
                _logger.error(f"Error al sincronizar empleado {employee.name} (ID: {employee.id}) con FSM Person: {str(e)}")
                employee.fsm_sync_date = fields.Datetime.now()
                employee.fsm_sync_status = 'error'
                raise UserError(f"Error al sincronizar {employee.name}: {str(e)}")

    def action_create_fsm_person(self):
        """Acción manual para crear fsm.person."""
        for employee in self:
            if not employee.is_field_technician:
                raise UserError(
                    _("El empleado %s debe estar marcado como técnico de campo") % employee.name
                )
            employee._create_fsm_person()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Éxito'),
                'message': _('Persona FSM creada correctamente'),
                'type': 'success',
            }
        }
    
    def action_sync_to_fsm_person(self):
        """Acción manual para sincronizar empleado con FSM Person"""
        self.ensure_one()
        
        _logger.info(f"=== INICIO SINCRONIZACIÓN MANUAL === Empleado: {self.name} (ID: {self.id})")
        
        # Validaciones previas
        if not self.is_field_technician:
            _logger.info(f"Empleado {self.name} no es técnico de campo, omitiendo sincronización")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Información',
                    'message': 'Solo los técnicos de campo pueden sincronizarse con FSM.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        if not self.name:
            _logger.warning(f"Empleado ID {self.id} no tiene nombre definido")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error de Validación',
                    'message': 'El empleado debe tener un nombre definido.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        try:
            _logger.info(f"Iniciando sincronización manual para empleado: {self.name}")
            
            if not self.fsm_person_id:
                _logger.info(f"No existe FSM Person, creando nuevo registro")
                self._create_fsm_person()
                message = f'FSM Person creado exitosamente para {self.name}'
                _logger.info(f"=== ÉXITO === FSM Person creado para empleado: {self.name}")
            else:
                _logger.info(f"FSM Person existente (ID: {self.fsm_person_id.id}), actualizando datos")
                self._sync_to_fsm_person()
                message = f'Datos sincronizados exitosamente para {self.name}'
                _logger.info(f"=== ÉXITO === Datos sincronizados para empleado: {self.name}")
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Éxito',
                    'message': message,
                    'type': 'success',
                    'sticky': False,
                }
            }
            
        except Exception as e:
            _logger.error(f"=== ERROR === Sincronización manual fallida para empleado {self.name} (ID: {self.id}): {str(e)}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': f'Error al sincronizar {self.name}: {str(e)}',
                    'type': 'danger',
                    'sticky': True,
                }
            }
    
    def action_sync_skills_to_fsm(self):
        """Acción manual para sincronizar habilidades con FSM"""
        self.ensure_one()
        
        _logger.info(f"=== INICIO SINCRONIZACIÓN MANUAL DE HABILIDADES === Empleado: {self.name} (ID: {self.id})")
        
        # Validaciones previas
        if not self.is_field_technician:
            _logger.info(f"Empleado {self.name} no es técnico de campo, omitiendo sincronización de habilidades")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Información',
                    'message': 'Solo los técnicos de campo pueden sincronizar habilidades con FSM.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        if not self.fsm_person_id:
            _logger.warning(f"Empleado {self.name} no tiene FSM Person asociado")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error de Validación',
                    'message': 'El empleado debe tener un FSM Person asociado. Sincronice primero los datos básicos.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        if not self.employee_skill_ids:
            _logger.info(f"Empleado {self.name} no tiene habilidades definidas")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Información',
                    'message': 'El empleado no tiene habilidades definidas para sincronizar.',
                    'type': 'info',
                    'sticky': False,
                }
            }
        
        try:
            _logger.info(f"Iniciando sincronización manual de habilidades para empleado: {self.name} - Total habilidades: {len(self.employee_skill_ids)}")
            
            self._sync_skills_to_fsm()
            skills_count = len(self.employee_skill_ids)
            message = f"Se sincronizaron {skills_count} habilidades correctamente para {self.name}"
            _logger.info(f"=== ÉXITO === Habilidades sincronizadas para empleado: {self.name} - {skills_count} habilidades")
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sincronización de Habilidades Exitosa',
                    'message': message,
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            _logger.error(f"=== ERROR === Sincronización manual de habilidades fallida para empleado {self.name} (ID: {self.id}): {str(e)}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error de Sincronización',
                    'message': f"Error sincronizando habilidades de {self.name}: {str(e)}",
                    'type': 'danger',
                    'sticky': True,
                }
            }
    
    def _sync_skills_to_fsm(self):
        """Método interno para sincronizar habilidades con FSM."""
        self.ensure_one()
        
        _logger.info(f"Iniciando sincronización de habilidades para empleado: {self.name} (ID: {self.id})")
        
        if not self.fsm_person_id:
            _logger.warning(f"Empleado {self.name} no tiene FSM Person asociado")
            return
        
        try:
            _logger.info(f"FSM Person ID: {self.fsm_person_id.id}, Habilidades del empleado: {len(self.employee_skill_ids)}")
            
            # Sincronizar habilidades si el modelo fsm.person tiene el campo skill_ids
            if hasattr(self.fsm_person_id, 'skill_ids'):
                _logger.info(f"FSM Person tiene campo skill_ids, procediendo con sincronización")
                
                # Registrar habilidades actuales
                current_skills = self.fsm_person_id.skill_ids
                _logger.debug(f"Habilidades actuales en FSM Person: {len(current_skills)}")
                
                skill_mapping = []
                for emp_skill in self.employee_skill_ids:
                    skill_data = {
                        'skill_id': emp_skill.skill_id.id,
                        'skill_level_id': emp_skill.skill_level_id.id if emp_skill.skill_level_id else False,
                    }
                    skill_mapping.append((0, 0, skill_data))
                    _logger.debug(f"Preparando habilidad: {emp_skill.skill_id.name} - Nivel: {emp_skill.skill_level_id.name if emp_skill.skill_level_id else 'Sin nivel'}")
                
                # Limpiar habilidades existentes y agregar las nuevas
                self.fsm_person_id.skill_ids = [(5, 0, 0)] + skill_mapping
                
                if skill_mapping:
                    _logger.info(f"Se agregaron {len(skill_mapping)} habilidades a FSM Person")
                else:
                    _logger.info(f"No hay habilidades para sincronizar")
                
                # Actualizar estado de sincronización
                self.fsm_sync_date = fields.Datetime.now()
                self.fsm_sync_status = 'synced'
                
                _logger.info(
                    f"Sincronización de habilidades completada exitosamente para empleado: {self.name}"
                )
            else:
                _logger.warning(
                    f"FSM Person no tiene campo skill_ids, omitiendo sincronización de habilidades"
                )
        
        except Exception as e:
            _logger.error(f"Error al sincronizar habilidades para empleado {self.name} (ID: {self.id}): {str(e)}")
            self.fsm_sync_date = fields.Datetime.now()
            self.fsm_sync_status = 'error'
            raise UserError(
                _("Error al sincronizar habilidades para %s: %s") % (self.name, str(e))
            )
    
    @api.model
    def action_sync_all_field_technicians(self):
        """Acción manual para sincronizar todos los técnicos de campo"""
        _logger.info("=== INICIO SINCRONIZACIÓN MASIVA DE TÉCNICOS DE CAMPO ===")
        
        try:
            field_technicians = self.search([('is_field_technician', '=', True)])
            
            _logger.info(f"Técnicos de campo encontrados: {len(field_technicians)}")
            
            if not field_technicians:
                _logger.info("No se encontraron técnicos de campo para sincronizar")
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Sin Técnicos',
                        'message': "No se encontraron técnicos de campo para sincronizar",
                        'type': 'info',
                        'sticky': False,
                    }
                }
            
            synced_count = 0
            error_count = 0
            error_details = []
            
            _logger.info(f"Iniciando sincronización masiva de {len(field_technicians)} técnicos de campo")
            
            for employee in field_technicians:
                _logger.info(f"--- Procesando técnico: {employee.name} (ID: {employee.id}) ---")
                try:
                    # Validar datos básicos del empleado
                    if not employee.name:
                        error_details.append(f"Empleado ID {employee.id}: Sin nombre")
                        error_count += 1
                        continue
                    
                    if not employee.fsm_person_id:
                        _logger.info(f"Creando FSM Person para: {employee.name}")
                        employee._create_fsm_person()
                        _logger.info(f"FSM Person creado exitosamente para: {employee.name}")
                    else:
                        _logger.info(f"Sincronizando datos existentes para: {employee.name} (FSM Person ID: {employee.fsm_person_id.id})")
                        employee._sync_to_fsm_person()
                        _logger.info(f"Datos sincronizados exitosamente para: {employee.name}")
                    
                    synced_count += 1
                    
                except Exception as e:
                    error_count += 1
                    error_msg = f"{employee.name}: {str(e)}"
                    error_details.append(error_msg)
                    _logger.error(f"Error sincronizando técnico {employee.name} (ID: {employee.id}): {str(e)}")
            
            # Preparar mensaje de resultado
            if error_count == 0:
                message = f"✅ Se sincronizaron {synced_count} técnicos correctamente"
                notification_type = 'success'
                _logger.info(f"=== ÉXITO TOTAL === Sincronización masiva completada: {synced_count} técnicos")
            elif synced_count > 0:
                message = f"⚠️ Se sincronizaron {synced_count} técnicos. {error_count} con errores."
                if len(error_details) <= 3:
                    message += f"\n\nErrores: {'; '.join(error_details)}"
                else:
                    message += f"\n\nPrimeros errores: {'; '.join(error_details[:3])}..."
                notification_type = 'warning'
                _logger.warning(f"=== ÉXITO PARCIAL === Sincronización masiva: {synced_count} éxitos, {error_count} errores")
            else:
                message = f"❌ No se pudo sincronizar ningún técnico. {error_count} errores."
                if len(error_details) <= 5:
                    message += f"\n\nErrores: {'; '.join(error_details)}"
                notification_type = 'danger'
                _logger.error(f"=== FALLO TOTAL === Sincronización masiva fallida: {error_count} errores")
            
            _logger.info(f"=== FIN SINCRONIZACIÓN MASIVA === Total procesados: {len(field_technicians)}, Éxitos: {synced_count}, Errores: {error_count}")
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sincronización Masiva Completada',
                    'message': message,
                    'type': notification_type,
                    'sticky': error_count > 0,  # Mantener visible si hay errores
                }
            }
            
        except Exception as e:
            _logger.error(f"Critical error in mass sync: {str(e)}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error Crítico',
                    'message': f"Error crítico en sincronización masiva: {str(e)}",
                    'type': 'danger',
                    'sticky': True,
                }
            }

    @api.model
    def sync_all_field_technicians(self):
        """Método para sincronizar todos los técnicos de campo con fsm.person.
        
        Este método es llamado por el cron job para mantener la sincronización.
        """
        _logger.info("Starting sync of all field technicians with FSM persons")
        
        # Buscar todos los empleados marcados como técnicos de campo
        field_technicians = self.search([('is_field_technician', '=', True)])
        
        created_count = 0
        updated_count = 0
        error_count = 0
        
        for employee in field_technicians:
            try:
                if not employee.fsm_person_id:
                    employee._create_fsm_person()
                    created_count += 1
                else:
                    employee._sync_to_fsm_person()
                    updated_count += 1
            except Exception as e:
                _logger.error(
                    f"Error syncing employee {employee.name}: {str(e)}"
                )
                error_count += 1
        
        _logger.info(
            f"Sync completed: {created_count} created, {updated_count} updated, {error_count} errors"
        )
        
        return {
            'created': created_count,
            'updated': updated_count,
            'errors': error_count
        }

    @api.model
    def migrate_existing_technicians(self):
        """Método para migrar técnicos existentes a fsm.person.
        
        Este método debe ejecutarse una sola vez después de instalar el módulo.
        """
        _logger.info("Starting migration of existing field technicians")
        
        # Buscar técnicos de campo sin fsm.person
        technicians_to_migrate = self.search([
            ('is_field_technician', '=', True),
            ('fsm_person_id', '=', False)
        ])
        
        _logger.info(f"Found {len(technicians_to_migrate)} technicians to migrate")
        
        migrated_count = 0
        error_count = 0
        
        for employee in technicians_to_migrate:
            try:
                employee._create_fsm_person()
                migrated_count += 1
                _logger.info(f"Migrated employee {employee.name}")
            except Exception as e:
                _logger.error(
                    f"Error migrating employee {employee.name}: {str(e)}"
                )
                error_count += 1
        
        _logger.info(
            f"Migration completed: {migrated_count} migrated, {error_count} errors"
        )
        
        return {
            'migrated': migrated_count,
            'errors': error_count
        }