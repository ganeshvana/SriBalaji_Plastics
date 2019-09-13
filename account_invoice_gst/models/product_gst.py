# -*- coding: utf-8 -*-
from openerp import api, fields, models, _

class product_gst(models.Model):
    _name = "product.gst"
    
    name = fields.Char(
        string = 'Name',
        required = True,
        size=8,
    )
    cgst_sale_tax_id = fields.Many2one(
        'account.tax', 
        string='CGST Sale',
        required = True,
    )
    sgst_sale_tax_id = fields.Many2one(
        'account.tax', 
        string='SGST Sale',
        required = True,
    )
    igst_sale_tax_id = fields.Many2one(
        'account.tax', 
        string='IGST Sale',
        required = True,
    )
    cgst_purchase_tax_id = fields.Many2one(
        'account.tax', 
        string='CGST Purchase',
        required = True,
    )
    sgst_purchase_tax_id = fields.Many2one(
        'account.tax', 
        string='SGST Purchase',
        required = True,
    )
    igst_purchase_tax_id = fields.Many2one(
        'account.tax', 
        string='IGST Purchase',
        required = True,
    )
    product_category_id = fields.Many2one(
        'product.category',
        string = 'Product Category'
    )
    
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        categ_id = self.env.context.get('categ_id', False)
        if categ_id:
            self._cr.execute("""
                SELECT
                    id
                FROM
                    product_gst
                WHERE
                    product_category_id = %s
            """ %(categ_id))
            res = self._cr.dictfetchall()
            gst_ids = []
            if res:
                gst_ids = [i['id'] for i in res]
            args += [('id', 'in', gst_ids)]
        return super(product_gst, self)._search(args=args, offset=offset,
                                               limit=limit, order=order,
                                               count=count,access_rights_uid=access_rights_uid)