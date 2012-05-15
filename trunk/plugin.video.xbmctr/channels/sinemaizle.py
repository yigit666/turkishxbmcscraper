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
Addon = xbmcaddon.Addon('plugin.video.xbmcTR')
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmcTR')
__language__ = __settings__.getLocalizedString


FILENAME = "sinemaizle"


            
def main():
        xbmctools.addFolder(FILENAME,__language__(30011), "search()", '')
        xbmctools.addFolder(FILENAME,__language__(30016), "RECENT(url)", "http://www.sinemaizle.org/")
        link=xbmctools.get_url('http://www.sinemaizle.org/')
        match=re.compile('<li class="cat-item cat-item-.*?"><a href="(.*?)" title=".*?">(.*?)</a>\n</li>').findall(link)
        for url,videoTitle in match:
                xbmctools.addFolder(FILENAME,videoTitle, "Season(url)",url)
                
         

def search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            #print query
            url = ('http://www.sinemaizle.org/?s=' + query)
            Season(url)
                        
def RECENT(url):
        
        link=xbmctools.get_url(url)
         #next page        
        page=re.compile('class=\'current\'><a><b>.+?</b></a></li>\n<li><a href=\'(.+?)\' rel=\'nofollow\'><b>(.+?)</b></a></li>').findall(link)
        for Url,videoTitle in page:
                xbmctools.addFolder(FILENAME,__language__(30006)+' >> '+videoTitle,"RECENT(Url)",Url,'')
                
        match=re.compile('<a href="(.*?)" title=".*?"><img src="(.*?)" alt="(.*?)"').findall(link)
        for url,thumbnail,videoTitle in match:
                xbmctools.addFolder("scraper",videoTitle,"prepare_list(videoTitle,url)",url,thumbnail)
                
        
        
def Season(url):
        MAINMENU(url)
        link=xbmctools.get_url(url)
        match=re.compile('<a href="(.*?)" title=".*?"><img class="poster" src="(.*?)" alt="(.*?)"').findall(link)
        if match>[1]:
                for url,thumbnail,videoTitle in match:
                        xbmctools.addFolder("scraper",videoTitle,"prepare_list(videoTitle,url)",url,thumbnail)
        else:
                pass
        page=re.compile('page current\'>1</span></li><li><a href=\'(.*?)\' title=\'.*?\' class=\'page\'>(.*?)</a></li>').findall(link)
        for url,videoTitle in page:
                xbmctools.addFolder(FILENAME,__language__(30006)+' >> '+videoTitle,"Season(url)",url,'')
              


def MAINMENU(url):
         xbmctools.addFolder(FILENAME,'<<<'+__language__(30002),"main()",'http://diziport.com/','')
        

    
