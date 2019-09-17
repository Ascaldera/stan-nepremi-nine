# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class ExtendContacts(models.Model):
    _inherit = 'res.partner'
    _description = "Extend Contact"
    
    test = fields.Char(string="Test")
    
    
class ExtendInventory(models.Model):
    _inherit = 'product.template'
    _description = "Extend Inventory"
    
    test = fields.Char(string="Test")