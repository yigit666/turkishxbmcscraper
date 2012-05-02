import urllib,urllib2,re,sys
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
        

    
