from osv import fields, osv

class suplement(osv.osv):
    _name = 'suplement'
    _description = 'Detalles del contrato'
    _columns = {
        'no_suplement': fields.char('No. suplemento', size=10,  required=True),
        'date_suplement': fields.date('Fecha Contratacion', required=True),
        'represent': fields.many2one('hr.employee', 'Representante', select=True),
        'place_ids': fields.one2many('place.list.suplement', 'suplement_id', 'Listado de lugares de entrega'),
        'product_ids':fields.one2many('product.list.suplement', 'product_id', 'Information', required=False, ondelete='cascade'),
        'no_contract': fields.many2one('contract', 'No. Contrato'),
        'description': fields.text('Comentario'),
        }
suplement()

class place_list_suplement(osv.osv):
    _name = 'place.list.suplement'
    _description = 'Listado de lugares de entrega'
    _columns = {
        'place_id': fields.many2one('res.partner', 'Lugar de entrega', select=True),
        'suplement_id': fields.many2one('suplement', 'Suplemento', select=True),
        'sales_person': fields.many2one('hr.employee', 'Vendedor', select=True),
        }
place_list_suplement()


class product_list_suplement(osv.osv):
    _name = 'product.list.suplement'
    _description = 'Listado de lugares de entrega'
    _columns = {
        'product_id': fields.many2one('product.product', 'Descripcion', select=True),
        'suplement_id': fields.many2one('suplement', 'Suplemento', select=True),
        'count': fields.integer('Cantidad', size=11),
        'description': fields.text('Nota'),
        }
product_list_suplement()
