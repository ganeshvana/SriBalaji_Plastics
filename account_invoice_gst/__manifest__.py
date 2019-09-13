# -*- coding: utf-8 -*-
#########################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-TODAY Pseudo code. (<http://pseudocode.co>).

#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version. You can not redistribute or sale
#    without permission of Pseudo code. (<http://pseudocode.co>).

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################################
{
    'name': "GST Invoice",
    'summary': """GST Invoice""",
    'description': """
GST Invoice for Accounting purpose and report

Indian Accounting
GST
Indian GST
GST Report
GST Tax

    """,
    'author' : 'oodu implementers Pvt Ltd',
    'website': 'https://www.ooduimplementers.com',
    'category': 'Accounting & Finance',
    'version': '11.0',
    'depends': ['account'],
    'images': ['static/description/gst_logo.png'],
    'data': [
        'security/ir.model.access.csv',
        'report/gst_invoice_reg.xml',
        'report/gst_tax_invoice_view.xml',
        'views/account_invoice.xml',
        'views/product_view.xml',
        'views/product_gst_view.xml',
        'views/account_invoice_line_view.xml',
        'views/account_tax_view.xml',
        'views/product_category_view.xml',
    ],
}
