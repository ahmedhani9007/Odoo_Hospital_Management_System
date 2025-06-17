from odoo import models, fields

class HmsDoctor(models.Model):
    _name = 'hms.doctor'
    
    first_name = fields.Char('First Name', required=True)
    last_name = fields.Char('Last Name', required=True)
    image = fields.Image('Doctor Image')
    #Doctor A can treat more than one patient
    patient_ids = fields.Many2many('hms.patient', string='Patients')