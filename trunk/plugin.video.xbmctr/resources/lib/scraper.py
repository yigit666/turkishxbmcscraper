﻿# Multi Documentary Streams, is an XBMC add on that sorts and displays 
# video content from several websites to the XBMC user.
#
# Copyright (C) 2011, Ricardo Ocana Leal
#
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
'''
Editor: drascom
Date: 13/04/2012
'''

# -*- coding: iso-8859-9 -*-
import urllib, urllib2, re, sys, cookielib
import xbmc, xbmcaddon, xbmcgui
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
        urlList=''
        for pageUrl in match:                   #web page list function
                urlList=urlList+pageUrl #add page to list
                urlList=urlList+':;'    #add seperator
                total=Url+':;'+urlList  #add first url
                match = total.split(':;') #split links
                del match [-1]            #delete first seperator
        info='Film '+str(len(match))+' part.'
        print info
        return match


def prepare_play_links(videoTitle,match):
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
                for vk_link in match:
                        i+= 1
                        set_vk(videoTitle,vk_link,i)

def set_vk(videoTitle,vk_link,i):
        link=xbmctools.get_url(vk_link)
        vk=re.compile('<iframe src="(.*?)" width="708" height="450" frameborder="0"></iframe>').findall(link)
        print vk_link,vk,'*******************  vk    ***************'       
        for pageLink in vk:
                link=xbmctools.get_url(pageLink)
                scan=re.compile('video_host = \'(.*?)/\';\nvar video_uid = \'(.*?)\';\nvar video_vtag = \'(.*?)\'').findall(link)
                print scan,'**********scan********'
                for a,b,c in scan:
                        #http://cs505211.userapi.com/u144315788/video/f879d60fb3.360.mp4
                        videoLink=a +'/u'+ b +'/video/' + c + '.360.mp4'
                        xbmctools.addVideoLink(videoTitle+' Part '+str(i),videoLink,'')
                        playList.add(videoLink)











def prepare_list(videoTitle,Url):
        playList.clear()
        link=xbmctools.get_url(Url)
        '----------------------------'
        if Url.startswith('http://diziport.com'):
                match=re.compile('<b class="yellow"><a href="http://diziport.com/(.*?)-tekpartizle/(.*?)/1" title=".*?"><b class="yellow">Tek</b> Part</a>').findall(link)
                for u1,u2 in match:
                        url='http://diziport.com/playlist.php?bolum='+u2+'&dizi='+u1
                        print url,'------------diziport xml link----------'
                xmlScan=xbmctools.get_url(url)
                match=re.compile('<title>.*?</title>\n\t  <jwplayer:file>(.*?)</jwplayer:file>').findall(xmlScan)
                build_from_xml(videoTitle,match,'tvshow')
        else:
                pass
        '----------------------------'
        if Url.startswith('http://yabancidiziizle.com'):
                match=re.compile('{ file: "(.*?)" }').findall(link)
                build_from_xml(videoTitle,match,'tvshow')
        else:
                pass
        '----------------------------'
        if Url.startswith('http://www.dizihd.com'):
                match=re.compile('xmlAddress = \'(.+?)\'').findall(link)
                if len (match)<= 0:
                        vk=re.compile('<iframe src="(.*?)"').findall(link)
                        for url in vk:
                                link=xbmctools.get_url(url)
                                scan=re.compile('video_host = \'(.*?)/\';\nvar video_uid = \'(.*?)\';\nvar video_vtag = \'(.*?)\'').findall(link)
                                for a,b,c in scan:
                                      #http://cs505211.userapi.com/u144315788/video/f879d60fb3.360.mp4
                                      result=a +'/u'+ b +'/video/' + c + '.360.mp4'
                                build_single(videoTitle,result)
                                return False
                else:
                        for xml in match:
                                xmlScan=xbmctools.get_url(xml)
                                match=re.compile('v=(.+?)"').findall(xmlScan)
                                print match,'***************************'
                                if match<=2:
                                        for code in match:
                                                youtube='plugin://plugin.video.youtube/?action=play_video&videoid=' + code
                                                build_single(videoTitle,youtube)
                                                #xbmctools.addVideoLink(videoTitle,youtube,'')
                                                return False
                                else:
                                        match=re.compile('<videoPath value="(.+?)"').findall(xmlScan)
                try:
                        youtubelist=re.compile('/embed/(.*?)"').findall(link)
                        for code in youtubelist:
                                match='plugin://plugin.video.youtube/?action=play_video&videoid=' + code
                                print match,'youtubelist'
                except:
                        
                        pass
                build_from_xml(videoTitle,match,'tvshow')
        '----------------------------'
        if Url.startswith('http://www.filmifullizle.com'):
                match=re.compile('<embed src=\'.*?file=(.*?)&a').findall(link)#check xml link
                code = 1
                if not match:
                        match=re.compile('<iframe src="(.*?)" width="708" height="450" frameborder="0"></iframe>').findall(link)#check single part vk.com
                        code = 2
                if not match:
                        match=re.compile('src="http://www.youtube.com/embed/(.*?)"').findall(link)#check youtube
                        code = 3
                
                page=re.compile('<a href="(.*?)">Bolum .*?</a>').findall(link)#check multi part
                if len(page) > 1:
                        mode = 1
                else:
                        mode = 2
                
                print mode;print code;print '*************************** mode code *******************'
                if mode == 1:
                        if code == 1:#multi page facebook direct
                                match = prepare_page_list(Url,match)# add first page to list
                                page = prepare_play_links(videoTitle,match)
                        else:        #multipage vk.video
                                match = prepare_page_list(Url,page)
                                print match,' 1 in 2 si match'
                                page = prepare_vk(videoTitle,match,mode)
                                
                                
                elif mode == 2:
                        if code == 2:    #single vk.video                                              
                                match = prepare_vk(videoTitle,Url,mode)
                        else:
                                
                                videoLink='plugin://plugin.video.youtube/?action=play_video&videoid=' + str(match[0])
                                xbmctools.addVideoLink(videoTitle+' Fragman ',videoLink,'')
                                playList.add(videoLink)

                else:
                        print '*************************** code mode fısss *******************'
                                     
                xbmcPlayer.play(playList)               
        else:
                pass

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

        '--------------------------------------------------------------------------------------------------------------------------'
        if Url.startswith('http://www.dizimag.com'):
                lowres=re.compile('dusuk="(.*?)"').findall(link)
                highres=re.compile('yuksek="(.*?)"').findall(link)
                dialog = xbmcgui.Dialog()
                ret = dialog.select(__language__(30008), [__language__(30045), __language__(30046)])
                if ret == 0:
                        for x in lowres:
                                print x
                                url="http://www.dizimag.com/_list.asp?dil=1&x=%ss&d.xml"%(x)
                                link=xbmctools.get_url(url)
                                match=re.compile('url="(.*?)"').findall(link)
                        build_from_xml(videoTitle,match,'tvshow')
                if ret == 1:
                        for x in highres:
                                url="http://www.dizimag.com/_list.asp?dil=1&x=%ss&d.xml"%(x)
                                link=xbmctools.get_url(url)
                                match=re.compile('url="(.*?)"').findall(link)
                        build_from_xml(videoTitle,match,'tvshow')
        else:
                pass

                 
        '--------------------------------------------------------------------------------------------------------------------------'
        if Url.startswith('http://www.sinemaizle.org'):
                match=re.compile('name=".*?file=(.*?)&image=.*?"').findall(link)
                build_from_xml(videoTitle,match,'movie')
        else:
                pass


                
