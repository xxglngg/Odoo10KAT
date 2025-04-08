from odoo import models, fields, api
from datetime import datetime

class WorkOrder(models.Model):
    _name = 'work.order'
    _description = 'Work Order'
    _rec_name = 'wo_number'

    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default='pending', string='State')
    wo_number = fields.Char('WO Number', readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('work.order') or '')
    booking_order_id = fields.Many2one('sale.order', string='Booking Order Reference', readonly=True)
    team_id = fields.Many2one('service.team', string='Team', required=True)
    team_leader = fields.Many2one('res.users', string='Team Leader', required=True)
    team_members = fields.Many2many('res.users', string='Team Members')
    planned_start = fields.Datetime('Planned Start', required=True)
    planned_end = fields.Datetime('Planned End', required=True)
    date_start = fields.Datetime('Date Start', readonly=True)
    date_end = fields.Datetime('Date End', readonly=True)
    notes = fields.Text('Notes')

    def action_start_work(self):
        self.state = 'in_progress'
        self.date_start = fields.Datetime.now()

    def action_end_work(self):
        self.state = 'done'
        self.date_end = fields.Datetime.now()

    def action_reset(self):
        self.state = 'pending'
        self.date_start = False

    def action_cancel(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reason Cancel Work Order',
            'view_mode': 'form',
            'res_model': 'wizard.cancel.work.order',
            'target': 'new',
            'context': {
                'default_work_order_id': self.id
            }
        }