from odoo import api, fields, models, _


class NewLifePatient(models.Model):
    _name = 'newlife_hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'taking care of patient'

    name = fields.Char(string="Name", required=False, tracking=True)
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    age = fields.Char(string="Age", required=False, tracking=True)
    gender = fields.Selection(string="Gender", selection=[('male', 'Male'), ('female', 'Female'),
                                                          ('other', 'Other'), ], required=True, default="male")
    note = fields.Text(string="Description", required=False, tracking=True)
    state = fields.Selection(string="state", selection=[('draft', 'Draft'), ('confirm', 'Confirm'),
                                                        ('done', 'Done'), ('cancel', 'Cancel')], default='draft')
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count')

    def _compute_appointment_count(self):
        appointment_count = self.env['newlife_hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = appointment_count

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
        if not vals.get('note'):
            vals['note'] = 'new description'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        return super(NewLifePatient, self).create(vals)
