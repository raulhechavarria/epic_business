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

import tools
import logging
import openerp.pooler as pooler
from osv import osv
from workflow import wkf_expr
import inspect
import types


_logger = logging.getLogger(__name__)

'''
 This is an extension to allow the search for a similar translation when the original one not found

Created on May 16, 2013

@author: aek
'''

class df_translation(osv.osv):
    _name = 'ir.translation'
    _inherit = 'ir.translation'
    
    @tools.ormcache(skiparg=3)
    def _get_source(self, cr, uid, name, types, lang, source=None):
        """
        Returns the translation for the given combination of name, type, language
        and source. All values passed to this method should be unicode (not byte strings),
        especially ``source``.

        :param name: identification of the term to translate, such as field name (optional if source is passed)
        :param types: single string defining type of term to translate (see ``type`` field on ir.translation), or sequence of allowed types (strings)
        :param lang: language code of the desired translation
        :param source: optional source term to translate (should be unicode)
        :rtype: unicode
        :return: the request translation, or an empty unicode string if no translation was
                 found and `source` was not passed
        """
        # FIXME: should assert that `source` is unicode and fix all callers to always pass unicode
        # so we can remove the string encoding/decoding.
        if not lang:
            return u''
        if isinstance(types, basestring):
            types = (types,)
        if source:
            query = """SELECT value 
                       FROM ir_translation 
                       WHERE lang=%s 
                        AND type in %s 
                        AND src=%s"""
            params = (lang or '', types, tools.ustr(source))
            if name:
                query += " AND name=%s"
                params += (tools.ustr(name),)
            cr.execute(query, params)
        else:
            cr.execute("""SELECT value
                          FROM ir_translation
                          WHERE lang=%s
                           AND type in %s
                           AND name=%s""",
                    (lang or '', types, tools.ustr(name)))
        res = cr.fetchone()
        trad = res and res[0] or u''
        if source and not trad:
            cr.execute("""SELECT value
                          FROM ir_translation
                          WHERE lang=%s
                           AND lower(src)=lower(%s)""",
                    (lang or '', tools.ustr(source)))
            res = cr.fetchone()
            trad = res and res[0] or u''
            if source and not trad:
                trad = tools.ustr(source)
        return trad
    
    @tools.ormcache_multi(skiparg=3, multi=6)
    def _get_ids(self, cr, uid, name, tt, lang, ids):
        translations = dict.fromkeys(ids, False)
        if ids:
            cr.execute('select res_id,value ' \
                    'from ir_translation ' \
                    'where lang=%s ' \
                        'and type=%s ' \
                        'and name=%s ' \
                        'and res_id IN %s',
                    (lang,tt,name,tuple(ids)))
            for res_id, value in cr.fetchall():
                translations[res_id] = value
            for res_id in translations.keys():
                res_value = translations.get(res_id, False)
                if not res_value:
                    res_model,res_field = name.split(',')
                    cr.execute('select '+res_field +' from '+ \
                        self.pool.get(res_model)._table +' where id=%s ',
                        (res_id,))
                    source = cr.fetchone()
                    source = source and source[0] or u''
                    cr.execute("""SELECT value
                          FROM ir_translation
                          WHERE lang=%s
                           AND lower(src)=lower(%s)""",
                    (lang or '', tools.ustr(source)))
                    res = cr.fetchone()
                    trad = res and res[0] or u''
                    if source and not trad:
                        trad = tools.ustr(source)
                    translations[res_id] = trad
        return translations
df_translation()

"""
    The following is to pass the context to the browse method in workflows 
    actions to allow the translation of messages in the scope of those actions
"""

class Envi(dict):
    def __init__(self, cr, uid, model, ids):
        pool = pooler.get_pool(cr.dbname)
        
        self.cr = cr
        self.uid = uid
        self.model = model
        self.ids = ids
        self.obj = pool.get(model)
        self.columns = self.obj._columns.keys() + self.obj._inherit_fields.keys()
        
        user_pool = pool.get('res.users')
        user_data = user_pool.read(cr, uid, uid, ['context_lang'])
        
        self.context = {'lang': user_data['context_lang']}
        
    def __getitem__(self, key):
        if (key in self.columns) or (key in dir(self.obj)):
            attr = getattr(self.obj, key, False)
            args = [self.cr, self.uid, self.ids[0]]
            if isinstance(attr, (types.MethodType, types.LambdaType, types.FunctionType)) \
               and 'context' in inspect.getargspec(attr)[0]:
                args.append(self.context) 
            res = self.obj.browse(*args)
            return res[key]
        else:
            return super(Envi, self).__getitem__(key)
        
wkf_expr.Env = Envi