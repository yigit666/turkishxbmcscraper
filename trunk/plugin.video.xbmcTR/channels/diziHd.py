import urllib,urllib2,re,sys
import xbmcplugin,xbmcgui,xbmcaddon,xbmc
import scraper, xbmctools, helper

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
        match=re.compile('<a href="(.+?)"><img src="(.+?)" ></a>\r\n\t\t\t\t\t\t<h2><a href=".+?">(.+?)izle.*?</a>').findall(link)
        if match<= 0:
                Main()
        for url,thumbnail,videoTitle in match:
                xbmctools.addFolder(FILENAME,videoTitle,"scraper.Dizihd(videoTitle,url)",url,thumbnail)
'''        page=re.compile('<span class="current">.+?</span><a href="(.+?)" title="(.+?)">').findall(link)
        for url,name in page:
                xbmctools.addFolder('', name, "RECENT(url)",url,'')
   ''' 
       
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
               xbmctools.addFolder(FILENAME,videoTitle,"scraper.Dizihd(videoTitle,url)",url,thumbnail)

             

def MAINMENU(url):
         xbmctools.addFolder(FILENAME,'<<<'+__language__(30002),"main()",'http://diziport.com/','special://home/addons/plugin.video.diziport/resources/images/main.jpg')

