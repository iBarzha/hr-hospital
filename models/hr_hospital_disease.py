from odoo import models, fields


class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Hospital Disease'

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
