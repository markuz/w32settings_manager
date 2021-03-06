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
import sys
'''
Created on Nov 12, 2010

@author: marcoantonioislascruz

This module set several variables that are used accross the 
program.
'''
import os
import tempfile

def get_user_dir():
    if os.environ.has_key('XDG_CONFIG_HOME'):
        userdir = os.path.join(os.environ['XDG_CONFIG_HOME'],'win32s')
    else:
        userdir = os.path.join(os.environ["HOME"],".config","christine")
    return userdir

USERDIR = get_user_dir()
PLUGINSDIR=os.path.join(os.getcwd(), 'libw32s','Plugins')
LOGGERDIR=tempfile.tempdir
if '--devel' in sys.path or '-d' in sys.path:
    LOGDIR = os.getcwd()
    DBDIR = os.getcwd()
    CONFIGDIR = os.getcwd()
else:
    LOGDIR = os.path.join('/','var','log','win32server')
    DBDIR = USERDIR
    CONFIGDIR = USERDIR 
#Make sure the logdir exists.
for i in LOGDIR,DBDIR,CONFIGDIR:
    if not os.path.exists(i) and not os.path.isdir(i):
        os.makedirs(i)

DBFILE = os.path.join(DBDIR,'w32server.db')
CONFIGFILE = os.path.join(CONFIGDIR,'win32server.conf')