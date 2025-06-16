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
    
    @api.model
    def create_time_sheet(self,task_id,time):
        
        task = self.sudo().browse(task_id)
        
        vals = {
            'name': f'Timesheet for task {task.name}',
            'project_id': task.project_id.id,
            'task_id': task.id,
            'employee_id': task.employee.id,
            'unit_amount': time,  # e.g. 2.5 = 2.5 hours
            'date': fields.Date.today(),
        }
        timesheet = self.env['account.analytic.line'].sudo().create(vals)
        return timesheet.id
  