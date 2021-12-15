from odoo import api, fields, models


class SubTrans(models.Model):
    _name = 'sub.transaction'
    _description = 'New Description'

    name = fields.Many2one(comodel_name="sub.cont", string="name", required=False, )

    status_trans = fields.Selection(string="transaction status", selection=[('failed', 'Failed'), ('successfully', 'Successfully'), ], required=False, )