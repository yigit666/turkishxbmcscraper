import urllib,urllib2,re,sys
import xbmcplugin,xbmcgui,xbmcaddon,xbmc
import scraper, xbmctools, helper

# -*- coding: iso-8859-9 -*-
Addon = xbmcaddon.Addon('plugin.video.xbmctr')
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmctr')
__language__ = __settings__.getLocalizedString


FILENAME = "global"


def main():
        xbmctools.addFolder(FILENAME,__language__(30011), "Search()", '')


def search() :
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            try:
                   url = ('http://diziport.com/index.php?eleman=' + query + '&bolum=dizi&obje=diziler&olay=arama')
                   link=xbmctools.get_url(url)
                   match=re.compile('<li><img src="(.*?)\?hash=123" alt=".*?" width="113" height="113" />\n<a href="(.*?)" title="(.*?)">').findall(link)
                   for thumbnail,url,videoTitle in match:
                           xbmctools.addFolder("diziport",videoTitle,"Session(url)",'http://diziport.com/'+url,'http://diziport.com/'+thumbnail)
            except:
                   pass


            try:
                   url = ('http://www.dizihd.com/?s='+ query +'&x=0&y=0')
                   link=xbmctools.get_url(url)      
                   match=re.compile('<a href="(.+?)"><img src="(.+?)" ></a>\r\n\t\t\t\t\t\t<h2><a href=".+?">(.+?)izle.*?</a>').findall(link)
                   for url,thumbnail,videoTitle in match:
                        xbmctools.addFolder("scraper",videoTitle,"prepare_list(videoTitle,url)",url,thumbnail)
            except:
                   pass

            try:
                    url = ('http://www.filmifullizle.com/index.php?s=' + query)
                    main=re.compile('<div style="float: left;">\n<a href="(.*?)"><img src="(.*?)" alt="(.*?)"').findall(link)
                    for url,thumbnail,videoTitle in main:
                        xbmctools.addFolder("scraper",videoTitle, "prepare_list(videoTitle,url)",url,thumbnail)
                        
                    top=re.compile('<li>    <a href="(.*?)" title=".*?"><img src="(.*?)" alt="(.*?) izle " WIDTH=147 HEIGHT=205 class="guncover"/></a>\n    </li>').findall(link)
                    for url,thumbnail,name in top:
                        xbmctools.addFolder(scraper,'>> '+name, "prepare_list(videoTitle,url)",url,thumbnail)
            except:
                   pass
                   
