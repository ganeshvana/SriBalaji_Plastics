from odoo import api, fields, models

class InheritAccountInvoice(models.Model):
    _inherit = 'account.invoice'

    supply_type = fields.Char(string="Supply Type")
    sub_supply_type = fields.Char(string="Sub Supply Type")
    trans_type = fields.Char(string="Trans Type")
    doc_type = fields.Char(string="Doc Type")
    doc_no = fields.Char(string="Doc No")
    trans_mode = fields.Char(string="Trans Mode")
    trans_distance = fields.Char(string="Trans Distance")
    transporter_name = fields.Char(string="Transporter Name")
    transporterid = fields.Char(string="Transporter Id")
    trans_doc_no = fields.Char(string="Trans Doc No")
    trans_doc_date = fields.Date(string="Trans Doc Date")
    vehicle_no = fields.Char(string="vehicle No")
    vehicle_type = fields.Char(string="Vehicle Type")
    othvalue = fields.Char(string="Other Value")
    main_hsn_code = fields.Char(string="Main Hsn Code")

    # @api.one
    # @api.depends('total_item')
    # def compute_total_item(self):
    #     for account in self:
    #         for lines in account.invoice_line_ids:
    #             self.total_item += lines.item_no
    #             print (self.total_item, "self.total_itemself.total_itemself.total_itemself.total_itemself.total_itemself.total_item")
    #
    # total_item = fields.Integer("Total Item",  compute='compute_total_item', store=True, invisible = 1)

    @api.multi
    @api.depends('invoice_line_ids')
    def _compute_max_line_sequence(self):
        """Allow to know the highest sequence entered in invoice lines.
        Then we add 1 to this value for the next sequence.
        This value is given to the context of the o2m field in the view.
        So when we create new invoice lines, the sequence is automatically
        added as :  max_sequence + 1
        """
        for invoice in self:
            invoice.max_line_sequence = (
                    max(invoice.mapped('invoice_line_ids.sequence') or [0]) + 1)

    max_line_sequence = fields.Integer(string='Max sequence in lines',
                                       compute='_compute_max_line_sequence',
                                       store=True)

    @api.multi
    def _reset_sequence(self):
        for rec in self:
            current_sequence = 1
            for line in rec.invoice_line_ids:
                line.sequence = current_sequence
                current_sequence += 1

    @api.multi
    def write(self, values):
        res = super(InheritAccountInvoice, self).write(values)
        self._reset_sequence()
        return res

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    sequence = fields.Integer(help="Shows the sequence of this line in the "
                              " invoice.", default=9999)

    # shows sequence on the invoice line
    sequence2 = fields.Integer(help="Shows the sequence of this line in the "
                               " invoice.", related='sequence', readonly=True,
                               store=True)

    item_no = fields.Integer("Item No", default=1, invisible=1)