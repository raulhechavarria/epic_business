from openerp.report.interface import report_int
import openerp.pooler as pooler
import openerp.tools as tools
import addons

from openerp.report import render
from lxml import etree

import time, os
from report.printscreen.ps_list import report_printscreen_list as printer_list

import locale
from operator import itemgetter
from datetime import datetime
from tools.translate import _
from openerp.report import render, report_sxw


class report_printscreen_list(printer_list):
    def __init__(self, name):
        printer_list.__init__(self, name)

    
    def remove_repeat(self, element, collection):
        while collection.count(element) > 1:
            collection.remove(element)

    
    def explore_field(self, cr, uid, list_relation, model, context):
        pool = pooler.get_pool(cr.dbname)
        model_fields = pool.get('ir.model.fields')
        ids = model_fields.search(cr, uid, ['&', '&', ('name', '=', list_relation[0]), ('model', '=', model._name), ('ttype', 'not in', ['many2one', 'one2many', 'many2many'])])
        if ids:
            return model_fields.browse(cr, uid, ids, context)[0].field_description
        else:
            ids = model_fields.search(cr, uid, ['&', '&', ('name', '=', list_relation[0]), ('model', '=', model._name), ('ttype', '=', 'many2one')])
        
        list_relation.pop(0)
        model = pool.get(model_fields.browse(cr, uid, ids, context)[0].relation)
        
        return self.explore_field(cr, uid, list_relation, model, context)
        
        #model_field = 
    
    
    def result_criteria(self, fields, group, model, uid, cr, context):
        if not group:

            if len(fields) > 1:
                result = map(lambda * a: a[0][0], filter(lambda * b: isinstance(b[0], list), fields))
            else:
                result = map(lambda * a: a[0][0], fields)
        else:
            result = fields
 
        map(lambda * a: self.remove_repeat(a[0], result), result)
        fields = result
        relations = [x.split('.') for x in fields if x.find('.') != -1] 
        collection_desc = model.fields_get(cr, uid, fields, context)
        relations_desc = map(lambda * a: self.explore_field(cr, uid, a[0], model, context), relations)
        
        end_cad = ", ".join(map(lambda * a: a[0][1]['string'], collection_desc.items()))
        relations_desc.extend(end_cad.split(','))
        end_cad = ", ".join(map(lambda * a: a[0], relations_desc)) 
        return end_cad
    
    
    def create(self, cr, uid, ids, datas, context=None, only_select=False):
        if not context:
            context = {}
        self.cr = cr
        self.context = context
        self.groupby = context.get('group_by', [])
        self.groupby_no_leaf = context.get('group_by_no_leaf', False)
        dom = datas.get('_domain', [])
        pool = pooler.get_pool(cr.dbname)
        model = pool.get(datas['model'])
        field_manager = pool.get('ir.model.fields')
        model_id = pool.get('ir.model').search(cr, uid, [('model', '=', model._name)])
        
        view_id = datas['view_id']
        model_manager = pool.get('df.report.screen.config')
        found = model_manager.search(cr, uid, [('current_view_id', '=', view_id)])
        result = model.fields_view_get(cr, uid, view_type='tree', context=context)
        to_fields_order = []
        if found == []:
            model_desc = context.get('current_model_description', model._description)
            to_fields_order = self._parse_string(result['arch'])
        else:
            result_model_conf = model_manager.browse(cr, uid, found[0], context)
            model_desc = result_model_conf.current_view_title
            result_fields = [x.name for x in field_manager.browse(cr, uid, eval(result_model_conf.display_columns), context=context)]
            result_config = model.fields_get(cr, uid, result_fields , context=context)
            to_fields_order = [x for x in self._parse_string(result['arch']) if x in result_config.keys()]
        
        group_cad = filter_cad = ""
        
        if self.groupby:
            group_cad = self.result_criteria(self.groupby, True, model, uid, cr, context)
        if dom:
            filter_cad = self.result_criteria(dom, False, model, uid, cr, context)
        
        self.title = model_desc
        datas['ids'] = ids
        
        fields_order = self.groupby + to_fields_order
        if self.groupby != []:
            have_group = True
        else:
            have_group = False
        if self.groupby:
            rows = []
            def get_groupby_data(groupby=[], domain=[]):
                records = model.read_group(cr, uid, domain, fields_order, groupby , 0, None, context)
                for rec in records:
                    rec['__group'] = True
                    rec['__no_leaf'] = self.groupby_no_leaf
                    rec['__grouped_by'] = groupby[0] if (isinstance(groupby, list) and groupby) else groupby
                    for f in fields_order:
                        if f not in rec:
                            rec.update({f:False})
                        elif isinstance(rec[f], tuple):
                            rec[f] = rec[f][1]
                    rows.append(rec)
                    inner_groupby = (rec.get('__context', {})).get('group_by', [])
                    inner_domain = rec.get('__domain', [])
                    if only_select:
                        if datas['ids'] == []:
                            inner_domain.extend([('id', 'in', [])])
                        else:
                            inner_domain.extend([('id', 'in', datas['ids'])])
                    if inner_groupby:
                        get_groupby_data(inner_groupby, inner_domain)
                    else:
                        if self.groupby_no_leaf:
                            continue
                        child_ids = model.search(cr, uid, inner_domain)
                        res = model.read(cr, uid, child_ids, result['fields'].keys(), context)
                        #res.sort(lambda x, y: cmp(ids.index(x['id']), ids.index(y['id'])))
                        rows.extend(res)
            if len(ids):
                dom = [('id', 'in', ids)]
            else:
                dom = datas.get('_domain', [])
            #if self.groupby_no_leaf and len(ids) and not ids[0]:
            #    dom = datas.get('_domain', [])
            get_groupby_data(self.groupby, dom)
        else:
            if only_select:
                if datas['ids'] == []:
                    records = []
                else:
                    records = datas['ids']
                    
            else:   
                if datas['ids'] == []:
                    dom = datas.get('_domain', [])
                    records = model.search(cr, uid, dom, context=context)
                    datas['ids'] = records
                else:
                    records = datas['ids']                
            rows = model.read(cr, uid, records, result['fields'].keys(), context)
            ids2 = map(itemgetter('id'), rows) 

        res = self._create_table(uid, datas['ids'], result['fields'], fields_order, rows, context, group_cad, filter_cad, model_desc, self.groupby, have_group)
        return (self.obj.get(), 'pdf')
    
    
    def _create_table(self, uid, ids, fields, fields_order, results, context, group_cad, filter_cad, title='', list_groups=[], have_group=False):
        pageSize = [297.0, 210.0]

        new_doc = etree.Element("report")
        config = etree.SubElement(new_doc, 'config')
        groups_founds = []

        def _append_node(name, text):
            n = etree.SubElement(config, name)
            n.text = text

        #_append_node('date', time.strftime('%d/%m/%Y'))
        _append_node('date', time.strftime(str(locale.nl_langinfo(locale.D_FMT).replace('%y', '%Y'))))
        _append_node('PageSize', '%.2fmm,%.2fmm' % tuple(pageSize))
        _append_node('PageWidth', '%.2f' % (pageSize[0] * 2.8346,))
        _append_node('PageHeight', '%.2f' % (pageSize[1] * 2.8346,))
        _append_node('report-header', title)
        
        _append_node('filter_fields', _("Grouped by:"))
        _append_node('filter_content', group_cad)
        _append_node('group_fields', _("Filtered by:"))
        _append_node('group_content', filter_cad)

        _append_node('company', pooler.get_pool(self.cr.dbname).get('res.users').browse(self.cr, uid, uid).company_id.name)
        rpt_obj = pooler.get_pool(self.cr.dbname).get('res.users')
        rml_obj = report_sxw.rml_parse(self.cr, uid, rpt_obj._name, context)
        _append_node('header-date', str(rml_obj.formatLang(time.strftime("%Y-%m-%d"), date=True)) + ' ' + str(time.strftime("%H:%M")))
        l = []
        t = 0
        strmax = (pageSize[0] - 40) * 2.8346
        temp = []
        tsum = []
        for i in range(0, len(fields_order)):
            temp.append(0)
            tsum.append(0)
        ince = -1;
        for f in fields_order:
            s = 0
            ince += 1
            if fields[f]['type'] in ('date', 'time', 'datetime', 'float', 'integer'):
                s = 60
                strmax -= s
                if fields[f]['type'] in ('float', 'integer'):
                    temp[ince] = 1
            else:
                t += fields[f].get('size', 80) / 28 + 1

            l.append(s)
        for pos in range(len(l)):
            if not l[pos]:
                s = fields[fields_order[pos]].get('size', 80) / 28 + 1
                l[pos] = strmax * s / t

        _append_node('tableSize', ','.join(map(str, l)))

        header = etree.SubElement(new_doc, 'header')
        for f in fields_order:
            field = etree.SubElement(header, 'field')
            field.text = tools.ustr(fields[f]['string'] or '')

        lines = etree.SubElement(new_doc, 'lines')
        for line in results:
            node_line = etree.SubElement(lines, 'row')
            count = -1
            for f in fields_order:
                float_flag = 0
                count += 1
                if fields[f]['type'] == 'many2one' and line[f]:
                    if not line.get('__group'):
                        line[f] = line[f][1]
                if fields[f]['type'] == 'selection' and line[f]:
                    for key, value in fields[f]['selection']:
                        if key == line[f]:
                            line[f] = value
                            break
                if fields[f]['type'] in ('one2many', 'many2many') and line[f]:
                    line[f] = '( ' + tools.ustr(len(line[f])) + ' )'
                if fields[f]['type'] == 'float' and line[f]:
                    precision = (('digits' in fields[f]) and fields[f]['digits'][1]) or 2
                    prec = '%.' + str(precision) + 'f'
                    line[f] = prec % (line[f])
                    float_flag = 1

                if fields[f]['type'] == 'date' and line[f]:
                    new_d1 = line[f]
                    if not line.get('__group'):
                        format = str(locale.nl_langinfo(locale.D_FMT).replace('%y', '%Y'))
                        d1 = datetime.strptime(line[f], '%Y-%m-%d')
                        new_d1 = d1.strftime(format)
                    line[f] = new_d1

                if fields[f]['type'] == 'time' and line[f]:
                    new_d1 = line[f]
                    if not line.get('__group'):
                        format = str(locale.nl_langinfo(locale.T_FMT))
                        d1 = datetime.strptime(line[f], '%H:%M:%S')
                        new_d1 = d1.strftime(format)
                    line[f] = new_d1
                
                if fields[f]['type'] == 'datetime' and line[f]:
                    new_d1 = line[f]
                    if not line.get('__group'):
                        format = str(locale.nl_langinfo(locale.D_FMT).replace('%y', '%Y')) + ' ' + str(locale.nl_langinfo(locale.T_FMT))
                        d1 = datetime.strptime(line[f], '%Y-%m-%d %H:%M:%S')
                        new_d1 = d1.strftime(format)
                    line[f] = new_d1
                    
                if fields[f]['type'] == 'boolean' and line[f]:
                    line[f] = (_('Yes') if line[f] else _('No'))
                
                
                if line.get('__group'):
                    col = etree.SubElement(node_line, 'col', para='group', tree='no')
                else:
                    col = etree.SubElement(node_line, 'col', para='yes', tree='no')

                # Prevent empty labels in groups
                if f == line.get('__grouped_by') and line.get('__group') and not line[f] and not float_flag and not temp[count]:
                    col.text = line[f] = _('Undefined')
                    col.set('tree', _('undefined'))

                if (line[f] != None) and not have_group: 
                    col.text = tools.ustr(line[f] or '')
                    #if not tools.ustr(line[f] or '') in groups_founds:
                    #    groups_founds.append(tools.ustr(line[f] or ''))
                    #    col.text = tools.ustr(line[f] or '')

                    if float_flag:
                        col.set('tree', 'float')
                    if line.get('__no_leaf') and temp[count] == 1 and f != 'id' and not line['__context']['group_by']:
                        tsum[count] = float(tsum[count]) + float(line[f])
                    if not line.get('__group') and f != 'id' and temp[count] == 1:
                        tsum[count] = float(tsum[count]) + float(line[f]);
                
                if (line[f] != None) and have_group:
                    if line[f] and (f in list_groups):
                        if not tools.ustr(line[f] or '') in groups_founds:
                            groups_founds.append(tools.ustr(line[f] or ''))
                            col.text = tools.ustr(line[f] or '')


                    if line[f] and (not f in list_groups):
                        col.text = tools.ustr(line[f] or '')


                    if float_flag:
                        col.set('tree', 'float')
                    if line.get('__no_leaf') and temp[count] == 1 and f != 'id' and not line['__context']['group_by']:
                        tsum[count] = float(tsum[count]) + float(line[f])
                    if not line.get('__group') and f != 'id' and temp[count] == 1:
                        tsum[count] = float(tsum[count]) + float(line[f]);
                
                
                if line[f] == None:
                    col.text = '/'
                #else:
                #   col.text = '/'

        node_line = etree.SubElement(lines, 'row')
        for f in range(0, len(fields_order)):
            col = etree.SubElement(node_line, 'col', para='group', tree='no')
            col.set('tree', 'float')
            if tsum[f] != None:
                if tsum[f] != 0.0:
                    digits = fields[fields_order[f]].get('digits', (16, 2))
                    prec = '%%.%sf' % (digits[1],)
                    total = prec % (tsum[f],)
                    txt = str(total or '')
                else:
                    txt = str(tsum[f] or '')
            else:
                txt = '/'
            if f == 0:
                txt = 'Total'
                col.set('tree', 'no')
            col.text = tools.ustr(txt or '')
        
        transform = etree.XSLT(etree.parse(addons.get_module_path('df_report_base') + "/report/custom_new.xsl"))
        rml = etree.tostring(transform(new_doc))
        self.obj = render.rml(rml, title=self.title)
        self.obj.render()
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

