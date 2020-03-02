from odoo import fields, api, models, tools 
from odoo import exceptions
from datetime import date

class ExtendUser(models.Model):
    _inherit = ['res.users']
    
    #ADDONS
    school=fields.Char(String="Šola")