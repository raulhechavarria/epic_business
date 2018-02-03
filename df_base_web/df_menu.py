'''
Created on May 21, 2013

@author: Shaka
'''
from openerp.osv.osv import osv
from openerp.osv import fields
import tools
from openerp import SUPERUSER_ID

class extended_ir_ui_menu(osv):
    _name = 'ir.ui.menu'
    _inherit = 'ir.ui.menu'
    _description = 'Extended menu'
    
    @tools.ormcache()
    def _find_hiders(self, cr, uid, context=None):
        
        hider_model = self.pool.get('ir.ui.menu.hider')
        hiders_ids = hider_model.search(cr, SUPERUSER_ID, ['!', ('id', 'in', ())])
        return hider_model.browse(cr, SUPERUSER_ID, hiders_ids, context=context)
    
    def _filter_visible_menus(self, cr, uid, ids, context=None):
        
        result = super(extended_ir_ui_menu, self)._filter_visible_menus(cr, uid, ids, context=context)
        _out = []
        for hider in self._find_hiders(cr, uid, context):
            _out += [x.id for x in hider.hidden_items]
        filtered = filter(lambda x: x not in _out, result)
        return filtered

extended_ir_ui_menu()

class ir_ui_menu_hider(osv):
    _name = 'ir.ui.menu.hider'
    _description = 'Hider for menu items'
    _columns = {
                'hidden_items': fields.many2many('ir.ui.menu', 'ir_ui_menu_hider_ir_ui_menu_rel', 'hide_id', 'hidden_id')
                }

ir_ui_menu_hider()
