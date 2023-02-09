# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo import models, fields, api

# class MalaTecnica(http.Controller):
#   @http.route('/campanhasmkt', auth='public')
#   def index(self, **kw): 
#       users = http.request.env['res.users']
#       return http.request.render('kami_forms.maladireta', {
#           'users': users.search([])
#       })

#   @http.route('/set', auth='public', type="http", website=True)
#   def create(self, **post):
    
#     new_task = {
#       'name': f"{post['solicitacao']}-{post['departament']}",
#       'project_id': self.env.ref('kami_forms.tecnical_mala_project').id,
#       'user_id': post['responsavel']['value'],
#       'description': f"""teste"""

#     }
#     http.request.env["project.task"].sudo().create(new_task)
#     return http.request.render('kami_forms.success_page', {})

class CampanhasMarketing(http.Controller):
    @http.route('/campanhasmkt', type='http', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('kami_forms.campanhamkt', {})

    @http.route('/campanhasmkt', type='http', auth='public', website=True, methods=['POST'])
    def criar_projeto(self, **post):
        # Get the user who is responsible for the project
        users = http.request.env['res.users'].search([("name", "=", "Marc Demo")])

        # Get the values from the form to create a new project
        project_vals = {
            'project_id': self.env.ref('kami_forms.tecnical_mala_project').id,
            'name': f"{post['campaign_name']}",
            'user_id': users,
            'date_deadline': f"{post['data_vencimento']}",
            'description': f"{post['message']}"
        }

        # Create a new project in Odoo
        new_project = request.env['project.project'].sudo().create(project_vals)

        # Redirect the user to the newly created project
        return request.redirect('/projects/%s' % new_project.id)


