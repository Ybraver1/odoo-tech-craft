from odoo import models, fields

class Project(models.Model):
    _inherit = "project.project"
    
    tickets = fields.One2many(comodel_name="helpdesk.ticket",inverse_name="project")