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
import xbmctools,resolver
import mechanize

__settings__ = xbmcaddon.Addon(id='plugin.video.mc')
__language__ = __settings__.getLocalizedString


FILENAME = "scanner"




'''Constants'''
xbmcPlayer = xbmc.Player()
playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
value =[]


def TAB_LISTELE(Url,match):
        print 'Paging started'
        urlList=''
        for pageUrl in match:
                #web page list function
                urlList=urlList+pageUrl #add page to list
                urlList=urlList+':;'    #add seperator
                total=Url+':;'+urlList  #add first url
                match = total.split(':;') #split links
                del match [-1]            #delete first seperator
                #print match
        info='Film '+str(len(match))+' part.'
        print info
        return match


        
        
def TARA(tabList):
        Result=[]
        value =[]
        veri=[]
        vk=[]
        veri.append(tabList)
        print 'TABLIST',len(veri),veri
        for url in veri:
                print 'TARA GIRIS:',url
                playList.clear()
                mode=''
                link=xbmctools.get(url)
                divxstage=re.compile('src=.*?divxstage\.eu/embed\.php(.*?)\&').findall(link) 
                movshare=re.compile('src=.*?movshare\.net/embed\.php(.*?)\&').findall(link)        
                face_1=re.compile('xmlAddress = \'(.+?)\'').findall(link)
                vk_1=re.compile(r'http://vk.com/(.*?)"').findall(link)
                vk_2=re.compile('video_host = \'(.*?)/\';\nvar video_uid = \'(.*?)\';\nvar video_vtag = \'(.*?)\'').findall(link)
                streamer=re.compile('streamer: "(.*?)"').findall(link)#sayfada streamer linki
                full_1=re.compile('<embed src=\'.*?file=(.*?)&a').findall(link)#check direct link
                full_2=re.compile('<iframe src="(.*?)" width=".*?" height="450" frameborder="0"></iframe>').findall(link)#check single part vk.com
                full_3=re.compile('\/twtif.php\?id=(.*?)"').findall(link)
                lowres=re.compile('dusuk="(.*?)"').findall(link)
                highres=re.compile('yuksek="(.*?)"').findall(link)
                sinema_1=re.compile('name=".*?file=(.*?)&image=.*?"').findall(link)
                youtube_1=re.compile('youtube.com/.*?/(.*?)\?').findall(link)
                youtube_2=re.compile('youtube.com/.*?/(.*?)"').findall(link)
                music=re.compile('http://player.iyimix.com/config/(.*?).xml').findall(link)
                filmseven = re.compile('file=(.*?)&logo').findall(link)
##                print (' movshare= '+str(len(movshare)),
##                ' divxstage= '+str(len(divxstage)),
##                ' face_1= '+str(len(face_1)),
##                ' vk 1 = '+str(len(vk_1)),
##                ' vk 2 = '+str(len(vk_2)),
##                ' streamer='+str(len(streamer)),
##                ' full 1 = '+str(len(full_1)),
##                ' full 2 = '+str(len(full_2)),
##                ' full 3 = '+str(len(full_3)),
##                len(lowres),len(highres),
##                len(sinema_1),
##                ' youtube_1 = '+str(len(youtube_1)),
##                ' youtube_2 = '+str(len(youtube_2)),
##                ' music = '+str(len(music)))

                


                x=0 #sayac
                for code in face_1:
                        if len(code) > 0:
                                print '[face]'
                                value=code
                                
                                

                for code in divxstage:
                        if len(code) > 0:
                                print ('[divxstage]',divxstage)
                                findings=resolver.Divx(code)
                                value.append(('Divxshare ',findings))

                for code in movshare:
                        if len(code) > 0:
                                print ('[movshare]')
                                value=resolver.Mov(code)
                
                for code in vk_1:
                        print '[vk]'
                        code=code.replace('&#038;',"&")
                        Url = 'http://vk.com/'+code
                        vk.append(Url)
                        x+=1
                for code in youtube_1:
                        if len(code) > 0:
                                print '[youtube]'
                        

                       
                for code in youtube_2:
                        if len(code) > 0:
                                print ('[youtube]:',youtube_2)
                                findings=resolver.youtube_single(code)
                                value.append(('You Tube ',findings))
                                


                for code in full_1:
                        if len(code) > 0:
                                print '[full 1]'
        ##                match = prepare_page_list(Url,tab)# add first and all page to list
        ##                page = prepare_face_links(match) #send list to face
                        
                
                for code in music:
                        if len(code) > 0:
                                print '[music]'
                        url = 'http://player.iyimix.com/playlist/' + code+ '.xml'
        ##                xml_scanner(url)
                



                for code in streamer:
                        if len(code) > 0:
                                print '[streamer]'
                        url =code+'&&file=123.flv&start=0'



                
        if vk:
             vk_list=TAB_LISTELE('',vk)
             vk_sonuc=resolver.first_vk(vk_list)
             print vk_sonuc
             value.extend(vk_sonuc)
        print 'SCANNER VALUE:',value
        return value
def videoTitle_fix(videoTitle):
        videoTitle=videoTitle.replace(' Turkce Dublaj ',"TR").replace('izle',"").replace('Full',"").replace('(',"|").replace(')',"|")
        videoTitle=videoTitle.replace('\xc3\xa8',"'").replace('\xc5\x9f',"s").replace('&#038;',"&").replace('&#8217;',"'").replace('\xc3\xbc',"u").replace('\xc3\x87',"C").replace('\xc4\xb1',"i").replace('&#8211;',"-").replace('\xc3\xa7',"c").replace('\xc3\x96',"O").replace('\xc5\x9e',"S").replace('\xc3\xb6',"o").replace('\xc4\x9f',"g").replace('\xc3\X9C',"u").replace('\xc4\xb0',"I").replace('\xe2\x80\x93',"-")
        videoTitle=videoTitle.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g").replace('&#8211;',"-")
        videoTitle=videoTitle.replace('\u0131',"i")
        return videoTitle

##        if len(lowres) > 0:
##                dil=re.compile('dil=(.*?);').findall(link)
##                print dil,'**************** dil ************'
##                dialog = xbmcgui.Dialog()
##                ret = dialog.select(__language__(30008), [__language__(30045), __language__(30046)])
##                if ret == 0:
##                        for code in lowres:
##                                url="http://www.dizimag.com/_list.asp?dil="+str(dil[0])+"&x=%ss&d.xml"%(code)
##                                print url
##                                xml_scanner(url) 
##                if ret == 1:
##                        for code in highres:
##                                url="http://www.dizimag.com/_list.asp?dil="+str(dil[0])+"&x=%ss&d.xml"%(code)
##                                print url
##                                xml_scanner(url) 
##        else:
##                pass

##                xbmctools.addVideoLink(url,'')
        #i='http://llcdn8.twitvid.com/twitvidvideosv2/0/L/T/0LTBY.mp4?e=1343898960&r=twitvid.com,telly.com&h=4c6e2f034ef858ef295aa480cf8fe49c'
        #playList.add(i)
##        xbmcPlayer.play(playList)        
