# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Tasks(models.Model):
    _inherit = "project.task"
    
    employee = fields.Many2one("hr.employee",string="Epmloyee Assignee")
  