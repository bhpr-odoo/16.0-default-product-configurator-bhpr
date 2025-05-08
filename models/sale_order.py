# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    category_line = fields.One2many('global.info.attribute.line', 'order_id')
           
    def action_global_info(self):
        for order in self:
            categories = self.env['product.category'].search([('global_info', '=', True)])          
            existing_categories = order.category_line
            new_categories = []
            for cat in categories:
                category_exists = existing_categories.filtered(lambda l: l.category_id == cat and l.line_section)
                if not category_exists:
                    new_categories.append((0, 0, {
                        'category_id': cat.id,
                        'line_section': True,
                    }))
                for attr in cat.required_attribute_ids:
                    attribute_exist = existing_categories.filtered(lambda l: l.category_id == cat and l.attribute_id == attr and not l.line_section)
                    if not attribute_exist:
                        new_categories.append((0, 0, {
                            'category_id': cat.id,
                            'attribute_id': attr.id,
                        }))
            if new_categories:
                order.category_line = new_categories
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }
