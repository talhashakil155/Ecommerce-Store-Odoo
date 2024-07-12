from odoo import fields, models

class InheritProductCategory(models.Model):
    _inherit = 'product.category'

    cat_slug = fields.Char("Slug")
    cat_icon = fields.Char("Icon")
    cat_image = fields.Binary("Image")
    cat_details = fields.Html("Description")
    shop_id = fields.Many2one("market.place.shops", string="Shop ID")