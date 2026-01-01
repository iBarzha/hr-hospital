from odoo import api, fields, models


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
    date_from = fields.Date(
        required=True,
        default=lambda self: fields.Date.today().replace(day=1),
    )
    date_to = fields.Date(
        required=True,
        default=fields.Date.today,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids', [])
        active_model = self.env.context.get('active_model')
        if active_model == 'hr.hospital.doctor' and active_ids:
            res['doctor_ids'] = [(6, 0, active_ids)]
        return res

    def action_generate_report(self):
        self.ensure_one()
        domain = [
            ('diagnosis_date', '>=', self.date_from),
            ('diagnosis_date', '<=', self.date_to),
        ]

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        diagnoses = self.env['medical.diagnosis'].search(domain)

        return {
            'name': self.env._('Disease Report'),
            'type': 'ir.actions.act_window',
            'res_model': 'medical.diagnosis',
            'view_mode': 'tree,pivot,graph,form',
            'domain': [('id', 'in', diagnoses.ids)],
            'context': {'search_default_group_disease': 1},
            'target': 'current',
        }
