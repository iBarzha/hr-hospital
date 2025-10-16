{
    'name': 'Hospital Management',
    'summary': '',
    'author': 'Anton Bardzheiev',
    'website': 'http://hr.hospital',
    'category': 'Human Resources',
    'license': 'OPL-1',
    'version': '17.0.1.0.0',

    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': []
    },

    'data': [

        'security/ir.model.access.csv',

        'data/hr_hospital_disease_data.xml',

        'views/hr_hospital_menu.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_visit_views.xml',
    ],
    'demo': [
        'demo/hr_hospital_demo.xml',
    ],

    'installable': True,
    'auto_install': False,
}
