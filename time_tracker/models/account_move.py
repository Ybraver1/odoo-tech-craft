from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def open_wise_wizard(self):
        self.ensure_one()
        return {
            'name': 'Pay with Wise',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.pay.with.wise',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_bill_id': self.id,
                'default_amount': self.amount_total,
                
            }
        }
