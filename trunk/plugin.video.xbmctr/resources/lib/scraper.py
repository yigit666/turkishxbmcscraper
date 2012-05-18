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

# -*- coding: iso-8859-9 -*-
import urllib, urllib2, re, sys, cookielib
import xbmc, xbmcaddon, xbmcgui,xbmcplugin
import xbmctools


__settings__ = xbmcaddon.Addon(id='plugin.video.xbmctr')
__language__ = __settings__.getLocalizedString


FILENAME = "scraper"

#Used to allow the user to select quality on youtube videos
addonSettings = xbmcaddon.Addon(id='plugin.video.xbmctr')
videoQuality = ['small','medium','large','hd720']



'''Constants'''
xbmcPlayer = xbmc.Player()
playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)






'''
listing,pagination function
for multipage web site
'''

def prepare_page_list(Url,match):
        print match,url
        urlList=''
        for pageUrl in match:
                #web page list function
                urlList=urlList+pageUrl #add page to list
                urlList=urlList+':;'    #add seperator
                total=Url+':;'+urlList  #add first url
                match = total.split(':;') #split links
                del match [-1]            #delete first seperator
        info='Film '+str(len(match))+' part.'
        return match


def prepare_face_links(videoTitle,match):
        i=0
        for pageLink in match:
                link=xbmctools.get_url(pageLink)
                match=re.compile('<embed src=\'.*?file=(.*?)&a').findall(link)
                for videoLink in match:
                        i+=1
                        xbmctools.addVideoLink(videoTitle+' Part '+str(i),videoLink,'')
                        playList.add(videoLink)

def prepare_vk(videoTitle,match,mode):
        if mode == 2:
                vk_link = match
                set_vk(videoTitle,vk_link,'Tek Part')
        else:
                i=0
                for Url in match:
                        link=xbmctools.get_url(Url)
                        vk=re.compile('<iframe src="(.*?)" width="708" height="450" frameborder="0"></iframe>').findall(link)#check single part vk.com
                        for vk_link in vk:
                                i+= 1
                                set_vk(videoTitle,vk_link,i)

def set_vk(videoTitle,vk_link,i):
        link=xbmctools.get_url(vk_link)
        scan=re.compile('video_host = \'(.*?)/\';\nvar video_uid = \'(.*?)\';\nvar video_vtag = \'(.*?)\'').findall(link)
        for a,b,c in scan:
                #http://cs505211.userapi.com/u144315788/video/f879d60fb3.360.mp4
                videoLink=a +'/u'+ b +'/video/' + c + '.360.mp4'
                xbmctools.addVideoLink(videoTitle+' Part '+str(i),videoLink,'')
                playList.add(videoLink)
                #if i=='Tek Part':
                 #       return False
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)

def youtube_single(videoTitle,match):
        Url='plugin://plugin.video.youtube/?action=play_video&videoid=' + str(match)
        xbmctools.addVideoLink(videoTitle,Url,'')
        playList.add(Url)

        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)
                
def xml_scanner(videoTitle,match):        
        xmlScan=xbmctools.get_url(match)
        face_1=re.compile('<videoPath value="http://www.dizihd.com/(.+?)"').findall(xmlScan)#xml ici face link
        youtube_1=re.compile('v=(.*?)"').findall(xmlScan)#xml içi youtube link
        dizimag=re.compile('url="(.*?)"').findall(xmlScan) #xml ici dizimag                               
        music=re.compile('<file>(.*?)</file>').findall(xmlScan)
        try:
                if len(youtube_1)> 0  :
                        for i in youtube_1:
                                Url='plugin://plugin.video.youtube/?action=play_video&videoid='+str(youtube_1[0])
                                xbmctools.addVideoLink('Reklam',Url,'')
                x=1
                if len(face_1)> 0  :
                        for i in face_1:
                                Url='http://www.dizihd.com/'+str(i)
                                xbmctools.addVideoLink(videoTitle+' Part '+str(x),Url,'')
                                playList.add(Url)
                                x+=1
                if len(dizimag)> 0  :
                        for i in dizimag:
                                xbmctools.addVideoLink(videoTitle+' Part '+str(x),i,'')
                                playList.add(i)
                                x+=1
                if len(music)> 0  :
                        for i in music:
                                xbmctools.addVideoLink(videoTitle+' Part '+str(x),i,'')
                                playList.add(i)
                                x+=1
                                
        except:
                
                xbmcPlayer.play(playList)
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)



