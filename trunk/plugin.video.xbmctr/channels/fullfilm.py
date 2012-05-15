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


FILENAME = "fullfilm"

'''Constants'''
xbmcPlayer = xbmc.Player()
playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)


def main():
        xbmctools.addFolder(FILENAME,'!!DIKKAT!!Sitedeki BAZI izlenemiyor.[17.04.2012]', "Search()", '')
        xbmctools.addFolder(FILENAME,__language__(30011), "Search()", '')
        xbmctools.addFolder(FILENAME,__language__(30016), "Recent(url)", "http://www.filmifullizle.com/")
        xbmctools.addFolder(FILENAME,__language__(30039), "Recent(url)", "http://www.filmifullizle.com/kategori/filmler/yerli-filmler")
        xbmctools.addFolder(FILENAME,__language__(30040), "Recent(url)", "http://www.filmifullizle.com/kategori/filmler/yabanci-filmler")
        xbmctools.addFolder(FILENAME,__language__(30041), "Recent(url)", "http://www.filmifullizle.com/kategori/filmler/yabanci-filmler/turkce-dublaj")
        Url='http://www.filmifullizle.com/'
        link=xbmctools.get_url(Url)
        match=re.compile('<li class=".*?"><a href="(.*?)" title=".*?">(.*?)</a>\n</li>').findall(link)
        for Url,name in match:
                xbmctools.addFolder(FILENAME,'>> '+name, "Recent(url)",Url,"")


def Recent(Url):
        MAINMENU(Url)
        link=xbmctools.get_url(Url)
        link=link.replace('\xc5\x9f',"s").replace('&#038;',"&").replace('&#8217;',"'").replace('\xc3\xbc',"u").replace('\xc3\x87',"C").replace('\xc4\xb1',"ı").replace('&#8211;',"-").replace('\xc3\xa7',"c").replace('\xc3\x96',"O").replace('\xc5\x9e',"S").replace('\xc3\xb6',"o").replace('\xc4\x9f',"g").replace('\xc4\xb0',"I").replace('\xe2\x80\x93',"-")

        page=re.compile('<li class="active_page"><a href=".*?">.*?</a></li>\n<li><a href="(.*?)">(.*?)</a></li>').findall(link)
        for Url,name in page:
                xbmctools.addFolder(FILENAME,__language__(30006)+' >> '+name, "Recent(url)",Url,"")
        
    

        main=re.compile('<div style="float: left;">\n<a href="(.*?)"><img src="(.*?)" alt="(.*?)"').findall(link)
        for Url,thumbnail,videoTitle in main:
                xbmctools.addFolder("scraper",videoTitle, "prepare_list(videoTitle,url)",Url,thumbnail)
        
        top=re.compile('<li>    <a href="(.*?)" title=".*?"><img src="(.*?)" alt="(.*?) izle " WIDTH=147 HEIGHT=205 class="guncover"/></a>\n    </li>').findall(link)
        for Url,thumbnail,name in top:
                xbmctools.addFolder("scraper",'>> '+name, "prepare_list(videoTitle,url)",Url,thumbnail)         


def Search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            query=query.replace(' ','+')       
            Url = ('http://www.filmifullizle.com/index.php?s=' + query)
            Recent(Url)


def MAINMENU(Url):
         xbmctools.addFolder(FILENAME,'<<<'+__language__(30002),"main()",'http://www.filmifullizle.com/','')


