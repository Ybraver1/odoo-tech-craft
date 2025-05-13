from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from .. import const
from .carknox_request import CardknoxAPI
import json
import logging

_logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('cardknox', 'CardKnox')], ondelete={'cardknox': 'set default'})
    cardknox_token = fields.Char(string='CardKnox API Token', help='Your CardKnox API Token')
    cardknox_ifields_token = fields.Char(string='CardKnox iFields Token', help='Your CardKnox iFields API Token')

    def _compute_feature_support_fields(self):
        """ Override of `payment` to enable additional features. """
        super()._compute_feature_support_fields()
        self.filtered(lambda p: p.code == 'cardknox').update({
            'support_manual_capture': 'partial',
            'support_refund': 'partial',
            'support_tokenization': True,
            'support_express_checkout': True
        })

    def _cardknox_get_inline_form_values(self):
        """ Return the values used to initialize the iFields form.

        Note: self.ensure_one()

        :return: The JSON-compatible values to pass to the iFields form
        :rtype: str
        """
        self.ensure_one()

        inline_values = {
            'state': self.state,
            'ifields_token': self.cardknox_ifields_token
        }
        return json.dumps(inline_values)

    def _get_default_payment_method_codes(self):
        """ Override of payment to return the default payment method codes. """
        default = super()._get_default_payment_method_codes()
        if self.code != 'cardknox':
            return default
        return const.DEFAULT_PAYMENT_METHOD_CODES
        
    def _cardknox_make_request(self, endpoint_name, payload=None, method='POST'):
        """ Make a request to Cardknox API.

        Note: self.ensure_one()

        :param str endpoint_name: The endpoint name to be reached
        :param dict payload: The payload of the request
        :param str method: The HTTP method
        :return: The JSON-formatted content of the response
        :rtype: dict
        :raise ValidationError: If the request to the provider failed
        """
        self.ensure_one()
        
        # Initialize the Cardknox API client
        cardknox_api = CardknoxAPI(self)
        
        try:
            if endpoint_name == 'process_payment':
                return cardknox_api.process_payment(**payload)
            elif endpoint_name == 'save_token':
                return cardknox_api._save_token(**payload)
            elif endpoint_name == 'refund':
                return cardknox_api.refund_payment(**payload)
            elif endpoint_name == 'void':
                return cardknox_api.void_payment(**payload)
            else:
                raise ValidationError(_("Unsupported Cardknox API endpoint: %s", endpoint_name))
        except Exception as e:
            _logger.exception("Error making request to Cardknox: %s", str(e))
            raise ValidationError(_("Cardknox: %s", str(e)))


# class PaymentTransaction(models.Model):
#     _inherit = 'payment.transaction'

#     cardknox_reference = fields.Char('Cardknox Reference', help="Reference of the transaction in Cardknox")

    