#!/usr/bin/env python
#
# AdvancedThugLogging.py
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

from .ThugLogging import ThugLogging
from .MongoDB import MongoDB

import os
import copy
import errno
import hashlib
import datetime
import logging
log = logging.getLogger("Thug")

class AdvancedThugLogging(ThugLogging):
    def __init__(self, thug_version):
        ThugLogging.__init__(self, thug_version)

    def log_exploit_event(self, url, module, description, cve = None, data = None, forward = True):
        """
        Log file information for a given url

        @url            Url where this exploit occured
        @module         Module/ActiveX Control, ... that gets exploited
        @description    Description of the exploit
        @cve            CVE number (if available)
        @forward        Forward log to add_behavior_warn
        """
        ThugLogging.log_exploit_event(self, url, module, description, cve = cve, data = data)
        self.MongoDB.log_exploit_event(url, module, description, cve = cve, data = data)

    def add_behavior_warn(self, description = None, cve = None, method = "Dynamic Analysis"):
        ThugLogging.add_behavior_warn(self, description, cve, method)
        self.MongoDB.add_behavior_warn(description, cve, method)