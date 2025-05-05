from odoo import models,fields

class tasks(models.Model):
    _inherit = "project.task"
    
    ticket = fields.Many2one(comodel_name="helpdesk.ticket")