from osv import fields, osv
from tools.translate import _
#----------------------------------------------------------
# Organitations
#----------------------------------------------------------

class organization(osv.osv):
       
    _name = 'organization'
    _description = 'Organizations' 
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True)
        , 'description': fields.char('Description', size=300)
        }
   
organization()
