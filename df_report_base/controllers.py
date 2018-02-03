# -*- coding: utf-8 -*-
try:
    import json
except ImportError:
    import simplejson as json

try:
    import xlwt
except ImportError:
    xlwt = None
from web.controllers.main import Reports
from web.controllers.main import ExcelExport
from web.controllers.main import Binary
from web.controllers.main import View
from web.controllers.main import Action
from my_ps_list import report_printscreen_list as printer_tree
from my_ps_form import report_printscreen_list as printer_form
from web import common
from xlwt import *
from cStringIO import StringIO
from lxml  import etree
import openerp.pooler as pooler
import web.common.http as openerpweb
import re
import base64
import addons

class ViewParser():
    
    def __init__(self, context):
        self.context = context
        self.groupby = context.get('group_by', [])
    
    def _parse_node(self, root_node):
        result = []
        for node in root_node:
            field_name = node.get('name')
            if not eval(str(node.attrib.get('invisible', False)), {'context':self.context}):
                if node.tag == 'field':
                    if field_name in self.groupby:
                        continue
                    result.append(field_name)
                else:
                    result.extend(self._parse_node(node))
        return result
    
    def _parse_string(self, view):
        try:
            dom = etree.XML(view.encode('utf-8'))
        except:
            dom = etree.XML(view)
        return self._parse_node(dom)
    


class ExcelExportView(ExcelExport):
    _cp_path = '/web/export/xls_view'

    
    def from_data(self, fields, rows, field_indexes):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('Sheet 1')
        fnt = Font()
        fnt.name = 'Arial'
        fnt.size = 12
        fnt.outline = True
        fnt.bold = True
        
        borders = Borders()
        borders.bottom = 2
        
        style = XFStyle()
        style.font = fnt
        style.borders = borders
        
        for i, fieldname in enumerate(fields):
            worksheet.write(0, i, fieldname, style)
            worksheet.col(i).width = 8000
            
        style = xlwt.easyxf('align: wrap yes')
        
        row_index = 0
        
        for row in rows:
            cell_index = 0
            for order in field_indexes:
                cell_value = row[order]
                if isinstance(cell_value, basestring):
                    cell_value = re.sub("\r", " ", cell_value)
                if isinstance(cell_value, tuple):
                    cell_value = cell_value[1]
                if cell_value is False: cell_value = None
                worksheet.write(row_index + 1, cell_index, cell_value, style)
                cell_index += 1
            row_index += 1

        fp = StringIO()
        workbook.save(fp)
        fp.seek(0)
        data = fp.read()
        fp.close()
        return data
    
    @openerpweb.httprequest
    def index(self, req, data, token):
        values = json.loads(data)
        model = values.get('model', "")
        domain = values.get('domain', [])
        ids = values.get('ids', [])
        context = values.get("context", {})
        groupby = context.get('group_by', [])
        groupby_no_leaf = context.get('group_by_no_leaf', False)
        uid = req.session._uid

        cr = pooler.get_db(req.session._db).cursor()
        model_manager = pooler.get_pool(cr.dbname).get(model)
        result = []
        
        to_display = model_manager.fields_view_get(cr, uid, view_type='tree', context=context)
        view_parser = ViewParser(context)
        fields_order = groupby + view_parser._parse_string(to_display['arch'])
        if groupby:
            rows = []
            def get_groupby_data(groupby=[], domain=[]):
                records = model_manager.read_group(cr, uid, domain, fields_order, groupby , 0, None, context)
                for rec in records:
                    rec['__group'] = True
                    rec['__no_leaf'] = groupby_no_leaf
                    rec['__grouped_by'] = groupby[0] if (isinstance(groupby, list) and groupby) else groupby
                    for f in fields_order:
                        if f not in rec:
                            rec.update({f:False})
                        elif isinstance(rec[f], tuple):
                            rec[f] = rec[f][1]
                    rows.append(rec)
                    inner_groupby = (rec.get('__context', {})).get('group_by', [])
                    inner_domain = rec.get('__domain', [])
                    if inner_groupby:
                        get_groupby_data(inner_groupby, inner_domain)
                    else:
                        if groupby_no_leaf:
                            continue
                        child_ids = model_manager.search(cr, uid, inner_domain)
                        res = model_manager.read(cr, uid, child_ids, to_display['fields'], context)
                        res.sort(lambda x, y: cmp(ids.index(x['id']), ids.index(y['id'])))
                        rows.extend(res)
            dom = [('id', 'in', ids)]
            if groupby_no_leaf and len(ids) == 0:
                dom = domain
            get_groupby_data(groupby, dom)
        else:
            rows = model_manager.read(cr, uid, ids, fields_order, context)
        
        temp_headers = model_manager.fields_get(cr, uid, fields_order, context=context)
        columns_headers = []
        for item in fields_order:
            columns_headers.append(temp_headers[item]['string'])
        
        return req.make_response(self.from_data(columns_headers, rows, fields_order),
            headers=[('Content-Disposition', 'attachment; filename="%s"' % self.filename(model)),
                     ('Content-Type', self.content_type)],
            cookies={'fileToken': int(token)})

