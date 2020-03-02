from odoo import fields, api, models, tools 
from odoo import exceptions
from datetime import date

class ExtendUser(models.Model):
    _inherit = ['res.users']
    
    #ADDONS
    birthdate=fields.Date(String="Datum Rojstva")
    address=fields.Char(String="Trenutni naslov")
    phone_number=fields.Char(String="Telefonka številka")
    business_email=fields.Char(String='Službena e-pošta')
    school=fields.Char(String="Šola")