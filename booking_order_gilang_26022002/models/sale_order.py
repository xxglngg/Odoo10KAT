from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking_order = fields.Boolean(string="Is Booking Order", default=True)
    team = fields.Many2one('service.team', string="Team")
    team_leader = fields.Many2one('res.users', string="Team Leader")
    team_members = fields.Many2many('res.users', string="Team Members")
    booking_start = fields.Datetime(string="Booking Start")
    booking_end = fields.Datetime(string="Booking End")
    work_order_ids = fields.Many2many('work.order', string="Work Order")
    work_order_count = fields.Integer(compute="_compute_work_order_count", string='Work Order Count')

    def action_work_order_view(self):
        return {
            'name': 'Work Order',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'work.order',
            'domain': [('booking_order_id', '=', self.id)],
        }

    def _compute_work_order_count(self):
        work_orders = self.env['work.order']
        for record in self:
            record.work_order_count = work_orders.search_count([('booking_order_id', '=', record.id)])

    @api.onchange('team')
    def _onchange_team(self):
        if self.team:
            self.team_leader = self.team.team_leader
            self.team_members = self.team.team_members
    
    def check_team_availability(self):
        for order in self:
            work_orders = self.env['work.order'].search([
                ('team_id', '=', order.team.id),
                ('state', 'not in', ['cancelled']),
                ('planned_start', '<=', order.booking_end),
                ('planned_end', '>=', order.booking_start)
            ])
            if work_orders:
                raise UserError('Team already has work order during that period on SO %s' % (work_orders.booking_order_id.name))
            else:
                raise UserError("Team is available for booking")
    
    @api.model
    def action_confirm(self):
        for order in self:
            work_orders = self.env['work.order'].search([
                ('team_id', '=', order.team.id),
                ('state', 'not in', ['cancelled']),
                ('planned_start', '<=', order.booking_end),
                ('planned_end', '>=', order.booking_start)
            ])
            if work_orders:
                raise UserError('Team already has work order during that period on SO %s. Please book on another date.' % (work_orders.booking_order_id.name))
            else:
                work_order = self.env['work.order'].create({
                    'booking_order_id': order.id,
                    'team_id': order.team.id,
                    'team_leader': order.team_leader.id,
                    'team_members': [(6, 0, order.team_members.ids)],
                    'planned_start': order.booking_start,
                    'planned_end': order.booking_end,
                    'state': 'pending',
                })

                order.write({'work_order_ids': [(4, work_order.id)]})

            return super(SaleOrder, self).action_confirm()