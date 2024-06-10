from odoo import http
from odoo.http import request

class ShopOperationController(http.Controller):

    @http.route('/shops/list', type='json', methods=['GET'], auth='user')
    def get_shops_list(self, **kw):
        shops_list = request.env['market.place.shops'].search([])
        shops_response = []
        for shop in shops_list:
            shops_response.append({
                'shop_id': shop.id,
                'name': shop.name,
                'owner_id': shop.owner.id,
                'slug': shop.slug,
                'description': shop.shop_description,
                'logo': f'/web/image/market.place.shops/{shop.id}/logo',
                'cover_image': f'/web/image/market.place.shops/{shop.id}/cover_image',
                'is_active': (1 if shop.status else 0),
                'address': {
                    "country": shop.country_id.name,
                    "city": shop.city,
                    "state": shop.state,
                    "zip": shop.zip,
                    "street_address": shop.street_address
                },
                'settings': {
                    'contact': shop.contact_no,
                    'email': shop.contact_email
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
                }
            })
        return shops_response

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
            if 'shop_description' in parameters:
                update_params.update({'shop_description': parameters['shop_description']})
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

            try:
                request.env['market.place.shops'].browse(shop_id).write(update_params)
                return {'status': 'success'}
            except Exception as ex:
                return {'status': 'error','message': str(ex)}
        else:
            return {'status': 'error', 'message': 'Shop ID not found'}

    @http.route('/shops/delete/<int:shop_id>', type='json', methods=['GET'], auth='user', csrf=False)
    def delete_shops(self, shop_id=False, **kw):
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        if shop_id:
            try:
                request.env['market.place.shops'].sudo().browse(shop_id).unlink()
                return {'status': 'success'}
            except Exception as ex:
                return {'status': 'error', 'message': str(ex)}
        else:
            return {'status': 'error', 'message': 'Shop ID not found'}

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
        if 'shop_description' in parameters:
            update_params.update({'shop_description': parameters['shop_description']})
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

        try:
            created_shop = request.env['market.place.shops'].create(update_params)
            return {'status': 'success', 'shop_id': str(created_shop.id)}
        except Exception as ex:
            return {'status': 'error', 'message': str(ex)}


    @http.route('/shops/<string:slug>', type='json', methods=['GET'], auth='user')
    def get_shops(self, slug, **kw):
        if slug:
            # shop = request.env['market.place.shops'].search([('slug', '=', slug)])
            # shop_response = {
            #     'shop_id': shop.id,
            #     'name': shop.name,
            #     'owner_id': shop.owner.id,
            #     'slug': shop.slug,
            #     'description': shop.shop_description,
            #     'logo': f'/web/image/market.place.shops/{shop.id}/logo',
            #     'cover_image': f'/web/image/market.place.shops/{shop.id}/cover_image',
            #     'is_active': (1 if shop.status else 0),
            #     'address': {
            #         "country": shop.country_id.name,
            #         "city": shop.city,
            #         "state": shop.state,
            #         "zip": shop.zip,
            #         "street_address": shop.street_address
            #     },
            #     'settings': {
            #         'contact': shop.contact_no,
            #         'email': shop.contact_email
            #     },
            #     'created_at': str(shop.create_date),
            #     'updated_at': str(shop.write_date),
            #     'orders_count': 0,
            #     'products_count': 0,
            #     'owner': {
            #         "id": shop.owner.id,
            #         "name": shop.owner.name,
            #         "email": shop.owner.name,
            #         "created_at": str(shop.owner.create_date),
            #         "updated_at": str(shop.owner.write_date),
            #         "is_active": 1,
            #         "shop_id": shop.id
            #     }
            # }
            return {'msg': 'slug present'}
        else:
            return {'status': 'error', 'message': 'Shop slug not found'}
