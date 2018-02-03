# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv
from osv import fields
import sys
import re
import smtplib
import openerp.tools as tools
from tools.translate import _


class df_wizard_screen_config(osv.osv_memory):
    _name = "df.wizard.screen.config"
    _description = "Configuration for screen report from current View"
    
    
    def _internal_obtain(self, cr, uid, model_manager, field_manager, model_set, fields_set, context=None):
        found = model_manager.search(cr, uid, [('model', '=', model_set)])
        if found == []:
            return []
        else:
            model_created = self.pool.get(model_set)
            result = field_manager.search(cr, uid, ['&', ('model', '=', model_set), ('name', 'in', fields_set)] , context=context)
            if len(result) == len(fields_set):
                return result
               
            if (len(result) < len(fields_set)) and (len(result) > 0):
                new_fields_set = [item for item in fields_set if item not in [obj.name for obj in field_manager.browse(cr, uid, result, context)]]
                for (key, value) in model_created._inherits.items():
                    model_set = key
                    result.extend(self._internal_obtain(cr, uid, model_manager, field_manager, model_set, new_fields_set, context))
            if result == []:
                for (key, value) in model_created._inherits.items():
                    model_set = key
                    result.extend(self._internal_obtain(cr, uid, model_manager, field_manager, model_set, fields_set, context))
        return result
    
   
    def _get_columns(self, cr, uid, ids, field_name, arg, context):
        model_manager = self.pool.get('ir.model')
        field_manager = self.pool.get('ir.model.fields')
        model_set = context.get('current_model', '')
        fields_set = context.get('visible_fields', '')
        res = self._internal_obtain(cr, uid, model_manager, field_manager, model_set, fields_set, context)
        if ids:
            return dict((id, str(res)) for id in ids)
        return str(res)
    
    def _get_stored_columns(self, cr, uid, context):
        columns_manager = self.pool.get('df.report.screen.config')
        col_rows = columns_manager.search(cr, uid, [('current_view_id', '=', context.get('view_id', False))], context=context)
        displays = columns_manager.browse(cr, uid, col_rows, context=context)
        evaluated_columns = []
        if displays:
            evaluated_columns = eval(displays[0].display_columns)
        field_manager = self.pool.get('ir.model.fields')
        fields_rows = field_manager.search(cr, uid, [('id', 'in', evaluated_columns)], context=context)
        if len(fields_rows) == len(evaluated_columns):
            return evaluated_columns
        return fields_rows
    
    
    def _get_title(self, cr, uid, context):
        model_manager = self.pool.get('df.report.screen.config')
        found = model_manager.search(cr, uid, [('current_view_id', '=', context.get('view_id', False))])
        if found == []:
            res = context.get('current_model_description', _("This model no have name"))
        else:
            result = model_manager.browse(cr, uid, found[0], context)
            res = result.current_view_title
        return res 


    _columns = {
                'display_columns_ids': fields.many2many('ir.model.fields', 'columns_screen_report_rel', 'screen_id', 'field_id', 'Columns to display in screen report'),
                'current_view_title': fields.text('Title', required=True),
                'function_columns_ids':fields.function(_get_columns, method=True, string='Columns to display in screen report', type='text'),
                }
    
    _defaults = {
        'display_columns_ids': _get_stored_columns,
        'current_view_title': _get_title,
        'function_columns_ids': lambda self, cr, uid, context: self._get_columns(cr, uid, None, None, None, context) 
    }
    
    
    def save_screen_config(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        
        model_manager = self.pool.get('df.report.screen.config')
        config_val = {}
        config_val['current_view_title'] = data['current_view_title']
        config_val['current_view_id'] = context.get('view_id', False)
        config_val['display_columns'] = str(data['display_columns_ids'])

        found = model_manager.search(cr, uid, [('current_view_id', '=', context.get('view_id', False))])
        if not found:
            model_manager.create(cr, uid, config_val, context=context)
        else:
            model_manager.write(cr, uid, found, config_val, context=context)   
        
        values = {'type':'ir.actions.act_window_close'}
        return values    
     
      
df_wizard_screen_config()



class df_action_manager(osv.osv):
    _name = "df.action.manager"
    _description = "Manager for actions"

    _columns = {

    }
    
    def return_action_id(self, cr, uid, model, context=None):
        action_obj = self.pool.get("ir.actions.act_window")
        value = action_obj.search(cr, uid, [("res_model", "=", model)], context)
        return value

   
df_action_manager()
