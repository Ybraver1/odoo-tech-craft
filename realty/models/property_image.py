from odoo import models,fields

class PropertyImage(models.Model):
    _name = "realty.property_image"
    
    property_id = fields.Many2one(comodel_name="realty.property")
    image = fields.Image()