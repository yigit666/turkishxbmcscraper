import urllib,urllib2,re,sys
import xbmcplugin,xbmcgui,xbmcaddon,xbmc
import scraper, xbmctools, helper

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
        link=xbmctools.get_url(url)       
        match=re.compile('<a href="(.*?)" title=".*?" class="img"><img src="(.*?)" alt="(.*?)"').findall(link)
        for url,thumbnail,videoTitle in match:
                xbmctools.addFolder("scraper",videoTitle,"prepare_list(videoTitle,url)",'http://yabancidiziizle.com'+url,thumbnail)
                
        #next page        
        page=re.compile('class="aktif">.*?</a><a href="(.*?)">(.*?)</a>').findall(link)
        for url,videoTitle in page:
                xbmctools.addFolder(FILENAME,__language__(30006)+' >> '+videoTitle,"RECENT(url)",'http://diziport.com/'+url,'special://home/addons/plugin.video.diziport/resources/images/next.png')
        
        
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
        xbmctools.addDir(__language__(30002),'http://yabancidiziizle.com','','special://home/addons/plugin.video.diziport/resources/images/main.jpg')
