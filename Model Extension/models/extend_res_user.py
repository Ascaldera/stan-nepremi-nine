from odoo import fields, api, models, tools 
from odoo import exceptions
from datetime import date

class ExtendUser(models.Model):
    _inherit = ['res.users']
    
    #ADDONS
    first_name = fields.Char(String='Ime')
    last_name = fields.Char(String='Priimek')
    user_role = fields.Selection(selection=[('marketing', 'Marketinški ekspert'),('real_estate', 'Nepremičninski ekspert')])