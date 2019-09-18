# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, api, models, tools


class ExtendContacts(models.Model):
    _inherit = 'res.partner'
    
    test = fields.Char(string = 'Test')
    tip_stranke = fields.Char(string = 'Tip Stranke')
    
    
class ExtendInventory(models.Model):
    _inherit = 'product.template'
    
    test = fields.Char(string="Test")