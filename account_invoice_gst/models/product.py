# -*- coding: utf-8 -*-
from openerp import api, fields, models, _

class product_template(models.Model):
    _inherit = "product.template"

    is_gst = fields.Boolean(
        'Is GST',
        default=False,
        help="is it include in gst or not"
    )

    gst_id = fields.Many2one(
        'product.gst',
        string = 'HSN Code',
    )
    
    @api.onchange('is_gst')
    def is_gst_change(self):
        if not self.is_gst:
            self.gst_id = False