#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the Christine project
#
# Copyright (c) 2006-2007 Marco Antonio Islas Cruz
#
# win32settings_manager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# win32settings_manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
# @package   win32settings_manager
# @author    Marco Antonio Islas Cruz <markuz@islascruz.org>
# @copyright 2010 Marco Antonio Islas Cruz
# @license   http://www.gnu.org/licenses/gpl.txt
'''
Created on Nov 12, 2010

@author: Marco Antonio Islas Cruz

This app connects with a server and ask for several settings, then
apply them on the system.
'''
import os
from libw32s.logger import LoggerManager
from libw32s.globalvars import PLUGINSDIR

class main():
    '''
    This class is the manager for the plugins. Will load them and
    launch them if they are enabled
    '''
    def __init__(self):
        self.logger = LoggerManager().getLogger('main')
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        '''
        Search for the files and then use the __importByName to load them
        '''
        files = os.listdir(PLUGINSDIR)
        filteredf = [k for k in files \
                    if os.path.isdir(os.path.join(PLUGINSDIR, k)) and \
                    k not in ('.svn',)]
        for pluginname in filteredf:
            plugin = self.__importByName('libw32s.Plugins.%s'%pluginname,
                                         pluginname)
            if not plugin:
                continue
            try:
                func = getattr(plugin,'main', False)
                if func:
                    instance = func()
                    self.plugins[instance.name] = instance
            except Exception, e:
                self.logger.exception(e)


    def __importByName(self,modulename,name = None):
        '''
        Import a module by its name

        @param modulename: name of the package to import
        @param name: name of the module to import
        '''
        if name == None:
            lname = []
        else:
            lname = [name]
        try:
            self.logger.info('Importing %s - %s'%(modulename, lname))
            module = __import__(modulename,
                        globals(), locals(), lname)
        except ImportError, e:
            self.logger.exception(e)
            return None
        return module

#Try to import plugins