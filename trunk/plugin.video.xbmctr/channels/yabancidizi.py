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
Addon = xbmcaddon.Addon('plugin.video.xbmctr')
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmctr')
__language__ = __settings__.getLocalizedString


FILENAME = "yabancidizi"


            
def main():
        url='http://yabancidiziizle.com/'
        xbmctools.addFolder(FILENAME,__language__(30011), "search()", '')
        xbmctools.addFolder(FILENAME,__language__(30016), "RECENT(url)", "http://yabancidiziizle.com/")
        link=xbmctools.get_url(url)
        match=re.compile('<li><a href="(.*?)" title=".*?">(.*?)</a></li><li>').findall(link)	
        #kategori-1
        for url,videoTitle in match:
                xbmctools.addFolder(FILENAME,videoTitle,"Session(url)",'http://yabancidiziizle.com'+url,'')
        #kategori-2
        second=re.compile('<li><a href="(.*?)" title=".*?" class="iki">(.*?)</a></li><li>').findall(link)
        for url,videoTitle in second:
                xbmctools.addFolder(FILENAME,videoTitle,"Session(url)",'http://yabancidiziizle.com'+url,'')
        #sayfalama
        page=re.compile('class="aktif">.*?</a><a href="(.*?)">(.*?)</a>').findall(link)
        for url,videoTitle in page:
                xbmctools.addFolder(FILENAME,videoTitle,"main(url)",'http://yabancidiziizle.com'+url,'')
         

def search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            url = ('http://yabancidiziizle.com/ara.php?q='+ query)
            RECENT(url)
                        
def RECENT(url):
        MAINMENU(url)

        link=xbmctools.get_url(url)

        #next page        
        page=re.compile('class="aktif">.*?</a><a href="(.*?)">(.*?)</a>').findall(link)
        print page
        for url,videoTitle in page:
                xbmctools.addFolder(FILENAME,__language__(30006)+' >> '+videoTitle,"RECENT(url)",'http://diziport.com/'+url,'')
        

        match=re.compile('<a href="(.*?)" title=".*?" class="img"><img src="(.*?)" alt="(.*?)"').findall(link)
        for url,thumbnail,videoTitle in match:
                xbmctools.addFolder("scraper",videoTitle,"prepare_list(videoTitle,url)",'http://yabancidiziizle.com'+url,thumbnail)
                
        
def Session(url):
                link=xbmctools.get_url(url)
                match=re.compile('<a href="(.*?)" title=".*?" class="img"><img src="(.*?)" alt="(.*?)"').findall(link)
                for url,thumbnail,videoTitle in match:
                                xbmctools.addFolder(FILENAME,videoTitle, "Episodes(url)",url)
                
def Episodes(url):
        link=xbmctools.get_url(url)
        match=re.compile('<a href="(.*?)" title=".*?" class="img"><img src="(.*?)" alt="(.*?)"').findall(link)
        print match,'___________________--------------------------'
        for url,thumbnail,videoTitle in match:
            xbmctools.addFolder("scraper",videoTitle, "prepare_list(videoTitle,url)", 'http://yabancidiziizle.com/'+url)        


                
def MAINMENU(url):
         xbmctools.addFolder(FILENAME,'<<<'+__language__(30002),"main()",'http://yabancidiziizle.com/','')
