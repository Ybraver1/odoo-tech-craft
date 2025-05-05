from odoo import models, fields

class PaymentToken(models.Model):
    _inherit = 'payment.token'

    token = fields.Char(
        string="Card Token",
        help="Your CardKnox Credit Card Token.")
