# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, api, models, tools

class ExtendContacts(models.Model):
    _inherit = ['res.partner']
    
    tip_stranke = fields.Selection(selection=[('prodajalec', 'Prodajalec'),
                                              ('kupec', 'Kupec'),
                                              ('najemodajalec', 'Najemodajalec'),
                                              ('najemnik', 'Najemnik')])
    nepremicnine = fields.One2many(comodel_name='product.template', inverse_name="contact", string='Product ID')
    pridobitev = fields.Char()
    
    
class ExtendInventory(models.Model):
    _inherit = 'product.template'
    
    contact=fields.Many2one(comodel_name="res.partner", string="Contact")