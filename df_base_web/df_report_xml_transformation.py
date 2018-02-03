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
#from osv.orm import except_orm, browse_record
#from addons.base.ir.ir_translation import ir_translation

from web import common
openerpweb = common.http
from web.controllers.main import Reports
from openerp.pooler import get_db_and_pool

import simplejson
import base64
import time
import zlib


import logging
from lxml import etree

_logger = logging.getLogger(__name__)

'''
 This is an extension to allow to extends openerp reports via XPath transformations

Created on Jun 4, 2013

@author: aek
'''

class df_report_xml_transformation(osv.osv):
    _name = "ir.actions.report.xml.transformation"
    
    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
        'xpath': fields.char('XPath', size=256, required=True ),
        'position': fields.selection((
            ('inside','inside'),
            ('replace','replace'),
            ('after','after'),
            ('before', 'before'),
            ('attributes', 'attributes'),), 'Content Position', required=True, select=True),
        'content': fields.text('Content'),
        'report_id': fields.many2one('ir.actions.report.xml', 'Report xml', required=True, ondelete='cascade', select=True),
    }
df_report_xml_transformation()


class df_report_xml_process(osv.osv):
    _name = "ir.actions.report.xml.process"

    _columns = {
        'name': fields.char('Name', size=64, required=True, translate=True),
        'model': fields.char('XPath', size=256, required=True ),
        'method': fields.char('XPath', size=256, required=True ),
        'report_id': fields.many2one('ir.actions.report.xml', 'Report xml', required=True, ondelete='cascade', select=True)
    }

df_report_xml_process()

class df_report_xml(osv.osv):
    _name="ir.actions.report.xml"
    _inherit ="ir.actions.report.xml"
    
    def _report_content(self, cr, uid, ids, name, arg, context=None):
        def encode(s):
            if isinstance(s, unicode):
                return s.encode('utf8')
            return s
        res = super(df_report_xml, self)._report_content(cr, uid, ids, name, arg, context=context)
        for res_id in res.keys():
            if res[res_id] != False:
                transformation_ids = self.browse(cr, 1, res_id, context=context).transformation_ids
                if transformation_ids:
                    source = etree.fromstring(encode(res[res_id]))
                    for trans in transformation_ids:
                        nodes = source.xpath(trans.xpath)
                        for node in nodes:
                            if node is not None:
                                pos = trans.position
                                data = etree.fromstring(encode("<data>"+trans.content+"</data>"))
                                for content in data:
                                    if pos == 'replace':
                                        if node.getparent() is None:
                                            source = content
                                        else:
                                            node.addprevious(content)
                                            node.getparent().remove(node)
                                    elif pos == 'attributes':
                                        for child in content.getiterator('attribute'):
                                            attribute = (child.get('name'), child.text and child.text.encode('utf8') or None)
                                            if attribute[1]:
                                                node.set(attribute[0], attribute[1])
                                            else:
                                                del(node.attrib[attribute[0]])
                                    elif pos == 'inside':
                                        node.append(content)
                                    elif pos == 'after':
                                        node.addnext(content)
                                        node = content
                                    elif pos == 'before':
                                        node.addprevious(content)
                                    else:
                                        _logger.info('Skiped transformation due to invalid position value', trans.name)
                                        continue
                            else:
                                _logger.info('Skiped transformation due to invalid xpath expression', trans.name)
                    res[res_id] = etree.tostring(source, encoding="utf-8").replace('\t', '')
                process_ids = self.browse(cr, 1, res_id, context=context).process_ids
                if process_ids:
                    source = etree.fromstring(encode(res[res_id]))
                    for proc in process_ids:
                        source = getattr(self.pool.get(proc.model),proc.method)(cr, uid, res_id, source, context)
                    res[res_id] = etree.tostring(source, encoding="utf-8").replace('\t', '')
        return res
    
    def _report_content_inv(self, cursor, user, ids, name, value, arg, context=None):
        self.write(cursor, user, ids, {name+'_data': value}, context=context)
        
    _columns = {
        'transformation_ids': fields.one2many('ir.actions.report.xml.transformation', 'report_id', 'Report Transformations'),
        'report_rml_content': fields.function(_report_content, fnct_inv=_report_content_inv, type='binary', string='RML content'),
        'attachment': fields.char('Save As Attachment Prefix', size=128, translate=True,
                                  help='This is the filename of the attachment used to store the printing result. Keep empty to not save the printed reports. You can use a python expression with the object and time variables.'),
        'process_ids': fields.one2many('ir.actions.report.xml.process', 'report_id', 'Report Process'),
    }
df_report_xml()

def change_report_index():

    @openerpweb.httprequest
    def index(self, req, action, token):
        action = simplejson.loads(action)

        report_srv = req.session.proxy("report")
        context = req.session.eval_context(
            common.nonliterals.CompoundContext(
                req.context or {}, action[ "context"]))

        report_data = {}
        report_ids = context["active_ids"]
        if 'report_type' in action:
            report_data['report_type'] = action['report_type']
        if 'datas' in action:
            if 'ids' in action['datas']:
                report_ids = action['datas'].pop('ids')
            report_data.update(action['datas'])

        report_id = report_srv.report(
            req.session._db, req.session._uid, req.session._password,
            action["report_name"], report_ids,
            report_data, context)

        report_struct = None
        while True:
            report_struct = report_srv.report_get(
                req.session._db, req.session._uid, req.session._password, report_id)
            if report_struct["state"]:
                break

            time.sleep(self.POLLING_DELAY)

        db, pool = get_db_and_pool(req.session._db)
        cr = db.cursor()
        uid = req.session._uid
        lng = context.get('lang', False) or 'en_US'
        trans = pool.get('ir.translation')
        action['report_name'] = trans._get_source(cr, uid, 'ir.actions.report.xml',
                                                  'model', lng, 
                                                  action['report_name']) or action['report_name']
        report = base64.b64decode(report_struct['result'])
        if report_struct.get('code') == 'zlib':
            report = zlib.decompress(report)
        report_mimetype = self.TYPES_MAPPING.get(
            report_struct['format'], 'octet-stream')
        return req.make_response(report,
             headers=[
                 ('Content-Disposition', 'attachment; filename="%s.%s"' % (action['report_name'], report_struct['format'])),
                 ('Content-Type', report_mimetype),
                 ('Content-Length', len(report))],
             cookies={'fileToken': int(token)})
    
    setattr(Reports, 'index', index)

change_report_index()
