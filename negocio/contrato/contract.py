from osv import fields, osv

class contract(osv.osv):
    _name = 'contract'
    _description = 'Detalles del contrato'
    _rec_name = 'no_contract'
    _columns = {
        'no_contract': fields.char('No. contrato', size=10,  required=True),
        'date_contract': fields.date('Fecha Contratacion', required=True),
        'represent': fields.many2one('hr.employee', 'Representante', select=True,  required=True, help='Es el representante de la empresa Contratada'),
        'place_ids': fields.one2many('place.list', 'contract_id', 'Listado de lugares de entrega'),
        'product_ids':fields.one2many('product.list', 'contract_id', 'Lista de productos', required=False),
        'description': fields.text('Comentario'),
        'partner_id': fields.many2one('res.partner', 'Cliente', select=True,  required=True),

        'fecha_vencimiento': fields.date('Fecha de Vencimiento', required=True),
        'clausulas_lista':fields.one2many('clausulas.lista', 'contract_id', 'Clausulas', required=True),
        'responsable': fields.many2one('hr.employee', 'Responsable', select=True,  required=True, help='El responsable del contrato'),
        'state':fields.selection([
           ('draft','Borrador'),
           ('confirmed','Confirmado'),
           ('canceled','Cancelado')
           ], 'Estado', readonly=False, )
        
    }
    
    _defaults = {
        'state': 'draft'       
    }
    
    _sql_constraints = [
        ('name_uniq', 'unique(no_contract)', 'El numero de contrato debe ser unico'),
    ]
	
    def change_confirm(self, cr, uid, ids, *args):
        self.write(cr, uid, ids,{'state':'confirmed'})
        return True

    def change_cancel(self, cr, uid, ids, *args):
        self.write(cr, uid, ids,{'state':'canceled'})
        return True

    

contract()

class place_list(osv.osv):
    _name = 'place.list'
    _description = 'Listado de lugares de entrega de los productos contratados'
    _columns = {
        'place_id': fields.many2one('res.partner.address', 'Lugar de entrega', select=True),
        'contract_id': fields.many2one('contract', 'Contratacion', select=True),
        'sales_person': fields.many2one('hr.employee', 'Vendedor', select=True),
        }
place_list()

class product_list(osv.osv):
    _name = 'product.list'
    _description = 'Listado de productos a entregar'
    _columns = {
        'product_id': fields.many2one('product.product', 'Descripcion', select=True),
        'contract_id': fields.many2one('contract', 'Contratacion', select=True),
        'count': fields.integer('Cantidad', size=11),
        'description': fields.text('Nota'),
        }
product_list()
            
class clausulas_lista(osv.osv):
    _name = 'clausulas.lista'
    _description = 'clausulas del contrato'
    _columns = {
        'contract_id': fields.many2one('contract', 'Contratacion', select=True),
        'no_clausula': fields.char('No. Clausula', size=10,  required=True),
        'description': fields.text('Nota'),
        }
clausulas_lista()
