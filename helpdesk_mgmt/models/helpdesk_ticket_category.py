from odoo import fields, models


class HelpdeskCategory(models.Model):

    _name = "helpdesk.ticket.category"
    _description = "Helpdesk Ticket Category"

    active = fields.Boolean(
        string="Active",
        default=True,
    )
    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    default_team_id = fields.Many2one(
        comodel_name="helpdesk.ticket.team",
        string="Default team",
    )

    #type_ids = fields.Many2many('helpdesk.ticket.type', string = "Tipo")
