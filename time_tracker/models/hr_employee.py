from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    wise_email = fields.Char()
    wise_currency = fields.Char(default='USD')
    