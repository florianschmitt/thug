#!/usr/bin/env python
#
# ResourcePlugin.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA
from DOM import MIMEHandler

import logging
log = logging.getLogger("Thug")

import zope.interface
import os
import subprocess
from .IPlugin import IPlugin

class Handler:
    zope.interface.implements(IPlugin)

    scrutinizerPath = '/home/zack/projects/PDFScrutinizer/run.sh'
    
    def startProcess(self, path, urlid):
        params = [self.scrutinizerPath, '-pdf', path, '-mongo', str(urlid)]
        log.warn("starting scrutinizer process " + str(params))
        p = subprocess.Popen(params, shell=False, cwd='/home/zack/projects/PDFScrutinizer',)
        log.warn(p.stdout)

    def run(self, thug, log):
        log.warn('searching for content type application/pdf')
        path = os.getcwd()+'/..'+log.ThugLogging.baseDir[2:]+'/application/pdf'
        if os.path.exists(path):
            for x in os.listdir(path):
                self.startProcess(path+'/'+x, log.ThugLogging.MongoDB.url_id)
        else:
            log.warn("nothing found")