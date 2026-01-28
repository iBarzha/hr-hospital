=========================
Hospital Management System
=========================

.. |badge1| image:: https://img.shields.io/badge/licence-OPL--1-blue.svg
    :target: https://www.odoo.com/documentation/17.0/legal/licenses.html
    :alt: License: OPL-1

.. |badge2| image:: https://img.shields.io/badge/Odoo-17.0-purple.svg
    :target: https://www.odoo.com/
    :alt: Odoo 17.0

|badge1| |badge2|

A comprehensive hospital management module for Odoo 17 Community Edition.

**Table of contents**

.. contents::
   :local:

Features
========

Doctor Management
-----------------
* Complete doctor profiles with personal and professional information
* Speciality assignment and tracking
* Intern-mentor relationship management
* License number tracking with experience calculation
* Doctor schedule management
* Rating system for doctors

Patient Management
------------------
* Detailed patient records with medical information
* Personal doctor assignment with change history
* Blood type and allergy tracking
* Insurance information management
* Contact person for emergencies

Visit Management
----------------
* Schedule and track patient visits
* Multiple visit types: Primary, Follow-up, Preventive, Emergency
* Visit status workflow: Scheduled → Completed/Cancelled
* Visit rescheduling wizard
* Calendar and Kanban views for easy management

Medical Diagnosis
-----------------
* Disease classification based on ICD-10 codes
* Diagnosis recording per visit
* Severity levels: Mild, Moderate, Severe, Critical
* Approval workflow for intern diagnoses
* Treatment recommendations

Reports
-------
* Doctor report with visit history and patient list
* Color-coded visit status (scheduled/completed/cancelled)
* Disease statistics with pivot and graph views

Security
========

Role-based access control with hierarchical groups:

* **Patient** - View own visits only
* **Intern** - View and edit own visits
* **Doctor** - Manage own visits and intern visits
* **Manager** - View all visits
* **Administrator** - Full access with delete permissions

Installation
============

1. Copy the module to your Odoo addons directory
2. Update the module list in Odoo
3. Install the module from Apps menu

Configuration
=============

1. Go to Hospital → Configuration → Specialities to set up doctor specialities
2. Create doctors and assign specialities
3. Create patients and assign personal doctors
4. Start scheduling visits

Usage
=====

1. Navigate to Hospital menu
2. Create doctors with their specialities
3. Register patients
4. Schedule visits between patients and doctors
5. Record diagnoses during or after visits
6. Generate reports as needed

Bug Tracker
===========

If you encounter any issues, please report them at:
https://github.com/iBarzha/hr-hospital/issues

Credits
=======

Authors
-------
* Anton Bardzheiev

Maintainers
-----------
This module is maintained by Anton Bardzheiev.
