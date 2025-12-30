from odoo import api, fields, models


class PatientDoctorHistory(models.Model):
    _name = 'patient.doctor.history'
    _description = 'Patient Doctor History'
    _order = 'date_assigned desc'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
        ondelete='cascade',
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
    )
    date_assigned = fields.Date(
        required=True,
        default=fields.Date.today,
    )
    date_changed = fields.Date()
    change_reason = fields.Text()
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('patient_id'):
                self.search([
                    ('patient_id', '=', vals['patient_id']),
                    ('active', '=', True),
                ]).write({
                    'active': False,
                    'date_changed': fields.Date.today(),
                })
        return super().create(vals_list)
