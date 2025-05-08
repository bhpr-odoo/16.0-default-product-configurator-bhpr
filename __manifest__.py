# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Default Product Configurator",
    "version": "16.0.0.0.0",
    "summary": "Default attribute values for product configurator",
    "description": """
       This module enhances the product configuration process on the Sales Order by introducing a Global Info tab. 
       It enables predefining default product attribute values based on product categories.
    """,
    "category": 'Hidden',
    #Author
    "author": "Odoo PS",
    "website": "https://www.odoo.com",
    "license": "LGPL-3",
    # Dependency
    "depends": ['sale', 'stock_account'],
    "data": [
        "security/ir.model.access.csv",
        "views/product_views.xml",
        "views/sale_order_view.xml"
    ],
    "installable": True,
}
