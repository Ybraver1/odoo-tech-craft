from odoo import models,fields

class Partner(models.Model):
    _inherit = 'res.partner'
    
    property_ids = fields.One2many('realty.property','owner_id')
    property_showing_ids = fields.One2many('realty.property_showing','client_id')
    property_count = fields.Integer(compute='_compute_property_count')
    showing_count = fields.Integer(compute='_compute_showing_count')
    
    
    def _compute_property_count(self):
        for rec in self:
            rec.property_count = self.env['realty.property'].search_count([('owner_id','=',rec.id)])
            
    def _compute_showing_count(self):
        for rec in self:
            rec.showing_count = self.env['realty.property_showing'].search_count([('client_id','=',rec.id)])
            
    def action_view_showings(self):
        self.ensure_one()
        return {            
            'name': 'Showings',
            'type': 'ir.actions.act_window',
            'res_model': 'realty.property_showing',
            'view_mode': 'calendar,kanban,list,form',
            'domain': [('client_id', '=', self.id)],
            'context': {'default_client_id': self.id},
        }
        
    def action_view_properties(self):
        self.ensure_one()
        return {            
            'name': 'Properties',
            'type': 'ir.actions.act_window',
            'res_model': 'realty.property',
            'view_mode': 'kanban,list,form',
            'domain': [('owner_id', '=', self.id)],
            'context': {'default_owner_id': self.id},
        }