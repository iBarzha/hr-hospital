from odoo import _, fields, models
from odoo.exceptions import UserError


class RescheduleVisitWizard(models.TransientModel):
    _name = 'reschedule.visit.wizard'
    _description = 'Reschedule Visit Wizard'

    visit_id = fields.Many2one(
        comodel_name='hr.hospital.visit',
        string='Current Visit',
        readonly=True,
    )
    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='New Doctor',
    )
    new_date = fields.Date(required=True)
    new_time = fields.Float(required=True)
    reschedule_reason = fields.Text(required=True)

    def action_reschedule(self):
        self.ensure_one()

        if self.visit_id.state == 'completed':
            raise UserError(
                _('Cannot reschedule a completed visit!')
            )

        self.visit_id.write({'state': 'cancelled'})

        new_datetime = fields.Datetime.to_datetime(
            f'{self.new_date} {int(self.new_time):02d}:'
            f'{int((self.new_time % 1) * 60):02d}:00'
        )

        new_visit = self.env['hr.hospital.visit'].create({
            'patient_id': self.visit_id.patient_id.id,
            'doctor_id': (
                self.new_doctor_id.id
                if self.new_doctor_id
                else self.visit_id.doctor_id.id
            ),
            'scheduled_datetime': new_datetime,
            'visit_type': self.visit_id.visit_type,
            'state': 'scheduled',
        })

        return {
            'name': 'Rescheduled Visit',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'res_id': new_visit.id,
            'target': 'current',
        }
