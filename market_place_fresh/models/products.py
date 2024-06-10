from odoo import fields, models

class InheritedProductProduct(models.Model):
    _inherit = "product.template"

    shop_id = fields.Many2many("market.place.shops", string="Market Place Shop", required=1)
    product_slug = fields.Char("Product Slug")
    minimum_price = fields.Float("Minimum Price")
    maximum_price = fields.Float("Maximum Price")

    _sql_constraints = [('product_slug_uniq', 'unique (product_slug)', 'Product slug must be unique!')]