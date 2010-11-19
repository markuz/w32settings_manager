#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the Christine project
#
# Copyright (c) 2006-2007 Marco Antonio Islas Cruz
#
# Christine is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Christine is distributed in the hope that it will be useful,
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
import time
import thread
import os
from globalvars import USERDIR
import SOAPpy
import urllib
from libw32s.config import conf
'''
Created on Nov 12, 2010

@author: Marco Antonio Islas Cruz

This Plugin connect with the server and then try to set the new wallpaper

'''


class main():
    '''
    This Plugin connect with the zerver and then try to set the new 
    wallpaper..
    
    @requires: The webserver capable to respond to default_wallpaper.
    '''
    def __init__(self):
        self.service = None
        self.conf = conf()
        thread.start_new(self.__try_to_create_client, tuple())

    def __try_to_create_client(self):
        while True:
            self.__create_client()
            if self.service:
                thread.start_new(self.__ask_forever,tuple())
            time.sleep(10)
    
    def __create_client(self):
        host = self.conf['/webservice/host']
        port = self.conf['/webservice/port']
        self.service = SOAPpy.SOAPProxy("%s:%s"%(host, port))
    
    def __ask_forever(self):
        wallpaperurl = self.service.default_wallpaper()
        if not wallpaperurl.startswith("http"):
            self.logger.warning('The url \'%s\' is not a valid url')
        webfile = urllib.urlopen(wallpaperurl)
        wallpapername = wallpaperurl.split("/")[-1]
        filepath = os.path.join(USERDIR, wallpapername)
        file = open(filepath, 'w')
        file.write(webfile.read())
        file.close()
        webfile.close()
        for i in ('reg add "hkcu\control panel\desktop" /v wallpaper /t REG_SZ /d "" /f ',
                  'RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters ',
                  'reg add "hkcu\control panel\desktop" /v wallpaper /t REG_SZ /d "%s" /f'%filepath,
                  'UNDLL32.EXE user32.dll,UpdatePerUserSystemParameters ',
                  ):
            os.system(i)
            return True