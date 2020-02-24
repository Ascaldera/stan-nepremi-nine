# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details.
 
from odoo import fields, api, models, tools
    
class custom_location_regija(models.Model):   
    _name = 'custom.location.regija'
    _description = 'Config - Regija'

    name = fields.Char('Regija')
    code = fields.Char('Iskalno polje')
    
class custom_location(models.Model):   
    _name = 'custom.location'
    _description = 'Config - Upravne enote'

    regija = fields.Many2one('custom.location.regija', string='Regija')
    name = fields.Char('Upravna Enota')
    code = fields.Char('Iskalno polje')

class custom_nepremicnina_vrsta(models.Model):
    _name = 'custom.vrsta'
    _description = 'Config - Vrsta nepremičnine'
    
    name = fields.Char('')
    code = fields.Char('Iskalno polje')
    
class custom_nepremicnina_tip(models.Model):
    _name = 'custom.tip'
    _description = 'Config - Tip nepremičnine'
    
    vrsta = fields.Many2one('custom.vrsta', string='Vrsta nepremicnine')
    name = fields.Char('Tip nepremičnine')
    code = fields.Char('Iskalno polje')