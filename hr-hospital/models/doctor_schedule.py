from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DoctorSchedule(models.Model):
    _name = 'doctor.schedule'
    _description = 'Doctor Schedule'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
        domain="[('speciality_id', '!=', False)]",
    )
    day_of_week = fields.Selection(
        selection=[
            ('0', 'Monday'),
            ('1', 'Tuesday'),
            ('2', 'Wednesday'),
            ('3', 'Thursday'),
            ('4', 'Friday'),
            ('5', 'Saturday'),
            ('6', 'Sunday'),
        ],
        string='Day of Week',
    )
    date = fields.Date()
    time_from = fields.Float(string='Start Time')
    time_to = fields.Float(string='End Time')
    schedule_type = fields.Selection(
        selection=[
            ('working', 'Working Day'),
            ('vacation', 'Vacation'),
            ('sick_leave', 'Sick Leave'),
            ('conference', 'Conference'),
        ],
        string='Type',
        default='working',
    )
    notes = fields.Char()

    _sql_constraints = [
        (
            'check_time_range',
            'CHECK(time_to > time_from)',
            'End time must be greater than start time!'
        ),
    ]

    @api.constrains('time_from', 'time_to')
    def _check_time_range(self):
        for record in self:
            if record.time_from and record.time_to:
                if record.time_to <= record.time_from:
                    raise ValidationError(
                        self.env._('End time must be greater than start time!')
                    )
