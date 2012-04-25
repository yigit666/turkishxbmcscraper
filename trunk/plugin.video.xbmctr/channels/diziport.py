import urllib,urllib2,re,sys
import xbmcplugin,xbmcgui,xbmcaddon,xbmc
import scraper, xbmctools, helper

# -*- coding: iso-8859-9 -*-
Addon = xbmcaddon.Addon('plugin.video.xbmcTR')
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmcTR')
__language__ = __settings__.getLocalizedString


FILENAME = "diziport"


            
def main():
        xbmctools.addFolder(FILENAME,__language__(30011), "search()", '')
        xbmctools.addFolder(FILENAME,__language__(30016), "RECENT(url)", "http://diziport.com/")
        xbmctools.addFolder(FILENAME,__language__(30017), "Categories(url)", "http://diziport.com/")
        xbmctools.addFolder(FILENAME,__language__(30012), "RECENT(url)", "http://diziport.com/index.php?bolum=dizi&obje=en_cok_izlenenler")
        xbmctools.addFolder(FILENAME,__language__(30007), "Documentary(url)", "http://diziport.com/index.php?bolum=dizi&obje=diziler&tip=asya_dizileri")
        xbmctools.addFolder(FILENAME,__language__(30004), "Documentary(url)", "http://diziport.com/index.php?bolum=dizi&obje=diziler&tip=belgesel")  
       #xbmctools.addDir('Tum eklentiler ve daha fazlası -- xbmcTR.com--','Search',3,'')

         

def search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            #print query
            url = ('http://diziport.com/index.php?eleman=' + query + '&bolum=dizi&obje=diziler&olay=arama')
            print url
        link=xbmctools.get_url(url)
        match=re.compile('<li><img src="(.*?)\?hash=123" alt=".*?" width="113" height="113" />\n<a href="(.*?)" title="(.*?)">').findall(link)
        for thumbnail,url,videoTitle in match:
                xbmctools.addFolder(FILENAME,videoTitle,"Session(url)",'http://diziport.com/'+url,'http://diziport.com/'+thumbnail)
                        
def RECENT(url):
        link=xbmctools.get_url(url)       
        match=re.compile('<img src="(.+?)" alt=".+?" width="113" height="113" align="center" /></a>\n\t<h1 class="yellow"><a href="(.+?)" title="(.+?)">').findall(link)
        for thumbnail,url,videoTitle in match:
                xbmctools.addFolder("scraper",videoTitle,"prepare_list(videoTitle,url)",url,'http://diziport.com/'+thumbnail)
                
        #next page        
        page=re.compile('class=\'current\'><a><b>.+?</b></a></li>\n<li><a href=\'(.+?)\' rel=\'nofollow\'><b>(.+?)</b></a></li>').findall(link)
        for url,videoTitle in page:
                xbmctools.addFolder(FILENAME,__language__(30006)+' >> '+videoTitle,"RECENT(url)",'http://diziport.com/'+url,'special://home/addons/plugin.video.diziport/resources/images/next.png')
                
def Documentary(url):
        link=xbmctools.get_url(url)
        match=re.compile('<img src="(.*?)\?hash=123" alt=".*?" width="113" height="113" />\n<a href="(.*?)" title="(.*?)">').findall(link)
        for thumbnail,url,videoTitle in match:
                xbmctools.addFolder(FILENAME,videoTitle,"Session(url)",'http://diziport.com/'+url,'http://diziport.com/'+thumbnail)
        #next
        page=re.compile('<li><a href=\'(.*?)\' rel=\'nofollow\'><b>(.*?)</b>').findall(link)
        for url,videoTitle in page:
            xbmctools.addFolder(FILENAME,__language__(30006)+' >> '+videoTitle, "Documentary(url)", 'http://diziport.com/'+url)
        
        
def Categories(url):
        link=xbmctools.get_url(url)
        match=re.compile('<li><a href="(.+?)" alt=".+?" title="(.+?)">').findall(link)
        for url,videoTitle in match:
            xbmctools.addFolder(FILENAME,videoTitle,"Session(url)",'http://diziport.com/'+url,'')
        
def Session(url):
                link=xbmctools.get_url(url)
                match=re.compile('src="(.+?)" alt="" width="113" height="113" align="center"  />\n<a href="(.+?)" title="(.+?)"').findall(link)
                if match>[1]:
                        print 'sezonlu'
                        for thumbnail,url,videoTitle in match:
                                xbmctools.addFolder(FILENAME,videoTitle, "Episodes(url)", 'http://diziport.com/'+url)
                else:
                        print 'sezonsuz','--------------url------------',url
                        link=xbmctools.get_url(url)
                        new=re.compile('content="0;url=http://diziport.com/(.+?)"').findall(link)
                        if new<[1]:
                                print 'yonlendirmesiz','--------------url------------',url
                                Episodes(url)
                                
                        else:
                                print 'yonlendirmeli'
                                for url in new:
                                        Episodes('http://diziport.com/'+url)
                
def Episodes(url):
        link=xbmctools.get_url(url)
        match=re.compile('<a href="(.+?)"><img src="(.+?)" alt="(.+?)"').findall(link)
        for url,thumbnail,videoTitle in match:
            xbmctools.addFolder("scraper",videoTitle, "prepare_list(videoTitle,url)", 'http://diziport.com/'+url)        


def MAINMENU(url):
        xbmctools.addDir(__language__(30002),'http://diziport.com/','','special://home/addons/plugin.video.diziport/resources/images/main.jpg')
        

    
