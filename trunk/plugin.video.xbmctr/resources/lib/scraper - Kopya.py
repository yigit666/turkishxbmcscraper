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



def prepare_list(name,url):
        print url,'-------------------------'
        link=xbmctools.get_url(url)
        '----------------------------'
        if url.startswith('http://diziport.com'):
                match=re.compile('<b class="yellow"><a href="http://diziport.com/(.*?)-tekpartizle/(.*?)/1" title=".*?"><b class="yellow">Tek</b> Part</a>').findall(link)
                for u1,u2 in match:
                        url='http://diziport.com/playlist.php?bolum='+u2+'&dizi='+u1
                        print url,'------------diziport xml link----------'
                xmlScan=xbmctools.get_url(url)
                match=re.compile('<title>.*?</title>\n\t  <jwplayer:file>(.*?)</jwplayer:file>').findall(xmlScan)
                build_from_xml(match)
        else:
                pass
        '----------------------------'
        if url.startswith('http://yabancidiziizle.com'):
                match=re.compile('{ file: "(.*?)" }').findall(link)
                build_from_xml(match)
        else:
                pass
        '----------------------------'
        if url.startswith('http://www.dizihd.com'):
                match=re.compile('xmlAddress = \'(.+?)\'').findall(link)
                for url in match:
                        xmlScan=xbmctools.get_url(url)
                        match=re.compile('<videoPath value="(.+?)"').findall(xmlScan)
                        del match [0]
                build_from_xml(match)
        '----------------------------'
        if url.startswith('http://www.filmifullizle.com'):
                match=re.compile('<a href="(.*?)">Bolum .*?</a>').findall(link)
                build_from_page(url,match)
        else:
                pass

        '----------------------------'
        if url.startswith('http://video-klipleri.org/'):
                print 'Klip Source -----------------------'
                match=re.compile('http://player.iyimix.com/config/(.*?).xml').findall(link)
                for code in match:
                        url = 'http://player.iyimix.com/playlist/' + code+ '.xml'
                        link=xbmctools.get_url(url)
                        match=re.compile('<file>(.*?)</file>').findall(link)
                        del match[0]
                build_from_xml(match)
        else:
                pass


def build_from_page(url,match):
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
                for partLink in links:
                        link=xbmctools.get_url(url)
                        match=re.compile('<embed src=\'.*?file=(.*?)&a').findall(link)
                        for partLink in match:
                                name='Part'
                                nameCount=nameCount+1
                                name= name+' '+str(nameCount)
                        xbmctools.addVideoLink(name,partLink,'')
                        playList.add(partLink)
                xbmcPlayer.play(playList)
        if ret == 1:
                xbmcPlayer.play(playList)
                

        
def build_from_xml(match):
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
                        partLinkList = partLinkList + partLink
                        partLinkList = partLinkList + ':;'
                        xbmctools.addVideoLink(name,partLink,'')
                        playList.add(partLink)
                xbmcPlayer.play(playList)
             

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
