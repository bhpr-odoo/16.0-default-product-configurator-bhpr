# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class GlobalInfoAttributeLine(models.Model):
    _name = 'global.info.attribute.line'
    _description = 'Global Info Attribute Line'

    order_id = fields.Many2one('sale.order', ondelete='cascade')
    category_id = fields.Many2one('product.category')
    attribute_id = fields.Many2one('product.attribute', string='Attribute')
    attribute_value_id = fields.Many2one(
        'product.attribute.value',
        string = 'Attribute Value',
        domain = "[('attribute_id', '=', attribute_id)]",
        help = "Select a value that matches the attribute.",
    )
    line_section = fields.Boolean(default=False)
    category_name = fields.Char(compute='_compute_category_name', store=True)
    
    @api.depends('category_id')
    def _compute_category_name(self):
        for rec in self:
            rec.category_name = rec.category_id.name
