from odoo import models, fields, api
from .wise_api import WiseAPI
import logging

_logger = logging.getLogger(__name__)
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    wise_email = fields.Char()
    wise_currency = fields.Char(default='USD')
    wise_recipient_id = fields.Char()
    
    
    def create_wise_recipient(self):
        token = self.env['ir.config_parameter'].sudo().get_param('wise.api_key')
        profile_id = self.env['ir.config_parameter'].sudo().get_param('wise.profile_id')
        for employee in self:
            if employee.wise_email and not employee.wise_recipient_id:
                # Call Wise API to create recipient
                wise_api = WiseAPI(token, profile_id)
                recipient = wise_api.create_recipient(
                    account_holder_name=employee.name,
                    email=employee.wise_email,
                    currency=employee.wise_currency
                )
                _logger.warning(f"Wise recipient created: {recipient}")
                #employee.wise_recipient_id = recipient['id']


    @api.model
    def create(self, vals):
        employee = super().create(vals)
        employee.create_wise_recipient()
        return employee
    
    def write(self, vals):
        res = super().write(vals)
        self.create_wise_recipient()
        return res
