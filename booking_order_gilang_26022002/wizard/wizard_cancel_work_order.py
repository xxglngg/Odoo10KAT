from odoo import models, fields, api

class WizardCancelWorkOrder(models.TransientModel):
    _name = 'wizard.cancel.work.order'
    _description = 'Wizard Cancel Work Order'

    reason = fields.Text(string="Reason", required=True)
    work_order_id = fields.Many2one('work.order', string="Work Order", readonly=True)

    def confirm_cancel_work_order(self):
        self.work_order_id.state = 'cancelled'
        self.work_order_id.notes = self.reason