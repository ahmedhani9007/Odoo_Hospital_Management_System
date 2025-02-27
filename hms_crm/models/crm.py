import re
from odoo import models,fields, api
from datetime import datetime
from odoo.exceptions import ValidationError  
from lxml import etree

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Define the new field related to the patient
    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")
    
   #Make Tax ID field mandatory
    #vat is a predefined field in Odoo's res.partner model for storing Tax IDs, used for compliance and localization, and can be customized without creating duplicates.
    vat = fields.Char(string="Tax ID", required=True)
     
    @api.constrains('email')
    def _check_email_against_patients(self):
        """Prevent linking customers with emails that already exist in the patient model."""
        for record in self:
            if record.email:
                existing_patient = self.env['hms.patient'].search([('email', '=', record.email)], limit=1)
                if existing_patient:
                    raise ValidationError(f"The email '{record.email}' is already associated with a patient and cannot be used for a customer.")
                
                
    def unlink(self):
        """Prevent deletion of customers linked to a patient."""
        for record in self:
            if record.related_patient_id: #it means the customer is linked to a patient.
                raise ValidationError(f"Cannot delete customer '{record.name}' because they are linked to a patient.")
        return super(ResPartner, self).unlink()
   
   
   