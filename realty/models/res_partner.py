from odoo import models,fields

class Partner(models.Model):
    _inherit = 'res.partner'
    
    property_ids = fields.One2many('realty.property','owner_id')
    property_showing_ids = fields.One2many('realty.property_showing','client_id')