from odoo import models,fields

class PropertyShowingStage(models.Model):
    _name = 'realty.property_showing_stage'
    _order = 'sequence, id'
    
    name = fields.Char(string= "Stage Name", required=True)
    sequence = fields.Integer(default=1)
    fold= fields.Boolean('Folded in Kanban')
    