# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details.
 
from odoo import fields, api, models, tools

class custom_sifrant(models.Model):
    _name='custom.sifrant'
    _description='Sifrant izvora oglasa'
    _order = 'name asc'
    
    name=fields.Char(string="Ime oglaševanja")
    display=fields.One2many(string="Oglaševane nepremičnine",
                            comodel_name="product.template",
                            inverse_name="nepremicnina_oglasevana_kje")