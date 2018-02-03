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

{
    'name': 'Desoft Report Base',
    'version': '1.0',
    'category': 'Reporting Tools',
    'description': """This module allows users to print reports in 
        pdf and xls format on the view that has active.""",
    'author': 'Desoft',
    'maintainer': 'Desoft',
    'website': 'wwww.desoft.cu',
    'license': 'AGPL-3',
#    'depends': ['df_base', 'df_base_web'],
    'depends': ['df_base_web'],
    'data': [],
    'update_xml': [
                'security/report_base_security.xml',
                'security/ir.model.access.csv',
                'wizard/df_wizard_screen_config_view.xml',
                'view/df_report_main_menu.xml',
                    
    ],
    'js': [
        'static/js/web_advanced_export.js',
    ],
    'installable': True,
    'active': False,
    'auto_install': False,
    'application': False,
    'license': '',
}

