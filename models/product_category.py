# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    global_info = fields.Boolean(
        string = "Show on Global Info",
        default = False,
        help = "Boolean field that decides this category to be shown on the SO Global Info Tab"
    )

    required_attribute_ids = fields.Many2many(
        comodel_name = 'product.attribute',
        string = 'Required Attributes',
    )
