# -*- coding: utf-8 -*-

import urllib
import urllib2
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
from BeautifulSoup import BeautifulStoneSoup, BeautifulSoup, BeautifulSOAP
try:
    import json
except:
    import simplejson as json

addon = xbmcaddon.Addon('plugin.video.xbmcTR')
profile = xbmc.translatePath(addon.getAddonInfo('profile'))
__settings__ = xbmcaddon.Addon(id='plugin.video.xbmcTR')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
favorites = os.path.join( profile, 'favorites' )
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
source_file = 'http://drascom.dyndns.org/TV.xml'
if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
if os.path.exists(source_file)==True:
    SOURCES = open(source_file).read()

def Main_List():
    dizi_addDir('Diziler','http://diziport.com',10,'')
    dizi_addDir('Canlı TV','http://diziport.com',1,'')
    dizi_addDir('Sinema','http://www.filmifullizle.com/',21,'')

def dizi_categories():
        dizi_addDir(__language__(30011),'search',11,'special://home/addons/plugin.video.xbmcTR/resources/images/search.png')
        dizi_addDir(__language__(30000),'http://diziport.com/index.php?bolum=dizi&obje=default&sayfa=0',12,'special://home/addons/plugin.video.xbmcTR/resources/images/plusone.png')
        dizi_addDir(__language__(30001),'http://diziport.com/',14,'special://home/addons/plugin.video.xbmcTR/resources/images/all.png')
        dizi_addDir(__language__(30012),'http://diziport.com/index.php?bolum=dizi&obje=en_cok_izlenenler',12,'special://home/addons/plugin.video.xbmcTR/resources/images/all.png')
        dizi_addDir(__language__(30004),'http://diziport.com/index.php?bolum=dizi&obje=diziler&tip=belgesel',13,'special://home/addons/plugin.video.xbmcTR/resources/images/yeni.png')
        dizi_addDir(__language__(30007),'http://diziport.com/index.php?bolum=dizi&obje=diziler&tip=asya_dizileri',13,'special://home/addons/plugin.video.xbmcTR/resources/images/main.jpg')

def dizi_search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            #print query
            url = ('http://diziport.com/index.php?eleman=' + query + '&buton.x=19&buton.y=6&bolum=dizi&obje=diziler&olay=arama')
            print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('&amp;',"&").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('<meta http-equiv="refresh" content="0; url=(.*?)">').findall(link)
        print match
        for url in match:
                dizi_Session(url)
