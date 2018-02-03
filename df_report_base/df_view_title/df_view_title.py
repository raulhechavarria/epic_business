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



class df_view_title(osv.osv):
     _name = "df.view.title"
     _description = "Title for current View"

     _columns = {
        'current_view_title': fields.text('Title', required=True),
        'current_view_id': fields.many2one('ir.ui.view', 'Identifier of View', ondelete='cascade', required=True),
    }

#     def _validate_fields(self, cr, uid, values, context):
#         if values.has_key('name'):
#             regex = re.match("^([\w])+([\s]|[\w])*$", values['current_view_title'])
#             if not regex:
#                 raise osv.except_osv(_('Error'), _("The description just accept letters and numbers!"))
#         return True
#
#
#
#
#     def create(self, cr, uid, values, context=None):
#         if self._validate_fields(cr, uid, values, context):
#             aux = super(df_view_title, self).create(cr, uid, values, context=context)
#         return aux
#
#     def write(self, cr, uid, ids, values, context=None):
#         if self._validate_fields(cr, uid, values, context):
#             return super(df_view_title, self).write(cr, uid, ids, values, context=None)
df_view_title()
