# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    e_commerce_gst = fields.Char(
        string="E-commerce GSTIN",
        size=15,
    )
    reversed_charged = fields.Selection(
        [('y', 'Yes'), ('n', 'No')],
        string="Reverse Charge(Y/N)",
        default="n"
    )

    @api.multi
    def number_to_words(self, n):
        words = ''

        units = ['', 'One', 'Two', 'Three', 'Four', 'Five',
                'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven',
                'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen',
                'Seventeen', 'Eighteen', 'Nineteen']
        tens = ['', 'Ten', 'Twenty', 'Thirty', 'Forty', 'Fifty',
                'Sixty', 'Seventy', 'Eighty', 'Ninety']

        for group in ['', 'hundred', 'thousand', 'lac', 'crore']:

            if group in ['', 'thousand', 'lac']:
                n, digits = n // 100, n % 100
            elif group == 'hundred':
                n, digits = n // 10, n % 10
            else:
              digits = n

            if digits in range (1, 20):
                words = units [digits] + ' ' + group + ' ' + words
            elif digits in range (20, 100):
                ten_digit, unit_digit = digits // 10, digits % 10
                words = tens [ten_digit] + ' ' + units [unit_digit] + ' ' + group + ' ' + words
            elif digits >= 100:
                words = number_to_words (digits) + ' crore ' + words
        words = words + 'Rupees Only'
        return words
