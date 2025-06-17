# 🏥 Odoo Hospital Management System

An advanced hospital management system built with **Odoo 17**, designed to streamline patient care, departmental coordination, and customer relationship management (CRM). This project leverages Odoo’s modular architecture and ORM capabilities to deliver a complete, real-world-ready solution for medical institutions.

---

## 🚀 Key Features

### 🧍 Patient Management
- Full patient profile including name, birthdate, and medical history
- Auto-calculated patient age
- Automatic **PCR test requirement** for patients under 30
- Email field validation and uniqueness
- Patient status tracking with automatic log of all changes
- Relationships:
  - `Many2one` to hospital departments
  - `Many2many` with assigned doctors

### 🏥 Doctor & Department Management
- Manage hospital departments and assign doctors
- Link multiple doctors to patients for collaborative care

### 📇 CRM Integration
- Extension of `res.partner` to support patient-customer linkage
- Mandatory Tax ID for CRM contacts
- Prevent duplicate emails between patients and CRM partners
- Restrict deletion of CRM contacts linked to medical records

---

## 🛠️ Tech Stack & Tools

- **Odoo 17**
- Odoo ORM & business logic
- Model inheritance
- Computed & stored fields
- `@api.onchange`, constraints & validations
- Logging for traceability
- Custom override of `unlink()` method for safe deletions



