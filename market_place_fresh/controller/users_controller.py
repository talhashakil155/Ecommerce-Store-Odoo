from odoo import http
from odoo.http import request
import json

class UsersOperationController(http.Controller):

    @http.route('/users/groups/list', type='http', methods=['GET'], auth='user')
    def get_groups_list(self, **kw):
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        groups_list = request.env['res.groups'].search([])
        groups_response = []
        for group in groups_list:
            groups_response.append({
                'id': group.id,
                'name': group.name,
                'application_id': group.category_id.id,
                'application_name': group.category_id.name,
            })

        return request.make_response(json.dumps({'status': 'success', 'groups_response': groups_response}), headers=headers)

    @http.route('/users/list', type='http', methods=['GET'], auth='user')
    def get_users_list(self, **kw):
        users_list = request.env['res.users'].search([])
        users_response = []
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        for user in users_list:
            shops_list = request.env['market.place.shops'].search([('owner', '=', user.id)])
            u_resp = {
                'id': user.id,
                'name': user.name,
                'email': user.login,
                "email_verified_at": False,
                "created_at": str(user.create_date),
                "updated_at": str(user.write_date),
                "shop_id": [x.id for x in shops_list],
                "email_verified": False,
                "is_active": user.active,
                "photo": (f'/web/image/res.users/{user.id}/image_1920' if user.image_1920 else False),
                "profile": {
                    "id": False,
                    "avatar": (f'/web/image/res.partner/{user.partner_id.id}/image_1920' if user.partner_id.image_1920 else False),
                    "contact": user.partner_id.phone,
                    "customer_id": user.partner_id.id,
                    "created_at": str(user.partner_id.create_date),
                    "updated_at": str(user.partner_id.write_date),
                },
                "employee_details": {
                    "id": user.employee_id.id,
                    "name": user.employee_id.name,
                    "job_title": user.employee_id.job_title,
                    "department_id": (user.employee_id.department_id.id if user.employee_id.department_id else False),
                    "department_name": (user.employee_id.department_id.name if user.employee_id.department_id else False),
                    "job_position_id": (user.employee_id.job_id.id if user.employee_id.job_id else False),
                    "job_position_name": (user.employee_id.job_id.name if user.employee_id.job_id else False),
                } if user.employee_id else False,
                "address": [{
                    'id': x.id,
                    'type': x.type,
                    'default': 0,
                    'address': {
                        'zip': x.zip,
                        'city': x.city,
                        'state': (x.state_id.name if x.state_id else False),
                        'country': (x.country_id.name if x.country_id else False),
                        'street_address': x.street
                    }
                } for x in user.partner_id.child_ids],
                "groups_id": [{
                    'id': x.id,
                    'name': x.name,
                    'application_id': x.category_id.id,
                    'application_name': x.category_id.name
                } for x in user.groups_id]
            }
            u_resp['address'].append({
                'id': user.partner_id.id,
                'type': user.partner_id.type,
                'default': 0,
                'address': {
                    'zip': user.partner_id.zip,
                    'city': user.partner_id.city,
                    'state': (user.partner_id.state_id.name if user.partner_id.state_id else False),
                    'country': (user.partner_id.country_id.name if user.partner_id.country_id else False),
                    'street_address': user.partner_id.street
                }
            })
            users_response.append(u_resp)
        return request.make_response(json.dumps({'status': 'success', 'users_response': users_response}), headers=headers)

    @http.route('/users/<int:user_id>', type='http', methods=['GET'], auth='user')
    def get_users_byid(self, user_id=False, **kw):
        users_list = request.env['res.users'].browse(user_id)
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        if users_list:
            users_response = []
            for user in users_list:
                shops_list = request.env['market.place.shops'].search([('owner', '=', user.id)])
                u_resp = {
                    'id': user.id,
                    'name': user.name,
                    'email': user.login,
                    "email_verified_at": False,
                    "created_at": str(user.create_date),
                    "updated_at": str(user.write_date),
                    "shop_id": [x.id for x in shops_list],
                    "email_verified": False,
                    "is_active": user.active,
                    "photo": (f'/web/image/res.users/{user.id}/image_1920' if user.image_1920 else False),
                    "profile": {
                        "id": False,
                        "avatar": (
                            f'/web/image/res.partner/{user.partner_id.id}/image_1920' if user.partner_id.image_1920 else False),
                        "contact": user.partner_id.phone,
                        "customer_id": user.partner_id.id,
                        "created_at": str(user.partner_id.create_date),
                        "updated_at": str(user.partner_id.write_date),
                    },
                    "employee_details": {
                        "id": user.employee_id.id,
                        "name": user.employee_id.name,
                        "job_title": user.employee_id.job_title,
                        "department_id": (user.employee_id.department_id.id if user.employee_id.department_id else False),
                        "department_name": (user.employee_id.department_id.name if user.employee_id.department_id else False),
                        "job_position_id": (user.employee_id.job_id.id if user.employee_id.job_id else False),
                        "job_position_name": (user.employee_id.job_id.name if user.employee_id.job_id else False),
                    } if user.employee_id else False,
                    "address": [{
                        'id': x.id,
                        'type': x.type,
                        'default': 0,
                        'address': {
                            'zip': x.zip,
                            'city': x.city,
                            'state': (x.state_id.name if x.state_id else False),
                            'country': (x.country_id.name if x.country_id else False),
                            'street_address': x.street
                        }
                    } for x in user.partner_id.child_ids],
                    "groups_id": [{
                        'id': x.id,
                        'name': x.name,
                        'application_id': x.category_id.id,
                        'application_name': x.category_id.name
                    } for x in user.groups_id]
                }
                u_resp['address'].append({
                    'id': user.partner_id.id,
                    'type': user.partner_id.type,
                    'default': 0,
                    'address': {
                        'zip': user.partner_id.zip,
                        'city': user.partner_id.city,
                        'state': (user.partner_id.state_id.name if user.partner_id.state_id else False),
                        'country': (user.partner_id.country_id.name if user.partner_id.country_id else False),
                        'street_address': user.partner_id.street
                    }
                })
                users_response.append(u_resp)
            return request.make_response(json.dumps({'status': 'success', 'users_response': users_response}), headers=headers)
        else:
            return request.make_response(json.dumps({'status': 'error', 'users_response': "User Not Found"}), headers=headers)

    @http.route('/users/edit/<int:user_id>', type='json', methods=['POST'], auth='user', csrf=False)
    def edit_users(self, user_id=False, **kw):
        try:
            if user_id:
                user_deta = request.env['res.users'].browse(user_id)
                parameters = request.get_json_data()
                if user_deta:
                    if 'name' in parameters:
                        user_deta.write({'name': parameters['name']})
                    if 'email' in parameters:
                        user_deta.write({'login': parameters['email']})
                    if 'user_password' in parameters:
                        user_deta._change_password(parameters['user_password'])
                    if 'groups' in parameters:
                        for group_id in parameters['groups']:
                            request.env.cr.execute("select concat(module, '.', name) as template_name from ir_model_data where res_id='%s' and model='res.groups'", [group_id])
                            results = request.env.cr.fetchone()
                            if results:
                                if not user_deta.has_group(results[0]):
                                    user_deta.write({'groups_id': [(4, group_id)]})

                return {'status': 'success'}
            return {'status': 'error', 'message': "User not found"}
        except Exception as ex:
            return {'status': 'error', 'message': str(ex)}

    @http.route('/users/create', type='json', methods=['POST'], auth='user', csrf=False)
    def create_users(self, **kw):
        try:
            users_params = {}
            parameters = request.get_json_data()
            if 'name' in parameters:
                users_params.update({'name': parameters['name']})
            if 'email' in parameters:
                users_params.update({'login': parameters['email']})
            attach_groups = False
            department_id = False
            if 'department' in parameters:
                dept = request.env['hr.department'].search([('name', '=', parameters['department'])], limit=1)
                if dept:
                    department_id = dept.id
                    if dept.department_groups:
                        attach_groups = dept.department_groups
            created_user = request.env['res.users'].create(users_params)
            if created_user:
                if 'user_password' in parameters:
                    created_user._change_password(parameters['user_password'])
                if 'groups' in parameters:
                    for group_id in parameters['groups']:
                        request.env.cr.execute("select concat(module, '.', name) as template_name from ir_model_data where res_id='%s' and model='res.groups'", [group_id])
                        results = request.env.cr.fetchone()
                        if results:
                            if not created_user.has_group(results[0]):
                                created_user.write({'groups_id': [(4, group_id)]})
                if attach_groups:
                    for group_id in attach_groups:
                        request.env.cr.execute("select concat(module, '.', name) as template_name from ir_model_data where res_id='%s' and model='res.groups'", [group_id.id])
                        results = request.env.cr.fetchone()
                        if results:
                            if not created_user.has_group(results[0]):
                                created_user.write({'groups_id': [(4, group_id.id)]})

                self.createEmployee(created_user, department_id, parameters)

            return {'status': 'success', 'user_id': created_user.id}
        except Exception as ex:
            return {'status': 'error', 'message': str(ex)}

    @http.route('/users/delete/<int:user_id>', type='http', methods=['GET'], auth='user', csrf=False)
    def delete_shops(self, user_id=False, **kw):
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        if user_id:
            try:
                request.env['res.users'].sudo().browse(user_id).unlink()
                return request.make_response({'status': 'success'}, headers=headers)
            except Exception as ex:
                return request.make_response({'error': 'success', 'message': str(ex)}, headers=headers)
        else:
            return request.make_response(json.dumps({'error': 'success', 'message': 'User ID not found'}), headers=headers)

    def createEmployee(self, user_details, department_id, params):
        job_position = False
        if 'job_position' in params:
            hr_job = request.env['hr.job'].search([('name', '=', params['job_position'])], limit=1)
            if hr_job:
                job_position = hr_job.id
        request.env['hr.employee'].create({
            'name': user_details.name,
            'job_title': (params['job_title'] if 'job_title' in params else False),
            'mobile_phone': (params['mobile_phone'] if 'mobile_phone' in params else False),
            'work_phone': (params['work_phone'] if 'work_phone' in params else False),
            'work_email': user_details.login,
            'department_id': department_id,
            'job_id': job_position,
            'user_id': user_details.id
        })
