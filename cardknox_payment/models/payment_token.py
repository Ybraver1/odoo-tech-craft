from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PaymentToken(models.Model):
    _inherit = 'payment.token'

    cardknox_token = fields.Char(
        string="Cardknox Token",
        help="The token representing the payment details on Cardknox."
    )
    
    @api.model
    def _cardknox_create_token_from_data(self, provider_id, payment_details, partner_id=None, **kwargs):
        """Create a token for Cardknox.
        
        :param int provider_id: The provider handling the transaction
        :param dict payment_details: The payment details to tokenize
        :param int partner_id: The partner making the transaction
        :return: A token
        :rtype: recordset of `payment.token`
        """
        provider = self.env['payment.provider'].browse(provider_id)
        if provider.code != 'cardknox':
            return super()._cardknox_create_token_from_data(provider_id, payment_details, partner_id, **kwargs)
            
        if not payment_details.get('cardknox_token'):
            raise ValidationError(_("Cardknox: No token provided for tokenization."))
            
        # Extract card info from the token response
        card_type = payment_details.get('card_type', 'Card')
        last4 = payment_details.get('last4', '****')
        exp_month = payment_details.get('exp_month', '**')
        exp_year = payment_details.get('exp_year', '**')
        
        # Create the token
        token = self.create({
            'provider_id': provider_id,
            'partner_id': partner_id,
            'token': payment_details['cardknox_token'],
            'cardknox_token': payment_details['cardknox_token'],
            'payment_method_id': self.env.ref('payment.payment_method_card').id,
            'payment_details': f"{card_type} •••• {last4} (expires {exp_month}/{exp_year})",
        })
        
        return token
