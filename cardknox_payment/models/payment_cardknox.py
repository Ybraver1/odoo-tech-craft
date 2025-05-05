from odoo import models, fields, api
from .. import const
import json
class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('cardknox', 'CardKnox')], ondelete={'cardknox': 'set default'})
    cardknox_token = fields.Char(string='CardKnox Token', help='Your CardKnox API Token')
    cardknox_ifields_token = fields.Char(string='CardKnox iFields Token', help='Your CardKnox iFields API Token')

    def _compute_feature_support_fields(self):
        """ Override of `payment` to enable additional features. """
        super()._compute_feature_support_fields()
        self.filtered(lambda p: p.code == 'cardknox').update({
            'support_manual_capture': 'partial',
            'support_refund': 'partial',
            'support_tokenization': True,
        })

    def _cardknox_get_inline_form_values(self):

        self.ensure_one()

        inline_values = {
            'state':self.state,
            # 'token': self.cardknox_token,
            'ifields_token':  self.cardknox_ifields_token
        }
        return json.dumps(inline_values)

    def _get_default_payment_method_codes(self):
        default = super()._get_default_payment_method_codes()
        if self.code != 'cardknox':
            return default
        return const.DEFAULT_PAYMENT_METHOD_CODES
