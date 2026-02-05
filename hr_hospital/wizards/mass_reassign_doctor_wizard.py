from odoo import api, fields, models


class MassReassignDoctorWizard(models.TransientModel):
    _name = 'mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor Wizard'

    old_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Current Doctor',
    )
    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='New Doctor',
        required=True,
    )
    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string='Patients',
    )
    change_date = fields.Date(default=fields.Date.today)
    change_reason = fields.Text(required=True)

    @api.onchange('old_doctor_id')
    def _onchange_old_doctor_id(self):
        if self.old_doctor_id:
            return {
                'domain': {
                    'patient_ids': [
                        ('personal_doctor_id', '=', self.old_doctor_id.id)
                    ]
                }
            }
        return {'domain': {'patient_ids': []}}

    def action_reassign(self):
        self.ensure_one()
        for patient in self.patient_ids:
            patient.write({
                'personal_doctor_id': self.new_doctor_id.id,
            })
            self.env['patient.doctor.history'].create({
                'patient_id': patient.id,
                'doctor_id': self.new_doctor_id.id,
                'date_assigned': self.change_date,
                'change_reason': self.change_reason,
            })
        return {'type': 'ir.actions.act_window_close'}
