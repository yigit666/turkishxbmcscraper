import urllib,urllib2,re,sys
import xbmcplugin,xbmcgui,xbmcaddon,xbmc
import scraper, xbmctools

# -*- coding: iso-8859-9 -*-
Addon = xbmcaddon.Addon('plugin.video.xbmcTR')
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmcTR')
__language__ = __settings__.getLocalizedString


FILENAME = "dizimag"
MAINSITE="http://www.dizimag.com/"

            
def main():
        xbmctools.addFolder(FILENAME,__language__(30011), "search()", '')
        xbmctools.addFolder(FILENAME,__language__(30016), "RECENT(url)", "http://dizimag.com/_yenie.asp?a=1")
        xbmctools.addFolder(FILENAME,__language__(30043), "Yabanci(url)", "http://dizimag.com/_diziliste.asp")

         

def search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            #print query
            url = ('http://diziport.com/index.php?eleman=' + query + '&bolum=dizi&obje=diziler&olay=arama')
            print url
        link=xbmctools.get_url(url)
        for thumbnail,url,videoTitle in match:
                xbmctools.addFolder(FILENAME,videoTitle,"Season(url)",'http://diziport.com/'+url,'http://diziport.com/'+thumbnail)

def Yabanci(url):
        link=xbmctools.get_url(url)
        match=re.compile('<a *?href="/([a-zA-Z0-9-]*?)" *?class="tdiz yabanci">(.*?)</a>').findall(link)
        for url,videoTitle in match:
                thumbnail='http://i.dizimag.com/dizi/'+url+'.jpg'
                xbmctools.addFolder(FILENAME,videoTitle,"Season(videoTitle,url,thumbnail)",MAINSITE+url,thumbnail)
        

def RECENT(url):
        MAINMENU(url)
        link=xbmctools.get_url(url)
        match=re.compile('<a href=/(.*?) class="yana.*?"><img src=(.*?) class=avatar width=40><span><h1>(.*?)</h1>(.*?)<').findall(link)        
        for url,thumbnail,x,y in match:
                print url
                videoTitle=x+' - '+'('+y+')'
                xbmctools.addFolder("scraper",videoTitle,"prepare_list(videoTitle,url)",MAINSITE+url,'http://i.dizimag.com/dizi/'+url+'.jpg')
                
        
def Season(videoTitle,url,thumbnail):
                print url,thumbnail
                link=xbmctools.get_url(url)
                match=re.compile('id=(.*?) onclick="Dizi').findall(link)
                episodeurl=""
                if match>[1]:
                        print 'sezonlu'
                        i=1
                        episodeurl=""
                        for count in match:
                                newurl=url+'-'+str(i)+'-sezon-dizi.html'
                                xbmctools.addFolder(FILENAME,videoTitle+__language__(30044)+ str(i), "Episodes(url)",newurl,"")
                                i+=1
               
                
def Episodes(url):
        link=xbmctools.get_url(url)
        match=re.compile('<br><a href="/(.*?)"><b style=color:yellow>(.*?)<font color=gray>(.*?)</font>').findall(link)
        for url,videoTitle,EpisodeNo in match:
            xbmctools.addFolder("scraper",videoTitle+EpisodeNo, "prepare_list(videoTitle,url)",MAINSITE+url,"")        


        
        
def MAINMENU(url):
         xbmctools.addFolder(FILENAME,'<<<'+__language__(30002),"main()",'http://diziport.com/','')

        
    
