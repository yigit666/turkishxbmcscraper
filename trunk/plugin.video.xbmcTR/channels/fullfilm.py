import urllib,urllib2,re,sys
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
        url='http://www.filmifullizle.com/'
        link=xbmctools.get_url(url)
        match=re.compile('<li class=".*?"><a href="(.*?)" title=".*?">(.*?)</a>\n</li>').findall(link)
        for url,name in match:
                xbmctools.addFolder(FILENAME,'>> '+name, "Recent(url)",url,"")


def Recent(url):
        MAINMENU(url)
        link=xbmctools.get_url(url)
        link=link.replace('\xc5\x9f',"s").replace('&#038;',"&").replace('&#8217;',"'").replace('\xc3\xbc',"u").replace('\xc3\x87',"C").replace('\xc4\xb1',"ı").replace('&#8211;',"-").replace('\xc3\xa7',"c").replace('\xc3\x96',"O").replace('\xc5\x9e',"S").replace('\xc3\xb6',"o").replace('\xc4\x9f',"g").replace('\xc4\xb0',"I").replace('\xe2\x80\x93',"-")

        page=re.compile('<li class="active_page"><a href=".*?">.*?</a></li>\n<li><a href="(.*?)">(.*?)</a></li>').findall(link)
        for url,name in page:
                xbmctools.addFolder(FILENAME,__language__(30006)+' >> '+name, "Recent(url)",url,"")
        
    

        main=re.compile('<div style="float: left;">\n<a href="(.*?)"><img src="(.*?)" alt="(.*?)"').findall(link)
        for Url,thumbnail,videoTitle in main:
                xbmctools.addFolder("scraper",videoTitle, "prepare_list(videoTitle,url)",Url,thumbnail)
        
        top=re.compile('<li>    <a href="(.*?)" title=".*?"><img src="(.*?)" alt="(.*?) izle " WIDTH=147 HEIGHT=205 class="guncover"/></a>\n    </li>').findall(link)
        for url,thumbnail,name in top:
                xbmctools.addFolder("scraper",'>> '+name, "prepare_list(videoTitle,url)",url,thumbnail)         


def Search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            url = ('http://www.filmifullizle.com/index.php?s=' + query)
            Recent(url)


def MAINMENU(url):
         xbmctools.addFolder(FILENAME,'<<<'+__language__(30002),"main()",'http://www.filmifullizle.com/','')


