=========
Changelog
=========

17.0.2.0.0 (2024-01-28)
=======================

Added
-----
* Security groups: Patient, Intern, Doctor, Manager, Administrator
* Record rules for visit access control
* Ukrainian translation (uk.po)
* Doctor report with visit history and patient table
* Kanban view for doctors with intern list
* Unit tests for doctor, visit, and diagnosis models
* Module description (index.html)
* README.rst documentation

Changed
-------
* Improved pivot views for diagnoses and visits
* Fixed translation function usage

17.0.1.0.0 (2024-01-15)
=======================

Added
-----
* Disease report wizard
* Reschedule visit wizard
* Doctor schedule wizard
* Patient card export wizard
* Mass reassign doctor wizard
* Pivot and graph views for visits and diagnoses

17.0.0.2.0 (2024-01-10)
=======================

Added
-----
* Medical diagnosis model with approval workflow
* Doctor schedule management
* Patient doctor history tracking
* Disease classification with ICD-10 codes
* Visit type selection

Changed
-------
* Enhanced doctor model with license tracking
* Added experience years computation
* Added intern-mentor relationship validation

17.0.0.1.0 (2024-01-01)
=======================

Initial Release
---------------
* Hospital Doctor model
* Hospital Patient model
* Hospital Visit model
* Doctor Speciality model
* Contact Person model
* Basic views (tree, form, search)
* Menu structure
