# -*- coding: cp1254 -*-
'''
    Cache service for XBMC
    Copyright (C) 2012 Dr Ayhan Çolak

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    Version 0.8
'''
import sys
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

##
##__settings__ = xbmcaddon.Addon(id='script.module.xbmctr')
##home = __settings__.getAddonInfo('path')
##folders = xbmc.translatePath(os.path.join(Addon.getAddonInfo('path'), 'resources', 'lib'))
##sys.path.append(folders)


def run():
    import araclar
    return True

if __name__ == "__main__":
    if settings.getSetting("autostart") == "true":
        run()
