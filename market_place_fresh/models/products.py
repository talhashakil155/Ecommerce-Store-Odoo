from odoo import fields, models

class InheritedProductProduct(models.Model):
    _inherit = "product.template"

    shop_id = fields.Many2one("market.place.shops", string="Market Place Shop", required=1)
    product_slug = fields.Char("Product Slug")
    minimum_price = fields.Float("Minimum Price")
    maximum_price = fields.Float("Maximum Price")
    google_storage = fields.Char("Google Storage Bucket Image")
    brand = fields.Char("Brand")
    touchgroup = fields.Char("Touch Group")
    supplier_name = fields.Char("Supplier Name")
    sku_description = fields.Char("SKU Description")
    selling_price = fields.Monetary("Selling Price")
    carton_qty = fields.Float("Carton Quantity")
    allow_discount = fields.Boolean("Allow discount?")
    is_web_plu = fields.Boolean("Is Web Plu?")
    webpluid = fields.Char("Web Plu ID")
    web_plu_description = fields.Char("Web Plug Description")
