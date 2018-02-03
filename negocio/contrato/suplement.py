from osv import fields, osv

class suplement(osv.osv):
    _name = 'suplement'
    _rec_name = 'no_suplement'
    _description = 'Detalles del suplemento'
    _columns = {
        'no_suplement': fields.char('No. suplemento', size=10,  required=True),
        'date_suplement': fields.date('Fecha Suplemento', required=True),
        'represent': fields.many2one('hr.employee', 'Representante', select=True),
        'place_ids': fields.one2many('place.list.suplement', 'suplement_id', 'Listado de lugares de entrega'),
        'product_ids':fields.one2many('product.list.suplement', 'suplement_id', 'Information', required=False, ondelete='cascade'),
        'no_contract': fields.many2one('contract', 'No. Contrato',  required=True),
        'description': fields.text('Comentario'),

        'clausulas_lista':fields.one2many('clausulas.lista.suplement', 'suplement_id', 'clausulas', required=True),
        'state':fields.selection([
           ('draft','Borrador'),
           ('confirmed','Confirmado'),
           ('canceled','Cancelado')
           ], 'Estado', readonly=False, )
        
    }
    
    _defaults = {
        'state': 'draft'
    } 

    def change_confirm(self, cr, uid, ids, *args):
        self.write(cr, uid, ids,{'state':'confirmed'})
        return True

    def change_cancel(self, cr, uid, ids, *args):
        self.write(cr, uid, ids,{'state':'canceled'})
        return True

     


suplement()

class place_list_suplement(osv.osv):
    _name = 'place.list.suplement'
    _description = 'Listado de lugares de entrega del suplemento'
    _columns = {
        'place_id': fields.many2one('res.partner.address', 'Lugar de entrega', select=True),
        'suplement_id': fields.many2one('suplement', 'Suplemento', select=True),
        'sales_person': fields.many2one('hr.employee', 'Vendedor', select=True),
        }
place_list_suplement()


class product_list_suplement(osv.osv):
    _name = 'product.list.suplement'
    _description = 'Listado de productos del suplemento'
    _columns = {
        'product_id': fields.many2one('product.product', 'Descripcion', select=True),
        'suplement_id': fields.many2one('suplement', 'Suplemento', select=True),
        'count': fields.integer('Cantidad', size=11),
        'description': fields.text('Nota'),
        }
product_list_suplement()

class clausulas_lista_suplement(osv.osv):
    _name = 'clausulas.lista.suplement'
    _description = 'clausulas del suplemento'
    _columns = {
        'suplement_id': fields.many2one('suplement', 'Suplemento', select=True),
        'description': fields.text('Nota'),
        }
clausulas_lista_suplement()
