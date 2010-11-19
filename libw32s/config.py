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
# @author    Marco Antonio Islas Cruz <markuz@islascruz.org>
# @copyright 2006-2008 Christine Development Group
# @license   http://www.gnu.org/licenses/gpl.txt
from ConfigParser import ConfigParser
from libw32s.Singleton import Singleton
from libw32s.Logger import LoggerManager
from libw32s.translate import translate
from libw32s.squitedb import sqlite3db
from libw32s.globalvars import CONFIGFILE
import os
import sys



class config(Singleton):
    '''
    This module is in charge to save all configurations. Server uses
    a sqlite database file.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.filepath = CONFIGFILE
        self.configParser = ConfigParser()
        self.db = sqlite3db()
        self.__notify = {}
        if os.path.exists(self.filepath):
            if not os.path.isfile(self.filepath):
                msg = _('%s is not a file'%self.filepath)
                sys.stderr.write(msg)
            f = open(self.filepath)
            self.configParser.readfp(f)
            f.close()
        else:
            self.create_basic_config_file()

    def setValue(self, key, value):
        '''
        Set the value on the key.

        @param key: key to work on, must be in the section/option way
        @param value: value for the key
        '''
        self.db.set_registry(key, value)
        self.__executeNotify(key, value)

    def get_value(self, key,):
        #Lets check if we have it in database, if we have it then 
        #use it.
        return self.db.get_registry(key)
            




