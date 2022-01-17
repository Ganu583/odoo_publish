from odoo import api, fields, models, _


class NewLifeAppointment(models.Model):
    _name = 'newlife_hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'New Description'

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            if self.patient_id.gender:
                self.gender = self.patient_id.gender
        else:
            self.gender = ''

    name = fields.Char(string="Name", required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    patient_id = fields.Many2one(comodel_name="newlife_hospital.patient", string="patient", required=False, )
    age = fields.Char(string="Age", related='patient_id.age', required=False, )
    state = fields.Selection(string="state", selection=[('draft', 'Draft'), ('confirm', 'Confirm'),
                                                        ('done', 'Done'), ('cancel', 'Cancel')], default='draft')
    gender = fields.Selection(string="Gender", selection=[('male', 'Male'), ('female', 'Female'),
                                                          ('other', 'Other')])
    appointment_date = fields.Datetime(string="Appointment Date", required=False, )

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.Appointment') or _('New')
        return super(NewLifeAppointment, self).create(vals)
