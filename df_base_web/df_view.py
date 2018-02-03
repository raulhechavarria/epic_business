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

from osv import fields, osv
from osv.orm import except_orm, browse_record
from osv.orm import BaseModel

from lxml import etree
from tools.translate import _

import os
import tools
import logging
import datetime

from web import common
openerpweb = common.http
from web.controllers.main import parse_domain

_logger = logging.getLogger(__name__)


'''
 This is an extension to add options to ir.ui.view fields so latter can be used 
to propagate this options to the View Widgets like ListView

Created on Aug 7, 2012

@author: aek
'''

_logger = logging.getLogger(__name__)

class ir_ui_view(osv.osv):
    _name = 'ir.ui.view'
    _inherit = 'ir.ui.view'

    def _check_xml(self, cr, uid, ids, context=None):
        for view in self.browse(cr, uid, ids, context):
            eview = etree.fromstring(view.arch.encode('utf8'))
            frng = tools.file_open(os.path.join('df_base_web', 'static', 'src', 'xml', 'view.rng'))
            try:
                relaxng_doc = etree.parse(frng)
                relaxng = etree.RelaxNG(relaxng_doc)
                if not relaxng.validate(eview):
                    for error in relaxng.error_log:
                        _logger.error(tools.ustr(error))
                    return False
            finally:
                frng.close()
        return True

    _constraints = [
        (_check_xml, 'Invalid XML for View Architecture!', ['arch'])
    ]

ir_ui_view()


def change_validate():

    def _validate(self, cr, uid, ids, context=None):
        context = context or {}
        lng = context.get('lang', False) or 'en_US'
        trans = self.pool.get('ir.translation')
        error_msgs = []
        for constraint in self._constraints:
            fun, msg, fields = constraint
            if not fun(self, cr, uid, ids):
                # Check presence of __call__ directly instead of using
                # callable() because it will be deprecated as of Python 3.0
                if hasattr(msg, '__call__'):
                    tmp_msg = msg(self, cr, uid, ids, context=context)
                    if isinstance(tmp_msg, tuple):
                        tmp_msg, params = tmp_msg
                        translated_msg = tmp_msg % params
                    else:
                        translated_msg = tmp_msg
                else:
                    translated_msg = trans._get_source(cr, uid, self._name,
                                                'constraint', lng, msg) or msg
                error_msgs.append(translated_msg)
                self._invalids.update(fields)
        if error_msgs:
            cr.rollback()
            raise except_orm(_('ValidateError'), '\n'.join(error_msgs))
        else:
            self._invalids.clear()
    
    setattr(BaseModel, '_validate', _validate)

change_validate()

class ViewExt(openerpweb.Controller):
    _cp_path = "/web/tools"
    
    @openerpweb.jsonrequest
    def build_domain(self, req, domain):
        return parse_domain(domain, req.session)

def change_read_group():
    f = getattr(BaseModel, 'read_group')
    setattr(BaseModel, 'old_read_group', f)

    def read_group(self, cr, uid, domain, fields, groupby, offset=0, limit=None, context=None, orderby=False):
        data = self.old_read_group(cr, uid, domain, fields, groupby, offset, limit, context, orderby)
        if groupby:
            if isinstance(groupby, list):
                groupby = groupby[0]
            fget = self.fields_get(cr, uid, fields)
            if data and groupby in data[0] and fget[groupby]['type'] in ('date', 'datetime'):
                monthnames = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                              'August', 'September', 'October', 'November', 'December']
                months = dict.fromkeys(range(1, 13), False)
                for d in data:
                    dt = datetime.datetime.strptime(d[groupby], '%B %Y')
                    if not months[dt.month]:
                        months[dt.month] = _(monthnames[dt.month - 1])
                    d[groupby] = "%s %s"  % (months[dt.month], dt.year)
        return data

    setattr(BaseModel, 'read_group', read_group)

change_read_group()

