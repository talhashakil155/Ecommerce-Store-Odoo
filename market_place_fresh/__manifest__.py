# -*- coding: utf-8 -*-
{
    'name': 'Modifications for Market Place Fresh',
    'category': 'Inventory',
    'description': """Modification required for Market Place Fresh""",
    'depends': ['web', 'stock', 'product'],
    'data': [
        'views/shops.xml',
        'views/products.xml',
        'views/product_categories.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'license': 'OEEL-1',
}