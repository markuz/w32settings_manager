# -*- coding: utf-8 -*-
#
# This file is part of the win32settings_manager project
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
# @package   Preferences
# @author    Marco Antonio Islas Cruz <markuz@islascruz.org>
# @copyright 2010 Marco Antonio Islas Cruz
# @license   http://www.gnu.org/licenses/gpl.txt
#

# This module define the classes and procedures to use SQLite3 on win32settings_manager
#
    
import sqlite3
from libw32s.globalvars import DBFILE
from libw32s.Singleton import Singleton
from libw32s.logger import LoggerManager

DBVERSIONS = (
                (0,0,0),
                (0,1,0),
            )

TYPEFUNCS = {
                'bool':bool,
                'list':list,
                'int':int,
                'float':float,
                'string':str,
                }

class sqlite3db(Singleton):
    def __init__(self):
        '''
        Constructor
        '''
        #create the 'connection'
        self.__logger = LoggerManager().getLogger('sqldb')
        self.connect()
    
    def connect(self):
        self.connection = sqlite3.connect(DBFILE)
        self.connection.isolation_level = None
        self.connection.row_factory = self.dict_factory
        self.connection.text_factory = str
        self.have_to_commit = False
        self.cursor = self.connection.cursor()
        self.cursor.row_factory = self.dict_factory
        if not self.check_version():
            self.__logger.debug('No se encontro la version de la base de datos.')
            self.__logger.debug(self.get_db_version())
        self.iface.db = self
        return True
    
    def check_version(self):
        try:
            version = self.get_registry('/core/dbversion')
            version = tuple(map(int, version.split(".")))
        except:
            version = (0,0,0)
        for i in DBVERSIONS:
            if version >= i:
                continue
            self.update_version(map(str, i ))
        return True

    def update_version(self, version):
        ver = '_'.join(version)
        update_func = getattr(self, '_update_%s'%ver, None)
        if update_func:
            update_func()


    def _update_0_1_0(self):
        '''
        Update database to 0.1.0
        '''
        sentences = (
                'CREATE TABLE IF NOT EXISTS registry (id INTEGER PRIMARY KEY, desc VARCHAR(255) NOT NULL, value VARCHAR(255) NOT NULL)',
                )
        self.__sentence_executer(sentences)
        self.set_registry('/core/dbversion', (0,1,0))
        self.set_registry('/webservice/host', 'localhost')
        self.set_registry('/webservice/host', '8080')
    
    def __sentence_executer(self, sentences):
        for strSQL in sentences:
            try:
                self.execute(strSQL)
                self.commit()
            except Exception, e:
                print e

    def get_registry(self,key):
        strSQL = '''SELECT * FROM registry WHERE key = ?'''
        try:
            res = self.execute(strSQL, key)
        except:
            raise ValueError('There is no key %s in registry'%key)
        result = self.fetchone()
        if not result:
            raise ValueError('The key \'%s\' is not in registry'%key)
        try:
            t = result['type']
        except KeyError:
            raise ValueError('Database must be upgraded at least to 0.7.0')
        if t == 'bool':
            value = result['value'] == 'True'
        else:
            value = TYPEFUNCS[t](result['value'])
        return value
            
            
    def set_registry(self,key, value):
        '''
        Set the value of value in the registry identified by key,
        Automatically checks the type of value and set the type to the
        registry.
        I if key does not exists then this function will create it.
        @param strung key: Key to create/update 
        @param * value: value to be set
        '''
        #Check if the key exists
        try:
            val = self.get_registry(key)
        except ValueError:
            self.create_key_registry(key)
        strvalue = str(value)
        type = 'string'
        if isinstance(value, bool):
            type = 'bool'
        else:
            for k, t in TYPEFUNCS.iteritems():
                if isinstance(value, t):
                    type = k
                    break
        strSQL = '''
        UPDATE registry SET value = ?, type=? WHERE key = ?
        '''
        self.execute(strSQL,strvalue, type, key)
        self.commit()
    
    def create_key_registry(self, key):
        strSQL = '''
        INSERT INTO registry VALUES(null,'','',?,'string')
        '''
        self.execute(strSQL, key)
        self.commit()

    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            val = row[idx]
            if isinstance(val, str):
                val = self.encode_text(val)
            d[col[0]] = val
        return d

    def execute(self, strSQL,*args):
        '''
        Execute an SQL sentence and save it to the logger.
        @param strSQL:
        '''
        tup = (strSQL, args)
        self.__logger.debug('Executing : %s',repr(tup))
        res = self.cursor.execute(strSQL,args)
        return res

    def fetchone(self):
        '''
        Wrapper for the fetchone cursor's method, but saves the value on the
        loger
        '''
        val = self.cursor.fetchone()
        return val

    def fetchall(self):
        '''
        Wrapper for the fetchall cursor's method, but saves the value on the
        loger
        '''
        val = self.cursor.fetchall()
        return val

    def fetchmany(self):
        '''
        Fecth all rows from a resultset, and saves the value on the logger.
        '''
        val = self.cursor.fetchmany()
        return val

    def commit(self):
        '''
        Do a self.connection.commit storing the event in the log.
        '''
        self.have_to_commit = True
    
    def do_commit(self):
        if self.have_to_commit:
            self.connection.commit()
            self.have_to_commit = False
        return True

    def get_db_version(self):
        '''
        Look for the version of the database schema. If it can't get the
        database version then it returns False
        '''
        return self.get_registry('/core/dbversion')

