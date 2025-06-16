from odoo import models, fields, api

class Tasks(models.Model):
    _inherit = "project.task"
    
    employee = fields.Many2one("hr.employee",string="Epmloyee Assignee")
    
    @api.model
    def get_tasks_by_employee(self,user_id):
        employee_id = self.get_employee_from_user(user_id)      
        tasks = self.sudo().search([('employee', '=',employee_id )]) 
        return tasks.read(['id','name','project_id']) or False
    
    @api.model
    def create_time_sheet(self,user_id,task_id,time):
        
        task = self.sudo().browse(task_id)
        so_line = task.sale_line_id
        employee_id = self.get_employee_from_user(user_id)
        vals = {
            'name': f'Timesheet for task {task.name}',
            'project_id': task.project_id.id,
            'task_id': task.id,
            'employee_id': employee_id,
            'unit_amount': time,  # e.g. 2.5 = 2.5 hours
            'date': fields.Date.today(),
        }
        if so_line:
            vals["so_line"] = so_line
        timesheet = self.env['account.analytic.line'].sudo().create(vals)
        return timesheet.id
    
    def get_employee_from_user(self,user_id):
        user = self.env['res.users'].browse(user_id)        
        partner =  user.self        
        employee = self.env['hr.employee'].sudo().search([           
            ('work_contact_id', '=', partner.id)
        ], limit=1) 
        return employee.id
  