from odoo import models, fields


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(required=True)
    specialty = fields.Char()
    phone = fields.Char()
    email = fields.Char()
    active = fields.Boolean(default=True)
