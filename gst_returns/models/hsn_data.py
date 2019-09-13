# -*- coding: utf-8 -*-

from odoo import models , fields , api , _


class hsn_data(models.Model):
    _name = 'hsn.data'

    gst_return_id = fields.Many2one('gstr.return', string='GST Return')
    gst_id = fields.Char(string='HSN')
    description = fields.Char(string='Description')
    uom_id = fields.Many2one('product.uom', string='UOM')
    total_quantity = fields.Float(string='Total Quantity')
    total_value = fields.Float(string='Total Value')
    taxable_value = fields.Float(string='Taxable Value')
    igst = fields.Float(string='Integrated Tax Amount')
    cgst = fields.Float(string='Central Tax Amount')
    sgst = fields.Float(string='State/UT Tax Amount')
    cess_amount = fields.Float(string='Cess Amount')
