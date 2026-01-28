from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrHospitalPatient(models.Model):
    """Model representing a hospital patient.

    Inherits from abstract.person for common personal fields.
    Tracks medical information, visits, and doctor assignments.
    """

    _name = 'hr.hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['abstract.person']

    name = fields.Char(
        compute='_compute_name',
        store=True,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Portal User',
    )
    personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Personal Doctor',
    )
    passport_data = fields.Char(size=10)
    contact_person_id = fields.Many2one(
        comodel_name='contact.person',
        string='Contact Person',
    )
    blood_type = fields.Selection(
        selection=[
            ('o_pos', 'O(I) Rh+'),
            ('o_neg', 'O(I) Rh-'),
            ('a_pos', 'A(II) Rh+'),
            ('a_neg', 'A(II) Rh-'),
            ('b_pos', 'B(III) Rh+'),
            ('b_neg', 'B(III) Rh-'),
            ('ab_pos', 'AB(IV) Rh+'),
            ('ab_neg', 'AB(IV) Rh-'),
        ],
    )
    allergies = fields.Text()
    insurance_company_id = fields.Many2one(
        comodel_name='res.partner',
        string='Insurance Company',
        domain="[('is_company', '=', True)]",
    )
    insurance_policy_number = fields.Char()
    doctor_history_ids = fields.One2many(
        comodel_name='patient.doctor.history',
        inverse_name='patient_id',
        string='Doctor History',
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='patient_id',
        string='Visits',
    )
    diagnosis_ids = fields.One2many(
        comodel_name='medical.diagnosis',
        compute='_compute_diagnosis_ids',
        string='Diagnoses',
    )
    active = fields.Boolean(default=True)

    def _compute_diagnosis_ids(self):
        for record in self:
            record.diagnosis_ids = self.env['medical.diagnosis'].search([
                ('visit_id.patient_id', '=', record.id)
            ])

    @api.depends('full_name')
    def _compute_name(self):
        for record in self:
            record.name = record.full_name or ''

    def write(self, vals):
        if 'personal_doctor_id' in vals:
            for record in self:
                old_doctor = record.personal_doctor_id
                new_doctor_id = vals.get('personal_doctor_id')
                if old_doctor and old_doctor.id != new_doctor_id:
                    self.env['patient.doctor.history'].create({
                        'patient_id': record.id,
                        'doctor_id': vals['personal_doctor_id'],
                        'change_reason': 'Personal doctor changed',
                    })
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.personal_doctor_id:
                self.env['patient.doctor.history'].create({
                    'patient_id': record.id,
                    'doctor_id': record.personal_doctor_id.id,
                    'change_reason': 'Initial assignment',
                })
        return records

    def unlink(self):
        """Delete patients, filtering out those with completed diagnosed visits."""
        to_delete = self.filtered(
            lambda p: not p.visit_ids.filtered(
                lambda v: v.diagnosis_ids and v.state == 'completed'
            )
        )
        return super(HrHospitalPatient, to_delete).unlink()

    def action_view_visits(self):
        self.ensure_one()
        patient_id = self.ids[0]
        return {
            'name': _('Visits of %s', self.name),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'tree,form,calendar',
            'domain': [('patient_id', '=', patient_id)],
            'context': {'default_patient_id': patient_id},
        }

    def action_quick_visit(self):
        self.ensure_one()
        patient_id = self.ids[0]
        doctor_id = self.personal_doctor_id.id or False
        return {
            'name': _('Create Visit'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': patient_id,
                'default_doctor_id': doctor_id,
            },
        }
