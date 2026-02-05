from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestHrHospitalDoctor(TransactionCase):
    """Test cases for hr.hospital.doctor model."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.speciality = cls.env['doctor.speciality'].create({
            'name': 'Test Speciality',
        })
        cls.doctor = cls.env['hr.hospital.doctor'].create({
            'first_name': 'John',
            'last_name': 'Doe',
            'license_number': 'LIC001',
            'license_date': date.today() - timedelta(days=365 * 5),
            'speciality_id': cls.speciality.id,
        })
        cls.intern = cls.env['hr.hospital.doctor'].create({
            'first_name': 'Jane',
            'last_name': 'Smith',
            'license_number': 'LIC002',
            'is_intern': True,
            'mentor_id': cls.doctor.id,
        })

    def test_compute_experience_years(self):
        """Test experience years computation from license date."""
        self.assertEqual(self.doctor.experience_years, 5)
        self.doctor.license_date = date.today() - timedelta(days=365 * 10)
        self.assertEqual(self.doctor.experience_years, 10)

    def test_check_mentor_cannot_be_intern(self):
        """Test that intern cannot be assigned as mentor."""
        with self.assertRaises(ValidationError):
            self.env['hr.hospital.doctor'].create({
                'first_name': 'New',
                'last_name': 'Intern',
                'license_number': 'LIC003',
                'is_intern': True,
                'mentor_id': self.intern.id,
            })

    def test_check_mentor_cannot_be_self(self):
        """Test that doctor cannot be their own mentor."""
        with self.assertRaises(ValidationError):
            self.doctor.write({
                'is_intern': True,
                'mentor_id': self.doctor.id,
            })


class TestHrHospitalVisit(TransactionCase):
    """Test cases for hr.hospital.visit model."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.speciality = cls.env['doctor.speciality'].create({
            'name': 'Test Speciality',
        })
        cls.doctor = cls.env['hr.hospital.doctor'].create({
            'first_name': 'John',
            'last_name': 'Doe',
            'license_number': 'LIC001',
            'speciality_id': cls.speciality.id,
        })
        cls.patient = cls.env['hr.hospital.patient'].create({
            'first_name': 'Patient',
            'last_name': 'One',
        })
        cls.visit = cls.env['hr.hospital.visit'].create({
            'doctor_id': cls.doctor.id,
            'patient_id': cls.patient.id,
            'visit_type': 'primary',
        })

    def test_action_complete(self):
        """Test visit completion action."""
        self.assertEqual(self.visit.state, 'scheduled')
        self.visit.action_complete()
        self.assertEqual(self.visit.state, 'completed')
        self.assertTrue(self.visit.actual_datetime)

    def test_action_cancel(self):
        """Test visit cancellation action."""
        self.assertEqual(self.visit.state, 'scheduled')
        self.visit.action_cancel()
        self.assertEqual(self.visit.state, 'cancelled')


class TestMedicalDiagnosis(TransactionCase):
    """Test cases for medical.diagnosis model."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.speciality = cls.env['doctor.speciality'].create({
            'name': 'Test Speciality',
        })
        cls.doctor = cls.env['hr.hospital.doctor'].create({
            'first_name': 'John',
            'last_name': 'Doe',
            'license_number': 'LIC001',
            'speciality_id': cls.speciality.id,
        })
        cls.patient = cls.env['hr.hospital.patient'].create({
            'first_name': 'Patient',
            'last_name': 'One',
        })
        cls.disease = cls.env['hr.hospital.disease'].create({
            'name': 'Test Disease',
            'icd10_code': 'T00',
            'is_contagious': True,
            'danger_level': 'high',
        })
        cls.visit = cls.env['hr.hospital.visit'].create({
            'doctor_id': cls.doctor.id,
            'patient_id': cls.patient.id,
            'state': 'completed',
        })
        cls.diagnosis = cls.env['medical.diagnosis'].create({
            'visit_id': cls.visit.id,
            'disease_id': cls.disease.id,
            'severity': 'moderate',
        })

    def test_action_approve(self):
        """Test diagnosis approval action."""
        self.assertFalse(self.diagnosis.is_approved)
        self.diagnosis.action_approve()
        self.assertTrue(self.diagnosis.is_approved)
        self.assertTrue(self.diagnosis.approval_date)
        self.assertEqual(self.diagnosis.approved_by_id, self.doctor)
