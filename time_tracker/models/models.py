from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class Tasks(models.Model):
    _inherit = "project.task"
    
    employee = fields.Many2one("hr.employee",string="Epmloyee Assignee")
    
    @api.model
    def get_tasks_by_employee(self,userId):
        user = self.env['res.users'].browse(userId)
        _logger.info("User-----------%s",user)
        partner =  self.env['res.partner'].browse(user.self)
        _logger.info("Partner-----------%s",partner)
        employee = self.env['hr.employee'].browse(partner.employee_ids[0])
        _logger.info("employee-----------%s",employee)
        
        return employee or False
        
  