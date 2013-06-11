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
from .IPlugin import IPlugin

class Handler:
    zope.interface.implements(IPlugin)
    
    def handleContent(self, data):
        log.warning("data length:" + str(len(data)))
        with open('/home/zack/tmp.pdf', 'wb') as fd:
            fd.write(data)
        return False

    def run(self, thug, log):
        log.info('registering handler for MIME type application/pdf')
        log.MIMEHandler["application/pdf"] = self.handleContent