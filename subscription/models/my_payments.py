from odoo import api, fields, models


class SubPay(models.Model):
    _name = 'sub.pay'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Many2one(comodel_name="sub.cont", string="sub_paymment", required=False, )
    payment_select = fields.Selection(string="payment method", selection=[('card', 'Card'),
                                                                          ('upi payment', 'UPI Payment'),
                                                                          ('cash', 'Cash'), ], required=False, )
    payment_date = fields.Datetime(string="payment_date", required=False, default=lambda self: fields.Datetime.now())

