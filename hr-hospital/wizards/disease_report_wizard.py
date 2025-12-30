from odoo import fields, models


class DiseaseReportWizard(models.TransientModel):
    _name = 'disease.report.wizard'
    _description = 'Disease Report Wizard'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases',
    )
    country_ids = fields.Many2many(
        comodel_name='res.country',
        string='Countries',
    )
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    report_type = fields.Selection(
        selection=[
            ('detailed', 'Detailed'),
            ('summary', 'Summary'),
        ],
        default='detailed',
    )
    group_by = fields.Selection(
        selection=[
            ('doctor', 'By Doctor'),
            ('disease', 'By Disease'),
            ('month', 'By Month'),
            ('country', 'By Country'),
        ],
        default='doctor',
    )

    def action_generate_report(self):
        self.ensure_one()
        domain = [
            ('visit_id.scheduled_datetime', '>=', self.date_from),
            ('visit_id.scheduled_datetime', '<=', self.date_to),
        ]

        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        if self.country_ids:
            domain.append(
                ('visit_id.patient_id.country_id', 'in', self.country_ids.ids)
            )

        diagnoses = self.env['medical.diagnosis'].search(domain)

        return {
            'name': 'Disease Report',
            'type': 'ir.actions.act_window',
            'res_model': 'medical.diagnosis',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', diagnoses.ids)],
            'target': 'current',
        }
