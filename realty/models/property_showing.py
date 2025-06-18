from odoo import fields,models

class PropertyShowing(models.Model):
    _name = "realty.property_showing"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    property_id = fields.Many2one("realty.property")
    client_id = fields.Many2one("res.partner")
    scheduled_showing = fields.Datetime()
    offer = fields.Float()
    stage_id = fields.Many2one("realty.property_showing_stage",tracking=True)
    name= fields.Char(compute='_compute_name')
    
    def _compute_name(self):
        for rec in self:
            rec.name = rec.client_id.name if rec.client_id else 'Showing'