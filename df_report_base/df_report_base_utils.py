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
from osv import fields, osv
from tools.translate import _
import addons
#YEAR CON SIGLO
DATE_FORMAT_YMD1 = '%Y-%m-%d' # 1
DATE_FORMAT_YMD2 = '%Y/%m/%d' # 2

DATE_FORMAT_DMY1 = '%d-%m-%Y' # 3
DATE_FORMAT_DMY2 = '%d/%m/%Y' # 4

DATE_FORMAT_MDY1 = '%m-%d-%Y' # 5
DATE_FORMAT_MDY2 = '%m/%d/%Y' # 6

#YEAR SIN SIGLO
DATE_FORMAT_YMD11 = '%y-%m-%d' # 11
DATE_FORMAT_YMD21 = '%y/%m/%d' # 21

DATE_FORMAT_DMY11 = '%d-%m-%y' # 31
DATE_FORMAT_DMY21 = '%d/%m/%y' # 41

DATE_FORMAT_MDY11 = '%m-%d-%y' # 51
DATE_FORMAT_MDY21 = '%m/%d/%y' # 61


#--------------------------------------------------------
#--------------------------------------------------------
class df_report_base_utils(osv.osv):
    _name ='df.report.base.utils'
    
    def get_number_date(self,cr,uid,ids,*arg):
        dicc={}
        user = self.pool.get('res.users').browse(cr, uid, uid, context=None)
        lang = user.context_lang
        lang_pool = self.pool.get('res.lang')
        lang_id = lang_pool.search(cr, uid, [('code','=',lang)], context=None)
        format = lang_pool.read(cr, uid, lang_id, ['date_format'], context=None)[0]['date_format']  
        n = 4
        
        if format==DATE_FORMAT_YMD1 : n = 1
        if format==DATE_FORMAT_YMD2 : n = 2
        
        if format==DATE_FORMAT_DMY1 : n = 3
        if format==DATE_FORMAT_DMY2 : n = 4
        
        if format==DATE_FORMAT_MDY1 : n = 5
        if format==DATE_FORMAT_MDY2 : n = 6
        
        
        if format==DATE_FORMAT_YMD11 : n = 11
        if format==DATE_FORMAT_YMD21 : n = 21
        
        if format==DATE_FORMAT_DMY11 : n = 31
        if format==DATE_FORMAT_DMY21 : n = 41
        
        if format==DATE_FORMAT_MDY11 : n = 51
        if format==DATE_FORMAT_MDY21 : n = 61
        
        dicc['format_date_number'] = n
        return dicc
#--------------------------------------------------------
#--------------------------------------------------------  
