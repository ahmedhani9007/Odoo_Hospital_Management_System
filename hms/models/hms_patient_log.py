from odoo import models, fields, api
from datetime import datetime

class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log History'
     #res.users: is Odoo's built-in model that represents system users.
     #self.env.user is a reference to the current user of the Odoo session.
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user, readonly=True)
    log_date = fields.Datetime(string='Date', default=datetime.now(), readonly=True)
    description = fields.Text(string='Description', required=True)
    patient_id = fields.Many2one('hms.patient', string='Patient', required=True)
