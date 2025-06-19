from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class Tasks(models.Model):
    _inherit = "project.task"
    
    employee = fields.Many2one("hr.employee",string="Epmloyee Assignee")
    
    def create(self, vals):
        task = super().create(vals)
        task.remove_non_user_follower()
        task._subscribe_employee_follower()
        return task

    def write(self, vals):
        res = super().write(vals)
        self._subscribe_employee_follower()
        return res  
    
    def remove_non_user_follower(self):
        creator_partner_id = self.env.user.partner_id.id
        for task in self:
            to_unfollow = []
            for follower in task.message_follower_ids:
                partner = follower.partner_id
                # ✅ Never remove the creator's partner!
                if partner.id == creator_partner_id:
                    continue

                users = partner.user_ids
                # If no linked users → not internal → remove
                if not users:
                    to_unfollow.append(partner.id)
                    continue

                # If none are internal → remove
                if not any(user.has_group('base.group_user') for user in users):
                    to_unfollow.append(partner.id)

        if to_unfollow:
            task.message_unsubscribe(partner_ids=to_unfollow)
              
    
    def _subscribe_employee_follower(self):
        for task in self:
            employee = task.sudo().employee
            if not employee or not employee.work_contact_id:
                continue            
            partner_id = employee.work_contact_id.id
            if partner_id not in task.sudo().message_follower_ids.mapped('partner_id').ids:
                task.sudo().message_subscribe(partner_ids=[partner_id])
                task.sudo().message_post(
                    body="You have been assigned as the employee for this task.",
                    subtype_xmlid="mail.mt_comment",
                    partner_ids=[partner_id]
                )
    
    @api.model
    def get_tasks_by_employee(self,user_id):
        employee_id = self.get_employee_from_user(user_id)      
        tasks = self.sudo().search([('employee', '=',employee_id )]) 
        return tasks.read(['id','name','project_id']) or False
    
    @api.model
    def create_time_sheet(self,user_id,task_id,time):
        _logger.debug("_______________---------------------",user_id,task_id,time)
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
            vals["so_line"] = so_line.id
        timesheet = self.env['account.analytic.line'].sudo().create(vals)
        return timesheet.id
    
    def get_employee_from_user(self,user_id):
        user = self.env['res.users'].browse(user_id)        
        partner =  user.self        
        employee = self.env['hr.employee'].sudo().search([           
            ('work_contact_id', '=', partner.id)
        ], limit=1) 
        return employee.id
  