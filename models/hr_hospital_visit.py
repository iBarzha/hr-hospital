from odoo import models, fields


class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Hospital Visit'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient', required=True)
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor', required=True)
    disease_id = fields.Many2one('hr.hospital.disease')
    visit_date = fields.Datetime(required=True, default=fields.Datetime.now)
    diagnosis = fields.Text()
    prescription = fields.Text()
    notes = fields.Text()
    active = fields.Boolean(default=True)
