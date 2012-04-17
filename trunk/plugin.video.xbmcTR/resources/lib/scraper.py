# Multi Documentary Streams, is an XBMC add on that sorts and displays 
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


import urllib, urllib2, re, sys, cookielib
import xbmc, xbmcaddon, xbmcgui
import xbmctools


__settings__ = xbmcaddon.Addon(id='plugin.video.multidocs')
__language__ = __settings__.getLocalizedString


FILENAME = "scraper"

#Used to allow the user to select quality on youtube videos
addonSettings = xbmcaddon.Addon(id='plugin.video.multidocs')
videoQuality = ['small','medium','large','hd720']

def Diziport(name,url):
        link=xbmctools.get_url(url)
        match=re.compile('<b class="yellow"><a href="http://diziport.com/(.*?)-tekpartizle/(.*?)/1" title=".*?"><b class="yellow">Tek</b> Part</a>').findall(link)
        for u1,u2 in match:
            url='http://diziport.com/playlist.php?bolum='+u2+'&dizi='+u1
        link=xbmctools.get_url(url)
    #creating url list for playlist
        partLinks = ''
        #this is final resolved mp4 url
        match=re.compile('<title>(.*?)</title>\n\t  <jwplayer:file>(.*?)</jwplayer:file>').findall(link)
                            
    #dialog let user choose watch or download...
        dialog = xbmcgui.Dialog()
        ret = dialog.select(__language__(30008), [__language__(30009), __language__(30010)])
        if ret == 0:
                for linkTitle,partLink in match:
                        videoTitle =str(linkTitle)
                        partLinks = partLinks + partLink
                        partLinks = partLinks + ':;'
                        listitem = xbmcgui.ListItem( linkTitle, iconImage="DefaultVideo.png", thumbnailImage='special://home/addons/plugin.video.diziport/resources/images/main.jpg')
                        listitem.setInfo( type="Video", infoLabels={ "Title": videoTitle } )
                        ok=True
                #create seperate links
                        xbmctools.addVideoLink(videoTitle,partLink,'')
                #create url1:;url2:;url3.....an send a directory to resolve and add to playlist...
                playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                playList.clear()
                #time.sleep(2)
                links = partLinks.split(':;')
                del links[-1]
                pDialog = xbmcgui.DialogProgress()
                ret = pDialog.create('Loading playlist...')
                totalLinks = len(links)
                loadedLinks = 0

                for videoLink in links:
                        playList.add(videoLink)
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = __language__(30019)+' [B]' +str(loadedLinks)+' / '+str(totalLinks)+'[/B]'+ __language__(30018)
                        pDialog.update(percent,__language__(30002),remaining_display)
                        if (pDialog.iscanceled()):
                                return False
                xbmcPlayer = xbmc.Player()
                xbmcPlayer.play(playList)
                if not xbmcPlayer.isPlayingVideo():
                        d = xbmcgui.Dialog()
                        d.ok('INVALID VIDEO PLAYLIST', 'videos cannot find.','Check other links.')
        return ok
                        
        if ret == 1:
                d = xbmcgui.Dialog()
                d.ok('HAZIR DEGIL', 'Acele Etmeyin.','Yakinda Hazir olacak.')

def yabancidizi(name,url):
        link=xbmctools.get_url(url)
#xml okuma
        page=re.compile('{ file: "(.*?)" }').findall(link)
        epname= 'part'
        a=0
#Create playlist
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
		
        for url in page:
                        a= a+1
                        name = epname + ' - '+str(a)
                        playList.add(url)
                        xbmctools.addLink(name,url,'')
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                        d = xbmcgui.Dialog()
                        d.ok('INVALID VIDEO PLAYLIST', 'videos cannot find.','Check other links.')
                        
def Dizihd(name,url):
        ok= True
        link=xbmctools.get_url(url)
#xml okuma
        page=re.compile('xmlAddress = \'(.+?)\'').findall(link)
        if len (page)<= 0:
                vk=re.compile('<iframe src="(.*?)"').findall(link)
                for url in vk:
                        vk_com(url)
                return False
        epname= 'part'
        a=0
