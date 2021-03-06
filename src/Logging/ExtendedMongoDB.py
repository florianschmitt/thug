#!/usr/bin/env python
#
# ExtendedMongoDB.py
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

from .MongoDB import MongoDB
import logging

log = logging.getLogger("Thug")

class ExtendedMongoDB(MongoDB):
    def __init__(self):
        MongoDB.__init__(self)
        self.exploits = self.db.exploits
        self.behavior = self.db.behavior
        self.profiles = self.db.profiles

    def log_exploit_event(self, url, module, description, cve = None, data = None):
        """
        Log file information for a given url

        @url            Url where this exploit occured
        @module         Module/ActiveX Control, ... that gets exploited
        @description    Description of the exploit
        @cve            CVE number (if available)
        """
        _data = {                     "module"      : module,
                                      "description" : description,
                                      "cve"         : cve,
                                      "data"        : data}
        item = self.exploits.find_one({"url_id" : self.url_id})
        if item is not None:
            self.exploits.update({"url_id" : self.url_id}, {"$push" : {"exploits" : _data}})
        else:
            self.exploits.insert({"url_id" : self.url_id, "exploits" : [_data]})

    def add_behavior_warn(self, description, cve, method):
        _data = {                     "description" : description,
                                      "cve"         : cve,
                                      "method"      : method}
        item = self.behavior.find_one({"url_id" : self.url_id})
        if item is not None:
            self.behavior.update({"url_id" : self.url_id}, {"$push" : {"behavior" : _data}})
        else:
            self.behavior.insert({"url_id" : self.url_id, "behavior" : [_data]})

    def check_plugin(self, plugin):
        if log.ThugVulnModules.shockwave_flash_disabled:
            if plugin['name'].find("Shockwave Flash") is not -1:
                return True
        if log.ThugVulnModules.acropdf_disabled:
            if plugin['name'].find("Adobe Acrobat") is not -1:
                return True
        if log.ThugVulnModules.javaplugin_disabled:
            if plugin['name'].find("Java") is not -1:
                return True
        return False

    def set_profile(self, personality, plugins):
        plugins = [x for x in plugins if not self.check_plugin(x)]
        item = self.profiles.find_one({"url_id" : self.url_id})
        if item is not None:
            self.profiles.update(item, {"personality" : personality, "plugins" : plugins})
        else:
            self.profiles.insert({"url_id" : self.url_id, "personality" : personality, "plugins" : plugins})