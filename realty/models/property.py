from odoo import models,fields,api

class Property(models.Model):
    _name = "realty.property"
    _description = "realty.property"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    
    name = fields.Char(string="Property Name")
    type = fields.Selection(string="Property Type",selection=[("sale","For Sale"),("rent","For Rent")])
    owner_id = fields.Many2one(string="Property Owner",comodel_name="res.partner")
    price = fields.Float(string="Price")
    description = fields.Html(string="Property Description")
    image_ids = fields.One2many(comodel_name="realty.property_image",inverse_name="property_id")
    stage_id= fields.Many2one("realty.property_stage",tracking=True,group_expand ='_read_group_stage_ids')
    showing_count = fields.Integer(string="Showing Count",compute='_compute_showing_count')
    
    def _compute_showing_count(self):
        for rec in self:
            rec.showing_count = self.env["realty.property_showing"].search_count([('property_id','=',rec.id)])
            
    def action_view_showings(self):
        self.ensure_one()
        return {            
            'name': 'Showings',
            'type': 'ir.actions.act_window',
            'res_model': 'realty.property_showing',
            'view_mode': 'calendar,kanban,list,form',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
        }
        
    @api.model
    def _read_group_stage_ids(self,stages,domain):
        stage_ids = stages.search([],order=order)
        return stages.browse(stage_ids)