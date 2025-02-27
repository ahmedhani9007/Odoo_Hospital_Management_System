import re
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError, ValidationError  

class HmsPatient(models.Model):
    _name = 'hms.patient'


    #calc age based on birthdate of patient
    @api.depends("birthdate")
    def calc_age(self):
        for patient in self:
            if patient.birthdate:
                today = datetime.today().date()
                birthdate = patient.birthdate
                patient.age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            else:
                patient.age = 0

            
            
    first_name = fields.Char('First Name')
    last_name = fields.Char('Last Name')
    birthdate = fields.Date('Birth Date')
    history = fields.Html('Medical History')
    cr_ratio = fields.Float('CR Ratio')
    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-')
    ], string='Blood Type')    
    pcr = fields.Boolean('PCR Test')
    image = fields.Image('Patient Image')
    address = fields.Text('Address')
    age = fields.Integer(compute="calc_age")
    department_id = fields.Many2one('hms.department', string='Department')
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors')

    department_capacity = fields.Integer(related="department_id.capacity")
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='Log History')
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], string='State', default='undetermined')
    
    email=fields.Char()
    
         # Define SQL constraints
    _sql_constraints = [
        # Enforce uniqueness on the 'name' field
        ('unique_email_name', 'unique(email)', 'The email must be unique for each patient.')
    ]
    
    @api.constrains('email')
    def _check_email_format(self):
        """Ensure the email format is correct."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError(f"The email '{record.email}' is not in a valid format. Please enter a valid email address.")
    
    
    @api.onchange('age')
    def _onchange_age(self):
        """Automatically check PCR if age < 30 and show a warning"""
        if self.age and self.age < 30:
            if not self.pcr:
                self.pcr = True
                return {
                    'warning': {
                        'title': "PCR Test Automatically Checked",
                        'message': "PCR Test has been automatically checked because the age is less than 30.",
                    }
                }
                
    @api.model
    def create(self, vals):
        """Ensure state logs are created on patient creation."""
        record = super(HmsPatient, self).create(vals)
        if 'state' in vals:
            record._create_log(f"State initialized to {vals['state']}")
        return record   
    
    def write(self, vals):
            """Log changes in state."""
            for record in self:
                if 'state' in vals and vals['state'] != record.state:
                    new_state = vals['state']
                    record._create_log(f"State changed to {new_state}")
            return super(HmsPatient, self).write(vals)

    def _create_log(self, description):
        """Helper method to create log entries."""
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': description,
            'log_date': datetime.now(),
            'created_by': self.env.user.id,
        })    
        
    
    ##
#Undetermined:
# The patient's condition has not been evaluated yet, or there isn't enough information to define their state.
# Good:
# The patient is in good health with no major issues.
# Fair:
# The patient's condition is relatively stable but may have minor issues that need monitoring.
# Serious:
# The patient is in critical or serious condition and requires immediate or ongoing medical attention.
##    
    
    