def dizi_Recent(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('&amp;',"&").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()        
        dizi_mainMenu(url)
        match=re.compile('<img src="(.+?)" alt=".+?" width="113" height="113" align="center" /></a>\n\t<h1 class="yellow"><a href="(.+?)" title="(.+?)">').findall(link)
        for thumbnail,url,name in match:
                dizi_addDir(name,url,17,'http://diziport.com/'+thumbnail)
                
        #next page        
        page=re.compile('class=\'current\'><a><b>.+?</b></a></li>\n<li><a href=\'(.+?)\' rel=\'nofollow\'><b>(.+?)</b></a></li>').findall(link)
        for url,name in page:
                dizi_addDir(__language__(30006)+' >> '+name,'http://diziport.com/'+url,12,'special://home/addons/plugin.video.xbmcTR/resources/images/next.png')

def dizi_Documentary(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('&amp;',"&").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        dizi_mainMenu(url)
        match=re.compile('<img src="(.*?)\?hash=123" alt=".*?" width="113" height="113" />\n<a href="(.*?)" title="(.*?)">').findall(link)
        for thumbnail,url,name in match:
                dizi_addDir(name,'http://diziport.com/'+url,15,'http://diziport.com/'+thumbnail)
        #next
        page=re.compile('class=\'current\'><a><b>.+?</b></a></li>\n<li><a href=\'(.+?)\' rel=\'nofollow\'><b>(.+?)</b></a></li>').findall(link)
        for url,name in page:
                dizi_addDir(__language__(30006)+' >> '+name,'http://diziport.com/'+url,13,'special://home/addons/plugin.video.xbmcTR/resources/images/next.png')
        #previous
        page=re.compile('<li><a href=\'(.*?)\' rel=\'nofollow\'><b>(.*?)</b>').findall(link)
        for url,name in page:
                dizi_addDir(__language__(30005)+' >> '+name,'http://diziport.com/'+url,13,'special://home/addons/plugin.video.xbmcTR/resources/images/next.png')

        
def dizi_All(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        dizi_mainMenu(url)
        match=re.compile('<li><a href="(.+?)" alt=".+?" title="(.+?)">').findall(link)
        for url,name in match:
                        dizi_addDir(name,'http://diziport.com/'+url,15,'')
        
def dizi_Session(url):
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
                response.close()
                match=re.compile('src="(.+?)" alt="" width="113" height="113" align="center"  />\n<a href="(.+?)" title="(.+?)"').findall(link)
                if match>[1]:
                        print 'sezonlu'
                        for thumbnail,url,name in match:
                                dizi_addDir(name,'http://diziport.com/'+url,16,'http://diziport.com/'+thumbnail)
                else:
                        print 'sezonsuz'
                        req = urllib2.Request(url)
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link=response.read()
                        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
                        response.close()
                        new=re.compile('content="0;url=http://diziport.com/(.+?)"').findall(link)
                        if new<[1]:
                                print 'yonlendirmesiz'
                                dizi_Episodes(url)
                        else:
                                print 'yonlendirmeli'
                                for url in new:
                                        dizi_Episodes('http://diziport.com/'+url)
                
def dizi_Episodes(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        dizi_mainMenu(url)
        match=re.compile('<a href="(.+?)"><img src="(.+?)" alt="(.+?)"').findall(link)
        for url,thumbnail,name in match:
                dizi_addDir(name,'http://diziport.com/'+url,17,'http://diziport.com/'+thumbnail)

def dizi_VideoLinks(name,url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
        match=re.compile('<b class="yellow"><a href="http://diziport.com/(.*?)-tekpartizle/(.*?)/1" title=".*?"><b class="yellow">Tek</b> Part</a>').findall(link)
        for u1,u2 in match:
            url='http://diziport.com/playlist.php?bolum='+u2+'&dizi='+u1
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xf6',"o").replace('&amp;',"&").replace('\xd6',"O").replace('\xfc',"u").replace('\xdd',"I").replace('\xfd',"i").replace('\xe7',"c").replace('\xde',"s").replace('\xfe',"s").replace('\xc7',"c").replace('\xf0',"g")
        response.close()
    #creating url list for playlist
        playList = ''
        #this is final resolved mp4 url
        match=re.compile('<title>(.*?)</title>\n\t  <jwplayer:file>(.*?)</jwplayer:file>').findall(link)
                            
    #dialog let user choose watch or download...
        dialog = xbmcgui.Dialog()
        ret = dialog.select(__language__(30008), [__language__(30009), __language__(30010)])
        if ret == 0:
                ok = True
                for mname,partLink in match:
                        a = name+'-'+mname
                        playList = playList + partLink
                        playList = playList + ':;'
                        listitem = xbmcgui.ListItem( name, iconImage="DefaultVideo.png", thumbnailImage='special://home/addons/plugin.video.xbmcTR/resources/images/main.jpg')
                        listitem.setInfo( type="Video", infoLabels={ "Title": name } )
                #create seperate links
                        dizi_addLink(a,partLink,'')
                #create url1:;url2:;url3.....an send a directory to resolve and add to playlist...
                dizi_addPlayListLink(__language__(30015),playList,18,'')
                        
        if ret == 1:
                for mname,url in match:
                        a = name+'-'+mname
                        dizi_addDir(a,url,19,'special://home/addons/plugin.video.xbmcTR/resources/images/izle.png')
                        

def dizi_playList_videoLinks(name,url):
        ok=True
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        #time.sleep(2)
        links = url.split(':;')
        print links
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        totalLinks = len(links)
        loadedLinks = 0
        remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
        pDialog.update(0,'Please wait for the process to retrieve video link.',remaining_display)
        
        for videoLink in links:
                playList.add(videoLink)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                #print percent
                remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
                pDialog.update(percent,'Please wait for the process to retrieve video link.',remaining_display)
                if (pDialog.iscanceled()):
                        return False
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                d = xbmcgui.Dialog()
                d.ok('INVALID VIDEO PLAYLIST', 'videos cannot find.','Check other links.')
        return ok
        

def dizi_Download(url):
       filename = (name+'.mp4')
       downloadFolder = __settings__.getSetting('downloadFolder')
       print downloadFolder
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
                
def dizi_mainMenu(url):
        dizi_addDir(__language__(30002),'http://diziport.com/','','special://home/addons/plugin.video.xbmcTR/resources/images/main.jpg')







def getSources():
        if os.path.exists(favorites)==True:
            addDir('Favorites','url',5,xbmc.translatePath(os.path.join(home, 'resources', 'favorite.png')),fanart,'','','',False)        
        sources = source_file
        getData(sources,fanart)


def getSoup(url):
        print 'getSoup(): '+url
        if url.startswith('http://'):
            try:
                req = urllib2.Request(url)
                response = urllib2.urlopen(req)
                data = response.read()
                response.close()
            except urllib2.URLError, e:
                # errorStr = str(e.read())
                if hasattr(e, 'code'):
                    print 'We failed with error code - %s.' % e.code
                    xbmc.executebuiltin("XBMC.Notification(error code - "+str(e.code)+",10000,"+icon+")")
                elif hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                    xbmc.executebuiltin("XBMC.Notification(failed to reach a server. - "+str(e.reason)+",10000,"+icon+")")
        else:
            data = open(url, 'r').read()
        soup = BeautifulSOAP(data, convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        return soup


def getData(url,fanart):
        soup = getSoup(url)
        if len(soup('channels')) > 0:
            channels = soup('channel')
            for channel in channels:
                name = channel('name')[0].string
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    thumbnail = ''
                    
                try:    
                    if not channel('fanart'):
                        if __settings__.getSetting('use_thumb') == "true":
                            fanArt = thumbnail
                        else:
                            fanArt = fanart
                    else:
                        fanArt = channel('fanart')[0].string
                    if fanArt == None:
                        raise
                except:
                    fanArt = fanart
                    
                try:
                    desc = channel('info')[0].string
                except:
                    desc = ''

                try:
                    genre = channel('genre')[0].string
                except:
                    genre = ''

                try:
                    date = channel('date')[0].string
                except:
                    date = ''
                try:
                    addDir(name.encode('utf-8', 'ignore'),url,3,thumbnail,fanArt,desc,genre,date)
                except:
                    print 'There was a problem adding directory from getData(): '+name.encode('utf-8', 'ignore')
        else:
            fanArt = fanart
            getItems(soup('item'),fanArt)


def getChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('channel', attrs={'name' : name})
        items = channel_list('item')
        try:
            fanArt = channel_list('fanart')[0].string
            if fanArt == None:
                raise
        except:
            fanArt = fanart
        for channel in channel_list('subchannel'):
            name = channel('name')[0].string
            try:
                thumbnail = channel('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:    
                if not channel('fanart'):
                    if __settings__.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                else:
                    fanArt = channel('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                pass
            try:
                desc = channel('info')[0].string
            except:
                desc = ''

            try:
                genre = channel('genre')[0].string
            except:
                genre = ''

            try:
                date = channel('date')[0].string
            except:
                date = ''
            try:
                addDir(name.encode('utf-8', 'ignore'),url,4,thumbnail,fanArt,desc,genre,date)
            except:
                print 'There was a problem adding directory - '+name.encode('utf-8', 'ignore')
        print fanArt
        getItems(items,fanArt)


def getSubChannelItems(name,url,fanart):
        soup = getSoup(url)
        channel_list = soup.find('subchannel', attrs={'name' : name})
        items = channel_list('subitem')
        getItems(items,fanart)


def getItems(items,fanart):
        for item in items:
            try:
                name = item('title')[0].string
            except:
                print '-----Name Error----'
                name = ''
            try:
                if item('epg'):
                    if item('epg')[0].string > 1:
                        name += getepg(item('epg')[0].string)
                else:
                    pass
            except:
                print '----- EPG Error ----'

            try:
                if __settings__.getSetting('mirror_link') == "true":
                    try:
                        url = item('link')[1].string	
                    except:
                        url = item('link')[0].string
                if __settings__.getSetting('mirror_link_low') == "true":
                    try:
                        url = item('link')[2].string	
                    except:
                        try:
                            url = item('link')[1].string
                        except:
                            url = item('link')[0].string
                else:
                    url = item('link')[0].string
            except:
                print '---- URL Error Passing ----'+name
                pass

            try:
                thumbnail = item('thumbnail')[0].string
                if thumbnail == None:
                    raise
            except:
                thumbnail = ''
            try:    
                if not item('fanart'):
                    if __settings__.getSetting('use_thumb') == "true":
                        fanArt = thumbnail
                    else:
                        fanArt = fanart
                else:
                    fanArt = item('fanart')[0].string
                if fanArt == None:
                    raise
            except:
                fanArt = fanart
            try:
                desc = item('info')[0].string
            except:
                desc = ''

            try:
                genre = item('genre')[0].string
            except:
                genre = ''

            try:
                date = item('date')[0].string
            except:
                date = ''
            try:
                addLink(url,name.encode('utf-8', 'ignore'),thumbnail,fanArt,desc,genre,date,True)
            except:
                print 'There was a problem adding link - '+name.encode('utf-8', 'ignore')
                
def film_Categories():
        dizi_addDir(__language__(30011),'Search',24,'special://home/addons/plugin.video.xbmcTR/resources/images/search.png')
        dizi_addDir(__language__(30020),'http://www.filmifullizle.com/',22,'special://home/addons/plugin.video.xbmcTR/resources/images/main.png')
        dizi_addDir(__language__(30021),'http://www.filmifullizle.com/kategori/filmler/yerli-filmler',22,'special://home/addons/plugin.video.xbmcTR/resources/images/tag.png')
        dizi_addDir(__language__(30022),'http://www.filmifullizle.com/kategori/filmler/yabanci-filmler',22,'special://home/addons/plugin.video.xbmcTR/resources/images/eye.png')
        dizi_addDir(__language__(30023),'http://www.filmifullizle.com/kategori/filmler/yabanci-filmler/turkce-dublaj',22,'special://home/addons/plugin.video.xbmcTR/resources/images/star.png')
        url='http://www.filmifullizle.com/'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li class=".*?"><a href="(.*?)" title=".*?">(.*?)</a>\n</li>').findall(link)
        for url,name in match:
                dizi_addDir('>> '+name,url,22,'')


def film_Main(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    main=re.compile('<div style="float: left;">\n<a href="(.*?)"><img src="(.*?)" alt="(.*?)"').findall(link)
    for url,thumbnail,name in main:
        dizi_addDir(name,url,23,thumbnail)
    top=re.compile('<li>    <a href="(.*?)" title=".*?"><img src="(.*?)" alt="(.*?) izle " WIDTH=147 HEIGHT=205 class="guncover"/></a>\n    </li>').findall(link)
    for url,thumbnail,name in top:
        dizi_addDir(name,url,23,thumbnail)
    page=re.compile('<li class="active_page"><a href=".*?">.*?</a></li>\n<li><a href="(.*?)">(.*?)</a></li>').findall(link)
    for url,name in page:
        dizi_addDir(__language__(30006)+name,url,22,'')
            
def film_playList(url):
        ok = True
        url= url +':;'+url+'/2:;' +url+'/3:;' +url+'/4:;'+url+'/5:;'+url+'/6:;'
        print url
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        links = url.split(':;')
        print links
        del links [6]
        totalLinks = len(links)
        loadedLinks = 0
        remaining_display = __language__(30004)+'[B]' +str(loadedLinks)+' / '+str(totalLinks)+'[/B]'+ __language__(30005)
        pDialog.update(0,__language__(30002),remaining_display)
        a=0
        for url in links:
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('<embed src=\'http:\/\/www.filmifullizle.com\/img\/player\.swf\?file=(.*?)&a').findall(link)
                for partLink in match:
                        name='Part'
                        a=a+1
                        name= name+' '+str(a)
                        dizi_addLink(name,partLink,'')
                        playList.add(partLink)
                        loadedLinks = loadedLinks + 1
                        percent = (loadedLinks * 100)/totalLinks
                        remaining_display = __language__(30004)+'[B]' +str(loadedLinks)+' / '+str(totalLinks)+'[/B]'+ __language__(30005)
                        pDialog.update(percent,__language__(30002),remaining_display)
                        if (pDialog.iscanceled()):
                                return False

        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                d = xbmcgui.Dialog()
                d.ok('Video Yok', 'Calamiyorum','Geri don.')
        return ok

def film_Search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            url = ('http://www.filmifullizle.com/index.php?s=' + query)
            film_Main(url)

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:
                    param[splitparams[0]]=splitparams[1]
        return param


def getFavorites():
        for i in json.loads(open(favorites).read()):
            name = i[0]
            url = i[1]
            iconimage = i[2]
            if __settings__.getSetting('use_thumb') == "true":
                fanArt = iconimage
            else:
                try:
                    fanArt = i[3]
                    if fanArt == None:
                        raise
                except:
                    fanArt = fanart
            addLink(url,name,iconimage,fanArt,'','','')


def addFavorite(name,url,iconimage,fanart):
        favList = []
        if os.path.exists(favorites)==False:
            print 'Making Favorites File'
            favList.append((name,url,iconimage,fanart))
            a = open(favorites, "w")
            a.write(json.dumps(favList))
            a.close()
        else:
            print 'Appending Favorites'
            a = open(favorites).read()
            data = json.loads(a)
            data.append((name,url,iconimage,fanart))
            b = open(favorites, "w")
            b.write(json.dumps(data))
            b.close()


def rmFavorite(name):
        print 'Remove Favorite'
        a = open(favorites).read()
        data = json.loads(a)
        for index in range(len(data)):
            try:
                if data[index][0]==name:
                    del data[index]
                    b = open(favorites, "w")
                    b.write(json.dumps(data))
                    b.close()
            except:
                pass


def addDir(name,url,mode,iconimage,fanart,description,genre,date,showcontext=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "Date": date } )
        liz.setProperty( "Fanart_Image", fanart )
        if showcontext == True:
            try:
                if name in SOURCES:
                    contextMenu = [('Remove from Sources','XBMC.Container.Update(%s?mode=8&name=%s)' %(sys.argv[0], urllib.quote_plus(name)))]
                    liz.addContextMenuItems(contextMenu, True)
            except:
                pass
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addLink(url,name,iconimage,fanart,description,genre,date,showcontext=True):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description, "Genre": genre, "Date": date } )
        liz.setProperty( "Fanart_Image", fanart )
        if showcontext:
            try:
                if name in FAV:
                    contextMenu = [('Remove from xbmcTR Favorites','XBMC.Container.Update(%s?mode=6&name=%s&url=%s&iconimage=%s)' %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage)))]
                else:
                    contextMenu = [('Add to xbmcTR Favorites','XBMC.Container.Update(%s?mode=5&name=%s&url=%s&iconimage=%s)' %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage)))]
            except:
                contextMenu = [('Add to xbmcTR Favorites','XBMC.Container.Update(%s?mode=5&name=%s&url=%s&iconimage=%s)' %(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url), urllib.quote_plus(iconimage)))]
            liz.addContextMenuItems(contextMenu)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def dizi_addPlayListLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


def dizi_addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player().play(liz)
        return ok


def dizi_addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


    
def getepg(link):
        url=urllib.urlopen(link)
        source=url.read()
        url.close()
        source2 = source.split("Jetzt")
        source3 = source2[1].split('programm/detail.php?const_id=')
        sourceuhrzeit = source3[1].split('<br /><a href="/')
        nowtime = sourceuhrzeit[0][40:len(sourceuhrzeit[0])]
        sourcetitle = source3[2].split("</a></p></div>")
        nowtitle = sourcetitle[0][17:len(sourcetitle[0])]
        nowtitle = nowtitle.replace("ö","oe")
        nowtitle = nowtitle.replace("ä","ae")
        nowtitle = nowtitle.replace("ü","ue")
        return "  - "+nowtitle+" - "+nowtime


xbmcplugin.setContent(int(sys.argv[1]), 'movies')
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
except:
    pass
try:
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_GENRE)
except:
    pass

