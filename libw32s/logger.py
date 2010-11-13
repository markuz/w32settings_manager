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
import os
import logging
import logging.handlers
from libw32s.Singleton import Singleton
from libw32s.options import options
from libw32s.globalvars import LOGGINGDIR


class LoggerManager(Singleton):
    def __init__(self):
        self.loggers = {}
        opts = options()
        formatter = logging.Formatter('%(asctime)s:%(levelname)-8s:%(name)-10s:%(lineno)4s: %(message)-80s')
        level = getattr(opts.options,'verbose','ERROR')
        if not level:
            level = 'ERROR'
        level = level.upper()
        nlevel = getattr(logging, level, None)
        if nlevel != None:
            self.LOGGING_MODE = nlevel
        else:
            self.LOGGING_MODE = logging.DEBUG
        if opts.options.verbose:
            self.LOGGING_HANDLER = logging.StreamHandler()
            self.ERROR_HANDLER = logging.StreamHandler()
        else:
            logfile = os.path.join(USERDIR, 'christine_events.log')
            errorfile = os.path.join(USERDIR, 'christine_errors.log')
            self.LOGGING_HANDLER = logging.handlers.RotatingFileHandler(logfile,'a',3145728, 3)
            self.ERROR_HANDLER = logging.handlers.RotatingFileHandler(errorfile,'a',1048576, 2)

        self.LOGGING_HANDLER.setFormatter(formatter)
        self.LOGGING_HANDLER.setLevel(self.LOGGING_MODE)
        self.ERROR_HANDLER.setFormatter(formatter)
        self.ERROR_HANDLER.setLevel(self.LOGGING_MODE)
    
    def getLogger(self, loggername):
        if not self.loggers.has_key(loggername):
            logger = Logger(loggername, self.LOGGING_HANDLER, 
                        self.ERROR_HANDLER, self.LOGGING_MODE)
            self.loggers[loggername] = logger
        return self.loggers[loggername]

class Logger:
    '''
    Implements the christine logging facility.
    '''
    def __init__(self, loggername, logging_handler, error_handler, logging_mode, 
                type='event'):
        '''
        Constructor, construye una clase de logger.
        
        @param loggername: Nombre que el logger tendra.
        @param type: Tipo de logger. Los valores disponibles son : event y error
                    por defecto apunta a event. En caso de utilizarse otro
                    que no sea event o error se apuntara a event.
        '''
        
        # Create two logger,one for info, debug and warnings and another for  
        # errors, exceptions and criticals
        self.__Logger = logging.getLogger(loggername)
        self.__ErrorLogger = logging.getLogger('Error'+ loggername)
        
        #Establecemos las propiedades de los loggers.
        self.__Logger.setLevel(logging_mode)
        self.__Logger.addHandler(logging_handler)
        
        self.__ErrorLogger.setLevel(logging_mode)
        self.__ErrorLogger.addHandler(error_handler)

        self.info = self.__Logger.info
        self.debug = self.__Logger.debug
        self.warning = self.__Logger.warning
        
        self.critical = self.__ErrorLogger.critical
        self.error = self.__ErrorLogger.error
        self.exception = self.__ErrorLogger.exception
    
