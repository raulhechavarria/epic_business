from osv import fields, osv
from tools import ustr
from tools.translate import _
from tools import re

#----------------------------------------------------------
# Partner
#----------------------------------------------------------

class partner(osv.osv):
    
    _name = "res.partner"
    _inherit = 'res.partner'
    _description = "This class contains information about a partner"    
    _columns = {
        'municipality': fields.related('address', 'municipality_id', type='many2one', relation='res.state.municipality', string='Municipality' )
        , 'code': fields.char('Code', size=10)
        , 'state': fields.related('address', 'state_id', type='many2one', relation='res.country.state', string='Fed. State')
        , 'nit_code': fields.integer('NIT code', size=11)
        , 'reeup_code': fields.char('REEUP code', size=64)
        , 'agenc_cup': fields.char('Agencia en CUP', size=64)
        , 'agenc_cuc': fields.char('Agencia en CUC', size=64)
        , 'account_cup': fields.char('Cuenta en CUP', size=64)
        , 'account_cuc': fields.char('Cuenta en CUC', size=64)
        , 'sector' : fields.selection([
                ('gubernamental', 'Gubernamental'),
                ('private', 'Private')],'Sector')
        , 'organization_id': fields.many2one('organization', 'Organization',  ondelete='set null', select=True)
        , 'productive_id': fields.many2one('productive.entity.type', 'Productive Entity Type')
        , 'padre_id': fields.many2one('res.partner', 'Empresa padre', select=True)
        , 'registro_comercial': fields.char('Registro Comercial', size=64)
        , 'representante_id': fields.many2one('hr.employee', 'Representante')
    }
    
    
    _defaults = {
        'supplier': lambda *a: 0,
        'customer': lambda *a: 1
    }    
    _constraints = [
    ]
    _sql_constraints = [
    ]
    
partner()


class state_municipality(osv.osv):
    _name = 'res.state.municipality'
    _description="This class contains information about a state municipality"
    _columns = {
        'state_id': fields.many2one('res.country.state', 'Provincia',required=True),
        'name': fields.char('Municipality name', size=64, required=True),
        'code': fields.char('Municipality code', size=3, help='The muncipality code in three chars.\n', required=True)
    }
   
    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        ids = self.search(cr, user, [('code', 'ilike', name)] + args, limit=limit,
                context=context)
        if not ids:
            ids = self.search(cr, user, [('name', operator, name)] + args,
                    limit=limit, context=context)
        return self.name_get(cr, user, ids, context)

    _order = 'code'
state_municipality()


class partner_address(osv.osv):
    _name = "res.partner.address"
    _inherit = 'res.partner.address'
    _description = "This class contains information about a partner's address"    
    _columns = {
        'municipality_id': fields.many2one("res.state.municipality", 'Municipality', domain="[('state_id','=',state_id)]")
    }
    _constraints = [
    ]
    _sql_constraints = [
    ]
partner_address()
    