# -*- coding: iso-8859-9 -*-
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
'''
Created on 21 sempember 2012

@author: drascom
@version: 0.2.0

'''

import os
import sys
import urllib
import xbmc, xbmcgui, xbmcaddon, xbmcplugin


addon_id = 'plugin.video.mc'
__settings__ = xbmcaddon.Addon(id=addon_id)
home = __settings__.getAddonInfo('path')
channels = os.path.join(__settings__.getAddonInfo('path'), 'channels')
fanart = xbmc.translatePath( os.path.join( home, 'fanart.png' ) )


# Fetch all folders needed to run the add on
folders = xbmc.translatePath(os.path.join(home, 'resources', 'lib'))
sys.path.append(folders)
folders = xbmc.translatePath(os.path.join(home, 'channels'))
sys.path.append(folders)
IMAGES_PATH = xbmc.translatePath(os.path.join(home, 'resoures','image'))
sys.path.append(IMAGES_PATH)

import xbmctools
#Imported later than other modules, because first the "lib" folder has to be appended. 

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
vTitle = None
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

##print "Ad: "+str(name)
##print "Dosya: "+str(fileName)
##print "Method: "+str(method)
##print "Url: "+str(url)
##print "Video Ad: "+str(videoTitle)
##print "Resim: "+str(thumbnail)

# All methods are run through various class files.
# If there is no "fileName" it must mean that the user
# is at the start of the script, and the "channels" should
# be displayed
if fileName == None:
    fileName=''
    xbmctools.loadImports()
    xbmctools.listChannels()
    #print 'kanallar:'+str(imps)
else:
    exec "import "+fileName+" as channel"
    exec "channel."+method

xbmcplugin.endOfDirectory(int(sys.argv[1]))



