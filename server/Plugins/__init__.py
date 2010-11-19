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
from libw32server.webservice import webservice
from libw32server.config import config

class Plugin(object):
    '''
    This is the base class for the plugins
    '''
    def __init__(self):
        self.enabled_key = ''
        self.webservice = webservice()
        self.config = config()
    
    def get_enabled(self):
        return self.conf.get_value(self.enabled_key)
    def set_enabled(self,value):
        return self.conf.set_value(self.enabled_key, bool(value))

    enabled = property(get_enabled, set_enabled, None, 
                       'If the plugin is enabled or not')