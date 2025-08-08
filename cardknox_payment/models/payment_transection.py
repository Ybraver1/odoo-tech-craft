import logging
import pprint

from odoo import _, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.payment import utils as payment_utils
from .carknox_request import CardknoxAPI
_logger = logging.getLogger(__name__)
class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'
    
    def create_cardknox_transection(self,payload):
        self.ensure_one()
        cardknox_api = CardknoxAPI(self.provider_id)
        _logger.info('payment: \n%s \n%s',pprint.pformat(self),pprint.pformat(payload))
        if payload['amount'] == 0:
            return cardknox_api._save_token(card_number=payload['card'],exp_date= payload['exp'],cvv= payload['cvv'])
        else:
            return cardknox_api.process_payment(amount=payload['amount'],card_number=payload['card'],exp= payload['exp'],cvv= payload['cvv'],reference=payload['reference'])
        
    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'cardknox':
            return
        
        
        response_content = notification_data.get('response')
        self.provider_reference = response_content.get('xRefNum')
        
        result = response_content.get('xResult')

        if result == 'A':
            _logger.info(response_content)
            self._set_done()
            if self.tokenize and not self.token_id:
                self.tokenize_cardknox(response_content)

    
    def tokenize_cardknox(self,response):

        token = self.env['payment.token'].create({
            'provider_id': self.provider_id.id,
            'payment_method_id': self.payment_method_id.id,
            'payment_details': response['xMaskedCardNumber'],
            'partner_id': self.partner_id.id,
            'provider_ref': response['xToken'],            
        })
        self.write({
            'token_id': token.id,
            'tokenize': False,
        })
        _logger.info(
            "created token with id %(token_id)s for partner with id %(partner_id)s from "
            "transaction with reference %(ref)s",
            {
                'token_id': token.id,
                'partner_id': self.partner_id.id,
                'ref': self.reference,
            },
        )
    
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
        

        # Use token for recurring payments
        if not self.token_id:
            
            raise ValidationError(_("Cardknox: No payment token provided."))
        
        
        else:
            cardknox_api = CardknoxAPI(self.provider_id)
            _logger.warning('payment: \n%s',pprint.pformat(self.token_id.token))
            response = cardknox_api.process_payment(amount = self.amount, reference = self.reference, token_id=self.token_id) 
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




           