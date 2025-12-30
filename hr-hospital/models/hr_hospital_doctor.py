from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'
    _inherit = ['abstract.person']

    name = fields.Char(
        compute='_compute_name',
        store=True,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
    )
    speciality_id = fields.Many2one(
        comodel_name='doctor.speciality',
        string='Speciality',
    )
    is_intern = fields.Boolean(
        string='Intern',
        default=False,
    )
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Mentor Doctor',
        domain="[('is_intern', '=', False), ('id', '!=', id)]",
    )
    license_number = fields.Char(
        required=True,
        copy=False,
    )
    license_date = fields.Date(
        string='License Issue Date',
    )
    experience_years = fields.Integer(
        string='Years of Experience',
        compute='_compute_experience_years',
    )
    rating = fields.Float(
        digits=(3, 2),
        default=0.0,
    )
    schedule_ids = fields.One2many(
        comodel_name='doctor.schedule',
        inverse_name='doctor_id',
        string='Work Schedule',
    )
    education_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country of Education',
    )
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='personal_doctor_id',
        string='Patients',
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='doctor_id',
        string='Visits',
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            'unique_license_number',
            'UNIQUE(license_number)',
            'License number must be unique!'
        ),
        (
            'check_rating',
            'CHECK(rating >= 0.00 AND rating <= 5.00)',
            'Rating must be between 0.00 and 5.00!'
        ),
    ]

    @api.depends('full_name')
    def _compute_name(self):
        for record in self:
            record.name = record.full_name or ''

    @api.depends('license_date')
    def _compute_experience_years(self):
        today = fields.Date.today()
        for record in self:
            if record.license_date:
                delta = today - record.license_date
                record.experience_years = delta.days // 365
            else:
                record.experience_years = 0

    @api.depends('full_name', 'speciality_id')
    def _compute_display_name(self):
        for record in self:
            name = record.full_name or ''
            if record.speciality_id:
                name = f'{name} ({record.speciality_id.name})'
            record.display_name = name

    @api.constrains('is_intern', 'mentor_id')
    def _check_mentor(self):
        for record in self:
            if record.mentor_id:
                if record.mentor_id.is_intern:
                    raise ValidationError(
                        self.env._('Cannot assign an intern as a mentor!')
                    )
                if record.mentor_id.id == record.id:
                    raise ValidationError(
                        self.env._('Doctor cannot be their own mentor!')
                    )

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        if not self.is_intern:
            self.mentor_id = False

    def write(self, vals):
        if vals.get('active') is False:
            for record in self:
                active_visits = record.visit_ids.filtered(
                    lambda v: v.state in ['scheduled', 'in_progress']
                )
                if active_visits:
                    raise UserError(
                        self.env._('Cannot archive doctor with active visits!')
                    )
        return super().write(vals)