def build_from_page(videoTitle,url,match,genre):
        print videoTitle,url,match,
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
                                print match,'********************** xml ************************'
                                name='Part'
                                for partLink in match:
                                        nameCount=nameCount+1
                                        name=str(name)+' '+str(nameCount)
                                        print partLink
                                        xbmctools.addVideoLink(videoTitle+' '+name,partLink,'')
                                        playList.add(partLink)
                        else:
                                match=re.compile('<iframe src="(.*?)hd=.*?"').findall(link)
                                print match,'********************** vk link ************************'
                                for partLink in match:
                                        link=xbmctools.get_url(partLink)
                                        scan=re.compile('video_host = \'(.*?)/\';\nvar video_uid = \'(.*?)\';\nvar video_vtag = \'(.*?)\'').findall(link)
                                        name='Part'
                                        for a,b,c in scan:
                                              #http://cs505211.userapi.com/u144315788/video/f879d60fb3.360.mp4
                                              partLink=a +'/u'+ b +'/video/' + c + '.360.mp4'
                                        nameCount=nameCount+1
                                        name=str(name)+' '+str(nameCount)
                                        print partLink
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
        print match,'*************xml*******************************'
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
                





                
def live(url):
        data = open(url, 'r').read()
        soup = BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        if len(soup('channels')) > 0:
            channels = soup('channel')
            for channel in channels:
                name = channel('name')[0].string
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    thumbnail = ''
        channel_list = soup.find('channel', attrs={'name' : name})
        items = channel_list('item')
        for channel in channel_list('subchannel'):
            name = channel('name')[0].string
            try:
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
        xbmctools.addFolder(FILENAME,videoTitle,"getChannelItems(name,url)",url,thumbnail)

def youTube(url, name, playlist=False):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8')
    response = urllib2.urlopen(req)
    link = response.read()
    precode = re.compile('url_encoded_fmt_stream_map=(.*)').findall(link)
    code = re.compile('url%3Dhttp%253A%252F%252F(.+?)%26itag').findall(precode[0])
    videourl = getQualityUrl(code)
    stringurl = "http://"+videourl.replace('%25','%')
    stringurl = stringurl.replace('\\','').replace('%2F','/').replace('%3F','?').replace('%3D','=').replace('%25','%').replace('%2F','/').replace('%26','&').replace('%2C', ',')
    stringurl += " | Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8"
    if playlist:
        liz = xbmcgui.ListItem(name)
        xbmc.PlayList(xbmc.PLAYLIST_VIDEO).add(url = stringurl, listitem=liz)
    else:
        xbmctools.addVideoLink("Play "+name, stringurl)