def prepare_list(videoTitle,Url):
        mode=''
        playList.clear()
        link=xbmctools.get_url(Url)

        tab=re.compile('<a href="(.*?)">Bolum [0-9].*?</a>').findall(link)#check full film multi part
        if len(tab) > 1:
                mode = 1 #multi page
        else:
                mode = 2 #single page
                
        face_1=re.compile('xmlAddress = \'(.+?)\'').findall(link)
        vk_1=re.compile('<iframe src="http://vk.com/(.*?)"').findall(link)
        vk_2=re.compile('video_host = \'(.*?)/\';\nvar video_uid = \'(.*?)\';\nvar video_vtag = \'(.*?)\'').findall(link)
        yabanci_1=re.compile('{ file: "(.*?)" }').findall(link)#sayfada face linkleri
        streamer=re.compile('streamer: "(.*?)"').findall(link)#sayfada streamer linki
        full_1=re.compile('<embed src=\'.*?file=(.*?)&a').findall(link)#check direct link
        full_2=re.compile('<iframe src="(.*?)" width="708" height="450" frameborder="0"></iframe>').findall(link)#check single part vk.com
        lowres=re.compile('dusuk="(.*?)"').findall(link)
        highres=re.compile('yuksek="(.*?)"').findall(link)
        sinema_1=re.compile('name=".*?file=(.*?)&image=.*?"').findall(link)
        youtube_1=re.compile('youtube.com/.*?/(.*?)\?').findall(link)
        youtube_2=re.compile('youtube.com/.*?/(.*?)"').findall(link)
        music=re.compile('http://player.iyimix.com/config/(.*?).xml').findall(link)
        result = face_1,vk_1,vk_2,yabanci_1,streamer,full_1,full_2,lowres,highres,sinema_1,youtube_1,youtube_2,music
        print result,Url

        

#mode ekleme
        x=1 #sayac
        for code in face_1:
                xml_scanner(videoTitle,code)

        for code in vk_1:
                if mode == 2:
                        Url = 'http://vk.com/'+str(vk_1[0])
                        prepare_vk(videoTitle,Url,mode)
                elif mode == 1:
                        match=prepare_page_list(Url,tab)# add first and all page to list
                        page = prepare_vk(videoTitle,match,mode) #send list to vk
        for code in youtube_1:
                if len(code)>1:
                        del youtube_2
                playList.clear()
                name='Youtube Alternatif '+str(x)
                youtube_single(videoTitle+name,code)
                x+=1
        for code in youtube_2:
                name='Youtube Alternatif '+str(x)
                youtube_single(videoTitle+name,code)
                x+=1

        for code in full_1:
                match = prepare_page_list(Url,tab)# add first and all page to list
                page = prepare_face_links(videoTitle,match) #send list to face

        for code in music:
                url = 'http://player.iyimix.com/playlist/' + code+ '.xml'
                xml_scanner(videoTitle,url)
        '''Dizimag section'''
        if len(lowres) > 0:
                dialog = xbmcgui.Dialog()
                ret = dialog.select(__language__(30008), [__language__(30045), __language__(30046)])
                if ret == 0:
                        for code in lowres:
                                url="http://www.dizimag.com/_list.asp?dil=1&x=%ss&d.xml"%(code)
                                xml_scanner(videoTitle,url) 
                if ret == 1:
                        for code in highres:
                                url="http://www.dizimag.com/_list.asp?dil=1&x=%ss&d.xml"%(code)
                                xml_scanner(videoTitle,url) 
        else:
                pass
        xbmcPlayer.play(playList)        

