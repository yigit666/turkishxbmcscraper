# xbmctr MEDIA CENTER, is an XBMC add on that sorts and displays 
# video content from several websites to the XBMC user.
#
# Copyright (C) 2011, DR Ayhan Colak
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



import urllib,urllib2,re,sys
import xbmcplugin,xbmcgui,xbmcaddon,xbmc
import scraper, xbmctools

# -*- coding: iso-8859-9 -*-
Addon = xbmcaddon.Addon('plugin.video.xbmctr')
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmctr')
__language__ = __settings__.getLocalizedString


FILENAME = "arama"


def main():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            query=query.replace(' ','+')
            query=xbmctools.name_fix(query)


        dialog = xbmcgui.Dialog()
        ret = dialog.select(__language__(30047), [__language__(30048), __language__(30049),__language__(30050)])
        if ret == 0:

                try:
                           
                        url ="http://i.dizimag.com/cache/d.js?s91a5"
                        link=xbmctools.get_url(url)      
                        match=re.compile('{ d: "*'+query+'.*?", s: "(.*?)" }').findall(link)
                        if len(match)>0:
                                xbmctools.addFolder(FILENAME,'--------DiziMag--------' ,"",'','')
                                for url in match:
                                        videoTitle=re.compile('/([^ ]*)').findall(str(url))
                                        videoTitle=xbmctools.name_fix(videoTitle[0])
                                        url="http://www.dizimag.com"+str(url)
                                        xbmctools.addFolder("dizimag",videoTitle,"Season(videoTitle,url,'')",url,'')
                except:
                            pass
                
                try:
                           
                           url = ('http://www.dizihd.com/?s='+ query +'&x=0&y=0')
                           link=xbmctools.get_url(url)      
                           match=re.compile('<a href="(.+?)"><img src="(.+?)" ></a>\r\n\t\t\t\t\t\t<h2><a href=".+?">(.+?)izle.*?</a>').findall(link)
                           if len(match)>0:
                                   xbmctools.addFolder(FILENAME,'--------Dizi HD--------' ,"",'','')
                                   for url,thumbnail,videoTitle in match:
                                           xbmctools.addFolder("scraper",videoTitle,"prepare_list(videoTitle,url)",url,thumbnail)
                except:
                            pass


               

        if ret == 1:
                
                
                try:
                        Url = ('http://www.filmifullizle.com/index.php?s=' + query)
                        print Url
                        link=xbmctools.get_url(Url)
                        match=re.compile('<div style="float: left;">\n<a href="(.*?)"><img src="(.*?)" alt="(.*?)"').findall(link)
                        if len(match)>1:
                                xbmctools.addFolder(FILENAME,'--------Sinema HD--------' ,"",'','')
                                for url,thumbnail,videoTitle in match:
                                        xbmctools.addFolder("scraper",videoTitle, "prepare_list(videoTitle,url)",url,thumbnail)
                except:
                        pass
                
        if ret == 2:
                        
                try:
                        Url = ('http://video-klipleri.org/arama?q='+ query)
                        link=xbmctools.get_url(Url)
                        match=re.compile('<a href="(.*?)"><img src="(.*?)"  alt="(.*?)"').findall(link)
                        if len(match)>1:
                                xbmctools.addFolder(FILENAME,'--------Klip TV--------' ,"",'','')
                                for url,thumbnail,videoTitle in match:
                                        xbmctools.addFolder("scraper",videoTitle, "prepare_list(videoTitle,url)",url,thumbnail)                        
                    
                except:
                        print 'okumadı'
