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


class df_report_screen_config(osv.osv):
     _name = "df.report.screen.config"
     _description = "Columns to display from current View"

     _columns = {
        'current_view_title': fields.text('Title', required=True),
        'display_columns': fields.text('Columns to display in screen report'),
        'current_view_id': fields.many2one('ir.ui.view', 'Identifier of View', ondelete='cascade', required=True),
    }
     

df_report_screen_config()
