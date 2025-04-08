from odoo import models, fields, api

class ServiceTeam(models.Model):
    _name = 'service.team'
    _description = 'Service Team'

    name = fields.Char('Team Name', required=True)
    team_leader = fields.Many2one('res.users', 'Team Leader', required=True)
    team_members = fields.Many2many('res.users', string='Team Members')
