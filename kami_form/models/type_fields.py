from odoo import fields, models

class HelpdeskType(models.Model):

    _name = "helpdesk.ticket.type"
    _description = "Helpdesk Ticket Type"
    _inherit = "helpdesk.ticket.type"

    category_ids = fields.Many2many('helpdesk.ticket.category', string = 'Categorias')




