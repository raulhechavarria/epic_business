# -*- coding: utf-8 -*-
##############################################################################
from osv import osv

class ir_ui_menu(osv.osv):
    _inherit = 'ir.ui.menu'

    def read_image(self, path):
        if not path:
            return False
        path_info = path.split(',')
        if len(path_info) < 2:
            return False
        return super(ir_ui_menu, self).read_image(path) 

ir_ui_menu()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

