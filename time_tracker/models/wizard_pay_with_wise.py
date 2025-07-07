from odoo import models, fields
import uuid,logging

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class WizardPayWithWise(models.TransientModel):
    _name = 'wizard.pay.with.wise'
    _description = 'Wizard to pay with Wise'

    bill_id = fields.Many2one('account.move', required=True)
    amount = fields.Float(string='Amount', required=True)
    

    def action_pay(self):
        self.ensure_one()
        move = self.bill_id
        
        token = self.env['ir.config_parameter'].sudo().get_param('wise.api_key')
        
        partner = move.partner_id
        employee = partner.employee_ids[0]
        if not employee.wise_recipient_id:
            raise UserError(f"Employee {employee.name} does not have a Wise recipient ID.")
        _logger.warning(f"Employee: {employee.wise_recipient_id}")