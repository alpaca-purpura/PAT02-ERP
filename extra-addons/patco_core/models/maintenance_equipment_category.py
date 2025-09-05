# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenanceEquipmentCategory(models.Model):
    _inherit = 'maintenance.equipment.category'
    
    # Campos para plantillas de checklist
    x_entry_checklist_template = fields.Html(
        string='Plantilla Checklist de Entrada',
        help='Plantilla HTML del checklist que debe completarse al iniciar el servicio'
    )
    
    x_exit_checklist_template = fields.Html(
        string='Plantilla Checklist de Salida', 
        help='Plantilla HTML del checklist que debe completarse al finalizar el servicio'
    )
    
    # Campo para base de conocimiento usando adjuntos nativos
    x_knowledge_base_count = fields.Integer(
        string='Documentos en Base de Conocimiento',
        compute='_compute_knowledge_base_count'
    )
    
    def _compute_knowledge_base_count(self):
        """Cuenta los adjuntos que sirven como base de conocimiento"""
        for record in self:
            attachments = self.env['ir.attachment'].search_count([
                ('res_model', '=', 'maintenance.equipment.category'),
                ('res_id', '=', record.id)
            ])
            record.x_knowledge_base_count = attachments
    
    def action_view_knowledge_base(self):
        """Acción para ver los documentos de la base de conocimiento"""
        self.ensure_one()
        return {
            'name': f'Base de Conocimiento - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'ir.attachment',
            'view_mode': 'tree,form',
            'domain': [('res_model', '=', 'maintenance.equipment.category'), ('res_id', '=', self.id)],
            'context': {
                'default_res_model': 'maintenance.equipment.category',
                'default_res_id': self.id,
            }
        }