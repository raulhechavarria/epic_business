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
	 'name'        : 'negocio_epi',
	 'version'     : '1.0.0',
	 'category'    : 'Administracion de negocio de la EPIC',
	 'description' : 'Subsistema de Gestión de la Negociación en la Empresa de Producción Industrial de Camagüey',
	 'author'      : 'Anailis Pardo Cangas',
	 'maintainer'  : '',
	 'website'     : '',
	 'license'     : '',
	 'installable' : True,
	 'application' : True,
	 'active'      : False,
	 'depends': [
			'base',
			'product',
            'hr',
            'df_report_base',

#			'base_report_designer',
     ],
	 'init_xml': [
     ],
	 'update_xml': [
#		'security/security.xml',
#      	'security/ir.model.access.csv',
        
#  board
		'contrato/view/board_contract.xml',
#  board

		'base/view/partner_view.xml',
        'base/view/product_view.xml',        
		'base/view/obra_view.xml',   
		'base/export_import/df_sicpt_export_data_view.xml',
        'base/export_import/df_sicpt_import_data_view.xml',
		'base/view/menu_view.xml',
        
        
        
		'contrato/view/contract_view.xml',
		'contrato/view/suplement_view.xml',
        'contrato/view/menu_view.xml',
        
        
        'solicitud/view/solicit_view.xml',
        'solicitud/view/offer_view.xml',
        'solicitud/view/menu_view.xml',
		
		
        
#        'data/productive_entity_data.xml',
#        'data/company_data.xml',
#        'data/product_category_data.xml',
#        'data/product_data.xml',
        ],
	 'demo_xml': [
     ],
	 'test': [
     ]
}
