import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AbstractPerson(models.AbstractModel):
    _name = 'abstract.person'
    _description = 'Abstract Person'
    _inherit = ['image.mixin']

    last_name = fields.Char(required=True)
    first_name = fields.Char(required=True)
    middle_name = fields.Char()
    full_name = fields.Char(
        compute='_compute_full_name',
        store=True,
    )
    phone = fields.Char()
    email = fields.Char()
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
    )
    date_of_birth = fields.Date(
        string='Date of Birth',
    )
    age = fields.Integer(
        compute='_compute_age',
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country of Citizenship',
    )
    lang_id = fields.Many2one(
        comodel_name='res.lang',
        string='Communication Language',
    )

    @api.depends('last_name', 'first_name', 'middle_name')
    def _compute_full_name(self):
        for record in self:
            parts = [
                record.last_name or '',
                record.first_name or '',
                record.middle_name or '',
            ]
            record.full_name = ' '.join(filter(None, parts))

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.date_of_birth:
                birth = record.date_of_birth
                record.age = today.year - birth.year - (
                    (today.month, today.day) < (birth.month, birth.day)
                )
            else:
                record.age = 0

    @api.constrains('phone')
    def _check_phone(self):
        phone_pattern = re.compile(r'^[\d\s\-+()]+$')
        for record in self:
            if record.phone and not phone_pattern.match(record.phone):
                raise ValidationError(
                    self.env._('Phone number can only contain digits, spaces, '
                               'hyphens, plus sign and parentheses.')
                )

    @api.constrains('email')
    def _check_email(self):
        email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        for record in self:
            if record.email and not email_pattern.match(record.email):
                raise ValidationError(
                    self.env._('Please enter a valid email address.')
                )

    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.date_of_birth and record.age <= 0:
                raise ValidationError(
                    self.env._('Age must be greater than 0.')
                )

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            lang = self.env['res.lang'].search([
                ('code', '=like', self.country_id.code.lower() + '%'),
                ('active', '=', True),
            ], limit=1)
            if lang:
                self.lang_id = lang
