from odoo import models,fields
from collections import defaultdict

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'
    
    def _timesheet_create_invoice_line(self, grouped_invoice_vals, timesheet_values):
        task_map = defaultdict(float)
        
        for timesheet in timesheet_values:
            task = timesheet['task_id']
            unit_amount = timesheet['unit_amount']
            task_map[task] += unit_amount
            
        for task, unit_amount in task_map.items():
            invoice_line_vals = self._prepare_invoice_line()
            invoice_line_vals['name'] = f"{self.name} - {task.name}"
            invoice_line_vals['quantity'] = unit_amount
            invoice_line_vals['task_id'] = task.id
            
            grouped_invoice_vals.append(invoice_line_vals)
            
        return grouped_invoice_vals