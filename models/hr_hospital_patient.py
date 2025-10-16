from odoo import models, fields


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(required=True)
    date_of_birth = fields.Date()
    age = fields.Integer(compute='_compute_age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
    phone = fields.Char()
    email = fields.Char()
    address = fields.Text()
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor', string='Attending Doctor')
    active = fields.Boolean(default=True)

    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = fields.Date.today()
                record.age = today.year - record.date_of_birth.year
            else:
                record.age = 0
