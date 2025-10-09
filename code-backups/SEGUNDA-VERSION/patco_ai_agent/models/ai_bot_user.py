from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AIBotUser(models.Model):
    _name = 'ai.bot.user'
    _description = 'Gestión de Usuario Bot IA'
    
    name = fields.Char('Nombre del Bot', default='🤖 Asistente IA PATCO')
    user_id = fields.Many2one('res.users', 'Usuario del Bot', required=True)
    partner_id = fields.Many2one('res.partner', 'Partner del Bot', required=True)
    is_active = fields.Boolean('Activo', default=True)
    
    @api.model
    def get_or_create_bot_user(self):
        """Obtiene o crea el usuario bot IA"""
        
        bot = self.search([('is_active', '=', True)], limit=1)
        
        if not bot:
            # Buscar si ya existe el usuario
            existing_user = self.env['res.users'].search([('login', '=', 'ai_bot_patco')], limit=1)
            
            if existing_user:
                # Si existe el usuario pero no el bot, crear solo el registro del bot
                bot = self.create({
                    'name': '🤖 Asistente IA PATCO',
                    'user_id': existing_user.id,
                    'partner_id': existing_user.partner_id.id,
                    'is_active': True
                })
                _logger.info(f"Registro bot IA creado para usuario existente: {bot.name} (ID: {bot.user_id.id})")
            else:
                # Crear partner para el bot
                partner = self.env['res.partner'].create({
                    'name': '🤖 Asistente IA PATCO',
                    'is_company': False,
                    'email': 'ai-bot@patco.com.pe',
                    'phone': '+51-1-AI-PATCO',
                    'comment': 'Usuario bot para asistente IA conversacional'
                })
                
                # Crear usuario para el bot
                user = self.env['res.users'].create({
                    'name': '🤖 Asistente IA PATCO',
                    'login': 'ai_bot_patco',
                    'email': 'ai-bot@patco.com.pe',
                    'partner_id': partner.id,
                    'groups_id': [(4, self.env.ref('base.group_user').id)],
                    'active': True,
                    'is_system': True
                })
                
                # Crear registro del bot
                bot = self.create({
                    'name': '🤖 Asistente IA PATCO',
                    'user_id': user.id,
                    'partner_id': partner.id,
                    'is_active': True
                })
                
                _logger.info(f"Usuario bot IA creado: {bot.name} (ID: {bot.user_id.id})")
        
        return bot