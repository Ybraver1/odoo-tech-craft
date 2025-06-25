from odoo import models,fields


class Partner(models.Model):
    _inherit = 'res.partner'
    
    calls_count = fields.Integer(compute='compute_call_count')
    
    def compute_call_count(self):
        for rec in self:
            rec.calls_count = self.env['voip.call'].search_count([('partner_id','=',rec.id)])
            
    def action_view_calls(self):
        self.ensure_one()
        return {
            'name': 'Calls',
            'type': 'ir.actions.act_window',
            'res_model': 'voip.call',
            'view_mode': 'list',
            'domain': [('partner_id', '=', self.id)]            
        }