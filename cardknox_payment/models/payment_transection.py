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
            return cardknox_api._save_token(card_number=payload['cardNo'],exp_date= payload['exp'],cvv= payload['cvv'])
        # else:
        #     return cardknox_api.process_payment(amount=payload['amount'],)