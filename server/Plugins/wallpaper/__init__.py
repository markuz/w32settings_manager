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
Created on Nov. 15, 2010

This module answers the default_wallpaper function call.
@author: Marco Antonio Islas Cruz
'''
from libw32server.Plugins import Plugin
from libw32server.Logger import LoggerManager

class wallpaper(Plugin):
    def __init__(self):
        self.enabled_key = '/plugins/wallaper/enabled'
        self.logger = LoggerManager().getLogger('plugins_wallpaper')
        #Check if the plugin is installed or not.
        if not self.config.get_value('/core/version') >= (0,1,0):
            self.logger.error('Not the valid database for the plugin')
        self.__proceed()
    
    def __proceed(self):
        if not self.check_installed():
            self.__install_plugin()
        self.webservice.register_function(self.default_wallpaper)
        self.webservice.register_function(self.set_default_wallpaper)
    
    def __install_plugin(self):
        self.config.setValue('/plugins/wallpaper/default_url', '')
    
    def default_wallpaper(self):
        '''
        This function returns the default wallpaper url. This is very likely
        to be over a http server or any other know methods by urllib (maybe ftp)
        '''
        if not self.available:
            return ''
        try:
            return self.conf.get_value('/plugins/wallpaper/default_url')
        except:
            return ''
        
    def set_default_wallpaper(self, url):
        '''
        This method set the default wallpaper url in database
        @param url:
        '''
        self.conf.set_value('/plugins/wallpaper/default_url',url)
        return True