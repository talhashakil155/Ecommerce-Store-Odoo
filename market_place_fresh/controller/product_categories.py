from odoo import http
from odoo.http import request
import json


class ProductCategoriesController(http.Controller):

    @http.route('/categories/list', type='http', methods=['GET'], auth='user')
    def get_categories_list(self, **kw):
        parameters = request.httprequest.args
        domain = []
        if 'cat_slug' in parameters:
            domain = [('cat_slug', '=', parameters['cat_slug'])]
        categories = request.env['product.category'].search(domain)
        cat_response = []
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        for cat in categories:
            childrens = request.env['product.category'].search([('parent_id', '=', cat.id)])
            cat_response.append({
                'id': cat.id,
                'name': cat.name,
                'display_name': cat.display_name,
                'slug': cat.cat_slug,
                'icon': cat.cat_icon,
                'image': f'/web/image/product.category/{cat.id}/cat_image' if cat.id else False,
                'details': cat.cat_details,
                'type_id': cat.shop_id.id,
                'created_at': str(cat.create_date),
                'updated_at': str(cat.write_date),
                'parent_id': (cat.parent_id.id if cat.parent_id else False),
                'product_count': cat.product_count,
                'type': {
                    'id': cat.shop_id.id,
                    'slug': cat.shop_id.slug,
                    "created_at": str(cat.shop_id.create_date),
                    "updated_at": str(cat.shop_id.write_date),
                    'logo': f'/web/image/market.place.shops/{cat.shop_id.id}/logo' if cat.shop_id else False,
                } if cat.shop_id else False,
                'children': [{
                    'id': x.id,
                    'name': x.name,
                    'display_name': x.display_name,
                    'slug': x.cat_slug,
                    'icon': x.cat_icon,
                    'image': f'/web/image/product.category/{x.id}/cat_image' if x.id else False,
                    'details': x.cat_details,
                    'type_id': x.shop_id.id,
                    'created_at': str(x.create_date),
                    'updated_at': str(x.write_date),
                    'parent_id': (x.parent_id.id if x.parent_id else False),
                    'product_count': x.product_count
                } for x in childrens]
            })
        return request.make_response(json.dumps({'status': 'success', 'cat_response': cat_response}), headers=headers)

    @http.route('/categories/<string:slug>', type='http', methods=['GET'], auth='user')
    def get_category(self, slug, **kw):
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        if slug:
            category = request.env['product.category'].search([('cat_slug', '=', slug)])
            if category:
                childrens = request.env['product.category'].search([('parent_id', '=', category.id)])
                cat_response = {
                    'id': category.id,
                    'name': category.name,
                    'display_name': category.display_name,
                    'slug': category.cat_slug,
                    'icon': category.cat_icon,
                    'image': f'/web/image/product.category/{category.id}/cat_image' if category.id else False,
                    'details': category.cat_details,
                    'type_id': category.shop_id.id,
                    'created_at': str(category.create_date),
                    'updated_at': str(category.write_date),
                    'parent_id': (category.parent_id.id if category.parent_id else False),
                    'product_count': category.product_count,
                    'type': {
                        'id': category.shop_id.id,
                        'slug': category.shop_id.slug,
                        "created_at": str(category.shop_id.create_date),
                        "updated_at": str(category.shop_id.write_date),
                        'logo': f'/web/image/market.place.shops/{category.shop_id.id}/logo' if category.shop_id else False,
                    } if category.shop_id else False,
                    'children': [{
                        'id': x.id,
                        'name': x.name,
                        'display_name': x.display_name,
                        'slug': x.cat_slug,
                        'icon': x.cat_icon,
                        'image': f'/web/image/product.category/{x.id}/cat_image' if x.id else False,
                        'details': x.cat_details,
                        'type_id': x.shop_id.id,
                        'created_at': str(x.create_date),
                        'updated_at': str(x.write_date),
                        'parent_id': (x.parent_id.id if x.parent_id else False),
                        'product_count': x.product_count
                    } for x in childrens]
                }
                return request.make_response(json.dumps({'status': 'success', 'cat_response': cat_response}), headers=headers)
            else:
                return request.make_response(json.dumps({'status': 'success', 'cat_response': 'Category not found'}), headers=headers)
        else:
            return request.make_response(json.dumps({'status': 'success', 'cat_response': 'Slug not found'}), headers=headers)

    @http.route('/categories/<int:cat_id>', type='http', methods=['GET'], auth='user', csrf=False)
    def delete_category(self, cat_id=False, **kw):
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        if cat_id:
            try:
                request.env['product.category'].sudo().browse(cat_id).unlink()
                return request.make_response({'status': 'success'}, headers=headers)
            except Exception as ex:
                return request.make_response({'error': 'success', 'message': str(ex)}, headers=headers)
        else:
            return request.make_response(json.dumps({'error': 'success', 'message': 'Category ID not found'}), headers=headers)

    @http.route('/categories/create', type='json', methods=['POST'], auth='user', csrf=False)
    def create_category(self, **kw):
        update_params = {}
        parameters = request.get_json_data()
        if 'name' in parameters:
            update_params.update({'name': parameters['name']})
        if 'slug' in parameters:
            update_params.update({'cat_slug': parameters['slug']})
        if 'icon' in parameters:
            update_params.update({'cat_icon': parameters['icon']})
        if 'details' in parameters:
            update_params.update({'cat_details': parameters['details']})
        if 'details' in parameters:
            update_params.update({'cat_details': parameters['details']})
        if 'type_id' in parameters:
            update_params.update({'shop_id': parameters['type_id']})
        if 'parent_id' in parameters:
            update_params.update({'parent_id': parameters['parent_id']})

        try:
            created_shop = request.env['product.category'].create(update_params)
            return {'status': 'success', 'category_id': str(created_shop.id)}
        except Exception as ex:
            return {'status': 'error', 'message': str(ex)}

    @http.route('/categories/edit/<int:cat_id>', type='json', methods=['POST'], auth='user', csrf=False)
    def update_category(self, cat_id=False, **kw):
        update_params = {}
        if cat_id:
            parameters = request.get_json_data()
            if 'name' in parameters:
                update_params.update({'name': parameters['name']})
            if 'slug' in parameters:
                update_params.update({'cat_slug': parameters['slug']})
            if 'icon' in parameters:
                update_params.update({'cat_icon': parameters['icon']})
            if 'details' in parameters:
                update_params.update({'cat_details': parameters['details']})
            if 'details' in parameters:
                update_params.update({'cat_details': parameters['details']})
            if 'type_id' in parameters:
                update_params.update({'shop_id': parameters['type_id']})
            if 'type_id' in parameters:
                update_params.update({'shop_id': parameters['type_id']})
            if 'parent_id' in parameters:
                update_params.update({'parent_id': parameters['parent_id']})

        try:
            request.env['product.category'].browse(cat_id).write(update_params)
            return {'status': 'success'}
        except Exception as ex:
            return {'status': 'error','message': str(ex)}
