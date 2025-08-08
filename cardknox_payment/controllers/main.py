import logging
import pprint

from odoo import _, http
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.payment import utils as payment_utils

_logger = logging.getLogger(__name__)

class CardknoxController(http.Controller):
    @http.route('/payment/cardknox/payment',type='json')
    def cardknox_payment(self,payment_info,payment_perems):
        
        tx_sudo = request.env['payment.transaction'].sudo().search([('reference', '=', payment_perems['reference'])])
        _logger.info("tx_sudo:\n%s \n%s",pprint.pformat(tx_sudo), pprint.pformat(self))
        response_content = tx_sudo.create_cardknox_transection({
            'amount':payment_perems['amount'],
            'card':payment_info['cardNo'],
            'exp':payment_info['exp'],
            'cvv':payment_info['cvv'], 
            'reference':payment_perems['reference']           
        })
        _logger.info("res content \n%s",pprint.pformat(response_content))
        tx_sudo._handle_notification_data('cardknox', response_content)
        