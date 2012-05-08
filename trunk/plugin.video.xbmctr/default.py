# Multi Documentary Streams, is an XBMC add on that sorts and displays 
# video content from several websites to the XBMC user.
#
# Copyright (C) 2011, Ricardo Ocana Leal
#
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

'''
Created on 6 nov 2011

@author: drascom
@version: 0.1.0

'''

import os
import sys
import urllib
import xbmc, xbmcgui, xbmcaddon, xbmcplugin

# -*- coding: iso-8859-9 -*-
Addon = xbmcaddon.Addon('plugin.video.xbmctr')

addon_id = 'plugin.video.xbmctr'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon_path = selfAddon.getAddonInfo('path')


# Fetch all folders needed to run the add on
folders = xbmc.translatePath(os.path.join(Addon.getAddonInfo('path'), 'resources', 'lib'))
sys.path.append(folders)
folders = xbmc.translatePath(os.path.join(Addon.getAddonInfo('path'), 'channels'))
sys.path.append(folders)

#Imported later than other modules, because first the "lib" folder has to be appended. 
import xbmctools

'''
Adds all folders in XBMC to the various websites.
'''
def listChannels():
    xbmctools.addFolder("arama", "GLOBAL ARAMA", "main()", "", "arama")
    xbmctools.addFolder("live", "Live TV ", "main()", "", "live")
    xbmctools.addFolder("dizimag", "DiziMag Streams", "main()", "", "dizimag")
    xbmctools.addFolder("diziport", "DiziPort Streams", "main()", "", "diziport")
    xbmctools.addFolder("diziHd", "DiziHD Streams", "main()", "", "diziHd")
    xbmctools.addFolder("yabancidizi", "Full Yabancı", "main()", "", "yabancidizi")
    xbmctools.addFolder("fullfilm", "Sinema HD", "main()", "", "fullfilm")
    xbmctools.addFolder("sinemaizle", "Sinema sd", "main()", "", "sinemaizle")
    xbmctools.addFolder("klip", "Music TV", "main()", "", "klip")
     
'''
Gets the various system parameters.

@return: param
'''
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param
    
    
params = get_params()
name = None
fileName = None
method = None
url = None
videoTitle = None
thumbnail = None

#Try-catch blocks to see which parameters are available 
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    fileName = urllib.unquote_plus(params["fileName"])
except:
    pass
try:
    method = urllib.unquote_plus(params["method"])
except:
    pass
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    videoTitle = urllib.unquote_plus(params["videoTitle"])
except:
    pass
try:
    thumbnail = urllib.unquote_plus(params["thumbnail"])
except:
    pass
print "Name: "+str(name)
print "FileName: "+str(fileName)
print "Method: "+str(method)
print "Url: "+str(url)
print "VideoTitle: "+str(videoTitle)
print "Thumbnail: "+str(thumbnail)

# All methods are run through various class files.
# If there is no "fileName" it must mean that the user
# is at the start of the script, and the "channels" should
# be displayed
if fileName == None:
    listChannels()
else:
    exec "import "+fileName+" as channel"
    exec "channel."+method

xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Documentary')
xbmcplugin.setContent(int(sys.argv[1]), 'Movies')
xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)
