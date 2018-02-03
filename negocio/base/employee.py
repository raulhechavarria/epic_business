#from osv import fields, osv
#from tools import ustr
#import addons
#from tools.translate import _
#from tools import re
#
#class employee(osv.osv):
#    
#
#
#    def _get_full_name(self, cr, uid, ids, name=None, arg=None, context=None):
#        res = {}
#        for emp in self.browse(cr, uid, ids, context):
#            res[emp.id] = '%s %s %s' % (emp.name , emp.middle_name or "" , emp.last_name or "")
#        return res
#    
#    _name = "hr.employee"
#    _description = "Employee"
#    _inherit = 'hr.employee'
#    _columns = {
#        'full_name': fields.function(_get_full_name, type='char', string='Full Name',store=False),
#        'middle_name': fields.char('Middle Name', size=60),
#        'last_name': fields.char('Last Name', size=60)
#    }
#    
#employee()