#! /usr/bin/env python
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
# @category  Multimedia
# @package   win32settings_manager
# @author    Marco Antonio Islas Cruz <markuz@islascruz.org>
# @copyright 2010 Marco Antonio Islas Cruz
# @license   http://www.gnu.org/licenses/gpl.txt

from optparse import OptionParser
from libw32s.Singleton import Singleton


class options(Singleton):
    def __init__(self):
        '''
        Constructor. Parsea los valores que vienen en sys.argv[1:] y almacena
        los valores en self.options.
        
        Utiliza optparse para parsear las opciones.
        
        Las opciones disponibles son:
        
        self.options.debug (-v , --debug)
        self.options.daemon (-D, --daemon)
        '''
        usage ='%prog [args]'
        version = '%prog' 
        parser = OptionParser(usage = usage,version=version)
        parser.add_option('-l','--verbose-level',type='string',action='store',
                          dest='verbose_level')
        parser.add_option('-d','--devel',type='string',action='store',
                          dest='verbose_level')
        self.options, self.args = parser.parse_args()
        
    