params=get_params()

url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
except:
    pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
    print "Main List"
    Main_List()
    
elif mode==1:
    print "getSources"
    getSources()
elif mode==2:
    print "getData"
    getData(url,fanart)

elif mode==3:
    print "getChannelItems"
    getChannelItems(name,url,fanart)

elif mode==4:
    print ""
    getSubChannelItems(name,url,fanart)

elif mode==5:
    print ""
    getFavorites()

elif mode==6:
    print ""
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    addFavorite(name,url,iconimage,fanart)
    getFavorites()

elif mode==7:
    print ""
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    rmFavorite(name)
    getFavorites()
    
elif mode==7:
    print "addSource"
    addSource(url)

elif mode==8:
    print "rmSource"
    rmSource(name)

elif mode==9:
    print "getUpdate"
    getUpdate()
    
elif mode==10:
    print "DiziPort Start"
    dizi_categories()
elif mode==11:
    print "DiziPort Search"
    dizi_search()
elif mode==12:
    print "DiziPort Recent"
    dizi_Recent(url)
elif mode==13:
    print "DiziPort Documentary"
    dizi_Documentary(url)
elif mode==14:
    print "DiziPort All"
    dizi_All(url)
elif mode==15:
    print "DiziPort Session"
    dizi_Session(url)

elif mode==16:
    print "DiziPort Episodes"
    dizi_Episodes(url)
elif mode==17:
    print "DiziPort VideoLinks"
    dizi_VideoLinks(name,url)
elif mode==18:
    print "DiziPort Playlist"
    dizi_playList_videoLinks(name,url)
elif mode==19:
    print "DiziPort Download"
    dizi_Download(url)
elif mode==20:
    print "DiziPort Main Menu"
    dizi_mainMenu(url)

    
elif mode==21:
    print "Fullfilm Start"
    film_Categories()
elif mode==22:
    print "Film Main"
    film_Main(url)
elif mode==23:
    print "Playlist"
    film_playList(url)
elif mode==24:
    print "Film arama"
    film_Search()












    


    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
