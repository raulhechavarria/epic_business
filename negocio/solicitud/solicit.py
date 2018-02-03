from osv import fields, osv

class solicit(osv.osv):
    _name = 'solicit'
    _description = 'Detalles de la solicitud'
    _rec_name = 'no_contract'
    _columns = {
        'solicit_type': fields.selection((
            ('prefabricado','Prefabricado'),
            ('hormigon_premesclado','Hormigon_premesclado'),
            ), 'Tipo de solicitud', required=True, select=True),
        'no_solicit': fields.char('No. Solicitud', size=10,  required=True),
        'new_contract': fields.boolean('Nuevo Contrato', help="Esta solicitud es para un contrato nuevo"),
        'no_suplement': fields.many2one('suplement', 'No. Suplemento'),
        'responsable': fields.many2one('hr.employee', 'Responsable', select=True),
        'client_id': fields.many2one('res.partner', 'No. Cliente', select=True),
        'date_limit': fields.date('Fecha Limite', required=True),
        'object_ids': fields.one2many('object.obra', 'solicit_id', 'Objetos de Obras'),
        'element_ids':fields.one2many('element', 'solicit_id', 'Solicitud de elementos', required=False, ondelete='cascade'),
        'resource_client': fields.boolean('Recursos entregados por el cliente', help="?Los recursos son entregados por el propio cliente?"),
        'description': fields.text('Descripcion'),
        }
solicit()

class object_obra(osv.osv):
    _name = 'object.obra'
    _description = 'Listado de Objetos de Obras'
    _columns = {
        'solicit_id': fields.many2one('solicit', 'solicitud', select=True),
        'name': fields.char('Nombre de la obra', size=100,  required=True),
        'description': fields.text('Descripcion'),
        'state':fields.selection([
           ('iniciada','iniciada'),
           ('en_proceso','en_proceso'),
           ('terminada','terminada')
           ], 'Estado', readonly=False, )
        
        }
object_obra()

class element(osv.osv):
    _name = 'element'
    _description = 'Listado de elementos'
    _columns = {
        'product_id': fields.many2one('product.product', 'Descripcion', select=True),
        'solicit_id': fields.many2one('solicit', 'solicitud', select=True),
        'count': fields.integer('Cantidad', size=11),
        'description': fields.text('Nota'),
        }
element()