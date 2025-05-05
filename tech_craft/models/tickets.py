from odoo import models,fields,api

class ticket(models.Model):
    _inherit = "helpdesk.ticket"
    
    project = fields.Many2one(comodel_name = "project.project")
    tasks = fields.One2many(comodel_name="project.task",inverse_name="ticket")
    