from odoo import fields, models

class shopsModel(models.Model):
    _name = 'market.place.shops'

    name = fields.Char('Name', required=True)
    slug = fields.Char('Slug', required=True)
    shop_description = fields.Html('Shop Description')
    owner = fields.Many2one('res.users', 'Owner', required=True)
    logo = fields.Binary('Shop Logo')
    cover_image = fields.Binary('Cover Image')
    status = fields.Boolean('Status')
    contact_email = fields.Char('Contact Email')
    contact_no = fields.Char('Contact No')
    no_of_orders = fields.Integer('Number Of Orders', default=0)
    notifications = fields.Boolean('Notifications')
    warehouse_id = fields.Many2one('stock.warehouse', 'Shop Warehouse', required=True)
    country_id = fields.Many2one('res.country', 'Country', required=True)
    city = fields.Char('City', required=True)
    state = fields.Char('State', required=True)
    zip = fields.Char('Zip', required=True)
    street_address = fields.Char('Street Address', required=True)
    categ_ids = fields.One2many("product.category", "shop_id", string="Product Categories")
    payment_account = fields.Char("Bank Account")
    payment_account_name = fields.Char("Account Name")
    payment_account_email = fields.Char("Account Email")
    payment_account_bank = fields.Char("Account Bank Name")

    _sql_constraints = [('shop_slug_uniq', 'unique (slug)', 'Shop slug must be unique!')]
