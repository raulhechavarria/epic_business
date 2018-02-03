# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
'''
This extension allows you to restrict the views in which an 
action(report, wizard, window) will be displayed.

Created on Jul 23, 2013

@author: Ann  

'''

from osv import osv,fields
import openerp.addons.web.controllers.main as webmain
     
class ir_values_filter(osv.osv):
    _name = 'ir.values.filter'
    _columns =  {
         'ir_values_id':fields.many2one('ir.values', 'Value', required=True, 
                                        ondelete='cascade'),
         'ir_ui_view_id':fields.many2one('ir.ui.view', 'View', required=True, 
                                         ondelete='cascade')
    }
ir_values_filter()
 
class ir_values(osv.osv):
    _name = 'ir.values'
    _inherit = 'ir.values'
    _columns =  {
        'ir_values_filter_ids':fields.one2many('ir.values.filter',
                                               'ir_values_id', 'Values Filter')
    }
ir_values()

def change_fields_view_get():
    def fields_view_get(self, req, model, view_id, view_type,
                        transform=True, toolbar=False, submenu=False):
        Model = req.session.model(model)
        context = req.session.eval_context(req.context)
        fvg = Model.fields_view_get(view_id, view_type, context, toolbar, 
                                    submenu)
        # todo fme?: check that we should pass the evaluated context here
        self.process_view(req.session, fvg, context, transform, 
                          (view_type == 'kanban'))
        if toolbar and transform:
            Values = req.session.model('ir.values')
            Values_Filter = req.session.model('ir.values.filter')
            toolbar_copy = fvg['toolbar'].copy()
            ir_values_type = {
                'print': 'client_print_multi',
                'action': 'client_action_multi',
                'relate': 'client_action_relate'
            }
            def pass_action(self, action, act_type):
                value = action['type'] + "," + str(action['id'])
                search_value = Values.search_read([('model', '=', model),
                    ('value', '=', value),
                    ('key2', '=', ir_values_type[act_type])],
                    ['ir_values_filter_ids'], context = context)[0]
                ir_values_filter_ids = search_value.get('ir_values_filter_ids', 
                                                        False)
                permit_view_ids = []
                if ir_values_filter_ids:
                    dict_permit_view = Values_Filter.read(ir_values_filter_ids,
                                                    ['ir_ui_view_id'],context)
                    permit_view_ids = [x['ir_ui_view_id'][0] \
                                       for x in dict_permit_view]  
                return not permit_view_ids or view_id in permit_view_ids
            for act_type,actions in toolbar_copy.items():
                filter_actions =  filter(lambda action: pass_action(model, 
                                            action, act_type),actions)\
                                                if actions else actions
                fvg['toolbar'][act_type]= filter_actions 
            self.process_toolbar(req, fvg['toolbar'])
        return fvg    
    setattr(webmain.View, 'fields_view_get', fields_view_get)
change_fields_view_get()
