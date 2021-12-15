from odoo import api, fields, models
from datetime import datetime, timedelta


class SubscripMember(models.Model):
    _name = 'sub.memb'
    _description = 'this is for other'

    @api.onchange('end_date', 'start_date')
    def onchange_validity_1(self):
        if self.validity_1 == '1_year':
            self.end_date = self.start_date + timedelta(days=365)
        elif self.validity_1 == '2_years':
            self.end_date = self.start_date + timedelta(days=730)

    validity_1 = fields.Selection(string="validity", selection=[('1_year', '1 year'), ('2_years', '2 years')], )
    name = fields.Many2one(comodel_name="sub.cont", string="name", required=False,
                           domain="[('name','in',self.sub.cont)]")
    start_date = fields.Date(string="", required=False, )
    end_date = fields.Date(string="", required=False, )

    _sql_constraints = [
        ("check_subscription_start_date",
         "CHECK (start_date >= current_date)",
         "start date must not be in the past."),
    ]

    def get_data_sub(self):
        return {
            'name': 'subscriptions',
            'domain': [('name', '=', int(self.name))],
            'view_type': 'form',
            'res_model': 'sub.memb',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    def get_data_pay(self):
        return {
            'name': 'payments',
            'domain': [('name', '=', int(self.name))],
            # 'view_type': 'form',
            'target': 'current',
            'res_model': 'sub.pay',
            # 'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    def get_data_trans(self):
        return {
            'name': 'transactions',
            'domain': [('name', '=', int(self.name))],
            'view_type': 'form',
            'res_model': 'sub.transaction',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }
