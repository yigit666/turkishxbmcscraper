# -*- coding: utf-8 -*-
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
from BeautifulSoup import BeautifulSoup as BS
import urllib,urllib2,re,sys,os

## -------------   addon stuff--------------------------------------##
Addon = xbmcaddon.Addon('plugin.video.mc')
__settings__ = xbmcaddon.Addon(id='plugin.video.mc')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
XMLYOLU = xbmc.translatePath(os.path.join(home,'resources','temp'))
## ------------- ----------------------------------------------------##

import xbmctools,resolver,scanner

fileName = "fullfilm"

'''Constants'''
player = xbmc.Player()
playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
KATEGORI=['kategoriler','yeni','yerli','yabanci','yabanci','tr_dublaj']

def main():
        kategori_list('http://www.filmifullizle.com')
        xbmctools.addFolder(fileName,__language__(30011), "Search()", "","search")
        xbmctools.addFolder(fileName,__language__(30016), "RUN(url,'yeni')", "http://www.filmifullizle.com/")
        xbmctools.addFolder(fileName,__language__(30039), "RUN(url,'yerli')", "http://www.filmifullizle.com/kategori/filmler/yerli-filmler",'')
        xbmctools.addFolder(fileName,__language__(30040), "RUN(url,'yabanci')", "http://www.filmifullizle.com/kategori/filmler/yabanci-filmler")
        xbmctools.addFolder(fileName,__language__(30041), "RUN(url,'tr_dublaj')", "http://www.filmifullizle.com/kategori/filmler/yabanci-filmler/turkce-dublaj")
        RUN("http://www.filmifullizle.com/",'kategoriler')

def kategori_list(url):
        link=xbmctools.get(url)
        match=re.compile(u'<li class=".*?"><a href=".*?" title=".*?">(.*?)</a>\n</li>').findall(link)
        for name in match:
                name=xbmctools.encode_fix(name)
                name=xbmctools.videoTitle_fix(name)
                name=name.replace(' ',"_")
                KATEGORI.append(name)
        return KATEGORI


def SCAN(marker,url):
        
        if player.isPlaying():
                player.stop()
        playlist.clear()
        print ('SCAN GIRIS:',marker,url)
        Result=[]
        BOLUM=''
        link=xbmctools.get(url)
        if marker=='kategoriler':
                BOLUM='kategoriler'
                match=re.compile(u'<li class=".*?"><a href="(.*?)" title=".*?">(.*?)</a>\n</li>').findall(link)
                for url,name in match:
                        name=xbmctools.encode_fix(name)
                        name=xbmctools.videoTitle_fix(name)
                        Result.append((name,url,'','aciklama'))
                filepath=xbmctools.xml_yap(fileName,BOLUM,Result)
        
        elif marker in KATEGORI:
                BOLUM=marker
                main=re.compile('<div style="float: left;">\n<a href="(.*?)"><img src="(.*?)" alt="(.*?)"').findall(link)
                for url,thumbnail,videoTitle in main:
                        videoTitle=xbmctools.encode_fix(videoTitle)
                        videoTitle=xbmctools.videoTitle_fix(videoTitle)
                        Result.append((videoTitle,url,thumbnail,'aciklama'))
                filepath=xbmctools.xml_yap(fileName,BOLUM,Result)
                
        elif marker=='video':
                BOLUM=marker
                value=scanner.TARA(url)
                for name,url in value:
                        Result.append((name,url,'','aciklama'))        
                for videoTitle,url,img,desc in Result:
                        if 'VK' in videoTitle:
                                playlist.add(url)
                        xbmctools.addVideoLink(videoTitle,url,'')
                xbmc.Player().play(playlist)

        else:
                print 'Bolum Bulunamadi'
                pass
                
        print ('BOLUM:',BOLUM)


def RUN(url,marker):
        KATEGORI=kategori_list('http://www.filmifullizle.com')
       
        if marker in KATEGORI:#gelen turu kontrol et klasor ise degistirme
                print 'MARKER VAR DOGRU',marker
                pass
        else:
                marker='video'  # video sayfasi ise marker video olacak
                
        finalResult=xbmctools.check_xml_status(fileName,marker,url) #dosya kontrol yoksa olustur varsa tarih bak oku listele
        
        for videoTitle,url,thumbnail in finalResult:
                if marker =='kategoriler':
                        videoTitle=videoTitle.replace(' ',"_")#kategorilerdeki boslugu alr cizgi ile degistir.Xml hatası olamsın diye
                else:
                        pass
                xbmctools.addVideoFolder(fileName,str(videoTitle),"RUN(url,videoTitle)",url,thumbnail,{"Title":videoTitle})
        

                

def NEXT(Url,marker):
        page=re.compile('<li class="active_page"><a href=".*?">.*?</a></li>\n<li><a href="(.*?)">(.*?)</a></li>').findall(link)
        for Url,name in page:
                xbmctools.addFolder(fileName,__language__(30006)+' >> '+name, "RUN(url,marker)",Url,"next")
        
     

def Search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            query=query.replace(' ','+')
            query=xbmctools.name_fix(query)       
            Url = ('http://www.filmifullizle.com/index.php?s=' + query)
            Recent(Url)


def MAINMENU(Url):
         xbmctools.addFolder(fileName,'<<<'+__language__(30002),"main()",'http://www.filmifullizle.com/','')


