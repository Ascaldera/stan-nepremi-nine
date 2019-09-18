# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, api, models, tools

class ExtendContacts(models.Model):
    _inherit = ['res.partner']
    
    product_id = fields.Many2one('product.product', string='Kaj Prodaja')
    product_kraj = fields.One2many('product.product', 'product_id', string='Kdo Prodaja')
    product_cena = fields.One2many('product.product', 'product_id', string='Cena')
    
    tip_stranke = fields.Selection(string='Tip Stranke', selection=[('prodajalec', 'Prodajalec'), , 
                                                                    ('kupec', 'Kupec'), 
                                                                    ('najemodajalec', 'Najemodajalec'), 
                                                                    ('najemnik', 'Najemnik')])
    
    
"""class ExtendInventory(models.Model):
    _inherit = 'product.template'
    
    test = fields.Char(string="Test")"""