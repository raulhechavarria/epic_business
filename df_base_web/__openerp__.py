# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010 OpenERP s.a. (<http://openerp.com>).
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
    'name': 'Desoft Base Web',
    'version': '1.0',
    'category': 'tools',
    'description': """Modulo de Mejoras y Cambios al modulo web de OpenERP""",
    'author': 'desoft s.a.',
    'website': 'www.desoft.cu',
    'depends': ['base', 'web', 'web_graph','web_kanban','web_dashboard'],
    'update_xml': [
        'security/ir.model.access.csv',
        'view/df_report_xml_transformation.xml',
    ],
    'js': [
        'static/src/js/utils.js',
        'static/src/js/views.js',
        'static/src/js/fields.js',
        'static/src/js/boot.js',
    ],
    'css': [
        'static/src/css/styles.css'
    ],
    'qweb': ['static/src/xml/template.xml'
    ],
    'active': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
