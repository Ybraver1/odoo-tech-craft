from odoo import models,fields

class PropertyStage(models.Model):
    _name = 'realty.property_stage'
    _order = 'sequence, id'
    
    name = fields.Char(string= "Stage Name", required=True)
    sequence = fields.Integer(default=1)
    fold= fields.Boolean('Folded in Kanban')
    