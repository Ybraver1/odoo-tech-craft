from odoo import fields,models

class PropertyShowing(models.Model):
    _name = "realty.property_showing"
    
    property_id = fields.Many2one("realty.propery")
    client_id = fields.Many2one("res.partner")
    scheduled_showing = fields.Datetime()
    offer = fields.Float()
    stage_id = fields.Many2one("realty.property_showing_stage")