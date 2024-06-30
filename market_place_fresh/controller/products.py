from odoo import http
from odoo.http import request
import json

class ShopProductsController(http.Controller):

    @http.route('/shop/products/list', type='http', methods=['GET'], auth='user')
    def get_products_list(self, **kw):
        parameters = request.httprequest.args
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        if 'shop_id' in parameters:
            search_domain = []
            if parameters['shop_id'] != 'all':
                search_domain = [('shop_id', 'in', int(parameters['shop_id']))]
            product_list = request.env['product.product'].search(search_domain)
            product_response = []
            for product in product_list:
                product_response.append({
                    'id': product.id,
                    'name': product.name,
                    'slug': product.product_slug,
                    'product_image': f'/web/image/product.product/{product.id}/image_1920',
                    'description': product.description,
                    'type': product.detailed_type,
                    'sale_price': product.list_price,
                    'price': product.standard_price,
                    'min_price': product.minimum_price,
                    'max_price': product.maximum_price,
                    'sku': product.default_code,
                    'quantity': product.qty_available,
                    'forecast_quantity': product.virtual_available,
                    "status": "publish",
                    "created_at": str(product.create_date),
                    "updated_at": str(product.write_date),
                    "is_taxable": (1 if product.taxes_id else 0),
                    "currency": product.currency_id.name,
                    "tax_details": [{
                        'tax_id': x.id,
                        'name': x.name,
                        'price_include': x.price_include,
                        'tax_amount': x.amount,
                        'tax_amount_type': x.amount_type
                    } for x in product.taxes_id],
                    "vendor_ids": [{
                        'id': x.partner_id.id,
                        'name': x.partner_id.name,
                        'price': x.price,
                        'delivery_time': x.delay,
                        'discount': x.discount
                    } for x in product.seller_ids],
                    "categories": {
                        "id": product.categ_id.id,
                        "name": product.categ_id.name,
                        "created_at": str(product.categ_id.create_date),
                        "updated_at": str(product.categ_id.write_date),
                    },
                    "shops": [{
                        "id": product.shop_id.id,
                        "name": product.shop_id.name,
                        "slug": product.shop_id.slug,
                        "created_at": str(product.shop_id.create_date),
                        "updated_at": str(product.shop_id.write_date),
                        "owner_id": product.shop_id.owner.id,
                        "owner_name": product.shop_id.owner.name,
                        "description": product.shop_id.shop_description
                    } for x in product.shop_id],
                    'unit_of_measure': {
                        'id': product.uom_id.id,
                        'name': product.uom_id.name,
                        'uom_type': product.uom_id.uom_type,
                        'ratio': product.uom_id.ratio,
                        'rounding': product.uom_id.rounding
                    } if product.uom_id else False
                })
            return request.make_response(json.dumps({'status': 'success', 'product_response': product_response}), headers=headers)

    @http.route('/shop/product/edit/<int:product_id>', type='json', methods=['POST'], auth='user', csrf=False)
    def edit_product(self, product_id=False, **kw):
        if product_id:
            update_params = {}
            parameters = request.get_json_data()
            if 'name' in parameters:
                update_params.update({'name': parameters['name']})
            if 'slug' in parameters:
                update_params.update({'product_slug': parameters['slug']})
            if 'description' in parameters:
                update_params.update({'description': parameters['description']})
            if 'sale_price' in parameters:
                update_params.update({'list_price': parameters['sale_price']})
            if 'cost_price' in parameters:
                update_params.update({'standard_price': parameters['cost_price']})
            if 'sku' in parameters:
                update_params.update({'default_code': parameters['sku']})
            if 'categories' in parameters:
                update_params.update({'categ_id': parameters['categories']})

            try:
                request.env['product.product'].browse(product_id).write(update_params)
                return {'status': 'success'}
            except Exception as ex:
                return {'status': 'error', 'message': str(ex)}
        else:
            return {'status': 'error', 'message': 'Product ID not found'}

    @http.route('/shop/product/delete/<int:product_id>', type='http', methods=['GET'], auth='user', csrf=False)
    def delete_product(self, product_id=False, **kw):
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        if product_id:
            try:
                request.env['product.product'].browse(product_id).unlink()
                return request.make_response({'status': 'success'}, headers=headers)
            except Exception as ex:
                return request.make_response({'status': 'success', 'message': str(ex)}, headers=headers)
        else:
            return request.make_response(json.dumps({'status': 'error', 'message': 'Product ID not found'}), headers=headers)

    @http.route('/shop/product/create', type='json', methods=['POST'], auth='user', csrf=False)
    def create_product(self, **kw):
        update_params = {}
        parameters = request.get_json_data()
        if 'name' in parameters:
            update_params.update({'name': parameters['name']})
        if 'slug' in parameters:
            update_params.update({'product_slug': parameters['slug']})
        if 'description' in parameters:
            update_params.update({'description': parameters['description']})
        if 'sale_price' in parameters:
            update_params.update({'list_price': parameters['sale_price']})
        if 'cost_price' in parameters:
            update_params.update({'standard_price': parameters['cost_price']})
        if 'sku' in parameters:
            update_params.update({'default_code': parameters['sku']})
        if 'categories' in parameters:
            update_params.update({'categ_id': parameters['categories']})

        try:
            created_shop = request.env['product.product'].create(update_params)
            return {'status': 'success', 'product_id': str(created_shop.id)}
        except Exception as ex:
            return {'status': 'error', 'message': str(ex)}

    @http.route('/shop/product/availability', type='json', methods=['POST'], auth='public', csrf=False)
    def product_availability(self, **kw):
        parameters = request.get_json_data()
        if 'product_id' in parameters and 'quantity' in parameters and 'shop_id' in parameters:
            product_details = request.env['product.product'].sudo().browse(parameters['product_id'])
            shop_id = request.env['market.place.shops'].sudo().browse(parameters['shop_id'])
            if not shop_id:
                return {'status': 'error', 'message': 'Shop ID not found'}
            if product_details:
                p_warehouse = request.env['stock.quant'].sudo().search([('warehouse_id', '=', shop_id.warehouse_id.id), ('product_id', '=', product_details.id)])
                if p_warehouse:
                    if p_warehouse.available_quantity >= parameters['quantity']:
                        return {'status': 'success', 'message': 'available'}
                    else:
                        return {'status': 'success', 'message': 'not available'}
                else:
                    return {'status': 'success', 'message': 'not available'}
            else:
                return {'status': 'error', 'message': 'Product ID not found'}
        else:
            return {'status': 'error', 'message': 'Required parameter not found'}