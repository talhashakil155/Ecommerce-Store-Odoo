from odoo import http
from odoo.http import request
import json

class ShopOperationController(http.Controller):

    @http.route('/shops/list', type='http', methods=['GET'], auth='user')
    def get_shops_list(self, **kw):
        shops_list = request.env['market.place.shops'].search([])
        shops_response = []
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        for shop in shops_list:
            shops_response.append({
                'id': shop.id,
                'name': shop.name,
                'owner_id': shop.owner.id,
                'slug': shop.slug,
                'description': shop.shop_description,
                "cover_image": {
                    "thumbnail": f'http://45.79.219.141:8070/web/image/market.place.shops/{shop.id}/cover_image',
                    "original": f'http://45.79.219.141:8070/web/image/market.place.shops/{shop.id}/cover_image',
                    "id": 1,
                    "file_name": "cover_image"
                },
                "logo": {
                    "thumbnail": f'http://45.79.219.141:8070/web/image/market.place.shops/{shop.id}/logo',
                    "original": f'http://45.79.219.141:8070/web/image/market.place.shops/{shop.id}/logo',
                    "id": 2,
                    "file_name": "logo"
                },
                'is_active': (1 if shop.status else 0),
                'address': {
                    "country": shop.country_id.name,
                    "city": shop.city,
                    "state": shop.state,
                    "zip": shop.zip,
                    "street_address": shop.street_address
                },
                'settings': {
                    "notifications": {
                        "email": "null"
                    },
                    'contact': shop.contact_no,
                    'email': shop.contact_email,
                    "location": [],
                    "socials": []
                },
                "notifications": "null",
                'created_at': str(shop.create_date),
                'updated_at': str(shop.write_date),
                'orders_count': 6,
                'products_count': 15,
                'owner': {
                    "id": shop.owner.id,
                    "name": shop.owner.name,
                    "email": shop.owner.login,
                    "email_verified_at": "null",
                    "created_at": str(shop.owner.create_date),
                    "updated_at": str(shop.owner.write_date),
                    "is_active": 1,
                    "shop_id": shop.id,
                    "email_verified": "false",
                    "profile": {
                        "id": shop.owner.id,
                        "avatar": {
                            "id": "883",
                            "original": "",
                            "thumbnail": ""
                        },
                        "bio": "This is the store owner and we have 6 shops under our banner. We are running all the shops to give our customers hassle-free service and quality products. Our goal is to provide best possible customer service and products for our clients",
                        "socials": "null",
                        "contact": shop.owner.phone,
                        "notifications": "null",
                        "customer_id": 1,
                        "created_at": str(shop.owner.create_date),
                        "updated_at": str(shop.owner.write_date)
                    }
                },
                'account_info': {
                    'account': shop.payment_account,
                    'name': shop.payment_account_name,
                    'email': '',
                    'bank': shop.payment_account_bank
                },
                'balance': {
                    "id": 342,
                    "admin_commission_rate": 10,
                    "shop": "null",
                    "total_earnings": 3450,
                    "withdrawn_amount": 650,
                    "current_balance": 2800,
                    "payment_info": {
                        'account': shop.payment_account,
                        'name': shop.payment_account_name,
                        'email': shop.payment_account_email,
                        'bank': shop.payment_account_bank
                    }
                }
            })
        return request.make_response(json.dumps({'status': 'success', 'shops_response': shops_response}), headers=headers)

    @http.route('/shops/edit/<int:shop_id>', type='json', methods=['POST'], auth='user', csrf=False)
    def edit_shops(self, shop_id=False, **kw):
        if shop_id:
            update_params = {}
            parameters = request.get_json_data()
            if 'name' in parameters:
                update_params.update({'name': parameters['name']})
            if 'slug' in parameters:
                update_params.update({'slug': parameters['slug']})
            if 'owner' in parameters:
                update_params.update({'owner': int(parameters['owner'])})
            if 'shop_description' in parameters:
                update_params.update({'shop_description': parameters['shop_description']})
            if 'cover_image' in parameters:
                update_params.update({'cover_image': parameters['cover_image']})
            if 'logo' in parameters:
                update_params.update({'logo': parameters['logo']})
            if 'email' in parameters:
                update_params.update({'contact_email': parameters['email']})
            if 'contact' in parameters:
                update_params.update({'contact_no': parameters['contact']})
            if 'country' in parameters:
                country_search = request.env['res.country'].search([('name','=',parameters['country'])], limit=1)
                if country_search:
                    update_params.update({'country_id': country_search.id})
            if 'city' in parameters:
                update_params.update({'city': parameters['city']})
            if 'state' in parameters:
                update_params.update({'state': parameters['state']})
            if 'zip' in parameters:
                update_params.update({'zip': parameters['zip']})
            if 'street_address' in parameters:
                update_params.update({'street_address': parameters['street_address']})
            if 'warehouse_id' in parameters:
                update_params.update({'warehouse_id': int(parameters['warehouse_id'])})
            if 'account' in parameters:
                update_params.update({'payment_account': (parameters['account'])})
            if 'account_name' in parameters:
                update_params.update({'payment_account_name': (parameters['account_name'])})
            if 'account_email' in parameters:
                update_params.update({'payment_account_email': (parameters['account_email'])})
            if 'account_bank' in parameters:
                update_params.update({'payment_account_bank': (parameters['account_bank'])})

            try:
                request.env['market.place.shops'].browse(shop_id).write(update_params)
                return {'status': 'success'}
            except Exception as ex:
                return {'status': 'error','message': str(ex)}
        else:
            return {'status': 'error', 'message': 'Shop ID not found'}

    @http.route('/shops/delete/<int:shop_id>', type='http', methods=['GET'], auth='user', csrf=False)
    def delete_shops(self, shop_id=False, **kw):
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        if shop_id:
            try:
                request.env['market.place.shops'].sudo().browse(shop_id).unlink()
                return request.make_response({'status': 'success'}, headers=headers)
            except Exception as ex:
                return request.make_response({'error': 'success', 'message': str(ex)}, headers=headers)
        else:
            return request.make_response(json.dumps({'error': 'success', 'message': 'Shop ID not found'}), headers=headers)

    @http.route('/shops/create', type='json', methods=['POST'], auth='user', csrf=False)
    def create_shop(self, **kw):
        update_params = {}
        parameters = request.get_json_data()
        if 'name' in parameters:
            update_params.update({'name': parameters['name']})
        if 'owner' in parameters:
            update_params.update({'owner': int(parameters['owner'])})
        if 'slug' in parameters:
            update_params.update({'slug': parameters['slug']})
        if 'shop_description' in parameters:
            update_params.update({'shop_description': parameters['shop_description']})
        if 'status' in parameters:
            update_params.update({'status': (parameters['status'])})
        if 'cover_image' in parameters:
            update_params.update({'cover_image': parameters['cover_image']})
        if 'logo' in parameters:
            update_params.update({'logo': parameters['logo']})
        if 'email' in parameters:
            update_params.update({'contact_email': parameters['email']})
        if 'contact' in parameters:
            update_params.update({'contact_no': ['contact']})
        if 'country' in parameters:
            country_search = request.env['res.country'].search([('name', '=', parameters['country'])], limit=1)
            if country_search:
                update_params.update({'country_id': country_search.id})
        if 'city' in parameters:
            update_params.update({'city': parameters['city']})
        if 'state' in parameters:
            update_params.update({'state': parameters['state']})
        if 'zip' in parameters:
            update_params.update({'zip': parameters['zip']})
        if 'street_address' in parameters:
            update_params.update({'street_address': parameters['street_address']})
        if 'warehouse_id' in parameters:
            update_params.update({'warehouse_id': int(parameters['warehouse_id'])})
        if 'account' in parameters:
            update_params.update({'payment_account': (parameters['account'])})
        if 'account_name' in parameters:
            update_params.update({'payment_account_name': (parameters['account_name'])})
        if 'account_email' in parameters:
            update_params.update({'payment_account_email': (parameters['account_email'])})
        if 'account_bank' in parameters:
            update_params.update({'payment_account_bank': (parameters['account_bank'])})

        try:
            created_shop = request.env['market.place.shops'].create(update_params)
            return {'status': 'success', 'shop_id': str(created_shop.id)}
        except Exception as ex:
            return {'status': 'error', 'message': str(ex)}

    @http.route('/shops/<string:slug>', type='http', methods=['GET'], auth='user')
    def get_shops(self, slug, **kw):
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        if slug:
            shop = request.env['market.place.shops'].search([('slug', '=', slug)])
            if shop:
                shop_response = {
                    'id': shop.id,
                    'name': shop.name,
                    'owner_id': shop.owner.id,
                    'slug': shop.slug,
                    'description': shop.shop_description,
                    "cover_image": {
                        "thumbnail": f'http://45.79.219.141:8070/web/image/market.place.shops/{shop.id}/cover_image',
                        "original": f'http://45.79.219.141:8070/web/image/market.place.shops/{shop.id}/cover_image',
                        "id": 1,
                        "file_name": "cover_image"
                    },
                    "logo": {
                        "thumbnail": f'http://45.79.219.141:8070/web/image/market.place.shops/{shop.id}/logo',
                        "original": f'http://45.79.219.141:8070/web/image/market.place.shops/{shop.id}/logo',
                        "id": 2,
                        "file_name": "logo"
                    },
                    'is_active': (1 if shop.status else 0),
                    'address': {
                        "country": shop.country_id.name,
                        "city": shop.city,
                        "state": shop.state,
                        "zip": shop.zip,
                        "street_address": shop.street_address
                    },
                    'settings': {
                        "notifications": {
                            "email": "null"
                        },
                        'contact': shop.contact_no,
                        'email': shop.contact_email,
                        "location": [],
                        "socials": []
                    },
                    'created_at': str(shop.create_date),
                    'updated_at': str(shop.write_date),
                    'orders_count': 0,
                    'products_count': 0,
                    'owner': {
                        "id": shop.owner.id,
                        "name": shop.owner.name,
                        "email": shop.owner.name,
                        "created_at": str(shop.owner.create_date),
                        "updated_at": str(shop.owner.write_date),
                        "is_active": 1,
                        "shop_id": shop.id
                    },
                    'account_info': {
                        'account': shop.payment_account,
                        'name': shop.payment_account_name,
                        'email': '',
                        'bank': shop.payment_account_bank
                    }
                }
                return request.make_response(json.dumps({'status': 'success', 'shop_response':shop_response}), headers=headers)
            else:
                return request.make_response(json.dumps({'status': 'success', 'shop_response': 'Shop not found'}), headers=headers)
        else:
            return request.make_response(json.dumps({'status': 'success', 'shop_response': 'Slug not found'}), headers=headers)



