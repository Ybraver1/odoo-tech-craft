from odoo import models, fields, api

class Tasks(models.Model):
    _inherit = "project.task"
    
    employee = fields.Many2one("hr.employee",string="Epmloyee Assignee")
    
    @api.model
    def get_tasks_by_employee(self,userId):
        user = self.env['res.users'].browse(userId)        
        partner =  user.self        
        employee = self.env['hr.employee'].sudo().search([           
            ('work_contact_id', '=', partner.id)
        ], limit=1)       
        tasks = self.sudo().search([('employee', '=', employee.id)]) 
        return tasks.read(['id','name','project_id']) or False
        
  