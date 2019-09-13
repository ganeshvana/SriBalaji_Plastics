# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.import xlwt
import io
from io import StringIO
import base64
import time
import xlwt
from datetime import datetime, date, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _, exceptions

class InvoiceExcelReport(models.Model):
    _name = 'account.invoice.excel.report'

    @api.model
    def default_get(self, fields):
        account_obj = self.env['account.invoice']
        accounts = []
        res = super(InvoiceExcelReport, self).default_get(fields)
        active_ids = self._context.get('active_ids', [])

        for acc in account_obj.browse(active_ids):
            accounts.append(acc.id)

        res.update({'account_ids': [(6, 0, accounts)]})
        return res

    account_ids = fields.Many2many('account.invoice', string='Account Ids')

    @api.multi
    def get_data(self):
        workbook = xlwt.Workbook()
        title_style_center = xlwt.easyxf('align: horiz center ;font: name Times New Roman,bold off, italic off')
        title_style_left = xlwt.easyxf('font: name Times New Roman, height 200;align: horiz left ')
        title_style_right = xlwt.easyxf('font: name Times New Roman, height 200;align: horiz right ')
        title_style1_table_head_right = xlwt.easyxf(
            'font: name Times New Roman,bold on, italic off, height 200;align: horiz right ;')
        title_style1_table_head_center = xlwt.easyxf(
            'align: horiz center ;font: name Times New Roman,bold on, italic off, height 200')
        title_style1_table_head_left = xlwt.easyxf(
            'align: horiz left ;font: name Times New Roman,bold on, italic off, height 200')
        row_date_count = 0

        # Invoice

        sheet = workbook.add_sheet('Invoice Analysis Report')
        sheet.write(row_date_count, 0, "userGstin ", title_style1_table_head_center)
        sheet.write(row_date_count, 1, "supplyType", title_style1_table_head_center)
        sheet.write(row_date_count, 2, "subSupplyType", title_style1_table_head_center)
        sheet.write(row_date_count, 3, "transType", title_style1_table_head_center)
        sheet.write(row_date_count, 4, "docType", title_style1_table_head_center)
        sheet.write(row_date_count, 5, "docNo", title_style1_table_head_center)
        sheet.write(row_date_count, 6, "docDate", title_style1_table_head_center)
        sheet.write(row_date_count, 7, "fromGstin", title_style1_table_head_center)


        sheet.write(row_date_count, 8, "fromTrdName", title_style1_table_head_center)
        sheet.write(row_date_count, 9, "fromAddr1", title_style1_table_head_center)
        sheet.write(row_date_count, 10, "fromAddr2 ", title_style1_table_head_center)
        sheet.write(row_date_count, 11, "fromPlace", title_style1_table_head_center)
        sheet.write(row_date_count, 12, "fromPincode", title_style1_table_head_center)
        sheet.write(row_date_count, 13, "fromStateCode", title_style1_table_head_center)
        sheet.write(row_date_count, 14, "actualFromStateCode", title_style1_table_head_center)
        sheet.write(row_date_count, 15, "toGstin", title_style1_table_head_center)
        sheet.write(row_date_count, 16, "toTrdName", title_style1_table_head_center)
        sheet.write(row_date_count, 17, "toAddr1", title_style1_table_head_center)
        sheet.write(row_date_count, 18, "toAddr2", title_style1_table_head_center)
        sheet.write(row_date_count, 19, "toPlace", title_style1_table_head_center)


        sheet.write(row_date_count, 20, "toPincode ", title_style1_table_head_center)
        sheet.write(row_date_count, 21, "toStateCode", title_style1_table_head_center)
        sheet.write(row_date_count, 22, "actualToStateCode", title_style1_table_head_center)
        sheet.write(row_date_count, 23, "totalValue", title_style1_table_head_center)
        sheet.write(row_date_count, 24, "gst", title_style1_table_head_center)
        sheet.write(row_date_count, 25, "transMode", title_style1_table_head_center)
        sheet.write(row_date_count, 26, "transDistance", title_style1_table_head_center)


        sheet.write(row_date_count, 27, "transporterName ", title_style1_table_head_center)
        sheet.write(row_date_count, 28, "transporterId", title_style1_table_head_center)
        sheet.write(row_date_count, 29, "transDocNo", title_style1_table_head_center)
        sheet.write(row_date_count, 30, "transDocDate", title_style1_table_head_center)
        sheet.write(row_date_count, 31, "vehicleNo", title_style1_table_head_center)
        sheet.write(row_date_count, 32, "vehicleType", title_style1_table_head_center)
        sheet.write(row_date_count, 33, "totInvValue", title_style1_table_head_center)
        sheet.write(row_date_count, 34, "OthValue", title_style1_table_head_center)
        sheet.write(row_date_count, 35, "mainHsnCode", title_style1_table_head_center)
        row_date_count += 1
        count = 0

        acc_values = []
        for acc_ids in self:
            browse = acc_ids.env['account.invoice'].search([('id', 'in', acc_ids.account_ids.ids)])
            for browse_account in browse:
                for account in browse_account:
                    company_vat = account.company_id.vat
                    supply_type = account.supply_type
                    sub_supply_type = account.sub_supply_type
                    trans_type = account.trans_type
                    doc_type = account.doc_type
                    doc_no = account.doc_no
                    date_invoice = account.date_invoice

                    company_name = account.company_id.name
                    company_street = account.company_id.street
                    company_city = account.company_id.city
                    company_zip = account.company_id.zip
                    company_code = account.company_id.state_id.code
                    partner_vat = account.partner_id.vat
                    partner_name = account.partner_id.name
                    partner_street = account.partner_id.street
                    partner_city = account.partner_id.city

                    partner_zip = account.partner_id.zip
                    partner_code = account.partner_id.state_id.code
                    amount_untaxed = account.amount_untaxed
                    amount_tax = account.amount_tax
                    trans_mode = account.trans_mode
                    trans_distance = account.trans_distance

                    transporter_name = account.transporter_name
                    transporterid = account.transporterid
                    trans_doc_no = account.trans_doc_no
                    trans_doc_date = account.trans_doc_date
                    vehicle_no = account.vehicle_no
                    vehicle_type = account.vehicle_type
                    amount_total = account.amount_total
                    othvalue = account.othvalue
                    main_hsn_code = account.main_hsn_code
                    acc_data = {

                        'company_vat': company_vat,
                        'supply_type': supply_type,
                        'sub_supply_type': sub_supply_type,
                        'trans_type': trans_type,
                        'doc_type': doc_type,
                        'doc_no': doc_no,
                        'date_invoice': date_invoice,


                        'company_name': company_name,
                        'company_street': company_street,
                        'company_city': company_city,
                        'company_zip': company_zip,
                        'company_code': company_code,
                        'partner_vat': partner_vat,
                        'partner_name': partner_name,
                        'partner_street': partner_street,
                        'partner_city': partner_city,

                        'partner_zip': partner_zip,
                        'partner_code': partner_code,
                        'amount_untaxed': amount_untaxed,
                        'amount_tax': amount_tax,
                        'trans_mode': trans_mode,
                        'trans_distance': trans_distance,


                        'transporter_name': transporter_name,
                        'transporterid': transporterid,
                        'trans_doc_no': trans_doc_no,
                        'trans_doc_date': trans_doc_date,

                        'vehicle_no': vehicle_no,
                        'vehicle_type': vehicle_type,
                        'amount_total': amount_total,
                        'othvalue': othvalue,
                        'main_hsn_code': main_hsn_code,

                    }
                    acc_values.append(acc_data)


            for acc_val in acc_values:
                count += 1

                sheet.write(row_date_count, 0, acc_val['company_vat'], title_style_left)
                sheet.write(row_date_count, 1, acc_val['supply_type'], title_style_left)
                sheet.write(row_date_count, 2, acc_val['sub_supply_type'], title_style_left)
                sheet.write(row_date_count, 3, acc_val['trans_type'], title_style_left)
                sheet.write(row_date_count, 4, acc_val['doc_type'], title_style_left)
                sheet.write(row_date_count, 5, acc_val['doc_no'], title_style_left)
                sheet.write(row_date_count, 6, acc_val['date_invoice'], title_style_left)
                sheet.write(row_date_count, 7, acc_val['company_vat'], title_style_left)

                sheet.write(row_date_count, 8, acc_val['company_name'], title_style_left)
                sheet.write(row_date_count, 9, acc_val['company_street'], title_style_left)
                sheet.write(row_date_count, 10, " ", title_style_left)
                sheet.write(row_date_count, 11, acc_val['company_city'], title_style_left)
                sheet.write(row_date_count, 12, acc_val['company_zip'], title_style_left)
                sheet.write(row_date_count, 13, acc_val['company_code'], title_style_left)
                sheet.write(row_date_count, 14, acc_val['company_code'], title_style_left)
                sheet.write(row_date_count, 15, acc_val['partner_vat'], title_style_left)
                sheet.write(row_date_count, 16, acc_val['partner_name'], title_style_left)
                sheet.write(row_date_count, 17, acc_val['partner_street'], title_style_left)
                sheet.write(row_date_count, 18, " ", title_style_left)
                sheet.write(row_date_count, 19, acc_val['partner_city'], title_style_left)


                sheet.write(row_date_count, 20, acc_val['partner_zip'], title_style_left)
                sheet.write(row_date_count, 21, acc_val['partner_code'], title_style_left)
                sheet.write(row_date_count, 22, acc_val['partner_code'], title_style_left)
                sheet.write(row_date_count, 23, acc_val['amount_untaxed'], title_style_left)
                sheet.write(row_date_count, 24, acc_val['amount_tax'], title_style_left)
                sheet.write(row_date_count, 25, acc_val['trans_mode'], title_style_left)
                sheet.write(row_date_count, 26, acc_val['trans_distance'], title_style_left)


                sheet.write(row_date_count, 27, acc_val['transporter_name'], title_style_left)
                sheet.write(row_date_count, 28, acc_val['transporterid'], title_style_left)
                sheet.write(row_date_count, 29, acc_val['trans_doc_no'], title_style_left)
                sheet.write(row_date_count, 30, acc_val['trans_doc_date'], title_style_left)
                sheet.write(row_date_count, 31, acc_val['vehicle_no'], title_style_left)
                sheet.write(row_date_count, 32, acc_val['vehicle_type'], title_style_left)
                sheet.write(row_date_count, 33, acc_val['amount_total'], title_style_left)
                sheet.write(row_date_count, 34, acc_val['othvalue'], title_style_left)
                sheet.write(row_date_count, 35, acc_val['main_hsn_code'], title_style_left)
                row_date_count += 1


            row_date_count += 1

            sheet.write(row_date_count, 0, "Si. No", title_style1_table_head_center)
            sheet.write(row_date_count, 1, "productName", title_style1_table_head_center)
            sheet.write(row_date_count, 2, "productDesc ", title_style1_table_head_center)
            sheet.write(row_date_count, 3, "hsnCode", title_style1_table_head_center)
            sheet.write(row_date_count, 4, "quantity", title_style1_table_head_center)
            sheet.write(row_date_count, 5, "qtyUnit", title_style1_table_head_center)
            sheet.write(row_date_count, 6, "taxableAmount", title_style1_table_head_center)
            sheet.write(row_date_count, 7, "gstRate", title_style1_table_head_center)
            sheet.write(row_date_count, 8, "itemNo ", title_style1_table_head_center)
            row_date_count += 1

            values = []
            hsn = qty_unit = tax = '-'
            browse = self.env['account.invoice'].search([('id', 'in', self.account_ids.ids)])
            for browse_account in browse:
                for account in browse_account:
                    for line in account.invoice_line_ids:
                        product_id = line.product_id.name
                        desc = line.name
                        hsn = line.product_id.l10n_in_hsn_code
                        qty = line.quantity
                        qty_unit = line.uom_id.name
                        price = line.price_unit
                        sub_total = line.price_subtotal
                        for tax_id in line.invoice_line_tax_ids:
                            tax = tax_id.name
                        data = {

                            'product_id': product_id,
                            'desc': desc,
                            'hsn':hsn,
                            'qty': qty,
                            'qty_unit': qty_unit,
                            'price': price,
                            'tax': tax,
                            'sub_total': sub_total,
                        }
                        values.append(data)
            for val in values:
                count += 1
                sheet.write(row_date_count, 0, (count -2), title_style_left)
                sheet.write(row_date_count, 1, val['product_id'], title_style_left)
                sheet.write(row_date_count, 2, val['desc'], title_style_left)
                sheet.write(row_date_count, 3, val['hsn'], title_style_left)
                sheet.write(row_date_count, 4, val['qty'], title_style_left)
                sheet.write(row_date_count, 5, val['qty_unit'], title_style_left)
                sheet.write(row_date_count, 6, val['price'], title_style_left)
                sheet.write(row_date_count, 7, val['tax' ] , title_style_left)
                sheet.write(row_date_count, 8, (count - 2), title_style_left)
                row_date_count += 1
            stream = io.BytesIO()
            workbook.save(stream)
            attach_id = self.env['i.excel.output'].create({
                'name': "Invoice Excel",
                'filename': base64.encodestring(stream.getvalue())
            })
            return attach_id.download()