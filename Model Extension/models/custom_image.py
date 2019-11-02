# -*- coding: utf-8 -*- 
# Part of Odoo. See LICENSE file for full copyright and licensing details.
 
from odoo import fields, api, models, tools

class custom_image(models.Model):   
    _name = 'custom.image'
    _description = 'Custom Image'

    name = fields.Char('Name')
    image = fields.Binary('Image', attachment=True)
    image_many = fields.Many2many('ir.attachment', string='slike')
    product_tmpl_id = fields.Many2one('product.template', 'Related Product', copy=True)
    prikaz=fields.Selection(string='Prikaz', selection = [('splet','Splet'),('arhiv','Arhiv')], default = 'splet')
    
    
class extend_attachment(models.Model):   
    _inherit = 'ir.attachment'

    product_tmpl_id = fields.Many2one('product.template', 'Related Product', copy=True)
    prikaz=fields.Selection(string='Prikaz', selection = [('splet','Splet'),('arhiv','Arhiv')], default = 'splet')