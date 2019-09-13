# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
from openerp.exceptions import UserError


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"
    
    gst_id = fields.Char(      
        string = 'HSN Number',
    )
      

    @api.multi
    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(AccountInvoiceLine,self)._onchange_product_id()
        if self.product_id.l10n_in_hsn_code:
            self.gst_id = self.product_id.l10n_in_hsn_code            
        else:
            self.gst_id = False
        return res

#    def _set_gst_taxes(self):
#        user_state_id = self.env.user.company_id.state_id
#        if not self.invoice_id.partner_id:
#            raise UserError(
#                        _("Please add the Customer")
#                    )
#         if self.product_id:
#             if not self.product_id.is_gst and self.gst_id:
#                 self.gst_id ={}
#                 raise UserError(
#                             _("HSN Number not allow.")
#                         )
#             elif not self.gst_id and self.product_id.is_gst:
#                 raise UserError(
#                             _("HSN Number Required.")
#                         )
#        customer_state_id = self.invoice_id.partner_id.state_id
#        if self.product_id.gst_id and self.invoice_id.partner_id.supplier:
#            if customer_state_id == user_state_id:
#                self.invoice_line_tax_ids += self.gst_id.cgst_purchase_tax_id + self.gst_id.sgst_purchase_tax_id
#            else:
#                self.invoice_line_tax_ids += self.gst_id.igst_purchase_tax_id
#        elif self.product_id.gst_id and self.invoice_id.partner_id.customer:
#            if customer_state_id == user_state_id:
#                self.invoice_line_tax_ids += self.gst_id.cgst_sale_tax_id + self.gst_id.sgst_sale_tax_id
#            else:
#                self.invoice_line_tax_ids += self.gst_id.igst_sale_tax_id

#    def _set_taxes(self):
#        res = super(AccountInvoiceLine,self)._set_taxes()
#        self._set_gst_taxes()
#        return res

#    @api.onchange('gst_id')
#    def gst_id_change(self):
#        self._set_gst_taxes()
#        
#    @api.model
#    def create(self, vals):
#        res = super(AccountInvoiceLine, self).create(vals)
#        
#        if res.product_id.is_gst and not res.gst_id:
#            raise UserError(
#                        _("Please add hsn number")
#                    )
#        elif not res.product_id.is_gst and res.gst_id.id:  
#            res.gst_id ={}
#            raise UserError(
#                        _("HSN Number not allow!")
#                    )
#        return res
#    
    
