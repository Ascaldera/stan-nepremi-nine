# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details.
 
from odoo import fields, api, models, tools

class custom_location(models.Model):   
    _name = 'custom.location'
    _description = 'Config - Upravne enote'

    regija = fields.Many2one('custom.location.regija', string='Regija')
    name = fields.Char('Upravna Enota')
    
class custom_location_regija(models.Model):   
    _name = 'custom.location.regija'
    _description = 'Config - Regija'

    name = fields.Char('Regija')
    drzava = fields.Many2one('res.country', string = 'Država')