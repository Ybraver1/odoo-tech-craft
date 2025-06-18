from odoo import fields,models

class PropertyShowing(models.Model):
    _name = "realty.property_showing"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    property_id = fields.Many2one("realty.property")
    client_id = fields.Many2one("res.partner")
    scheduled_showing = fields.Datetime()
    offer = fields.Float()
    stage_id = fields.Many2one("realty.property_showing_stage",tracking=True)