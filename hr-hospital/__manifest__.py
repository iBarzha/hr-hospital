{
    'name': 'Hospital Management',
    'summary': 'Hospital management system for patients, doctors and visits',
    'author': 'Anton Bardzheiev',
    'website': 'https://github.com/iBarzha/hr-hospital',
    'category': 'Healthcare',
    'license': 'LGPL-3',
    'version': '17.0.2.0.0',

    'depends': [
        'base',
    ],

    'external_dependencies': {
        'python': []
    },

    'installable': True,

    'data': [
        'security/hr_hospital_groups.xml',
        'security/ir.model.access.csv',
        'security/hr_hospital_rules.xml',

        'data/hr_hospital_disease_data.xml',

        'views/contact_person_views.xml',
        'views/doctor_speciality_views.xml',
        'views/doctor_schedule_views.xml',
        'views/medical_diagnosis_views.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_visit_views.xml',

        'wizards/mass_reassign_doctor_wizard_views.xml',
        'wizards/disease_report_wizard_views.xml',
        'wizards/reschedule_visit_wizard_views.xml',
        'wizards/doctor_schedule_wizard_views.xml',
        'wizards/patient_card_export_wizard_views.xml',

        'report/hr_hospital_doctor_report.xml',

        'views/hr_hospital_menu.xml',
    ],

    'demo': [
        'demo/hr_hospital_demo.xml',
    ],
}
