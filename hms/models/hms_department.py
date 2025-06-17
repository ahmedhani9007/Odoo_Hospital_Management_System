from odoo import models, fields

class HmsDepartment(models.Model):
    _name = 'hms.department'
    
    name = fields.Char('Name', required=True)
    capacity = fields.Integer(string="Capacity")
    is_opened = fields.Boolean(string="Is Opened")
    # Add the One2many field for the relationship
    patient_ids = fields.One2many('hms.patient', 'department_id', string="Patients")
