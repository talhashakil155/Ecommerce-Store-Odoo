from odoo import http
from odoo.http import request
import json

class UserAuthenticateController(http.Controller):

    @http.route('/user/authenticate/login', type='json', methods=['POST'], auth='public', csrf=False)
    def userAuthenticateLogin(self, **kw):
        parameters = request.get_json_data()
        if 'username' in parameters and 'password' in parameters:
            try:
                uid = request.session.authenticate(request.session.db, parameters['username'], parameters['password'])
                return {'status': 'success'}
            except Exception as ex:
                return {'status': 'error', 'message': str(ex)}
        else:
            return {'status': 'error', 'message': 'Please provide login credentials'}

    @http.route('/user/authenticate/logout', type='http', methods=['GET'], auth='user')
    def userAuthenticateLogout(self, **kw):
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        request.session.logout()
        return request.make_response(json.dumps({'status': 'success'}), headers=headers)
