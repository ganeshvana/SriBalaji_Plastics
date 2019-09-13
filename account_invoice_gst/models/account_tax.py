# -*- coding: utf-8 -*-
from openerp import api, fields, models, _

class AccountTax(models.Model):
    _inherit = 'account.tax'
    
    tax_type = fields.Selection(
        string="GST Tax Type",
        selection=[
                ('cgst', 'CGST'),
                ('sgst', 'SGST'),
                ('igst', 'IGST'),
                ]
    )
