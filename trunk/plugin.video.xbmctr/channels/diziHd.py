import urllib,urllib2,re,sys
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

import xbmcplugin,xbmcgui,xbmcaddon,xbmc
import scraper, xbmctools

# -*- coding: iso-8859-9 -*-
'''Addon = xbmcaddon.Addon('plugin.video.xbmcTR')
'''
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmcTR')
__language__ = __settings__.getLocalizedString


FILENAME = "diziHd"


            
def main():
        xbmctools.addFolder(FILENAME,__language__(30011), "Search()", '')
        xbmctools.addFolder(FILENAME,__language__(30016), "RECENT(url)", "http://www.dizihd.com/")
        xbmctools.addFolder(FILENAME,__language__(30017), "Categories(url)", "http://www.dizihd.com/")
        xbmctools.addFolder(FILENAME,__language__(30004), "RECENT(url)", "http://www.dizihd.com/dizi-izle/belgesel-izle/")  
        #xbmctools.addDir('Tum eklentiler ve daha fazlası -- xbmcTR.com--','Search',3,'')

def Search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            url = ('http://www.dizihd.com/?s='+ query +'&x=0&y=0')
            RECENT(url)
def RECENT(url):
        MAINMENU(url)
        link=xbmctools.get_url(url)      
        page=re.compile('<span class="current">.+?</span><a href="(.+?)" title="(.+?)">').findall(link)
        for url,name in page:
                xbmctools.addFolder(FILENAME,__language__(30006)+' >> '+name, "RECENT(url)",url,'')

        match=re.compile('<a href="(.+?)"><img src="(.+?)" ></a>\r\n\t\t\t\t\t\t<h2><a href=".+?">(.+?)izle.*?</a>').findall(link)

        for url,thumbnail,videoTitle in match:
                xbmctools.addFolder("scraper",videoTitle,"prepare_list(videoTitle,url)",url,thumbnail)
        page=re.compile('<span class="current">.+?</span><a href="(.+?)" title="(.+?)">').findall(link)
        for url,name in page:
                xbmctools.addFolder(FILENAME,'>> SAYFA '+name, "RECENT(url)",url,'')
 
       
def Categories(url):
        MAINMENU(url)
        link=xbmctools.get_url(url)
        match=re.compile('<li class="cat-item cat-item-.*?"><a href="(.+?)" title=".*?">(.+?)izle</a>\r\n</li>').findall(link)
        #http://www.dizihd.com/dizi-izle/alin-yazisi-izle
        for url,videoTitle in match:
                xbmctools.addFolder(FILENAME,videoTitle,"Session(url)",url,'')

def Session(url):
        MAINMENU(url)
        link=xbmctools.get_url(url)
        match=re.compile('<a href="(.+?)"><img src="(.+?)" ></a>\r\n\t\t\t\t\t\t<h2><a href=".+?">(.+?)izle.*?</a>').findall(link)
        for url,thumbnail,videoTitle in match:
               xbmctools.addFolder("scraper",videoTitle,"prepare_list(videoTitle,url)",url,thumbnail)

             

def MAINMENU(url):
         xbmctools.addFolder(FILENAME,'<<<'+__language__(30002),"main()",'http://www.dizihd.com/','')