'''                
               '--------------------------------------------------------------------------------------------------------------------------'
        if Url.startswith('http://video-klipleri.org/'):
                print 'Klip Source -----------------------'
                code=re.compile(r'.*?_(.*?).html').findall(Url)
                Url = 'http://player.iyimix.com/playlist/' + code[0]+ '.xml'
                
                link2=xbmctools.get_url(Url)
                match=re.compile(r'<file.*?>(.*?)</file').findall(link2)
                dialog = xbmcgui.Dialog()
                ret = dialog.select(__language__(30008), [__language__(30045), __language__(30046)])
                if ret == 0:
                        xbmctools.addVideoLink(videoTitle,match[0],'')
                        playList.add(match[0])
                if ret == 1:
                        xbmctools.addVideoLink(videoTitle,match[1],'')
                        playList.add(match[1])

                                
                xbmcPlayer.play(playList)
                return code
        else:
                pass

    

'''
                
def build_from_page(videoTitle,url,match,genre):
        section='page'
        urlList=''
        nameCount=0
        playList.clear()
        dialog = xbmcgui.Dialog()
        ret = dialog.select(__language__(30008), [__language__(30009), __language__(30010)])
        if ret == 0:
                for pageUrl in match:
                        urlList=urlList+pageUrl
                        urlList=urlList+':;'
                #list all page
                        total=url+':;'+urlList
                        links = total.split(':;')
                        del links [-1]
                #grab partlink from list
                for pageLink in links:
                        link=xbmctools.get_url(pageLink)
                        match=re.compile('<embed src=\'.*?file=(.*?)&a').findall(link)
                        if len(match)>=1:
                        
                                name='Part'
                                for partLink in match:
                                        nameCount=nameCount+1
                                        name=str(name)+' '+str(nameCount)
                                        print partLink
                                        xbmctools.addVideoLink(videoTitle+' '+name,partLink,'')
                                        playList.add(partLink)
                        else:
                                match=re.compile('<iframe src="(.*?)hd=.*?"').findall(link)
                                for partLink in match:
                                        link=xbmctools.get_url(partLink)
                                        scan=re.compile('video_host = \'(.*?)/\';\nvar video_uid = \'(.*?)\';\nvar video_vtag = \'(.*?)\'').findall(link)
                                        name='Part'
                                        for a,b,c in scan:
                                              #http://cs505211.userapi.com/u144315788/video/f879d60fb3.360.mp4
                                              partLink=a +'/u'+ b +'/video/' + c + '.360.mp4'
                                        nameCount=nameCount+1
                                        name=str(name)+' '+str(nameCount)
                                        xbmctools.addVideoLink(videoTitle+' '+name,partLink,'')
                                        playList.add(partLink)
                xbmcPlayer.play(playList)
                                
                        
        if ret == 1:
                for pageUrl in match:
                                urlList=urlList+pageUrl
                                urlList=urlList+':;'
                                total=url+':;'+urlList
                xbmctools.Download_list(videoTitle,total,genre,section)
                

        
def build_from_xml(videoTitle,match,genre):
        section='xml'
        partLinkList = ''
        nameCount=0
        playList.clear()
        dialog = xbmcgui.Dialog()
        ret = dialog.select(__language__(30008), [__language__(30009), __language__(30010)])
        if ret == 0:
                for partLink in match:
                        name='Part'
                        nameCount=nameCount+1
                        name= name+' '+str(nameCount)
                        #add play all part keep from future
                        partLinkList = partLinkList + partLink
                        partLinkList = partLinkList + ':;'
                        xbmctools.addVideoLink(videoTitle+' '+name,partLink,'')
                        playList.add(partLink)
                xbmcPlayer.play(playList)
        if ret == 1:
                for partLink in match:
                                partLinkList = partLinkList + partLink
                                partLinkList = partLinkList + ':;'
                xbmctools.Download_list(videoTitle,partLinkList,genre,section)
        
        
def build_single(videoTitle,url):
       
        playList.clear()
        dialog = xbmcgui.Dialog()
        ret = dialog.select(__language__(30008), [__language__(30009), __language__(30010)])
        if ret == 0:
                playList.add(url)
                xbmcPlayer.play(playList)
        if ret == 1:
                xbmctools.Download_single(videoTitle,url)
                
