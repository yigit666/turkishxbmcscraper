#-*-coding: iso-8859-9 -*-
import urllib,urllib2,re,sys,time,os
import xbmcplugin,xbmcgui,xbmcaddon,xbmc

from BeautifulSoup import BeautifulSoup as BS


## -------------   addon stuff--------------------------------------##
Addon = xbmcaddon.Addon('plugin.video.mc')
__settings__ = xbmcaddon.Addon(id='plugin.video.mc')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
XMLYOLU = xbmc.translatePath(os.path.join(home,'resources','temp'))
## ------------- ----------------------------------------------------##

import xbmctools,resolver,scanner

fileName = "bicaps"
count=0
xbmcPlayer = xbmc.Player()
playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)




def main():
        #xbmctools.addFolder(fileName,__language__(30011), "search()", "","search")
        xbmctools.addFolder(fileName,__language__(30016), "RUN(url,'yeni')", "http://bicaps.com/")
        xbmctools.addFolder(fileName,__language__(30017), "RUN(url,'kategoriler')", "http://bicaps.com/")

        xbmc.executebuiltin("Container.SetViewMode(500)")

def SCAN(marker,url):
        print ('SCAN GIRIS:',marker,url)
        Result=[]
        BOLUM=''
        value=''
        link=xbmctools.get(url)
        soup = BS(link)
        if marker=='kategoriler':
                BOLUM='kategoriler'
                panel = soup.findAll("div", {"class": "sidebar-right"},smartQuotesTo=None)
                liste=BS(str(panel))
                for li in liste.findAll('li'):
                    a=li.find('a')
                    url= a['href']
                    videoTitle= li.text
                    videoTitle=xbmctools.encode_fix(videoTitle)
                    Result.append((videoTitle,url,'','aciklama'))

                filepath=xbmctools.xml_yap(fileName,BOLUM,Result)
        
        elif marker in ("yerli", "yabanci","tr_dublaj","yeni"):
                BOLUM=marker
                panel = soup.findAll("div", {"class": "leftC"},smartQuotesTo=None)
                panel = panel[0].findAll("div", {"class": "moviefilm"})
                
                for i in range (len (panel)): 
                        a=panel[i].find('a')
                        url= a['href']
                        img=panel[i].find('img')
                        thumbnail= img['src']
                        videoTitle=img['alt']
                        videoTitle=xbmctools.encode_fix(videoTitle)
                        Result.append((videoTitle,url,thumbnail,'aciklama'))
                        
                filepath=xbmctools.xml_yap(fileName,BOLUM,Result)
                
        elif marker=='video':
                BOLUM=marker
                tabList=TABS(url,link)#parların url lerini al 1. ile birleştir liste yap
                print 'TAB LIST:',tabList
                
                Result=scanner.TARA(tabList)#listedeki herbir url için videolink taraması yap
                print 'SCAN VALUE:',Result
                for server,url in value:
                        Result.extend((server,url))
                
                        
                print 'video RESULT:',Result

        else:
                print 'Bolum Bulunamadi'
                pass
                
        print ('BOLUM:',BOLUM)
        return Result


def RUN(url,marker):
        if marker in ("yerli", "yabanci","tr_dublaj","yeni","kategoriler"):#gelen turu kontrol et klasor ise degistirme
                pass
        else:
                marker='video'  # video sayfasi ise marker video olacak

        if marker =='video':
                finalResult=SCAN(marker,url)
                for x in finalResult:
                        name=x[0]
                        url=x[1]
                        xbmctools.addVideoLink(name,url,'')   
        else:
                finalResult=xbmctools.check_xml_status(fileName,marker,url) #dosya kontrol yoksa olustur varsa tarih bak oku listele
                for videoTitle,url,thumbnail in finalResult:
                        videoTitle=xbmctools.encode_fix(videoTitle)
                        xbmctools.addVideoFolder(fileName,str(videoTitle),"RUN(url,videoTitle)",url,thumbnail,{"Title":videoTitle})
                
def TABS(url,link):
        value=[]
        soup = BS(link)
        panel = soup.findAll("div", {"class": "keremiya_part"})
        match=re.compile('<a href="(.*?)"><span>.*?</span></a>').findall(str(panel[0])) #tab url ler bulunuyor.
        if len(match)<1:
                xbmc.executebuiltin('Notification("Media Center",TAB BOS YADA HATALI)')
        
        value=scanner.TAB_LISTELE(url,match)
        return value
        


      
