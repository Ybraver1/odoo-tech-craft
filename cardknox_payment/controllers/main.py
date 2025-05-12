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
        _logger.info(
            "payment request response for transaction with reference %s:\n%s",
            pprint.pformat(payment_info), pprint.pformat(payment_perems)
        )
        tx_sudo = request.env['payment.transaction'].sudo().search([('reference', '=', payment_perems['reference'])])
        _logger.info("tx_sudo:\n%s",pprint.pformat(tx_sudo))
        