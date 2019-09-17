# -*- coding: utf-8 -*-
from odoo import http

# class ExpandModels(http.Controller):
#     @http.route('/expand_models/expand_models/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/expand_models/expand_models/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('expand_models.listing', {
#             'root': '/expand_models/expand_models',
#             'objects': http.request.env['expand_models.expand_models'].search([]),
#         })

#     @http.route('/expand_models/expand_models/objects/<model("expand_models.expand_models"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('expand_models.object', {
#             'object': obj
#         })