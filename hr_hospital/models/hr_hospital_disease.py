from odoo import fields, models


class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Hospital Disease'
    _parent_name = 'parent_id'
    _parent_store = True

    name = fields.Char(required=True)
    description = fields.Text()
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Parent Disease',
        index=True,
        ondelete='cascade',
    )
    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Child Diseases',
    )
    parent_path = fields.Char(index=True)
    icd10_code = fields.Char(
        string='ICD-10 Code',
        size=10,
    )
    danger_level = fields.Selection(
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
    )
    is_contagious = fields.Boolean(
        string='Contagious',
        default=False,
    )
    symptoms = fields.Text()
    region_ids = fields.Many2many(
        comodel_name='res.country',
        string='Spread Regions',
        relation='disease_country_rel',
        column1='disease_id',
        column2='country_id',
    )
    active = fields.Boolean(default=True)
