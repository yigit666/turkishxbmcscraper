# -*- coding: cp1254 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon

__settings__ = xbmcaddon.Addon(id='plugin.video.jetfilm')
__language__ = __settings__.getLocalizedString


def CATEGORIES():
        #addDir(__language__(30008),'Search',6,'special://home/addons/plugin.video.diziport/resources/images/search.png')
        addDir(__language__(30000),'http://jetfilmizle.com/',1,'special://home/addons/plugin.video.diziport/resources/images/yeni.png')
        url='http://jetfilmizle.com/'
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xc3\xbc',"u").replace('\xc3\xa7;',"c").replace('&#8211;',"-").replace('&#8217;',"'")
        response.close()        
        match=re.compile('<li class=".*?"><a href="(.*?)" title=".*?">(.*?)</a>\n</li>').findall(link)
        for url,name in match:
                addDir(name,url,1,'')
        page=re.compile('<li class="active_page"><a href=".*?">.*?</a></li>\n<li><a href="(.*?)">(.*?)</a></li>').findall(link)
        for url,name in page:
                addDir(__language__(30001)+name,url,1,'')
def Search():
        keyboard = xbmc.Keyboard("", 'Search', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            url = ('http://www.dizihd.com/?s='+ query +'&x=0&y=0')
            RECENT(url)
def RECENT(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xc3\xbc',"u").replace('\xc3\xa7;',"c").replace('&#8211;',"-").replace('&#8217;',"'")
        response.close()        
        match=re.compile('<div class="cover">\n<a href="(.*?)" rel="bookmark"><img src="(.*?)" alt="(.*?)Dublaj izle"').findall(link)
        for url,thumbnail,name in match:
                addDir(name,url+'/0',2,thumbnail)
        page=re.compile('<li class="active_page"><a href=".*?">.*?</a></li>\n<li><a href="(.*?)">(.*?)</a></li>').findall(link)
        for url,name in page:
                addDir(__language__(30001)+name,url,1,'')

       
def GrabXml(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('settingsFile=(.*?)"').findall(link)
        print match
        print '----------------------------------'
        for url in match:
                VideoLinks(url)

def VideoLinks(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        link=link.replace('\xc3\xbc',"u").replace('\xc3\xa7;',"c").replace('\xc4\xb1',"ı").replace('&#8211;',"-").replace('&#8217;',"'")
        response.close()
#xml okuma
        page=re.compile('<videoPath value="(.*?)"').findall(link)
        epname= 'part'
        a=0
#Create playlist
        ok=True
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        for url in page:
                a= a+1
                name = epname + ' - '+str(a)
                playList.add(url)
                addLink(name,url,'special://home/addons/plugin.video.dizihd/resources/images/izle.png')
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                d = xbmcgui.Dialog()
                d.ok('INVALID VIDEO PLAYLIST', 'videos cannot find.','Press Backspace :).')
        return ok       

def Download(url):
        #rename file with end of url
        filename = name+'.mp4'
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
        if (__settings__.getSetting('download') == ''):
                        __settings__.openSettings('download')
        filepath = xbmc.translatePath(os.path.join(__settings__.getSetting('download'),filename))
        download(url, filepath)
        
def MAINMENU(url):
        addDir(__language__(30002),'http://diziport.com/','','special://home/addons/plugin.video.diziport/resources/images/main.jpg')
        
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



def addList(name,url,iconimage):
        pl=xbmc.PlayList(1)
        pl.clear()
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmc.PlayList(1).add(handle=int(sys.argv[1]),url=url, listitem=liz)
        xbmc.Player().play(pl)
        return ok

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player().play(liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
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
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
elif mode==1:
        print ""+url
        RECENT(url)
elif mode==2:
        print ""+url
        GrabXml(url)
elif mode==3:
        print ""+url
        SESSION(url)
elif mode==4:
        print ""+url
        VideoLinks(url)
elif mode==5:
        print ""+url
        Download(url)
elif mode==6:
        print ""+url
        Search()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
