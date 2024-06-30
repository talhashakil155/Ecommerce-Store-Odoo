from odoo import fields, models


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    shop_id = fields.Many2one("market.place.shops", "Shop ID")
    payment_provider = fields.Many2one('payment.provider', 'Payment Gateway')
