# -*- coding: utf-8 -*-
from openerp import api, fields, models, _

class product_category(models.Model):
    _inherit = "product.category"
    
    gst_ids = fields.One2many(
        'product.gst','product_category_id',
        string = 'HSN Code',
    )