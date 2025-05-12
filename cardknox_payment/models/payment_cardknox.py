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


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    cardknox_reference = fields.Char('Cardknox Reference', help="Reference of the transaction in Cardknox")

    def _get_specific_processing_values(self, processing_values):
        """ Override of payment to return Cardknox-specific processing values.

        Note: self.ensure_one()

        :param dict processing_values: The generic processing values of the transaction
        :return: The dict of provider-specific processing values
        :rtype: dict
        """
        res = super()._get_specific_processing_values(processing_values)
        if self.provider_code != 'cardknox':
            return res

        return {
            'cardknox_token': processing_values.get('cardknox_token'),
        }

    def _process_transaction_data(self, data):
        """ Override of payment to process the transaction based on Cardknox data.

        Note: self.ensure_one()

        :param dict data: The Cardknox data
        :return: None
        """
        super()._process_transaction_data(data)
        if self.provider_code != 'cardknox':
            return

        # Extract the Cardknox reference from the data
        self.cardknox_reference = data.get('xRefNum')

        # Update the transaction state based on the response
        if data.get('xStatus') == 'Approved':
            self._set_done()
        elif data.get('xStatus') == 'Declined':
            self._set_canceled(data.get('xError', 'Payment declined by Cardknox'))
        else:
            self._set_error(data.get('xError', 'Unknown error'))

    def _send_payment_request(self):
        """ Override of payment to send a payment request to Cardknox.

        Note: self.ensure_one()

        :return: None
        :raise: ValidationError if the transaction is not linked to a token
        """
        super()._send_payment_request()
        if self.provider_code != 'cardknox':
            return

        # Make the payment request to Cardknox
        payload = {
            'amount': self.amount,
            'reference': self.reference,
            'customer_name': f"{self.partner_id.name}",
            'customer_email': self.partner_id.email,
        }

        # Add billing address if available
        if self.partner_id:
            payload['billing_address'] = {
                'street': self.partner_id.street or '',
                'city': self.partner_id.city or '',
                'state': self.partner_id.state_id.code if self.partner_id.state_id else '',
                'zip': self.partner_id.zip or '',
                'country': self.partner_id.country_id.code if self.partner_id.country_id else '',
            }

        # Use token for recurring payments
        if self.token_id:
            payload['token_id'] = self.token_id.token
        # Use card token for one-time payments
        elif self.cardknox_token:
            payload['card_token'] = self.cardknox_token
        else:
            raise ValidationError(_("Cardknox: No payment token provided."))

        response = self.provider_id._cardknox_make_request('process_payment', payload)
        self._process_transaction_data(response)

    def _send_refund_request(self, amount_to_refund=None):
        """ Override of payment to send a refund request to Cardknox.

        Note: self.ensure_one()

        :param float amount_to_refund: The amount to refund
        :return: The refund transaction
        :rtype: recordset of `payment.transaction`
        """
        refund_tx = super()._send_refund_request(amount_to_refund)
        if self.provider_code != 'cardknox':
            return refund_tx

        # Make the refund request to Cardknox
        payload = {
            'amount': amount_to_refund or self.amount,
            'reference': refund_tx.reference,
            'transaction_id': self.cardknox_reference,
        }

        response = self.provider_id._cardknox_make_request('refund', payload)
        refund_tx._process_transaction_data(response)
        return refund_tx

    def _send_void_request(self):
        """ Override of payment to send a void request to Cardknox.

        Note: self.ensure_one()

        :return: None
        """
        super()._send_void_request()
        if self.provider_code != 'cardknox':
            return

        # Make the void request to Cardknox
        payload = {
            'transaction_id': self.cardknox_reference,
        }

        response = self.provider_id._cardknox_make_request('void', payload)
        self._process_transaction_data(response)
