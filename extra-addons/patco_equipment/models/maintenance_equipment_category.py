# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import base64
import zipfile
import io

_logger = logging.getLogger(__name__)


class MaintenanceEquipmentCategory(models.Model):
    """Extensión del modelo de categorías de equipos para funcionalidades avanzadas.
    
    Agrega funcionalidades de plantillas de checklist y base de conocimiento
    para mejorar la gestión de equipos en servicios técnicos.
    Incluye herencia inteligente de checklists y documentación desde categorías padre.
    """
    _inherit = 'maintenance.equipment.category'
    
    # Knowledge base for equipment categories
    x_knowledge_base = fields.Html(
        string='Knowledge Base',
        help='Technical documentation and knowledge base for this equipment category'
    )
    
    # Campo Many2many para adjuntos directos
    x_attachment_ids = fields.One2many(
        'ir.attachment',
        'res_id',
        string='Documentos Adjuntos',
        domain=[('res_model', '=', 'maintenance.equipment.category')],
        help='Documentos técnicos adjuntos a esta categoría de equipos'
    )
    
    # Campos para plantillas de checklist
    x_entry_checklist_template = fields.Html(
        string='Plantilla Checklist Entrada',
        help='Plantilla HTML para el checklist de entrada del equipo'
    )
    
    x_exit_checklist_template = fields.Html(
        string='Plantilla Checklist Salida', 
        help='Plantilla HTML para el checklist de salida del equipo'
    )
    
    # Campo computado para contar documentos en base de conocimiento
    x_knowledge_base_count = fields.Integer(
        string='Documentos Base Conocimiento',
        compute='_compute_knowledge_base_count',
        help='Número de documentos adjuntos en la base de conocimiento'
    )
    
    # Campos para herencia inteligente
    x_inherit_checklists = fields.Boolean(
        string='Heredar Checklists',
        default=True,
        help='Si está marcado, hereda las plantillas de checklist de la categoría padre'
    )
    
    x_inherit_knowledge_base = fields.Boolean(
        string='Heredar Base de Conocimiento',
        default=True,
        help='Si está marcado, incluye documentos de la base de conocimiento de categorías padre'
    )
    
    # Campos computados para plantillas heredadas
    x_effective_entry_checklist = fields.Html(
        string='Checklist Entrada Efectivo',
        compute='_compute_effective_checklists',
        help='Plantilla de checklist de entrada considerando herencia'
    )
    
    x_effective_exit_checklist = fields.Html(
        string='Checklist Salida Efectivo',
        compute='_compute_effective_checklists',
        help='Plantilla de checklist de salida considerando herencia'
    )
    
    x_inherited_knowledge_count = fields.Integer(
        string='Documentos Heredados',
        compute='_compute_inherited_knowledge_count',
        help='Número de documentos heredados de categorías padre'
    )
    
    @api.depends('x_attachment_ids')
    def _compute_knowledge_base_count(self):
        """Calcula el número de documentos adjuntos para esta categoría.
        
        Cuenta los adjuntos directamente relacionados con esta categoría
        para mostrar el contador en la vista.
        """
        for record in self:
            record.x_knowledge_base_count = len(record.x_attachment_ids)
    
    @api.depends('x_entry_checklist_template', 'x_exit_checklist_template', 
                 'parent_id.x_effective_entry_checklist', 'parent_id.x_effective_exit_checklist',
                 'x_inherit_checklists')
    def _compute_effective_checklists(self):
        """Calcula las plantillas de checklist efectivas considerando herencia.
        
        Si la categoría tiene herencia habilitada y no tiene plantillas propias,
        utiliza las plantillas de la categoría padre.
        """
        for record in self:
            # Checklist de entrada
            if record.x_entry_checklist_template:
                record.x_effective_entry_checklist = record.x_entry_checklist_template
            elif record.x_inherit_checklists and record.parent_id:
                record.x_effective_entry_checklist = record.parent_id.x_effective_entry_checklist
            else:
                record.x_effective_entry_checklist = False
            
            # Checklist de salida
            if record.x_exit_checklist_template:
                record.x_effective_exit_checklist = record.x_exit_checklist_template
            elif record.x_inherit_checklists and record.parent_id:
                record.x_effective_exit_checklist = record.parent_id.x_effective_exit_checklist
            else:
                record.x_effective_exit_checklist = False
    
    @api.depends('parent_id', 'x_inherit_knowledge_base')
    def _compute_inherited_knowledge_count(self):
        """Calcula el número de documentos heredados de categorías padre.
        
        Cuenta todos los documentos disponibles desde categorías padre
        cuando la herencia está habilitada.
        """
        for record in self:
            inherited_count = 0
            if record.x_inherit_knowledge_base and record.parent_id:
                # Obtener todas las categorías padre
                parent_categories = record._get_parent_categories()
                for parent in parent_categories:
                    inherited_count += len(parent.x_attachment_ids)
            record.x_inherited_knowledge_count = inherited_count
    
    def _get_parent_categories(self):
        """Obtiene todas las categorías padre en la jerarquía.
        
        Returns:
            recordset: Todas las categorías padre desde la actual hasta la raíz
        """
        parents = self.env['maintenance.equipment.category']
        current = self.parent_id
        while current:
            parents |= current
            current = current.parent_id
        return parents
    
    def _get_all_attachments(self):
        """Obtiene todos los adjuntos disponibles (propios + heredados).
        
        Returns:
            recordset: Todos los adjuntos disponibles para esta categoría
        """
        self.ensure_one()
        all_attachments = self.x_attachment_ids
        
        if self.x_inherit_knowledge_base and self.parent_id:
            parent_categories = self._get_parent_categories()
            for parent in parent_categories:
                all_attachments |= parent.x_attachment_ids
        
        return all_attachments
    
    def action_view_knowledge_base(self):
        """Acción para abrir la vista de base de conocimiento.
        
        Abre una vista de adjuntos filtrada para esta categoría de equipo,
        permitiendo gestionar documentos técnicos y manuales.
        Incluye documentos heredados si la herencia está habilitada.
        
        Returns:
            dict: Acción de ventana para abrir la vista de adjuntos
        """
        self.ensure_one()
        
        # Construir dominio base
        domain = [('res_model', '=', self._name), ('res_id', '=', self.id)]
        
        # Incluir documentos heredados si está habilitado
        if self.x_inherit_knowledge_base and self.parent_id:
            parent_categories = self._get_parent_categories()
            parent_ids = parent_categories.ids + [self.id]
            domain = [('res_model', '=', self._name), ('res_id', 'in', parent_ids)]
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'📖 Base de Conocimiento - {self.complete_name or self.name}',
            'res_model': 'ir.attachment',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {
                'default_res_model': self._name,
                'default_res_id': self.id,
                'default_name': f'Documento - {self.complete_name or self.name}',
            },
            'target': 'current',
        }
    
    def action_view_inherited_knowledge_base(self):
        """Acción para ver solo los documentos heredados de categorías padre.
        
        Returns:
            dict: Acción de ventana para abrir la vista de adjuntos heredados
        """
        self.ensure_one()
        
        if not self.x_inherit_knowledge_base or not self.parent_id:
            return {'type': 'ir.actions.act_window_close'}
        
        parent_categories = self._get_parent_categories()
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'📚 Documentos Heredados - {self.complete_name or self.name}',
            'res_model': 'ir.attachment',
            'view_mode': 'list,form',
            'domain': [
                ('res_model', '=', self._name),
                ('res_id', 'in', parent_categories.ids)
            ],
            'context': {
                'create': False,  # No permitir crear documentos en vista heredada
            },
            'target': 'current',
        }
    
    def action_export_knowledge_base(self):
        """Acción para exportar todos los documentos disponibles en un ZIP.
        
        Crea un archivo ZIP con todos los documentos propios y heredados
        para facilitar la distribución de documentación técnica.
        
        Returns:
            dict: Acción de descarga del archivo ZIP
        """
        self.ensure_one()
        
        all_attachments = self._get_all_attachments()
        
        if not all_attachments:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': '⚠️ Sin Documentos',
                    'message': 'No hay documentos disponibles para exportar en esta categoría.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        # Crear archivo ZIP en memoria
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for attachment in all_attachments:
                if attachment.datas:
                    # Determinar carpeta según origen
                    folder = "Propios" if attachment.res_id == self.id else "Heredados"
                    file_path = f"{folder}/{attachment.name}"
                    
                    # Agregar archivo al ZIP
                    file_data = base64.b64decode(attachment.datas)
                    zip_file.writestr(file_path, file_data)
        
        zip_buffer.seek(0)
        zip_data = base64.b64encode(zip_buffer.getvalue()).decode()
        
        # Crear adjunto temporal para descarga
        zip_name = f"Documentacion_{self.name.replace(' ', '_')}_{fields.Date.today().strftime('%Y%m%d')}.zip"
        
        zip_attachment = self.env['ir.attachment'].create({
            'name': zip_name,
            'type': 'binary',
            'raw': zip_data,
            'res_model': 'maintenance.equipment.category',
            'res_id': self.id,
            'mimetype': 'application/zip',
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{zip_attachment.id}?download=true',
            'target': 'self',
        }