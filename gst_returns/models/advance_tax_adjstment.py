# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class tax_adjustment(models.Model):
    _name = 'tax.adjustment'

    gst_return_id = fields.Many2one('gstr.return', string='GST Return')
    state_name = fields.Many2one('res.country.state', string='Place of Supply')
    rate = fields.Float(string='Rate')
    gross_advance_adjustment = fields.Char(string='Gross advance Adjustment')
    cess_amount = fields.Float(string='Cess Amount')
