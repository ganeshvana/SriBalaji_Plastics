# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json
import datetime
import base64
from datetime import datetime
from json import dumps
from io import StringIO


class InvoiceJsonReport(models.Model):

    _name = 'account.invoice.json.report'

    @api.model
    def default_get(self, fields):
        account_obj = self.env['account.invoice']
        accounts = []
        res = super(InvoiceJsonReport, self).default_get(fields)
        active_ids = self._context.get('active_ids', [])

        for acc in account_obj.browse(active_ids):
            accounts.append(acc.id)

        res.update({'account_ids': [(6, 0, accounts)]})
        return res

    account_ids = fields.Many2many('account.invoice', string='Account Ids')

    @api.multi
    def get_json(self):

        acc_values = []
        browse = self.env['account.invoice'].search([('id', 'in', self.account_ids.ids)])
        for browse_account in browse:
            for account in browse_account:
                inv_dt = str(account.date_invoice)
                doc_dt = str(account.trans_doc_date)

                acc_data = {
                    'userGstin': account.company_id.vat,
                    'supplyType': account.supply_type,
                    'subSupplyType': account.sub_supply_type,
                    'transType': account.trans_type,
                    'docType': account.doc_type,
                    'docNo': account.doc_no,
                    'docDate': inv_dt,
                    'fromGstin': account.company_id.vat,
                    'fromTrdName': account.company_id.name,
                    'fromAddr1': account.company_id.street,
                    'fromAddr2': " ",
                    'fromPlace': account.company_id.city,
                    'fromPincode': account.company_id.zip,
                    'fromStateCode': account.company_id.state_id.code,
                    'actualFromStateCode': account.company_id.state_id.code,
                    'toGstin': account.partner_id.vat,
                    'toTrdName': account.partner_id.name,
                    'toAddr1': account.partner_id.street,
                    'toAddr2': "",
                    'toPlace': account.partner_id.city,
                    'toPincode': account.partner_id.zip,
                    'toStateCode': account.partner_id.state_id.code,
                    'actualToStateCode': account.partner_id.state_id.code,
                    'totalValue': account.amount_untaxed,
                    'gst': account.amount_tax,
                    'transMode': account.trans_mode,
                    'transDistance': account.trans_distance,
                    'transporterName': account.transporter_name,
                    'transporterId': account.transporterid,
                    'transDocNo': account.trans_doc_no,
                    'transDocDate': doc_dt,
                    'vehicleNo': account.vehicle_no,
                    'vehicleType': account.vehicle_type,

                    'totInvValue': account.amount_total,
                    'OthValue': account.othvalue,
                    'mainHsnCode': account.main_hsn_code

                }
                acc_values.append(acc_data)

        if "itemList" not in acc_data:
            acc_data.update({"itemList": []})
        browse = self.env['account.invoice'].search([('id', 'in', self.account_ids.ids)])
        for account_browse in browse:
            line_ids = account_browse.invoice_line_ids
            for line in line_ids:
                if line.invoice_line_tax_ids:
                    for tax in line.invoice_line_tax_ids:
                        tax_name = tax.name
                    line_items = {
                        'productName': line.product_id.name,
                        'productDesc': line.name,
                        'hsnCode': line.product_id.l10n_in_hsn_code,
                        'quantity': line.quantity,
                        'qtyUnit': line.uom_id.name,
                        'taxableAmount': line.price_unit,
                        'gst': tax_name,
                        'itemNo': line.sequence2
                    }
                    acc_data["itemList"].append(line_items)
                else:
                    line_items = {
                        'productName': line.product_id.name,
                        'productDesc': line.name,
                        'hsnCode': line.product_id.l10n_in_hsn_code,
                        'quantity': line.quantity,
                        'qtyUnit': line.uom_id.name,
                        'taxableAmount': line.price_unit,
                        'gst': " ",
                        'itemNo': line.sequence2
                    }
                    acc_data["itemList"].append(line_items)

        d = json.dumps(acc_values)

        attach_id = self.env['i.json.output'].create({
            'name': 'Invoice Json',
            'filename': base64.b64encode(bytes(d, "utf-8"))
        })
        return attach_id.download()