class PDFExportView(Reports):
    _cp_path = '/df_report_base/export'
    
    @openerpweb.httprequest
    def pdf_view(self, req, data, token):
        values = json.loads(data);
        action = values.get("action", {})
        ids = values.get("ids", [])
        only_select = values.get("only_select", [])
        view_id = values.get("view_id", False)

        context = values.get("context", {})
        model = values.get("model", "")
        view_type = values.get("view_type", "tree")
        
        if view_type == "tree" :
            if context.has_key('group_by') and (not isinstance(context['group_by'], list)):
                context['group_by'] = [context.get('group_by', "")]
        
        datas = {}
        datas['model'] = model
        datas['_domain'] = values.get('domain', [])
        datas['view_id'] = view_id
        cr = pooler.get_db(req.session._db).cursor()
        checked_report = False
        
        if view_type == "tree" : 
            printer_tree.remove("report." + (model or "screen"))
            obj_print = printer_tree("report." + (model or "screen"))
            checked_report = obj_print.create(cr, req.session._uid, ids, datas, context, only_select)
        if view_type == "form" : 
            printer_form.remove("report." + (model or "screen"))
            obj_print = printer_form("report." + (model or "screen"))
            checked_report = obj_print.create(cr, req.session._uid, ids, datas, context)

        return req.make_response(checked_report[0],
                    headers=[('Content-Disposition', 'attachment; filename="%s"' % (context.get('current_model_description', datas['model']) + "." + checked_report[1])),
                            ('Content-Type', checked_report[1])],
                            cookies={'fileToken': int(token)})

  
    @openerpweb.httprequest
    def pdf_full_view(self, req, data, token):
        values = json.loads(data);
        action = values.get("action", {})
        ids = values.get("ids", [])
        view_id = values.get("view_id", False)

        context = values.get("context", {})
        model = values.get("model", "")
        view_type = values.get("view_type", "tree")
        
        if view_type == "tree" :
            if context.has_key('group_by') and (not isinstance(context['group_by'], list)):
                context['group_by'] = [context.get('group_by', "")]
        
        datas = {}
        datas['model'] = model
        datas['_domain'] = values.get('domain', [])
        datas['view_id'] = view_id
        cr = pooler.get_db(req.session._db).cursor()
        checked_report = False
        
        if view_type == "tree" : 
            printer_tree.remove("report." + (model or "screen"))
            obj_print = printer_tree("report." + (model or "screen"))
            checked_report = obj_print.create(cr, req.session._uid, ids, datas, context)

        return req.make_response(checked_report[0],
                    headers=[('Content-Disposition', 'attachment; filename="%s"' % (context.get('current_model_description', datas['model']) + "." + checked_report[1])),
                            ('Content-Type', checked_report[1])],
                            cookies={'fileToken': int(token)})


class Binary(Binary):  
    _cp_path = "/web/binary/saveas_ajax"
    
    @openerpweb.httprequest
    def index(self, req, data, token):
        jdata = json.loads(data)
        model = jdata['model']
        field = jdata['field']
        id = jdata.get('id', None)
        filename_field = jdata.get('filename_field', None)
        context = jdata.get('context', dict())

        context = req.session.eval_context(context)
        Model = req.session.model(model)
        fields = [field]
        if filename_field:
            fields.append(filename_field)
        if id:
            res = Model.read([int(id)], fields, context)[0]
        else:
            res = Model.default_get(fields, context)
        if res.has_key('file') and  res.has_key('filename'):
            if not res['file']:
                res.pop('file')
            if not res['filename']:
                res.pop('filename')
        filecontent = base64.b64decode(res.get(field, ''))
        if not filecontent:
            exit
            #return req.make_response(None, headers=[], cookies={}) 
        if filecontent:
            filename = '%s_%s' % (model.replace('.', '_'), id)
            if filename_field:
                filename = res.get(filename_field, '') or filename
            return req.make_response(filecontent,
                headers=[('Content-Type', 'application/octet-stream'),
                        ('Content-Disposition', 'attachment; filename="%s"' % filename)],
                cookies={'fileToken': int(token)})
