from odoo import fields, models

class InheritedProductProduct(models.Model):
    _inherit = "product.template"

    shop_id = fields.Many2one("market.place.shops", string="Market Place Shop", required=1)
    product_slug = fields.Char("Product Slug")
    minimum_price = fields.Float("Minimum Price")
    maximum_price = fields.Float("Maximum Price")
    google_storage = fields.Char("Google Storage Bucket Image")