from osv import fields, osv

#----------------------------------------------------------
# Productively
#----------------------------------------------------------
class productive_entity_type(osv.osv):
       
    _name = 'productive.entity.type'
    _description = 'Tipo de Empresa Productiva'
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True)
        , 'description': fields.char('Description', size=300)
        }
   
productive_entity_type()