from odoo import fields,models,api

class PropertyShowing(models.Model):
    _name = "realty.property_showing"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    property_id = fields.Many2one("realty.property")
    client_id = fields.Many2one("res.partner")
    scheduled_showing = fields.Datetime()
    offer = fields.Float()
    stage_id = fields.Many2one("realty.property_showing_stage",tracking=True,group_expand ='_read_group_stage_ids')
    name= fields.Char(compute='_compute_name')
    
    def _compute_name(self):
        for rec in self:
            parts = []
            if rec.client_id:
                parts.append(rec.client_id.name)
            if rec.property_id:
                parts.append(rec.property_id.name)
            rec.name = ' - '.join(parts) if parts else 'Showing'
            
    @api.model
    def _read_group_stage_ids(self,stages,domain,order):
        stage_ids = stages.search([],order=order)
        return stages.browse(stage_ids)