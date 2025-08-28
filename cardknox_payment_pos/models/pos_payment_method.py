from odoo import models, fields

class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    def _get_payment_terminal_selection(self):
        # This method adds 'CardKnox' to the list of available payment terminals.
        return super()._get_payment_terminal_selection() + [('cardknox', 'CardKnox')]

   