#Create playlist
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
#xmlAddress = 'http://www.dizihd.com/player/dizihd/supernaturals07e01hd.xml'
        for url in page:
                link=xbmctools.get_url(url)
                #<videoPath value="http://www.dizihd.com/dizihdd.php?git=http://video.ak.fbcdn.net/cfs-ak-ash4/344221/498/112810335493302_60183.mp4"/>
                match=re.compile('<videoPath value="(.+?)"').findall(link)
                del match [0]
                for url in match:
                        a= a+1
                        name = epname + ' - '+str(a)
                        playList.add(url)
                        xbmctools.addLink(name,url,'special://home/addons/plugin.video.dizihd/resources/images/izle.png')
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                        d = xbmcgui.Dialog()
                        d.ok('INVALID VIDEO PLAYLIST', 'videos cannot find.','Check other links.')
        return ok
def vk_com(url):
      link=xbmctools.get_url(url)
      match=re.compile('video_host = \'(.*?)/\';\nvar video_uid = \'(.*?)\';\nvar video_vtag = \'(.*?)\'').findall(link)
      for a,b,c in match:
              #http://cs505211.userapi.com/u144315788/video/f879d60fb3.360.mp4
              url=a +'/u'+ b +'/video/' + c + '.360.mp4'
              xbmctools.addLink('Play',url,'')
def fullfilm(url):
        ok = True
        liste=''
        link=xbmctools.get_url(url)
        match=re.compile('<a href="(.*?)">Bolum .*?</a>').findall(link)
        for link in match:
                liste=liste+link
                liste=liste+':;'
        total=url+':;'+liste
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        links = total.split(':;')
        del links [-1]
        totalLinks = len(links)
        loadedLinks = 0
        a=0
        for url in links:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<embed src=\'.*?file=(.*?)&a').findall(link)
                for partLink in match:
                        name='Part'
                        a=a+1
                        name= name+' '+str(a)
                        xbmctools.addVideoLink(name,partLink,'')
                        playList.add(partLink)
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = __language__(30019)+' [B]' +str(loadedLinks)+' / '+str(totalLinks)+'[/B]'+ __language__(30018)
                        pDialog.update(percent,__language__(30002),remaining_display)
                        if (pDialog.iscanceled()):
                                return False

        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)

def klip(url):
        link=xbmctools.get_url(url)
        match=re.compile('http://player.iyimix.com/config/(.*?).xml').findall(link)
        for code in match:
                url = 'http://player.iyimix.com/playlist/' + code+ '.xml'
                link=xbmctools.get_url(url)
                sd=re.compile('<file>(.*?)</file>').findall(link)
                del sd[0]
                name=re.compile('<title>(.*?)</title>').findall(link)
                for url in sd:
                        xbmctools.addVideoLink('Play',url,'')
                xbmcPlayer = xbmc.Player()
                xbmcPlayer.play(url)
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
def Download(url):
       filename = (name+'.mp4')
       downloadFolder = __settings__.getSetting('downloadFolder')
       if downloadFolder is '':
                d = xbmcgui.Dialog()
                d.ok('Download Error','You have not set the download folder.\n Please set the addon settings and try again.','','')
                __settings__.openSettings(sys.argv[ 0 ])
       else:
                if not os.path.exists(downloadFolder):
                        print 'Download Folder Doesnt exist. Trying to create it.'
                        os.makedirs(downloadFolder)

                def download(url, dest):
                                dialog = xbmcgui.DialogProgress()
                                dialog.create('Downloading Movie','From Source', filename)
                                urllib.urlretrieve(url, dest, lambda nb, bs, fs, url = url: _pbhook(nb, bs, fs, url, dialog))
                def _pbhook(numblocks, blocksize, filesize, url = None,dialog = None):
                                try:
                                                percent = min((numblocks * blocksize * 100) / filesize, 100)
                                                dialog.update(percent)
                                except:
                                                percent = 100
                                                dialog.update(percent)
                                if dialog.iscanceled():
                                                dialog.close()
                if (__settings__.getSetting('downloadFolder') == ''):
                                __settings__.openSettings('downloadFolder')
                filepath = xbmc.translatePath(os.path.join(__settings__.getSetting('downloadFolder'),filename))
                download(url, filepath)
                iscanceled = True
                xbmc.executebuiltin('Notification("Diziport","Select&Download")')
