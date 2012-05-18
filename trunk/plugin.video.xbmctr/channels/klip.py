import urllib,urllib2,re,sys
# xbmctr MEDIA CENTER, is an XBMC add on that sorts and displays 
# video content from several websites to the XBMC user.
#
# Copyright (C) 2011, Dr Ayhan Colak
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
Addon = xbmcaddon.Addon('plugin.video.xbmcTR')
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmcTR')
__language__ = __settings__.getLocalizedString


FILENAME = "klip"


def main():
        xbmctools.addFolder(FILENAME,__language__(30011), "Search()", '')
        xbmctools.addFolder(FILENAME,__language__(30013), "Recent(url)", "http://video-klipleri.org/en-yeni-klipler")
        xbmctools.addFolder(FILENAME,__language__(30014), "Recent(url)", "http://video-klipleri.org/en-iyi-klipler")
        xbmctools.addFolder(FILENAME,__language__(30012), "Last_searched(url)", "http://video-klipleri.org/")
        
#sağdaki menuden kategorileri alıyor
        url = 'http://video-klipleri.org'
        link=xbmctools.get_url(url)
        match=re.compile('<div class="i_cats"><a href="(.*?)" title="(.*?)">.*?</a></div>').findall(link)
        ##
        for url,name in match:
                xbmctools.addFolder(FILENAME,name, "Blog_view(url)",url)

        	
def Search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            url = ('http://video-klipleri.org/arama?q='+ query )
        ##
        link=xbmctools.get_url(url)  
        match=re.compile('<a href="(.*?)"><img src="(.*?)"  alt="(.*?)"').findall(link)
        for url,thumbnail,name in match:
                xbmctools.addFolder("scraper",name, "prepare_list(videoTitle,url)",url)
def Recent(url):
        link=xbmctools.get_url(url)    
        match=re.compile('<a href="(.*?)"><img src="(.*?)" alt="(.*?)"').findall(link)
        ##
        for url,thumbnail,name in match:
                xbmctools.addFolder("scraper",name, "prepare_list(videoTitle,url)",url,thumbnail)
        page=re.compile('erzu').findall(link)
        for url,name in page:
                addDir(__language__(30006)+' >> '+name,url,1,'')
    
def Categories(url):
        link=xbmctools.get_url(url)
        match=re.compile('<div class="i_cats"><a href="(.*?)" title="(.*?)">.*?</a></div>').findall(link)
        ##
        for url,name in match:
                xbmctools.addFolder(FILENAME,name, "Blog_view(url)",url) 
        MAINMENU(url)

        
def Last_searched(url):
        link=xbmctools.get_url(url)
        match=re.compile('<span class="i_cats"><a target="_top" href="(.*?)" title=".*?">(.*?)</a></span>').findall(link)
        ##
        for url,name in match:
             xbmctools.addFolder(FILENAME,name, "Popular(url)",url)   
def Popular(url):
        link=xbmctools.get_url(url)
        match=re.compile('<a href="(.*?)"><span class="imag"><img src="(.*?)" alt="(.*?)"  width="128" height="72" /></span>').findall(link)
        for url,thumbnail,name in match:
                xbmctools.addFolder("scraper",name, "prepare_list(videoTitle,url)",url,thumbnail)
    
        MAINMENU(url)
def Blog_view(url):
        link=xbmctools.get_url(url)
        match=re.compile('<a href="(.*?)" class="video-resim-wrap" title=".*?"><span class="video-resim kucuk-resim-80"><span class="clip"><img src="(.*?)"  width="80" height="45" alt="(.*?)"').findall(link)
        for url,thumbnail,name in match:
                xbmctools.addFolder("scraper",name, "prepare_list(videoTitle,url)",url,thumbnail)
        MAINMENU(url)       
                

        
def MAINMENU(url):
        xbmctools.addFolder(FILENAME,"Ana Menu", "main()","")
        

