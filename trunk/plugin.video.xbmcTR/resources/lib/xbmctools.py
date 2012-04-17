# xbmcTR, is an XBMC add on that sorts and displays 
# video content from several websites to the XBMC user.
#
# Copyright (C) 2012, dr Ayhan Colak 
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
# -*- coding: iso-8859-9 -*-
'''
Edited on 5 April 2012

@author: Dr Ayhan Colak

'''
import urllib,urllib2
import sys,re
import os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import helper
site='http://drascom.dyndns.org/site/'
site2='http://192.168.0.52/site'
Addon = xbmcaddon.Addon('plugin.video.xbmcTR')
# Get the system path to where the thumbnail images are stored-
IMAGES_PATH = xbmc.translatePath(os.path.join(Addon.getAddonInfo('path'), 'resources', 'images'))
def setUrl():
        url=site+'sys.html'
        link=get_url(url)
        safe=re.compile('<link>(.*?)</link>').findall(link)
        if len(safe)>0:
                for url in safe:
                        return url
        else:
                url=site2+'sys.html'
                link=get_url(url)
                safe=re.compile('<link>(.*?)</link>').findall(link)
                for url in safe:
                        return url

def get_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('&amp;',"&").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        link=link.replace('\xc5\x9f',"s").replace('&#038;',"&").replace('&#8217;',"'").replace('\xc3\xbc',"u").replace('\xc3\x87',"C").replace('\xc4\xb1',"ı").replace('&#8211;',"-").replace('\xc3\xa7',"c").replace('\xc3\x96',"O").replace('\xc5\x9e',"S").replace('\xc3\xb6',"o").replace('\xc4\x9f',"g").replace('\xc4\xb0',"I").replace('\xe2\x80\x93',"-")
        response.close()
        return link

def addFolder(FILENAME, name, method, url="", thumbnail=""):
    u = sys.argv[0]+"?fileName="+urllib.quote_plus(FILENAME)+"&method="+urllib.quote_plus(method)+"&url="+urllib.quote_plus(url)
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    

def addVideoFolder(FILENAME, videoTitle, url, method, thumbnail, info):
    u = sys.argv[0]+"?fileName="+urllib.quote_plus(FILENAME)+"&videoTitle="+urllib.quote_plus(videoTitle)+"&method="+urllib.quote_plus(method)+"&url="+urllib.quote_plus(url)
    liz = xbmcgui.ListItem(videoTitle, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    liz.setInfo(type="Video", infoLabels=info)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

def addVideoLink(linkTitle, url, thumbnail=""):
    liz = xbmcgui.ListItem(linkTitle, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
    liz.setInfo(type="Video", infoLabels={"Title":linkTitle})
    liz.setProperty("IsPlayable", "true")
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
    

def addPlaylistLink(FILENAME, linkTitle, playlistUrls, playlistTitles, method):
    u = sys.argv[0]+"?fileName="+urllib.quote_plus(FILENAME)+"&method="+urllib.quote_plus(method)+"&url="+urllib.quote_plus(playlistUrls)+"&videoTitle="+urllib.quote_plus(playlistTitles)
    liz = xbmcgui.ListItem(linkTitle, iconImage="DefaultVideo.png")
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)


def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player().play(liz)
        return ok
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

