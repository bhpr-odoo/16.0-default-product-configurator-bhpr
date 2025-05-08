# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.addons.sale_product_configurator.controllers.main import ProductConfiguratorController
from odoo.http import request


class ProductConfiguratorExtended(ProductConfiguratorController):
    @http.route(['/sale_product_configurator/configure'], type='json', auth="user", methods=['POST'])
    def configure(self, product_template_id, pricelist_id, **kw):
        add_qty = float(kw.get('quantity', 1))
        product_template = request.env['product.template'].browse(int(product_template_id))
        pricelist = self._get_pricelist(pricelist_id)
        
        product_combination = False
        sale_order_id = request.context.get('order_id')
        expected_lines = request.env['global.info.attribute.line'].search([
            ('order_id', '=', sale_order_id),
            ('category_id', '=', product_template.categ_id.id),
            ('attribute_id', '!=', False),
        ])
        configured_value_ids = []
        selected_lines = expected_lines.filtered(lambda l: l.attribute_value_id)
        missing_lines = expected_lines.filtered(lambda l: not l.attribute_value_id)
        
        for line in selected_lines:
            selected_value = line.attribute_value_id
            exist_value = request.env['product.template.attribute.line'].search([
                ('attribute_id', '=', line.attribute_id.id),
                ('product_tmpl_id', '=', product_template_id),
                ('value_ids', 'in', [selected_value.id])
            ])
            if exist_value:
                configured_value_ids.append(selected_value.id)
            else:
                line = request.env['product.template.attribute.line'].search([
                    ('attribute_id', '=', line.attribute_id.id),
                    ('product_tmpl_id', '=', product_template.id),
                    ('value_ids', 'not in', [selected_value.id]), 
                ],limit=1)
                configured_value_ids.append(line.value_ids[0].id)

        for line in missing_lines:
            value = request.env['product.template.attribute.line'].search([
                ('attribute_id', '=', line.attribute_id.id),
                ('product_tmpl_id', '=', product_template.id)
            ],limit=1)
            configured_value_ids.append(value.value_ids[0].id)

        attribute_value_ids = request.env['product.template.attribute.value'].search([
            ('product_attribute_value_id', 'in', configured_value_ids)
        ]).ids

        if attribute_value_ids:
            product_combination = request.env['product.template.attribute.value'].browse(
                attribute_value_ids
            ).filtered(lambda ptav: ptav.product_tmpl_id == product_template)
        else:
            return super(ProductConfiguratorExtended, self).configure(
                    product_template_id, pricelist_id, **kw)
        if pricelist:
            product_template = product_template.with_context(pricelist=pricelist.id, partner=request.env.user.partner_id)
        return request.env['ir.ui.view']._render_template(
            "sale_product_configurator.configure",
            {
                'product': product_template,
                'pricelist': pricelist,
                'add_qty': add_qty,
                'product_combination': product_combination
            },
        )

    def _show_advanced_configurator(self, product_id, variant_values, pricelist, handle_stock, **kw):
        product = request.env['product.product'].browse(int(product_id))
        add_qty = float(kw.get('add_qty', 1))
        sale_order_id = request.context.get('order_id')
        expected_lines = request.env['global.info.attribute.line'].search([
            ('order_id', '=', sale_order_id),
            ('category_id', '=', product.product_tmpl_id.categ_id.id),
            ('attribute_id', '!=', False),
        ])
        configured_value_ids = []
        selected_lines = expected_lines.filtered(lambda l: l.attribute_value_id)
        missing_lines = expected_lines.filtered(lambda l: not l.attribute_value_id)

        for line in selected_lines:
            selected_value = line.attribute_value_id
            exist_value = request.env['product.template.attribute.line'].search([
                ('attribute_id', '=', line.attribute_id.id),
                ('product_tmpl_id', '=', product.product_tmpl_id.id),
                ('value_ids', 'in', [selected_value.id])
            ])
            if exist_value:
                configured_value_ids.append(selected_value.id)
            else:
                line = request.env['product.template.attribute.line'].search([
                    ('attribute_id', '=', line.attribute_id.id),
                    ('product_tmpl_id', '=', product.product_tmpl_id.id),
                    ('value_ids', 'not in', [selected_value.id])
                ],limit=1)
                configured_value_ids.append(line.value_ids[0].id)

        for line in missing_lines:
            value = request.env['product.template.attribute.line'].search([
                ('attribute_id', '=', line.attribute_id.id),
                ('product_tmpl_id', '=', product.product_tmpl_id.id)
            ], limit=1)
            configured_value_ids.append(value.value_ids[0].id)

        attribute_value_ids = request.env['product.template.attribute.value'].search([
            ('product_attribute_value_id', 'in', configured_value_ids)
        ]).ids
        if attribute_value_ids:
            combination = request.env['product.template.attribute.value'].browse(attribute_value_ids)
        else:
            return super()._show_advanced_configurator(product_id, variant_values, pricelist, handle_stock, **kw)
            
        no_variant_attribute_values = combination.filtered(
                lambda product_template_attribute_value: product_template_attribute_value.attribute_id.create_variant == 'no_variant'
        )
        if no_variant_attribute_values:
            product = product.with_context(no_variant_attribute_values=no_variant_attribute_values)
        
        return request.env['ir.ui.view']._render_template(
            "sale_product_configurator.optional_products_modal", 
            {
                'product': product,
                'combination': combination,
                'add_qty': add_qty,
                'parent_name': product.name,
                'variant_values': variant_values,
                'pricelist': pricelist,
                'handle_stock': handle_stock,
                'already_configured': kw.get("already_configured", False),
                'mode': kw.get('mode', 'add'),
                'product_custom_attribute_values': kw.get('product_custom_attribute_values', None),
                'no_attribute': kw.get('no_attribute', False),
                'custom_attribute': kw.get('custom_attribute', False)
            }
        )
