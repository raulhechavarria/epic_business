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

from osv import osv
import os
from os.path import join as opj
import zipfile
import modules
import logging

_logger = logging.getLogger(__name__)

class df_module(osv.osv):
    _inherit = 'ir.module.module'

    def update_translations(self, cr, uid, ids, filter_lang=None, context=None):
        context2 = context or {'overwrite': True}
        ids.sort()
        super(df_module, self).update_translations(cr, uid, ids, filter_lang, context2)
df_module() 

'''
 Replace get_modules function from openerp.modules.module.py in order to
load modules according to dependency graph. This allow to load translations
on the suitable order
 
Created on Sep 5, 2013

@author: Roberto
'''

def change_get_modules():
    
    def get_modules():
        """Returns the list of module names
        """
        def listdir(ad_dir):
            def clean(name):
                name = os.path.basename(name)
                if name[-4:] == '.zip':
                    name = name[:-4]
                return name
        
            def is_really_module(name):
                name = opj(ad_dir, name)
                return os.path.isdir(name) or zipfile.is_zipfile(name)
            return map(clean, filter(is_really_module, os.listdir(ad_dir)))
        
        plist = []
        res = []
        packages = {}
        modules.module.initialize_sys_path()
        for ad in modules.module.ad_paths:
            plist.extend(listdir(ad))
        plist=list(set(plist))
        for package in plist:
            info = modules.module.load_information_from_description_file(package)
            if info:
                if len(info['depends']):
                    packages[package]=info
                else:
                    res.append(package)
        plist = packages.keys()
        while len(plist):
            package = plist.pop(0)
            info = packages[package]
            info['depends'] = filter(lambda m: m not in res, info['depends'])
            if len(info['depends']):
                unmet_deps = filter(lambda m: m not in plist, info['depends'])
                if len(unmet_deps):
                    _logger.error('module %s: Unmet dependencies: %s', package, ', '.join(unmet_deps))
                else:
                    plist.append(package)
            else:
                res.append(package)
        return res
    
    setattr(modules, 'get_modules', get_modules)
    setattr(modules.module, 'get_modules', get_modules)

change_get_modules()

