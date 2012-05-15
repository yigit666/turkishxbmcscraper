# xbmctr MEDIA CENTER, is an XBMC add on that sorts and displays 
# video content from several websites to the XBMC user.
#
# Copyright (C) 2011, Emin Ayhan Colak
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# for more info please visit http://xbmctr.com

import urllib
import urllib2
import re
import os,sys
import xbmcplugin,xbmcgui,xbmc,xbmcaddon 
import scraper, xbmctools
# -*- coding: iso-8859-9 -*-
Addon = xbmcaddon.Addon('plugin.video.xbmcTR')
profile = xbmc.translatePath(Addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmcTR')
__language__ = __settings__.getLocalizedString



FILENAME = "live"

url='http://drascom.dyndns.org/site/'

def main():
     xbmctools.addFolder(FILENAME,__language__(30030), "BuildPage(code='TR')", "tr")
     xbmctools.addFolder(FILENAME,__language__(30031), "BuildPage(code='DE')", "")
     xbmctools.addFolder(FILENAME,__language__(30032), "BuildPage(code='EN')", "")
     xbmctools.addFolder(FILENAME,__language__(30033), "BuildPage(code='IT')", "")
     xbmctools.addFolder(FILENAME,__language__(30034), "BuildPage(code='RU')", "")
     xbmctools.addFolder(FILENAME,__language__(30035), "BuildPage(code='FR')", "")
     xbmctools.addFolder(FILENAME,__language__(30036), "BuildPage(code='YE')", "")
     xbmctools.addFolder(FILENAME,__language__(30037), "BuildPage(code='CA')", "")
     xbmctools.addFolder(FILENAME,__language__(30038), "BuildPage(code='CA2')", "")


def BuildPage(code):
    link=xbmctools.get_url(xbmctools.setUrl())
    match=re.compile('<tr><td>'+code+'</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>').findall(link)
    for videoTitle,Url,Thumbnail in match:
            xbmctools.addVideoLink(videoTitle,Url,Thumbnail)


   
