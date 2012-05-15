import urllib,urllib2,re,sys
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
import scraper, xbmctools

# -*- coding: iso-8859-9 -*-
Addon = xbmcaddon.Addon('plugin.video.xbmcTR')
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmcTR')
__language__ = __settings__.getLocalizedString



FILENAME = "dizimag"
MAINSITE="http://www.dizimag.com/"
SEARCH="http://i.dizimag.com/cache/d.js?s91a5"

            
def main():
        xbmctools.addFolder(FILENAME,__language__(30011), "search()", '')
        xbmctools.addFolder(FILENAME,__language__(30016), "RECENT(url)", "http://dizimag.com/_yenie.asp?a=1")
        xbmctools.addFolder(FILENAME,__language__(30043), "Yabanci(url)", "http://dizimag.com/_diziliste.asp")


        

def search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            query=query.replace(' ','+')
            query=xbmctools.name_fix(query)
            print query
            url = SEARCH
            link=xbmctools.get_url(url)      
            match=re.compile('{ d: "*'+query+'.*?", s: "(.*?)" }').findall(link)
            print match
            for url in match:
                   videoTitle=re.compile('/([^ ]*)').findall(str(url))
                   videoTitle=xbmctools.name_fix(videoTitle[0])
                   url="http://www.dizimag.com"+str(url)
                   xbmctools.addFolder(FILENAME,videoTitle,"Season(videoTitle,url,'')",url,'')

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
                                xbmctools.addFolder(FILENAME,videoTitle+'  '+__language__(30044)+ str(i), "Episodes(videoTitle,url)",newurl,"")
                                i+=1
               
                
def Episodes(videoTitle,url):
        link=xbmctools.get_url(url)
        match=re.compile('<td width=30 class=fp><a href="(.*?).html"><img src=(.*?).jpg class=avatar width=30 height=30></a>').findall(link)
        for url,thumbnail in match:
                videoTitle=re.compile('/(.*?)-izle-dizi').findall(str(url))
                for name in videoTitle:
                        videoTitle=xbmctools.name_fix(name)
                url="http://www.dizimag.com"+str(url)+'.html'
                xbmctools.addFolder("scraper",videoTitle, "prepare_list(videoTitle,url)",url,'')        

       


def MAINMENU(url):
         xbmctools.addFolder(FILENAME,'<<<'+__language__(30002),"main()",'http://diziport.com/','')

        
    
