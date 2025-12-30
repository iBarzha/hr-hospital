import base64
import json

from odoo import fields, models


class PatientCardExportWizard(models.TransientModel):
    _name = 'patient.card.export.wizard'
    _description = 'Patient Card Export Wizard'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
    )
    date_from = fields.Date()
    date_to = fields.Date()
    include_diagnoses = fields.Boolean(default=True)
    include_recommendations = fields.Boolean(default=True)
    lang_id = fields.Many2one(
        comodel_name='res.lang',
        string='Report Language',
    )
    export_format = fields.Selection(
        selection=[
            ('json', 'JSON'),
            ('csv', 'CSV'),
        ],
        default='json',
        required=True,
    )
    export_file = fields.Binary(readonly=True)
    export_filename = fields.Char()

    def action_export(self):
        self.ensure_one()

        domain = [('patient_id', '=', self.patient_id.id)]
        if self.date_from:
            domain.append(('scheduled_datetime', '>=', self.date_from))
        if self.date_to:
            domain.append(('scheduled_datetime', '<=', self.date_to))

        visits = self.env['hr.hospital.visit'].search(domain)

        patient_data = {
            'patient': {
                'name': self.patient_id.full_name,
                'date_of_birth': str(self.patient_id.date_of_birth or ''),
                'gender': self.patient_id.gender or '',
                'blood_type': self.patient_id.blood_type or '',
                'allergies': self.patient_id.allergies or '',
                'phone': self.patient_id.phone or '',
                'email': self.patient_id.email or '',
            },
            'visits': [],
        }

        for visit in visits:
            visit_data = {
                'date': str(visit.scheduled_datetime),
                'doctor': visit.doctor_id.full_name,
                'type': visit.visit_type or '',
                'status': visit.state,
            }

            if self.include_diagnoses:
                visit_data['diagnoses'] = [
                    {
                        'disease': d.disease_id.name,
                        'severity': d.severity or '',
                        'description': d.description or '',
                    }
                    for d in visit.diagnosis_ids
                ]

            if self.include_recommendations:
                visit_data['recommendations'] = visit.recommendations or ''

            patient_data['visits'].append(visit_data)

        if self.export_format == 'json':
            content = json.dumps(patient_data, indent=2, ensure_ascii=False)
            filename = f'patient_card_{self.patient_id.id}.json'
        else:
            lines = ['Patient Name,Date of Birth,Gender,Blood Type']
            lines.append(
                f'{self.patient_id.full_name},'
                f'{self.patient_id.date_of_birth or ""},'
                f'{self.patient_id.gender or ""},'
                f'{self.patient_id.blood_type or ""}'
            )
            lines.append('')
            lines.append('Visit Date,Doctor,Type,Status')
            for visit in visits:
                lines.append(
                    f'{visit.scheduled_datetime},'
                    f'{visit.doctor_id.full_name},'
                    f'{visit.visit_type or ""},'
                    f'{visit.state}'
                )
            content = '\n'.join(lines)
            filename = f'patient_card_{self.patient_id.id}.csv'

        self.write({
            'export_file': base64.b64encode(content.encode('utf-8')),
            'export_filename': filename,
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.ids[0],
            'view_mode': 'form',
            'target': 'new',
        }
