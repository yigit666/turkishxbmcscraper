# xbmctr MEDIA CENTER, is an XBMC add on that sorts and displays 
# video content from several websites to the XBMC user.
#
# Copyright (C) 2011, Dr Ayhan Colak
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

'''
Author: drascom
Date: 13/04/2012
'''

import urllib, urllib2, re, sys, cookielib
import xbmc, xbmcaddon, xbmcgui,xbmcplugin
import xbmctools
import mechanize

__settings__ = xbmcaddon.Addon(id='plugin.video.mc')
__language__ = __settings__.getLocalizedString


FILENAME = "resolver"




def prepare_face_links(videoTitle,match):
        i=0
        for pageLink in match:
                link=xbmctools.get(pageLink)
                match=re.compile('<embed src=\'.*?file=(.*?)&a').findall(link)
                for videoLink in match:
                        i+=1
                        xbmctools.addVideoLink(videoTitle+' Part '+str(i),videoLink,'')
                        playList.add(videoLink)
def Divx(code):
        value=[]
        xbmc.executebuiltin('Notification("Media Center",DIVXSTAGE Deneniyor.)')
        url='http://embed.divxstage.eu/embed.php'+code
        link=xbmctools.get(url)
        match=re.compile('domain="http://www.divxstage.eu";\n\t\t\tflashvars.file="(.*?)";\n\t\t\tflashvars\.filekey="(.*?)"').findall(link)
        for dosya,key in match:
            url ='http://www.divxstage.eu/api/player.api.php?file='+dosya+'&key='+key
            link=xbmctools.get(url)
            match=re.compile('url=(.*?)&').findall(link)
            vaule=match[0]
        return value
def Mov(code):
        value=[]
        xbmc.executebuiltin('Notification("Media Center",MOVSHARE Deneniyor.)')
        url='http://embed.movshare.net/embed.php'+code
        link=xbmctools.get(url)
        match=re.compile('domain="http://www.movshare.net";\n\t\t\tflashvars.file="(.*?)";\n\t\t\tflashvars\.filekey="(.*?)"').findall(link)
        for dosya,key in match:
            url ='http://www.movshare.net/api/player.api.php?file='+dosya+'&key='+key
            link=xbmctools.get(url)
            match=re.compile('url=(.*?)&').findall(link)

            for url in match[0]:
                    if url.endswith('flv'):
                            value.append((url,''))
                    else:
                            value=''
                            print 'movshare Web Sayfa Hatasi'
                            return ["/unable to play " + url]               

def fullfilm_singlepage(videoTitle,code):
        url="http://www.filmifullizle.com/db/tw-"+str(code)+".mp4"
        request = mechanize.Request(url)
        response = mechanize.urlopen(request)
        url = response.geturl()
        response.close()
        xbmctools.addVideoLink(videoTitle,str(url),'')
        playList.add(url)

def fullfilm_multipage(videoTitle,match):
        print videoTitle,match,'**************************************'
        i=0
        for pageLink in match:
                print pageLink
                link=xbmctools.get(pageLink)
                match=re.compile('\/twtif.php\?id=(.*?)"').findall(link)
                for code in match:
                        i+=1
                        url="http://www.filmifullizle.com/db/tw-"+str(code)+".mp4"
                        print url
                        try:
                                request = mechanize.Request(url)
                                response = mechanize.urlopen(request)
                                url = response.geturl()
                                response.close()
                                xbmctools.addVideoLink(' Part '+str(i),str(url),'')
                                playList.add(url)
                        except :
                                xbmc.executebuiltin('Notification("Media Center",Part Linki Kırık)')
                                return
                        


        

def first_vk(vk_list):
        value=[]
        count=[]
        fixed=''
        gecis=0
        resolutions = ["240", "360", "480", "720", "1080"]
        del vk_list[0]
        print 'VK LIST',vk_list
        for url in vk_list:
                link=xbmctools.get2(url)
                host=re.compile("host=(.*?)&").findall(link)
                uid=re.compile("uid=(.*?)&").findall(link)
                vtag=re.compile("vtag=(.*?)&").findall(link)
                hd = re.compile("hd_def=(.*?)&").findall(link)
                flv = re.compile("no_flv=(.*?)&").findall(link)
                #http://cs514110.userapi.com/u175995076/video/ac8f196d08.xxx.mp4
                start_url=host[0]+'u'+uid[0]+'/video/' + vtag[0]
                x=(int(hd[0])+1)
                if hd >0 or flv == 1:
                        for i in range (x):
                                i=resolutions[i]+' p'
                                count.append(i) 
                        if gecis==0:
                                dialog = xbmcgui.Dialog()
                                ret = dialog.select(__language__(30008),count)
                                for i in range (x):
                                        if ret == i:
                                                url=start_url+'.'+str(resolutions[i])+'.mp4'
                                                fixed=str(resolutions[i])
                                                gecis+=1
                                                
                                        else:
                                                'VK SECIM YOK'
                        else:
                                url=start_url+'.'+fixed+'.mp4'
                                print 'SECIM KULLANILDI'
                                gecis+=1
                        value.append(('VK Part '+str(gecis),url))
                else:
                        print 'HD FLV YANLIS'
                        
                        

        return value
        
       
        

def youtube_single(code):
        code='plugin://plugin.video.youtube/?action=play_video&videoid=' + str(code)
        return code
                
def xml_scanner(videoTitle,match):
        playList.clear()
        xmlScan=xbmctools.get(match)
        face_1=re.compile('http://dizihd.com/dizihdd.php(.+?)"').findall(xmlScan)#xml ici face link
        youtube_1=re.compile('v=(.*?)"').findall(xmlScan)#xml içi youtube link
        dizimag=re.compile('url="(.*?)"').findall(xmlScan) #xml ici dizimag                               
        music=re.compile('<file>(.*?)</file>').findall(xmlScan)
        try:
                if len(youtube_1)> 0  :
                        print '[youtube]'
                        for i in youtube_1:
                                Url='plugin://plugin.video.youtube/?action=play_video&videoid='+str(youtube_1[0])
                                xbmctools.addVideoLink('Reklam',Url,'')
                x=1
                if len(face_1)> 0  :
                        print '[face]'
                        for i in face_1:
                                print i
                                Url='http://dizihd.com/dizihdd.php'+str(i)
                                xbmctools.addVideoLink(videoTitle+' Part '+str(x),Url,'')
                                playList.add(Url)
                                x+=1
                if len(dizimag)> 0  :
                        print '[dizimag]'
                        for i in dizimag:
                                print i
                                xbmctools.addVideoLink(videoTitle+' Part '+str(x),i,'')
                                playList.add(i)
                                x+=1
                if len(music)> 0  :
                        print '[music]'
                        for i in music:
                                xbmctools.addVideoLink(videoTitle+' Part '+str(x),i,'')
                                playList.add(i)
                                x+=1
                                
                                
        except:
                
                xbmcPlayer.play(playList)
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)




