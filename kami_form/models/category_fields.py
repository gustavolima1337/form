from odoo import fields, models

class HelpdeskCategory(models.Model):

    _name = "helpdesk.ticket.category"
    _description = "Helpdesk Ticket Category"
    _inherit = "helpdesk.ticket.category"

    type_ids = fields.Many2many('helpdesk.ticket.type', string = 'Tipos')