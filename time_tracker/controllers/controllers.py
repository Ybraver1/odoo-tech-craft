# -*- coding: utf-8 -*-
# from odoo import http


# class TimeTracker(http.Controller):
#     @http.route('/time_tracker/time_tracker', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/time_tracker/time_tracker/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('time_tracker.listing', {
#             'root': '/time_tracker/time_tracker',
#             'objects': http.request.env['time_tracker.time_tracker'].search([]),
#         })

#     @http.route('/time_tracker/time_tracker/objects/<model("time_tracker.time_tracker"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('time_tracker.object', {
#             'object': obj
#         })

