from odoo import http, Command
from odoo.http import request
import json


class SaleOrderMarketController(http.Controller):

    @http.route('/orders/list', type='http', methods=['GET'], auth='user')
    def get_all_orders(self, **kw):
        all_orders = self.get_orders_by_domain([])
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        return request.make_response(json.dumps({'status': 'success', 'orders_response': all_orders}), headers=headers)

    @http.route('/orders/<int:shop_id>/list', type='http', methods=['GET'], auth='user')
    def get_orders_by_shop(self, shop_id=False, **kw):
        headers = [('Content-Type', 'application/json'), ('Cache-Control', 'no-store')]
        if shop_id:
            shop_orders = self.get_orders_by_domain([('shop_id', '=', shop_id)])
            return request.make_response(json.dumps({'status': 'success', 'orders_response': shop_orders}), headers=headers)
        else:
            return request.make_response({'status': 'success', 'orders_response': 'Shop Id Not Found in Request'}, headers=headers)

    def get_orders_by_domain(self, domain):
        sale_orders = request.env['sale.order'].search(domain)
        orders_response = []
        deliver_fee = 0
        for order in sale_orders:
            order_line = []
            for x in order.order_line:
                if x.name == "Delivery Fee":
                    deliver_fee = x.price_unit
                    continue
                order_line.append({
                    "id": x.product_id.id,
                    "name": x.name,
                    "slug": x.product_id.product_slug,
                    "description": x.product_id.description,
                    "price": x.product_id.list_price,
                    "sale_price": x.price_unit,
                    "language": "en",
                    "min_price": x.product_id.minimum_price or False,
                    "max_price": x.product_id.maximum_price or False,
                    "sku": x.product_id.default_code,
                    "quantity": x.product_uom_qty,
                    "product_type": x.product_id.detailed_type,
                    "unit": x.product_uom.name,
                    "height": False,
                    "width": False,
                    "length": False,
                    "image": f'/web/image/product.product/{x.product_id.id}/image_1920',
                    "created_at": str(x.create_date),
                    "updated_at": str(x.write_date),
                })
            orders_response.append({
                'id': order.id,
                'name': order.name,
                'customer_contact': order.partner_id.phone,
                'customer_name': order.partner_id.name,
                'amount_untaxed': order.amount_untaxed,
                'amount_tax': order.amount_tax,
                'amount_total': order.amount_total,
                'order_status': order.state,
                'order_date': str(order.date_order),
                'note': order.note,
                'shop_id': order.shop_id.name if order.shop_id else False,
                'language': order.partner_id.lang,
                'parent_id': '',
                'cancelled_amount': 0.00,
                'cancelled_tax': 0.00,
                'cancelled_delivery_fee': 0.00,
                'payment_gateway': 'CASH_ON_DELIVERY',
                'discount': '',
                'payment_status': '',
                "logistics_provider": False,
                'customer': {
                    "id": order.partner_id.id,
                    "name": order.partner_id.name,
                    "email": order.partner_id.email,
                    "created_at": str(order.partner_id.create_date),
                    "updated_at": str(order.partner_id.write_date),
                } if order.partner_id else False,
                'billing_address': {
                    "zip": order.partner_invoice_id.zip,
                    "city": order.partner_invoice_id.city,
                    "state": order.partner_invoice_id.state_id.name,
                    "country": order.partner_invoice_id.country_id.name,
                    "street_address": order.partner_invoice_id.name
                } if order.partner_invoice_id else {
                    "zip": order.partner_id.zip,
                    "city": order.partner_id.city,
                    "state": order.partner_id.state_id.name,
                    "country": order.partner_id.country_id.name,
                    "street_address": order.partner_id.name
                },
                'shipping_address': {
                    "zip": order.partner_shipping_id.zip,
                    "city": order.partner_shipping_id.city,
                    "state": order.partner_shipping_id.state_id.name,
                    "country": order.partner_shipping_id.country_id.name,
                    "street_address": order.partner_shipping_id.name
                } if order.partner_shipping_id else False,
                'created_at': str(order.create_date),
                'updated_at': str(order.write_date),
                'products': order_line,
                "delivery_fee": deliver_fee,
                "delivery_status": order.delivery_status,
                "delivery_date": (str(order.commitment_date) if order.commitment_date else False)
            })
        return orders_response

    def prepare_order_array(self, req_params):
        order_arr = {}
        order_arr.update({'origin': 'Website API'})
        if 'customer_id' in req_params:
            order_arr.update({'partner_id': req_params['customer_id']})
        if 'billing_address' in req_params:
            order_arr.update({'partner_invoice_id': req_params['billing_address']})
        if 'shipping_address' in req_params:
            order_arr.update({'partner_shipping_id': req_params['shipping_address']})
        if 'date_order' in req_params:
            order_arr.update({'date_order': req_params['date_order']})
        if 'payment_gateway' in req_params:
            provider = request.env['payment.provider'].search([('name', '=', req_params['payment_gateway'])], limit=1)
            if provider:
                order_arr.update({'payment_provider': provider.id})
        return order_arr

    def prepare_order_line(self, product, order_id):
        line = {}
        if 'product_id' in product:
            line.update({'product_id': product['product_id']})
        if 'sale_price' in product:
            line.update({'price_unit': product['sale_price']})
        if 'product_name' in product:
            line.update({'name': product['product_name']})
        if 'unit' in product:
            uom = request.env['uom.uom'].search([('name', '=', product['unit'])], limit=1)
            if uom:
                line.update({'product_uom': uom.id})
        if 'quantity' in product:
            line.update({'product_uom_qty': product['quantity']})
        if 'discount' in product:
            line.update({'discount': product['discount']})
        if 'shop_id' in product:
            line.update({'shop_id': product['shop_id']})
        line.update({'order_id': order_id})
        line.update({'tax_id': []})
        return line

    def prepare_delivery_line(self, delivery_fee, order_id):
        line = {}
        deliver_prod = request.env['product.template'].search([('name', '=', 'Delivery Fee')])
        if deliver_prod:
            line.update({
                'product_id': deliver_prod.product_variant_id.id,
                'name': deliver_prod.name,
                'discount': 0,
                'product_uom_qty': 1,
                'price_unit': delivery_fee,
                'order_id': order_id,
                'tax_id': []
            })
            return line
        else:
            return False

    @http.route('/orders/create', type='json', methods=['POST'], auth='user')
    def create_order(self):
        req_params = request.get_json_data()
        order_arr = self.prepare_order_array(req_params)
        try:
            order_details = request.env['sale.order'].create(order_arr)
            if order_details:
                for product in req_params['products']:
                    oline = self.prepare_order_line(product, order_details.id)
                    request.env['sale.order.line'].create(oline)
                if 'delivery_fee' in req_params:
                    oline = self.prepare_delivery_line(req_params['delivery_fee'], order_details.id)
                    if oline:
                        request.env['sale.order.line'].create(oline)
            return {'status': 'success', 'order_id': order_details.id, 'order_name': order_details.name}
        except Exception as ex:
            return {'status': 'error', 'message': str(ex)}

    @http.route('/orders/<int:order_id>/update', type='json', methods=['POST'], auth='user')
    def update_order(self, order_id=False):
        if order_id:
            order = request.env['sale.order'].browse(order_id)
            if order:
                order_arr = self.prepare_order_array(request.get_json_data())
                try:
                    order_details = request.env['sale.order'].write(order_arr)
                    return {'status': 'success', 'order_id': order_details.id, 'order_name': order_details.name}
                except Exception as ex:
                    return {'status': 'error', 'message': str(ex)}
            else:
                return {'status': 'error', 'message': 'Order not found in system'}
        else:
            return {'status': 'error', 'message': 'Order ID not found'}
