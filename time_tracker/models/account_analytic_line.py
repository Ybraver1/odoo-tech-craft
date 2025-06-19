from odoo import models,fields,api

class AnaliticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    
    def action_validate_timesheet(self):
        # Call original method first
        result = super().action_validate_timesheet()

        # Your custom logic to create bills for freelancers
        self._create_freelancer_bills()

        return result
    
    def _create_freelancer_bills(self):
        freelancer_lines = self.filtered(lambda l: l.validated and l.employee_id and l.employee_id.employee_type == 'freelance')
        if not freelancer_lines:
            return
        freelancer_map = {}
        for line in freelancer_lines:
            freelancer_map.setdefault(line.employee_id, self.env['account.analytic.line'])
            freelancer_map[line.employee_id] |= line
        
        freelancer_bills = []
            
        for freelancer, lines in freelancer_map.items():
            bill_vals = {
                'partner_id': freelancer.work_contact_id.id,
                'type': 'in_invoice',
                'invoice_line_ids': [],
            }
             
            for line in lines:
                bill_vals['invoice_line_ids'].append(
                    (0, 0, {
                        'name': line.name or _('Timesheet Line'),
                        'account_id': line.project_id.analytic_account_id.id or self.env['account.account'].search([('user_type_id.name','=','Expenses')], limit=1).id,
                        'quantity': line.unit_amount,
                        'price_unit': line.employee_id.timesheet_cost or 0.0,
                    })
                )

            freelancer_bills.append(bill_vals)
            
        self.env['account.move'].create(freelancer_bills)