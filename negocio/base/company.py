from osv import fields, osv
from tools import ustr
from tools.translate import _
from tools import re



class company(osv.osv):
    _name = "res.company"
    _inherit = 'res.company'
    _description = "This class contains information about a company"
    _order = "name"
    
    def _get_address_data(self, cr, uid, ids, field_names, arg, context=None):
        return super(company, self)._get_address_data(cr, uid, ids, field_names, arg, context)

    def _set_address_data(self, cr, uid, company_id, name, value, arg, context=None):
        return super(company, self)._set_address_data(cr, uid, company_id, name, value, arg, context)
                
    _columns = {
        'code': fields.char('Code', size=10, required=True, help="The UEB code in three chars.\n")
        , 'nit_code': fields.related('partner_id', 'nit_code', string="NIT code", type="integer", size=11, required=True)  
        , 'reeup_code': fields.related('partner_id', 'reeup_code', string="REEUP code", type="char", size=64, required=True) 
        , 'municipality_id': fields.function(_get_address_data, fnct_inv=_set_address_data, type='many2one', domain="[('state_id', '=', state_id)]", relation='res.state.municipality', string="Municipality", multi='address') 
        , 'is_ueb_add': fields.boolean('Is an UEB ?', help="Check this box if the partner is an UEB.")
        , 'organization_id': fields.many2one('organization', 'Organization', ondelete='set null', select=True)

        , 'agenc_cup': fields.char('Agencia en CUP', size=64)
        , 'agenc_cuc': fields.char('Agencia en CUC', size=64)
        , 'account_cup': fields.char('Cuenta en CUP', size=64)
        , 'account_cuc': fields.char('Cuenta en CUC', size=64)
        , 'registro_comercial': fields.char('Registro Comercial', size=64)
        , 'representante_id': fields.many2one('hr.employee', 'Representante')
        
       

    }
    _constraints = [
    ]
    _sql_constraints = [
    ]
    _defaults = {
      'code': 666           
    }
    
    def create(self, cr, uid, vals, context=None):
        company_id = super(company, self).create(cr, uid, vals, context=context)
        if vals.get('nit_code', False) or vals.get('reeup_code', False):
            obj_partner = self.pool.get('res.partner')
            company = self.read(cr, uid, company_id, ['partner_id'], context)
            obj_partner.write(cr, uid, company['partner_id'][0], {'nit_code': vals['nit_code'], 'reeup_code': vals['reeup_code'], }, context=context)
        return company_id
    
company()
