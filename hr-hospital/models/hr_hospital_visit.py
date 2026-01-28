from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Hospital Visit'

    state = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No Show'),
        ],
        string='Status',
        default='scheduled',
        required=True,
    )
    scheduled_datetime = fields.Datetime(
        string='Scheduled Date & Time',
        required=True,
        default=fields.Datetime.now,
    )
    actual_datetime = fields.Datetime(
        string='Actual Date & Time',
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
        domain="[('license_number', '!=', False)]",
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
    )
    visit_type = fields.Selection(
        selection=[
            ('primary', 'Primary'),
            ('follow_up', 'Follow-up'),
            ('preventive', 'Preventive'),
            ('emergency', 'Emergency'),
        ],
    )
    diagnosis_ids = fields.One2many(
        comodel_name='medical.diagnosis',
        inverse_name='visit_id',
        string='Diagnoses',
    )
    diagnosis_count = fields.Integer(
        compute='_compute_diagnosis_count',
    )
    recommendations = fields.Html()
    cost = fields.Monetary(
        string='Visit Cost',
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    active = fields.Boolean(default=True)

    @api.depends('diagnosis_ids')
    def _compute_diagnosis_count(self):
        for record in self:
            record.diagnosis_count = len(record.diagnosis_ids)

    @api.constrains('doctor_id', 'patient_id', 'scheduled_datetime')
    def _check_duplicate_visit(self):
        for record in self:
            if record.scheduled_datetime:
                date = record.scheduled_datetime.date()
                duplicate = self.search([
                    ('id', '!=', record.id),
                    ('doctor_id', '=', record.doctor_id.id),
                    ('patient_id', '=', record.patient_id.id),
                    ('scheduled_datetime', '>=', f'{date} 00:00:00'),
                    ('scheduled_datetime', '<=', f'{date} 23:59:59'),
                    ('state', '!=', 'cancelled'),
                ], limit=1)
                if duplicate:
                    raise ValidationError(
                        _('Cannot schedule the same patient to the '
                          'same doctor more than once per day!')
                    )

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        if self.patient_id and self.patient_id.allergies:
            return {
                'warning': {
                    'title': _('Patient Allergies Warning'),
                    'message': _(
                        'This patient has allergies: %(allergies)s',
                        allergies=self.patient_id.allergies,
                    ),
                }
            }
        return None

    def write(self, vals):
        for record in self:
            if record.state == 'completed':
                protected_fields = {'doctor_id', 'scheduled_datetime'}
                if protected_fields & set(vals.keys()):
                    raise UserError(
                        _('Cannot modify doctor or date/time '
                          'for completed visits!')
                    )
        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.diagnosis_ids:
                raise UserError(
                    _('Cannot delete visit with diagnoses. '
                      'Please remove diagnoses first.')
                )
        return super().unlink()

    def action_complete(self):
        for record in self:
            record.write({
                'state': 'completed',
                'actual_datetime': fields.Datetime.now(),
            })
        return True

    def action_cancel(self):
        for record in self:
            record.write({'state': 'cancelled'})
        return True

    def action_no_show(self):
        for record in self:
            record.write({'state': 'no_show'})
        return True
