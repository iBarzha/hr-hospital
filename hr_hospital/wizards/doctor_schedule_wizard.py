from datetime import timedelta

from odoo import fields, models


class DoctorScheduleWizard(models.TransientModel):
    _name = 'doctor.schedule.wizard'
    _description = 'Doctor Schedule Wizard'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
    )
    start_week = fields.Date(required=True)
    weeks_count = fields.Integer(
        string='Number of Weeks',
        default=1,
        required=True,
    )
    schedule_type = fields.Selection(
        selection=[
            ('standard', 'Standard'),
            ('even_week', 'Even Week'),
            ('odd_week', 'Odd Week'),
        ],
        default='standard',
    )
    monday = fields.Boolean(default=True)
    tuesday = fields.Boolean(default=True)
    wednesday = fields.Boolean(default=True)
    thursday = fields.Boolean(default=True)
    friday = fields.Boolean(default=True)
    saturday = fields.Boolean(default=False)
    sunday = fields.Boolean(default=False)
    time_from = fields.Float(
        string='Start Time',
        default=9.0,
    )
    time_to = fields.Float(
        string='End Time',
        default=18.0,
    )
    break_from = fields.Float(default=13.0)
    break_to = fields.Float(default=14.0)

    def action_generate_schedule(self):
        self.ensure_one()

        day_mapping = {
            0: self.monday,
            1: self.tuesday,
            2: self.wednesday,
            3: self.thursday,
            4: self.friday,
            5: self.saturday,
            6: self.sunday,
        }

        current_date = self.start_week
        for _week in range(self.weeks_count):
            week_number = current_date.isocalendar()[1]

            should_create = True
            if self.schedule_type == 'even_week' and week_number % 2 != 0:
                should_create = False
            elif self.schedule_type == 'odd_week' and week_number % 2 == 0:
                should_create = False

            if should_create:
                for day_offset in range(7):
                    schedule_date = current_date + timedelta(days=day_offset)
                    day_of_week = schedule_date.weekday()

                    if day_mapping.get(day_of_week):
                        self.env['doctor.schedule'].create({
                            'doctor_id': self.doctor_id.id,
                            'date': schedule_date,
                            'day_of_week': str(day_of_week),
                            'time_from': self.time_from,
                            'time_to': self.time_to,
                            'schedule_type': 'working',
                        })

            current_date += timedelta(days=7)

        return {'type': 'ir.actions.act_window_close'}
