from odoo import fields, models


class ContactPerson(models.Model):
    _name = 'contact.person'
    _description = 'Contact Person'
    _inherit = ['abstract.person']

    relationship = fields.Char()
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='contact_person_id',
        string='Patients',
    )
    active = fields.Boolean(default=True)
