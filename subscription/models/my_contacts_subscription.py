from odoo import api, fields, models
from odoo import exceptions
import re


class SubscripContact(models.Model):
    _name = 'sub.cont'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'New Description'

    @api.constrains('mobile_no')
    def _validate_phone_no(self):
        c = re.findall('^[6-9]{1}[0-9]*', self.mobile_no)
        if c:
            if len(c[0]) != 10:
                raise exceptions.ValidationError("Please Enter Correct contact No")
        else:
            raise exceptions.ValidationError("Please Enter Correct contact No")

    @api.constrains('kyc')
    def _validate_kyc(self):
        if len(self.kyc) > 12:
            raise exceptions.ValidationError("Please Enter Correct Aadhar number")
        elif len(self.kyc) < 12:
            raise exceptions.ValidationError("Please Enter Correct Aadhar number")

    @api.onchange('email_id')
    def validate_mail(self):
        if self.email_id:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email_id)
            if match == None:
                raise exceptions.ValidationError('Not a valid E-mail ID')

    name = fields.Char(string="Name", required=True, )
    marital_status = fields.Selection(string="Marital Status", selection=[('married', 'Married'),
                                                                          ('unmarried', 'Unmarried')], required=True, )
    spouse = fields.Char(string="spouse", required=False, )
    address = fields.Text(string="Address", required=False, )
    date_of_birth = fields.Date(string="Date of Birth", required=True, )
    mobile_no = fields.Char(string="Contact", required=True, )
    email_id = fields.Char(string="Email", required=False, )
    kyc = fields.Char(string="Aadhar No", required=True, )
    date = fields.Datetime(string="Date", default=lambda self: fields.Datetime.now())
    signature = fields.Binary(string="signature ", )
    sub_mem = fields.One2many(comodel_name="sub.memb", inverse_name="name", string="sub_mem", required=False,
                              _compute="_compute_sub_mem")
    sub_paymment = fields.One2many(comodel_name="sub.pay", inverse_name="name", string="sub_paymment", required=False, )
    transaction_id = fields.One2many(comodel_name="sub.transaction", inverse_name="name", string="transaction status",
                                     required=False, )
    count_subscription = fields.Integer(string="", compute='count_subscriptions')
    count_payment = fields.Integer(string="", compute='count_payments')
    count_transaction = fields.Integer(string="Count", compute='count_transactions')
    company_id = fields.Many2one(comodel_name="res.users", string="admin", required=False)
    
    def action_send_to_email(self):
        print("email send done")
        template_id = self.env.ref('subscription_pro.email_template_subscription_contact').id
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    @api.depends('sub_mem')
    def _compute_sub_mem(self):
        for rec in self:
            sub_mem = self.env['sub.cont'].search_count([{'name', '=', 'validity_1'}])
            rec.sub_mem = sub_mem

    def get_data_subscriptions(self):
        return {
            'name': 'subscriptions',
            'domain': [('name', '=', self.id)],
            'view_type': 'form',
            'res_model': 'sub.memb',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    def get_data_payments(self):
        return {
            'name': 'payments',
            'domain': [('name', '=', self.id)],
            # 'view_type': 'form',
            'target': 'current',
            'res_model': 'sub.pay',
            # 'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    def get_data_transactions(self):
        return {
            'name': 'transactions',
            'domain': [('name', '=', self.id)],
            'view_type': 'form',
            'res_model': 'sub.transaction',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window'
        }

    @api.depends('count_subscription')
    def count_subscriptions(self):
        for partner in self:
            partner.count_subscription = self.env['sub.memb'].search_count([('name', '=', self.id)])

    @api.depends('count_payment')
    def count_payments(self):
        for partner in self:
            partner.count_payment = self.env['sub.pay'].search_count([('name', '=', self.id)])

    @api.depends('count_transaction')
    def count_transactions(self):
        for partner in self:
            partner.count_transaction = self.env['sub.transaction'].search_count([('name', '=', self.id)])

    _sql_constraints = [
        ("date_of_birth_check_date",
         "CHECK (date_of_birth <= current_date)",
         "Date of Birth must not be in the future."),
    ]
    # def action_send_mail(self):
    #     self.ensure_one()
    #     template_id = self.env.ref('repair.mail_template_repair_quotation').id
    #     ctx = {
    #         'default_model': 'repair.order',
    #         'default_res_id': self.id,
    #         'default_use_template': bool(template_id),
    #         'default_template_id': template_id,
    #         'default_composition_mode': 'comment',
    #         'custom_layout': 'mail.mail_notification_light',
    #     }
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'res_model': 'mail.compose.message',
    #         'target': 'new',
    #         'context': ctx,
    #     }

    #