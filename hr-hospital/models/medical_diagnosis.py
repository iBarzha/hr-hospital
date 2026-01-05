from odoo import api, fields, models


class MedicalDiagnosis(models.Model):
    _name = 'medical.diagnosis'
    _description = 'Medical Diagnosis'

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.visit',
        string='Visit',
        required=True,
        ondelete='cascade',
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
        required=True,
        domain="[('is_contagious', '=', True), "
               "('danger_level', 'in', ['high', 'critical'])]",
    )
    description = fields.Text()
    treatment = fields.Html()
    is_approved = fields.Boolean(
        string='Approved',
        default=False,
    )
    approved_by_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Approved By',
        readonly=True,
    )
    approval_date = fields.Datetime(readonly=True)
    severity = fields.Selection(
        selection=[
            ('mild', 'Mild'),
            ('moderate', 'Moderate'),
            ('severe', 'Severe'),
            ('critical', 'Critical'),
        ],
    )
    diagnosis_date = fields.Datetime(
        related='visit_id.scheduled_datetime',
        store=True,
        string='Diagnosis Date',
    )
    doctor_id = fields.Many2one(
        related='visit_id.doctor_id',
        store=True,
        string='Doctor',
    )
    disease_type = fields.Many2one(
        related='disease_id.parent_id',
        store=True,
        string='Disease Type',
    )

    def action_approve(self):
        for record in self:
            doctor = record.visit_id.doctor_id
            if doctor.is_intern:
                approver = doctor.mentor_id
            else:
                approver = doctor
            record.write({
                'is_approved': True,
                'approved_by_id': approver.id if approver else False,
                'approval_date': fields.Datetime.now(),
            })
        return True

    @api.onchange('visit_id')
    def _onchange_visit_id(self):
        if self.visit_id and self.visit_id.patient_id.allergies:
            return {
                'warning': {
                    'title': self.env._('Patient Allergies'),
                    'message': self.env._(
                        'Patient has allergies: %(allergies)s',
                        allergies=self.visit_id.patient_id.allergies,
                    ),
                }
            }
        return None
