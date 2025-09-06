# -*- coding: utf-8 -*-

from odoo import models, fields

class TimesheetsAnalysisReport(models.Model):
    _inherit = 'timesheets.analysis.report'
    
    # Campos FSM requeridos por fieldservice_sale_timesheet
    fsm_order_id = fields.Many2one(
        'fsm.order',
        string='FSM Order',
        readonly=True,
        help='Field Service Management Order related to this timesheet entry'
    )
    
    fsm_location = fields.Char(
        string='FSM Location',
        readonly=True,
        help='Field Service Management location'
    )
    
    fsm_customer = fields.Char(
        string='FSM Customer',
        readonly=True,
        help='Field Service Management customer'
    )
    
    def _select(self):
        """Extend the select clause to include FSM fields"""
        select_str = super()._select()
        select_str += """,
            A.fsm_order_id,
            COALESCE(rp.name, '') as fsm_location,
            COALESCE(rp.name, '') as fsm_customer"""
        return select_str
    
    def _from(self):
        """Extend the from clause to include fsm location join"""
        from_str = super()._from()
        from_str += """
            LEFT JOIN fsm_order fo ON (A.fsm_order_id = fo.id)
            LEFT JOIN fsm_location fl ON (fo.location_id = fl.id)
            LEFT JOIN res_partner rp ON (fl.partner_id = rp.id)"""
        return from_str
    
    def _group_by(self):
        """Extend the group by clause to include FSM fields"""
        group_by_str = super()._group_by()
        group_by_str += """,
            A.fsm_order_id,
            rp.name"""
        return group_by_str