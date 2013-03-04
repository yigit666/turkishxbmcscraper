# -*- coding: iso-8859-9 -*-

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
import urllib,urllib2,re,sys,time,os
import xbmcplugin,xbmcgui,xbmcaddon,xbmc
import scraper, xbmctools
import string
import base64
from BeautifulSoup import BeautifulSoup as BS

## -------------   addon stuff--------------------------------------##
Addon = xbmcaddon.Addon('plugin.video.mc')
__settings__ = xbmcaddon.Addon(id='plugin.video.mc')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
XMLYOLU = xbmc.translatePath(os.path.join(home,'resources','temp'))
## ------------- ----------------------------------------------------##

##-------- web site stuff ---------------------------------------##
fileName = "test"

MAINSITE="http://www.dizimag.com/"
SEARCH="http://i.dizimag.com/cache/d.js?s91a5"
FRONTPAGE='http://dizimag.com/service/?ser=yenie&t=1&a='
max_yeni_sayfa = 5
## ------------- ----------------------------------------------------##


##------------- Constants --- Sabitler ---------------------------#
xbmcPlayer = xbmc.Player()
playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
Result=[]
MAINRESULT=[]
## ------------- ----------------------------------------------------##



def decode_base64(substring, encoded):
    std_base64chars = \
             "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    my_base64chars = \
             "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef%slmnopqrstuvwxyz0123456789+/"

    encoded = encoded.translate(string.maketrans(my_base64chars % substring, \
                                                 std_base64chars))
    return base64.b64decode(encoded)

def get_show(videoTitle,url):
        playList.clear()
        link=xbmctools.get(url)


        duyuruid = re.search(r'duyuruid="(.*?)";', link)
        
        if duyuruid:
            duyuruid = duyuruid.group(1)
           

        if not duyuruid:
            return

        duyuruid = "".join(re.findall(r'[ghijk]', duyuruid))
        

        encoded_parts = re.findall(r"jQuery\.dzm\.d\('(.*?)'\)", link)
        
        parts = [decode_base64(duyuruid, x) for x in encoded_parts]
        

        x=1
        for i in parts:
                xbmctools.addVideoLink(videoTitle+' Part '+str(x),i,'')
                playList.add(i)
                x+=1

        xbmcPlayer.play(playList)        

 

        
#yeni eklenen sayfayi tarar sonucu result icinde depolanır
def SCAN():
        def YENI_TARA(url):
                Result=[]
                link=xbmctools.get(url)
                match=re.compile(r'<a href=/(.*?) class=".*?"><img src=(.*?) class=".*?" width=.*?><span><h1>(.*?)</h1>(.*?)</span>').findall(link)
                for url,thumbnail,x,y in match:
                        thumbnail=thumbnail.replace("-avatar",'')
                        videoTitle=x+' - '+'('+y+')'
                        videoTitle=videoTitle.replace('\xfc',"u").replace('\xf6',"o")
                        url='http://dizimag.com/'+str(url)
                        Result.append((videoTitle,url,thumbnail,'aciklama'))
                return Result


        for i in range(1,max_yeni_sayfa):         
                Result=YENI_TARA(FRONTPAGE+str(i)) #sayfayi taramaya yolla
                MAINRESULT.extend(Result)          #gelen sonuclari birlestir.         
                
        filepath=xbmctools.xml_yap(fileName,MAINRESULT)#xml olusturur.
        

def main():
##        xbmctools.addFolder(fileName,__language__(30011), "search()", "","search")
        xbmctools.addFolder(fileName,__language__(30016), "YENI(url)", "http://dizimag.com/service/?ser=yenie&t=1&a=1","new")
##        xbmctools.addFolder(fileName,__language__(30043), "Yabanci(url)", "http://dizimag.com/servisler.asp?ser=liste","yabanci")

        xbmc.executebuiltin("Container.SetViewMode(500)")


def YENI(url):

        Sonuc=xbmctools.check_empty_xml("xml=XMLYOLU +'\\'+kanal+'.xml'") #xml varligini kontrol et

        if Sonuc == 'YOK':
                print 'XML YOK'
                SCAN()
                print 'XML OLUSTURULDU'
        else:
                print 'XML BULUNDU'
                pass

        finalResult=xbmctools.check_xml_time(fileName) #dosya tarihini kontrol et

        for videoTitle,url,thumbnail in finalResult:
                xbmctools.addVideoFolder(fileName,str(videoTitle),"get_show(videoTitle,url)",url,thumbnail,{"Title":videoTitle})
