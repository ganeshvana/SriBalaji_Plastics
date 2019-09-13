# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
from openerp.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    state_id = fields.Many2one(
#         "res.country.state",
#         string='State',
        required=True
    )
    
    @api.onchange('state_id')
    def onchange_state_id(self):
        self.country_id = self.state_id.country_id

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        user_gst_state_code = str(res.vat)[:2]
        gst_state_code = res.state_id.l10n_in_tin
        
        if res.vat:
            if not res.state_id:
                raise UserError(
                        _("Please Add the State in the Address")
                    )
            if user_gst_state_code != gst_state_code:
                raise UserError(
                            _("Your GST code is not matching with the State!")
                        )
        return res

    @api.multi
    def write(self, vals):
        result = super(ResPartner, self).write(vals)
        for record in self:
            user_gst_state_code = str(record.vat)[:2]
            gst_state_code = record.state_id.l10n_in_tin
    
            if record.vat:
                if not self.state_id:
                    raise UserError(
                            _("Please Add the State in the Address")
                        )
                if user_gst_state_code != gst_state_code:
                    raise UserError(
                                _("Your GST code is not matching with the State!")
                            )
        return result