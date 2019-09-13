# -*- coding: utf-8 -*-
import time
from odoo import api, models, _
from datetime import datetime
from dateutil.relativedelta import relativedelta


class ReportAccountInvoice(models.AbstractModel):
    _name = 'report.account_invoice_gst.tax_invoice_report_view'
    
    def get_type(self, invoice):
        tax_type = []
        for rec in invoice.tax_line_ids:
            if rec.tax_id.tax_type not in tax_type:
                if rec.tax_id.tax_type:
                    tax_type.append(str(rec.tax_id.tax_type))
                else:
                    tax_type.append('other')
                print("tax_type",tax_type)
        return tax_type

    def get_tax_total(self, invoice):
        tax_total = {}
        for rec in invoice.tax_line_ids:
            tax_type = rec.tax_id.tax_type and rec.tax_id.tax_type or 'other'
            if tax_type not in tax_total:
                tax_total.update({
                    tax_type: rec.amount
                })
            else:
                tax_total[tax_type] += rec.amount
            print ("tax_total",tax_total)
        return tax_total
    
    def get_line_total(self, line):
        invoice = line.invoice_id
        price_total = 0.0
        for rec in line:
            price_total = line.price_subtotal
            for tax in rec.invoice_line_tax_ids:
                price_total = price_total + ((line.price_subtotal * tax.amount) / 100.0)
                print ("price_total",price_total)
        return price_total

    def get_line_tax(self, line):
        invoice = line.invoice_id
        price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        
        line_tax = []
        taxes = line.invoice_line_tax_ids.compute_all(price_unit,
                                                          invoice.currency_id,
                                                          line.quantity,
                                                          line.product_id,
                                                          invoice.partner_id)['taxes']
                                                        
        tax_dict = {}
        for line in taxes:
            tax = self.env['account.tax'].sudo().browse(line['id'])
            tax_type = tax.tax_type and tax.tax_type or 'other'
            if tax_type not in tax_dict:
                tax_dict[tax_type] = {}
            tax_dict[tax_type].update({
                'rate': tax.amount,
                'amount': line['amount'],
                'tax_type': tax_type,
                'tax_id': tax,
            })
        return tax_dict

    def get_lines(self, order):
        lines_by_tax_id = {}
        for line in order.order_line:
            if line.invoice_line_tax_ids:
                if line.invoice_line_tax_ids not in lines_by_tax_id:
                    lines_by_tax_id.update({line.invoice_line_tax_ids: {'lines': [], 'sum': 0.0}})
                lines_by_tax_id[line.product_id.tax_id]['lines'].append(line)
                lines_by_tax_id[line.product_id.tax_id]['sum'] += line.price_subtotal
                self.total += line.price_subtotal
        return lines_by_tax_id
    
    def get_amount_in_word(self , invoice):
        val = invoice.sudo().number_to_words(int(invoice.amount_total))
        return val
    
    def amount(self, line):
        invoice = line.invoice_id
        total_amt = 0.0
        for rec in line:
            total_amt = (rec.price_unit * rec.quantity)
        return total_amt

    def total_disc(self, order):
        total_amt = 0.0
        final = 0.0
        for rec in order.invoice_line_ids:
            total_amt = (rec.price_unit * rec.quantity)
            final = final + total_amt
        return final

    def get_total(self):
        return self.total   

    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     docs = self.env['account.invoice'].browse(docids)
    #     return {
    #         'doc_ids': self.ids,
    #         'doc_model': 'account.invoice',
    #         'docs': docs,
    #         'proforma': True
    #     }

 
    
    @api.model
    def _get_report_values(self, docids, data=None):
        print ("oooooo")
        docargs = {
            'get_type' : self.get_type,
            'doc_ids': self.ids,
            'doc_model': 'account.invoice',
            'docs': self.env['account.invoice'].browse(docids),
            'get_lines': self.get_lines,
            'get_line_tax': self.get_line_tax,
            'get_tax_total':self.get_tax_total,
            'amount':self.amount,
            'total_disc':self.total_disc,
            'get_line_total':self.get_line_total,
            'get_amount_in_word': self.get_amount_in_word,
        }
        print ("dddddddddddddddddddd",docargs)
        return docargs
    
