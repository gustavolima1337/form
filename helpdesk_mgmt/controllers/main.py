import base64
import logging

import werkzeug

import odoo.http as http
from odoo.http import request

_logger = logging.getLogger(__name__)


class HelpdeskTicketController(http.Controller):
    @http.route("/ticket/close", type="http", auth="user")
    def support_ticket_close(self, **kw):
        """Close the support ticket"""
        values = {}
        for field_name, field_value in kw.items():
            if field_name.endswith("_id"):
                values[field_name] = int(field_value)
            else:
                values[field_name] = field_value
        ticket = (
            http.request.env["helpdesk.ticket"]
            .sudo()
            .search([("id", "=", values["ticket_id"])])
        )
        ticket.stage_id = values.get("stage_id")

        return werkzeug.utils.redirect("/my/ticket/" + str(ticket.id))

    @http.route("/new/ticket", type="http", auth="public", website=True)
    def create_new_ticket(self, **kw):
        categories = request.env["helpdesk.ticket.category"].sudo().search(
            [("active", "=", True)]
        )        
        email = request.env.user.email
        name = request.env.user.name
        return request.env['ir.ui.view']._render_template(
            "helpdesk_mgmt.portal_create_ticket",
            {"categories": categories, "email": email, "name": name},
        )

    @http.route("/submitted/ticket", type="http", auth="user", website=True, csrf=True)
    def submit_ticket(self, **kw):
        category = http.request.env["helpdesk.ticket.category"].browse(
            int(kw.get("category"))
        )
        vals = {
            "company_id": category.company_id.id or http.request.env.user.company_id.id,
            "category_id": category.id,
            "description": kw.get("description"),
            "name": kw.get("subject"),
            "attachment_ids": False,
            "channel_id": request.env["helpdesk.ticket.channel"]
            .sudo()
            .search([("name", "=", "Web")])
            .id,
            "partner_id": request.env.user.partner_id.id,
            "partner_name": request.env.user.partner_id.name,
            "partner_email": request.env.user.partner_id.email,
        }
        new_ticket = request.env["helpdesk.ticket"].sudo().create(vals)
        new_ticket.message_subscribe(partner_ids=request.env.user.partner_id.ids)
        if kw.get("attachment"):
            for c_file in request.httprequest.files.getlist("attachment"):
                data = c_file.read()
                if c_file.filename:
                    request.env["ir.attachment"].sudo().create(
                        {
                            "name": c_file.filename,
                            "datas": base64.b64encode(data),
                            "res_model": "helpdesk.ticket",
                            "res_id": new_ticket.id,
                        }
                    )
        return werkzeug.utils.redirect("/my/ticket/%s" % new_ticket.id)
