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
    'name': "E-way Bill",
    'summary': """Invoice Json & Excel Reports""",
    'description': """E-way Bill, Invoice Json & Excel Reports""",
    "version": "12.0",
    "category": "Invoice",
    'author' : 'Oodu Implementers Private Limited',
    "website": "http://www.oodouimplementers.com",
    'installable': True,
    'images': ['static/description/gst_logo.png'],
    "depends": ['base', 'account'],
    "data": ['security/ir.model.access.csv', 'views/invoice_extend_view.xml', 'views/invoice_view.xml'],
}
