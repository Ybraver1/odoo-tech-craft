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
        # else:
        #     return cardknox_api.process_payment(amount=payload['amount'],)
        
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



           